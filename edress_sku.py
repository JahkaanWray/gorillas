import requests
import config

sku='5449000000996'
storeId = config.storeId
baseurl = 'https://prod-api.gorillas.io/api/market/products/'
token = config.gorillas_api_key
url = baseurl + '?searchString=' + sku + '&storeId=' + storeId + '&thirdPartyUid=Kp7DM8fbT6-MOCBUIzRF6w' + '&getInventory=true'

headers = {'Content-Type':'application/json',
    'Cookie':'JSESSIONID=CoTqtMsP-LnSrU0pdJdKeClvXHwClE1XeLBF2VxI',
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Connection':'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Authorization': 'Bearer ' + config.gorillas_api_key} 

r = requests.get(url, headers=headers)



if r.json()['recordCount'] == 1:
    productId = r.json()['productsList'][0]['id']
    print(productId)
    print(r.json()['productsList'][0]['label'])
    print(r.json()['productsList'][0]['productInventory'])
