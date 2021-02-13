import requests
import time
import json
import hmac
import hashlib
from urllib.parse import urlencode

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

def buy_test_order(coin):
    payload = {
        "symbol":f"{coin.upper()}BTC",
        "side":"x",
        "type":"MARKET",
        "quoteOrderQty":0.1
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

run()