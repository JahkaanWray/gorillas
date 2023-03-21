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

url = 'https://prod-api.gorillas.io/api/market/orders/list'

startTime = datetime(2022,8,31)
endTime = startTime + timedelta(hours=1) - timedelta(seconds=1)

orderVol = []

k=0

while k < 30:
    startTimeCode = startTime.strftime('%Y') + '-' + startTime.strftime('%m') + '-' + startTime.strftime('%d') + 'T' + startTime.strftime('%H') + ':' + startTime.strftime('%M') + ':' + startTime.strftime('%S') +'.000Z'
    endTimeCode = endTime.strftime('%Y') + '-' + endTime.strftime('%m') + '-' + endTime.strftime('%d') + 'T' + endTime.strftime('%H') + ':' + endTime.strftime('%M') + ':' + endTime.strftime('%S') +'.000Z'

    data = {'pageNumber':1,
        'recordsPerPage':'300',
        'orderStatus':['COMPLETE'],
        'storeIds':[storeId],
        'createdAfter':startTimeCode,
        'createdBefore':endTimeCode}


    r = requests.post(url, headers=headers, json=data)
    res = r.json()
    totalOrders = res['totalRecords']

    print(totalOrders)
    startTime -= timedelta(days=1)
    endTime -= timedelta(days=1)
    orderVol.append(totalOrders)
    k += 1

orderVol.reverse()
plt.plot(orderVol)
plt.show()