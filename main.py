import Utils
import requests
from datetime import datetime

def noweZamowienie(request):
  data = Utils.getBaselinkerOrders()
  for order in data['orders']:
    dataParser = {
                "orderNumber": "",
                "orderDate": 0,
                "orderSource": "",
                "sellingPrice": 0,
                "currency": "",
                "sellingPricePLN": 0,
                "buyingPrice": 0,
                "shippingCost": 0,
        }
    dataParser["orderNumber"] = order["external_order_id"]
    dataParser['orderDate'] = datetime.fromtimestamp(order["date_confirmed"])
    dataParser['orderDate'] = datetime.strftime(dataParser['orderDate'], "%Y-%m-%d")
    dataParser['orderSource'] = order['order_source']
    dataParser['sellingPrice'] = order['payment_done']
    dataParser['currency'] = order['currency']
    dataParser['sellingPricePLN'] = round(Utils.getMidRates(order['currency'], dataParser['orderDate']) * order['payment_done'], 2)
    for product in order['products']:
      productBuyPrice = Utils.getBuyPrices(product["product_id"], product["quantity"])
      dataParser['buyingPrice'] += productBuyPrice
    if dataParser['currency'] == "PLN":
      dataParser['shippingCost'] = 15
    else:
      dataParser['shippingCost'] = Utils.calculateShippingCost(product["product_id"], product["quantity"])

    airtableheader = {
                "Authorization": "Bearer patfeuDYWVl6yXnhw.0f65b1a67545106f4234654402b2c94b3755d1fe3cbaf0de9054181087a9ec82",
                'Content-Type': 'application/json'
        }
    airtablerequest = {
                "records": [{
                        "fields": {
                                "Nr zamówienia": dataParser['orderNumber'],
                                "Data zamówienia": dataParser['orderDate'],
                                "Źródło zamówienia": dataParser['orderSource'],
                                "Cena sprzedaży": dataParser['sellingPrice'],
                                "Waluta": dataParser["currency"],
                                "Koszt zakupu (zł)": dataParser["buyingPrice"],
                                "Koszt wysyłki (zł)": dataParser['shippingCost'],
                                "Cena sprzedaży (zł)": dataParser['sellingPricePLN']
                        }
                }]
        }
    requests.post("https://api.airtable.com/v0/appcseESnT4Odf0Wd/tblNW8qUXQbC6DmTs", json=airtablerequest, headers=airtableheader)
noweZamowienie("a")
