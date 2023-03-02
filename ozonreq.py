import requests
import json



#581144
#80983ce8-8a22-473e-bacf-51f96998536a
# 200 успех
# 403 не правильные токены

headers = {
    'Client-Id':'581144',
    'Api-Key':'80983ce8-8a22-473e-bacf-51f96998536a',
    'Content-Type':'application/json'
}
param = {
  "offer_id": [
    "27000"
  ],
  "product_id": [],
  "sku": []
}
response = requests.post('https://api-seller.ozon.ru/v2/product/info/list',headers=headers,data=json.dumps(param))

print(response.status_code)
# print(response.text)
responsew = json.loads(response.text)
print(json.dumps(responsew))





#posting_number
#offer_id
#created_at	
#name
#price
#status	



