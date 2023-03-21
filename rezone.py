import requests
import matplotlib.pyplot as plt
import json
from datetime import datetime
from datetime import timedelta
import math
import config

storeId = config.storeId

headers = {'Content-Type':'application/json',
    'Cookie':'JSESSIONID=CoTqtMsP-LnSrU0pdJdKeClvXHwClE1XeLBF2VxI',
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Connection':'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Authorization': 'Bearer ' + config.gorillas_api_key}

url = 'https://prod-api.gorillas.io/api/market/products/?pageNumber=1&recordsPerPage=100&getInventory=true&thirdPartyUid=Kp7DM8fbT6-MOCBUIzRF6w&storeId=' + config.storeId + '&sortDirection=DESC&sortBy=productInv.bin.zone&productInventory.bin.name="F9-5"'








r = requests.get(url, headers=headers)
print(r)
res = r.json()
 
pages = res['pages']

print(res)

for i in range(len(res['productsList'])):

    print(res['productsList'][i]['label'])
    