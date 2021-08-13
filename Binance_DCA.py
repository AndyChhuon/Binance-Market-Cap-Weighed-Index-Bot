from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import json

  
nb_coins = '100' #input how many top cryptocurrencies you would like to track
api_key = '' #input binance api key
api_secret = '' #input binance api secret key
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

tokens = json_extract(data, 'symbol')
tokens = list(dict.fromkeys(tokens))
mcap = json_extract(data, 'market_cap')


total_mcap = sum(mcap)

fraction_allocation= [token_mcap /total_mcap for token_mcap in mcap]

tokens_with_allocation = dict(zip(tokens,fraction_allocation))
del[tokens_with_allocation['BTC']]

for deltoken in unwanted_tokens:
    del[tokens_with_allocation[deltoken]]

client = Client(api_key, api_secret)
btc_dict = client.get_asset_balance(asset='BTC')

btc_balance = btc_dict['free']

print('btc balance: ' + btc_balance)


for k,v in tokens_with_allocation.items():
    
        try:
            avg_price = client.get_avg_price(symbol= k+'BTC')
            coin_price = avg_price['price']


        
            coin_qty = v * float(btc_balance) / float(coin_price)

            order = client.order_market_buy(
            symbol= k+'BTC',
            quantity=coin_qty)

            print('Purchase of ' + str(coin_qty) + ' ' + k + ' successful')

        except: 
            print('Purchase of ' + str(coin_qty) + ' ' + k + ' failed')

        
        
