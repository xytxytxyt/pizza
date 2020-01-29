import argparse

from sanic import Sanic
from sanic.response import json
from sanic.exceptions import InvalidUsage

from sanic_openapi import swagger_blueprint

from pymongo_inmemory import MongoClient

import menu as menu_module

app = Sanic()
app.blueprint(swagger_blueprint)

order_id_auto = None

menu = None

mongoClient = None
mongoDb = None
mongoCollection = None

google_api_key = None

order_statuses = (
    'order received',
    'ready to deliver',
    'delivered',
)


def order_ids():
    order_id = 0
    while True:
        yield order_id
        order_id += 1


@app.route("/")
async def name(request):
    return json("enterprise pizza")


@app.route("/menu")
async def menu(request):
    return json(menu.menu)


@app.route("/order", methods=["POST"])
async def order(request):
    if 'address' not in request.json:
        raise InvalidUsage('order missing address')

    if 'order' not in request.json or not request.json['order']:
        raise InvalidUsage('order is empty')

    for menu_item_id in request.json['order']:
        if not menu.is_valid_menu_item(menu_item_id):
            raise InvalidUsage(f'invalid menu item {menu_item_id}')
        amount = request.json['order'][menu_item_id]
        if not isinstance(amount, int):
            raise InvalidUsage(f'invalid amount {amount} for menu item {menu_item_id}')

    order_id = next(order_id_auto)
    request.json['_id'] = order_id
    request.json['status'] = 'order received'

    mongoCollection.insert_one(request.json)

    return json(request.json)


@app.route("/orders_to_make")
async def orders_to_make(request):
    return json({'orders': mongoCollection.find({"status": "order received"})})


@app.route("/orders_to_deliver")
async def orders_to_deliver(request):
    orders = [order for order in mongoCollection.find({"status": "ready to deliver"})]
    response = {'orders': orders}
    if orders and google_api_key is not None:
        addresses = [order['address'] for order in orders]
        addresses = '|'.join(addresses)
        google_map_url = f'https://maps.googleapis.com/maps/api/staticmap?markers={addresses}&size=1000x1000&key={google_api_key}'
        response['map_url'] = google_map_url
    return json(response)


def order_next_status(order_id, from_status):
    query = {'_id': order_id}
    order = mongoCollection.find_one(query)
    if order is None:
        raise InvalidUsage(f'order {order_id} not found')
    current_status = order['status']
    if current_status != from_status:
        raise InvalidUsage(f"order currently in status '{current_status}', not '{from_status}'")
    assert current_status in order_statuses
    for i in range(len(order_statuses)):
        if order_statuses[i] == current_status:
            break
    mongoCollection.update_one(query, {'$set': {'status': order_statuses[i + 1]}})
    order['status'] = order_statuses[i + 1]
    return order


@app.route("/order_ready_to_deliver/<order_id:int>/")
async def order_ready_to_deliver(request, order_id):
    order = order_next_status(order_id, 'order received')
    return json(order)


@app.route("/order_delivered/<order_id:int>/")
async def order_delivered(request, order_id):
    order = order_next_status(order_id, 'ready to deliver')
    return json(order)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--random_seed', dest='random_seed', required=False)
    parser.add_argument('--google_api_key', dest='google_api_key', required=False)
    args = parser.parse_args()

    order_id_auto = order_ids()

    menu = menu_module.Menu(
        n_pizzas=5,
        n_sides=5,
        n_drinks=5,
        random_seed=int(args.random_seed)
    )

    mongoClient = MongoClient()
    mongoDb = mongoClient['pizza']
    mongoCollection = mongoDb['orders']

    google_api_key = args.google_api_key

    app.run(host="0.0.0.0", port=8000)

    mongoClient.close()
