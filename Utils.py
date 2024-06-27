import requests
from datetime import datetime, timedelta
import json

def getBaselinkerOrders():
  a = datetime.now() - timedelta(1)
  a = datetime.timestamp(a)
  baselinkerUrl = "https://api.baselinker.com/connector.php"
  baselinkerOrderRequest = {
        "method": 'getOrders',
        "parameters": json.dumps({
            "date_confirmed_from": a,
            "get_unconfirmed_orders": "False"
        })
    }

  data = requests.post(baselinkerUrl, data=baselinkerOrderRequest, headers={"X-BLToken": "2001442-2004560-5XAT32VD6M0RLX85UO3YC8RJ49B54ZFHL9YNCYTL8XT3GXZWLUT52AK4BV2JBX94"})
  data = data.json()
  return (data)

def getMidRates(currency, date):
  if currency != "PLN":
    rate = requests.get("http://api.nbp.pl/api/exchangerates/rates/a/" + currency + "/" + date, "%Y-%m-%d")
    tempdate = date
    tempdate = datetime.strptime(tempdate, "%Y-%m-%d")
    while rate.status_code == 404:
      tempdate = tempdate + timedelta(-1)
      rate = requests.get("http://api.nbp.pl/api/exchangerates/rates/a/" + currency + "/" + datetime.strftime(tempdate,"%Y-%m-%d"))
    rate = rate.json()
    rate = rate["rates"][0]["mid"]
    return (rate)
  else:
    rate = 1
    return (rate)
def getProductData(produktID):
  baselinkerUrl = "https://api.baselinker.com/connector.php"
  baselinkerProductRequest = {
        "method": 'getInventoryProductsData',
        "parameters": json.dumps({
            "inventory_id": "4744",
            "products": produktID
        })
    }
  tempProductData = requests.post(baselinkerUrl, headers={"X-BLToken": "2001442-2004560-5XAT32VD6M0RLX85UO3YC8RJ49B54ZFHL9YNCYTL8XT3GXZWLUT52AK4BV2JBX94"},data=baselinkerProductRequest)
  tempProductData = tempProductData.json()
  return(tempProductData)

def getBuyPrices(productID, quantity):
  tempProductData = getProductData(productID)
  if tempProductData["status"] == "SUCCESS":
    oneProduct = int(tempProductData["products"][productID]['text_fields']["extra_field_2381"])
    buyPrice = oneProduct * quantity
    return(buyPrice)
  else:
    return(0)

def calculateShippingCost(productID, quantity):
  tempProductData = getProductData(productID)
  if tempProductData["status"] == "SUCCESS":
    if tempProductData["products"][productID]["weight"] > 15:
      oneProduct = int(tempProductData["products"][productID]['text_fields']["extra_field_2387"])
      shipPrice = 70 * oneProduct * quantity
      return(shipPrice)
    else:
      oneProduct = int(tempProductData["products"][productID]['text_fields']["extra_field_2387"])
      shipPrice = 50 * oneProduct * quantity
      return (shipPrice)
  else:
    return(50)
    

