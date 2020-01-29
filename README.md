ordering and delivery for a pizza store

```
pip install -r requirements.txt

python menu_test.py

python app_test.py

python app.py --random_seed 0

python app.py

curl -d '{"address": "201 E Randolph St, Chicago, IL 60602", "order": {"e3e70682-c209-4cac-629f-6fbed82c07cd": 1}}' -H "Content-Type: application/json" -X POST http://localhost:8000/order

...
```
