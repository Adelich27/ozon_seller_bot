import requests
import json


#авторизация
def auth(clientId,apiKey):
  response = None
  headers = {
      'Client-Id':f'{clientId}',
      'Api-Key':f'{apiKey}',
      'Content-Type':'application/json'
  }
  param = {
    "page": 0,
    "page_size": 0,
    "report_type": "ALL"
  }
  auth = requests.post('https://api-seller.ozon.ru/v1/report/list',headers=headers,data=json.dumps(param))
  if auth.status_code == 200:
    response = True
  else:
    response = False
  return response
#Журнал заказов
def ordersHistory(clientId,apiKey):
  headers = {
      'Client-Id':f'{clientId}',
      'Api-Key':f'{apiKey}',
      'Content-Type':'application/json'
  }
  param = {
      "dir": "desc",
      "filter": {
          "since": "2023-01-01T00:00:00.000Z",
          "status": "",
          "to": "2023-03-01T00:00:00.000Z"
      },
      "limit": 5,
      "offset": 0,
      "translit": True,
      "with": {
          "analytics_data": True,
          "financial_data": False
      }
  }
  response = requests.post('https://api-seller.ozon.ru/v2/posting/fbo/list',headers=headers,data=json.dumps(param))
  response = json.loads(response.text)
  return response
#поиск по номеру заказа
def searchOrder(clientId,apiKey,number):
  headers = {
      'Client-Id':f'{clientId}',
      'Api-Key':f'{apiKey}',
      'Content-Type':'application/json'
  }
  param = {
    "posting_number": f"{number}",
    "translit": True,
    "with": {
        "analytics_data": False,
        "financial_data": False,
    }
}
  response = requests.post('https://api-seller.ozon.ru/v2/posting/fbo/get',headers=headers,data=json.dumps(param))
  if response.status_code == 200:
    response = json.loads(response.text)
    return response
  else:
    return False
#cписок товаров
def itemsListOzon(clientId,apiKey):
  headers = {
      'Client-Id':f'{clientId}',
      'Api-Key':f'{apiKey}',
      'Content-Type':'application/json'
  }
  param = {
  "filter": {
    "visibility": "ALL"
  },
  "last_id": "",
  "limit": 100
}
  response = requests.post('https://api-seller.ozon.ru/v2/product/list',headers=headers,data=json.dumps(param))
  if response.status_code == 200:
    response = json.loads(response.text)
    return response
  else:
    return False
#поиск по артикулу карточки
def searchCardOzon(clientId,apiKey,number):
  headers = {
      'Client-Id':f'{clientId}',
      'Api-Key':f'{apiKey}',
      'Content-Type':'application/json'
  }
  param = {
  "offer_id": [
    f"{number}"
  ],
  "product_id": [],
  "sku": []
}
  response = requests.post('https://api-seller.ozon.ru/v2/product/info/list',headers=headers,data=json.dumps(param))
  if "id" in response.text:
    response = json.loads(response.text)
    return response
  else:
    return False