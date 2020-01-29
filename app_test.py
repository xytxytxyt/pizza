import unittest
import json

from pymongo_inmemory import MongoClient

import app as app_module
import menu as menu_module


class AppTest(unittest.TestCase):
    n_pizzas = 5
    n_sides = 5
    n_drinks = 5
    random_seed = 0

    @classmethod
    def setUpClass(cls):
        app_module.menu = menu_module.Menu(
            n_pizzas=cls.n_pizzas,
            n_sides=cls.n_sides,
            n_drinks=cls.n_drinks,
            random_seed=cls.random_seed
        )
        app_module.order_id_auto = app_module.order_ids()
        app_module.mongoClient = MongoClient()
        app_module.mongoDb = app_module.mongoClient['pizza']
        app_module.mongoCollection = app_module.mongoDb['orders']

    @classmethod
    def tearDownClass(cls):
        app_module.mongoClient.close()

    def test_swagger(self):
        request, response = app_module.app.test_client.get('/swagger')
        self.assertEqual(response.status, 200)

    def test_menu(self):
        request, response = app_module.app.test_client.get('/menu')
        self.assertEqual(response.status, 200)
        self.assertEqual(len(response.json['pizzas']), self.n_pizzas)
        self.assertEqual(len(response.json['sides']), self.n_sides)
        self.assertEqual(len(response.json['drinks']), self.n_drinks)

    def test_bad_orders(self):
        data = {'order': {'e3e70682-c209-4cac-629f-6fbed82c07cd': 1}}
        request, response = app_module.app.test_client.post('/order', data=json.dumps(data))
        self.assertEqual(response.status, 400)

        data = {'address': '121 N LaSalle St, Chicago, IL 60602', 'order': {}}
        request, response = app_module.app.test_client.post('/order', data=json.dumps(data))
        self.assertEqual(response.status, 400)

        data = {'address': '121 N LaSalle St, Chicago, IL 60602'}
        request, response = app_module.app.test_client.post('/order', data=json.dumps(data))
        self.assertEqual(response.status, 400)

    def test(self):
        data = {'address': '121 N LaSalle St, Chicago, IL 60602', 'order': {'e3e70682-c209-4cac-629f-6fbed82c07cd': 1}}
        request, response = app_module.app.test_client.post('/order', data=json.dumps(data))
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json['_id'], 0)
        self.assertEqual(response.json['order']['e3e70682-c209-4cac-629f-6fbed82c07cd'], 1)

        request, response = app_module.app.test_client.get('/orders_to_make')
        self.assertEqual(response.status, 200)
        self.assertEqual(len(response.json['orders']), 1)
        self.assertEqual(response.json['orders'][0]['_id'], 0)

        request, response = app_module.app.test_client.get('/orders_to_deliver')
        self.assertEqual(response.status, 200)
        self.assertEqual(len(response.json['orders']), 0)

        request, response = app_module.app.test_client.get('/order_ready_to_deliver/999')
        self.assertEqual(response.status, 400)

        request, response = app_module.app.test_client.get('/order_delivered/999')
        self.assertEqual(response.status, 400)

        request, response = app_module.app.test_client.get('/order_delivered/0')
        self.assertEqual(response.status, 400)

        request, response = app_module.app.test_client.get('/order_ready_to_deliver/0')
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json['_id'], 0)
        self.assertEqual(response.json['order']['e3e70682-c209-4cac-629f-6fbed82c07cd'], 1)
        self.assertEqual(response.json['status'], 'ready to deliver')

        request, response = app_module.app.test_client.get('/orders_to_deliver')
        self.assertEqual(response.status, 200)
        self.assertEqual(len(response.json['orders']), 1)
        self.assertEqual(response.json['orders'][0]['_id'], 0)

        request, response = app_module.app.test_client.get('/orders_to_make')
        self.assertEqual(response.status, 200)
        self.assertEqual(len(response.json['orders']), 0)

        request, response = app_module.app.test_client.get('/order_ready_to_deliver/0')
        self.assertEqual(response.status, 400)

        request, response = app_module.app.test_client.get('/order_delivered/0')
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json['_id'], 0)
        self.assertEqual(response.json['order']['e3e70682-c209-4cac-629f-6fbed82c07cd'], 1)
        self.assertEqual(response.json['status'], 'delivered')

        request, response = app_module.app.test_client.get('/orders_to_make')
        self.assertEqual(response.status, 200)
        self.assertEqual(len(response.json['orders']), 0)

        request, response = app_module.app.test_client.get('/orders_to_deliver')
        self.assertEqual(response.status, 200)
        self.assertEqual(len(response.json['orders']), 0)


if __name__ == '__main__':
    unittest.main()
