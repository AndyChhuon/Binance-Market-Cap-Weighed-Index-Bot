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

client = Client(api_key, api_secret)

symbol_info = client.get_symbol_info('BTCUSDT')
step_size = 0.0
for f in symbol_info['filters']:
    if f['filterType'] == 'LOT_SIZE':
        step_size = float(f['stepSize'])
precision = int(round(-math.log(step_size,10),0))
print(precision)



