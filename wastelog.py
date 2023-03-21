import requests
import matplotlib.pyplot as plt
import json
from datetime import datetime
from datetime import timedelta
import math

storeId = config.storeId

headers = {'Content-Type':'application/json',
    'Cookie':'JSESSIONID=CoTqtMsP-LnSrU0pdJdKeClvXHwClE1XeLBF2VxI',
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Connection':'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Authorization': 'Bearer ' + config.gorillas_api_key}

url = 'https://prod-api.gorillas.io/api/v1/market/inventory/logs'


startTime = datetime(2020,8,27)
endTime = datetime(2022,9,2)
delta = (endTime - startTime).days + 1
timePeriods = math.floor(delta/14)
leftover = delta % 14
if leftover != 0:
    timePeriods += 1


orders_by_rider = {}





startTimeCode = startTime.strftime('%Y') + '-' + startTime.strftime('%m') + '-' + startTime.strftime('%d') + 'T' + startTime.strftime('%H') + ':' + startTime.strftime('%M') + ':' + startTime.strftime('%S') +'.000Z'
endTimeCode = endTime.strftime('%Y') + '-' + endTime.strftime('%m') + '-' + endTime.strftime('%d') + 'T' + endTime.strftime('%H') + ':' + endTime.strftime('%M') + ':' + endTime.strftime('%S') +'.000Z'



print(startTimeCode)
print(endTimeCode)

data = {'pageNumber':1,
    'recordsPerPage':1000,
    'action':['CAPTURED'],
    'storeId':storeId,
    'productId':'6074365658af54a1d1671504',
    'startDate':startTimeCode,
    'endDate':endTimeCode}




r = requests.post(url, headers=headers, json=data)
res = r.json()

print(len(res))

total = 0

for i in range(len(res)):
    print(res[i]['label'])
    label = res[i]['label']
    a = label.find('QTY')
    b = label.find('FROM')

    total += int(label[a+4:])

print(total)
    



