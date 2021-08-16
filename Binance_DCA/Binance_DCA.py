from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import json
import math

nb_coins = '5' #input the range of top cryptocurrencies you would like to track
api_key = 'GgPmR1Z8e8AHVt9MezUtYgPyBtYFlFW4sDqPdLQEWkyinPOIGu45IoeVZOXCgCm2' #input binance api key
api_secret = 'ZJumkYhSq11p0leDfL1bVypxNh2WBHXqwfGfuAwyEIK0rJwn27kpuRQKklnkW8qN' #input binance api secret key
unwanted_tokens = [] #input symbol of undesired tokens in the top x coins (ex: unwated_tokens = ['ETH', 'BNB'])

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'limit' : nb_coins
}

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '6b64a05f-3235-4eb5-ac5e-18a113a310a3', #Input your own coinmarketcap api key if mine is out of API key usages for the day
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)

except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)


def json_extract(obj, key):
    
    arr = []

    def extract(obj, arr, key):
        
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)

        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values

tokens = json_extract(data, 'symbol') #gives list of tokens
tokens = list(dict.fromkeys(tokens))
mcap = json_extract(data, 'market_cap') #gives market cap of tokens listed

tokens_with_mcap = dict(zip(tokens, mcap)) #makes a dictionary of token name:market cap
for deltoken in unwanted_tokens:
    del[tokens_with_mcap[deltoken]] #delete unwanted tokens

total_mcap = 0
tokens_mcap=[]
wanted_tokens = []
for k,v in tokens_with_mcap.items(): #Find total mcap of wanted tokens and get array of wanted tokens' mcap and wanted tokens' name
    total_mcap = total_mcap + v
    tokens_mcap.append(v)
    wanted_tokens.append(k)

fraction_allocation = [token_mcap/total_mcap for token_mcap in tokens_mcap]

tokens_with_allocation = dict(zip(wanted_tokens, fraction_allocation)) #Get token:fraction_allocation dictionary

if 'BTC' not in unwanted_tokens:
    del[tokens_with_allocation['BTC']] #no need to purchase Btc because starts off with btc balance

client = Client(api_key, api_secret)
btc_dict = client.get_asset_balance(asset='BTC') 

btc_balance = btc_dict['free'] #find btc balance of binance account

print('btc balance: ' + btc_balance)

def get_qty_precision(symbol):
    try:
        symbol_info = client.get_symbol_info(symbol+'BTC')
        step_size = 0.0
        for f in symbol_info['filters']:
            if f['filterType'] == 'LOT_SIZE':
                step_size = float(f['stepSize'])
        precision = int(round(-math.log(step_size,10),0))
        return precision
    except:
        symbol_info = client.get_symbol_info('BTC' + symbol)
        step_size = 0.0
        for f in symbol_info['filters']:
            if f['filterType'] == 'LOT_SIZE':
                step_size = float(f['stepSize'])
        precision = int(round(-math.log(step_size,10),0))
        return precision

for k,v in tokens_with_allocation.items(): #Place order for tokens
    
        try:
            avg_price = client.get_avg_price(symbol= k+'BTC')

            coin_price = avg_price['price']
        
            precision = get_qty_precision(k)

            coin_qty = round(v * float(btc_balance) / float(coin_price), precision)


            order = client.order_market_buy(
            symbol= k+'BTC',
            quantity= coin_qty)

            print('Purchase of ' + str(coin_qty) + ' ' + k + ' successful')

        except: 
            try: 
                avg_price = client.get_avg_price(symbol= 'BTC' + k)

                coin_price = avg_price['price']

                precision = get_qty_precision(k)

        
                coin_qty = round (v * float(btc_balance), precision)
                eq_qty = v * float(btc_balance) * float(coin_price)

                order = client.order_market_sell(
                symbol= 'BTC' + k,
                quantity= coin_qty)

                print('Purchase of ' + str(eq_qty) + ' ' + k + ' successful')
            
            except:    
                try:    
                    print('Purchase of ' + str(coin_qty) + ' ' + k + ' failed')
                except:
                    print('Purchase of ' + k + ' failed')

                    


