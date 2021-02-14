import requests
import time
import json
import hmac
import hashlib
from urllib.parse import urlencode
from decimal import Decimal

with open('settings.json', 'r') as f:
    config = json.load(f)

api_key = config["api_key"]
api_secret = config["api_secret"]

def run():
    input('''       !
       !
       ^
      / \\
     /___\\
    |=   =|                  /$$$$$$$  /$$ /$$$$$$$
    |     |                 | $$__  $$|__/| $$__  $$
    |     |                 | $$  \ $$ /$$| $$  \ $$ /$$   /$$ /$$$$$$/$$$$   /$$$$$$ 
    |     |                 | $$$$$$$ | $$| $$$$$$$/| $$  | $$| $$_  $$_  $$ /$$__  $$
    |     |                 | $$__  $$| $$| $$____/ | $$  | $$| $$ \ $$ \ $$| $$  \ $$
    |     |                 | $$  \ $$| $$| $$      | $$  | $$| $$ | $$ | $$| $$  | $$                 
    |     |                 | $$$$$$$/| $$| $$      |  $$$$$$/| $$ | $$ | $$| $$$$$$$/                 
    |     |                 |_______/ |__/|__/       \______/ |__/ |__/ |__/| $$____/ 
    |     |                                                                 | $$      
    |     |                                                                 | $$
    |     |                                                                 |__/ 
   /|##!##|\\
  / |##!##| \\
 /  |##!##|  \\                                               by Meirewes
|  / ^ | ^ \  |
| /  ( | )  \ |
|/   ( | )   \|
    ((   ))
   ((  :  ))
   ((  :  ))
    ((   ))
     (( ))
      ( )
       .
       .
       .
       
       
[!] Press ENTER to continue       
''')

    choice = input('''[1] 
[2]''')

def hashing(query_string):
    return hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def current_milli_time():
    return int(time.time() * 1000)

def get_price(coin):
    payload = {
        "symbol":f"{coin.upper()}BTC"
    }

    r = requests.get('https://api.binance.com/api/v3/ticker/price', params=payload)

    return r.json()["price"]

def get_btc_bal():

    timestamp = current_milli_time()
    to_hash = f'timestamp={timestamp}'
    sig = hashing(to_hash)

    headers = {
        "content-type":"application/x-www-form-urlencoded",
        "X-MBX-APIKEY":api_key
    }

    payload = {
        "timestamp":timestamp,
        "signature":sig
    }

    r = requests.get('https://api.binance.com/api/v3/account', headers=headers, params=payload)
    return r.json()["balances"][0]["free"]

def place_test_order(coin):
    payload = {
        "symbol":f"{coin.upper()}BTC",
        "side":"BUY",
        "type":"MARKET",
        "quoteOrderQty":amount_to_purchase_with
    }

    query_string = urlencode(payload, True)

    if query_string:
        query_string = "{}&timestamp={}".format(query_string, current_milli_time())
    else:
        query_string = 'timestamp={}'.format(current_milli_time())

    headers = {
        "content-type":"application/x-www-form-urlencoded",
        "X-MBX-APIKEY":api_key
    }

    r = requests.post(f'https://api.binance.com/api/v3/order/test?{query_string}&signature={hashing(query_string)}', headers=headers)

    data = r.json()

    print(f'[BUY] Bought {data["fills"][0]["qty"]} {coin} @ {data["fills"][0]["price"]} BTC each, with a commission of {data["fills"][0]["commission"]} {data["fills"][0]["commissionAsset"]} // Trade ID: {data["fills"][0]["tradeId"]}')





# https://stackoverflow.com/questions/65551059/how-to-send-oco-order-to-binance





    payload = {
        "symbol":f"{coin.upper()}BTC",
        "side":"SELL",
        "type":"TAKE_PROFIT",
        "quantity":Decimal(str(float(data["fills"][0]["qty"]))).quantize(Decimal('0.00000001')),
        "stopPrice":Decimal(str(float(data["fills"][0]["price"]) * 1.3)).quantize(Decimal('0.00000001'))
    }

    query_string = urlencode(payload, True)

    if query_string:
        query_string = "{}&timestamp={}".format(query_string, current_milli_time())
    else:
        query_string = 'timestamp={}'.format(current_milli_time())


    r = requests.post(f'https://api.binance.com/api/v3/order/test?{query_string}&signature={hashing(query_string)}', headers=headers)

    data = r.json()

place_test_order('SKY')
