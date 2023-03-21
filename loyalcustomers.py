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


startTime = datetime(2022,10,7)
endTime = datetime(2022,11,8)
delta = (endTime - startTime).days + 1
timePeriods = math.floor(delta/14)
leftover = delta % 14
if leftover != 0:
    timePeriods += 1


orders_by_rider = {}

for i in range(timePeriods):

    aTime = startTime + timedelta(days=14*i)
    if i == timePeriods - 1:
        bTime = endTime + timedelta(days=1) - timedelta(seconds=1)
    else:
        bTime = startTime + timedelta(days=14*(i+1)) - timedelta(seconds=1)

    startTimeCode = aTime.strftime('%Y') + '-' + aTime.strftime('%m') + '-' + aTime.strftime('%d') + 'T' + aTime.strftime('%H') + ':' + aTime.strftime('%M') + ':' + aTime.strftime('%S') +'.000Z'
    endTimeCode = bTime.strftime('%Y') + '-' + bTime.strftime('%m') + '-' + bTime.strftime('%d') + 'T' + bTime.strftime('%H') + ':' + bTime.strftime('%M') + ':' + bTime.strftime('%S') +'.000Z'


    #print(delta)
    #print(timePeriods)

    print(startTimeCode)
    print(endTimeCode)

    data = {'pageNumber':1,
        'recordsPerPage':'300',
        'orderStatus':['COMPLETE'],
        'storeIds':[storeId],
        'createdAfter':startTimeCode,
        'createdBefore':endTimeCode}

    r = requests.post(url, headers=headers, json=data)
    res = r.json()
    totalOrders = res['totalRecords']
    pages = res['totalPages']
    leftover = totalOrders % 300
    print(res['totalRecords'])

    print('leftover: ' + str(leftover))

    

    for i in range(pages):
        print('page ' + str(i+1))
        data = {'pageNumber':i+1,
        'recordsPerPage':'300',
        'orderStatus':['COMPLETE'],
        'storeIds':[storeId],
        'createdAfter':startTimeCode,
        'createdBefore':endTimeCode}

        r = requests.post(url, headers=headers, json=data)
        res = r.json()

        if i != pages - 1:
            count = 300
        else:
            count = leftover

        for j in range(count):
                
                name = res['items'][j]['customer']['name']
                
                if name in orders_by_rider:
                    orders_by_rider[name] += 1
                else:
                    orders_by_rider[name] = 1

#print(orders_by_rider)

sorted_dict = {}
sorted_keys = sorted(orders_by_rider, key=orders_by_rider.get, reverse=True)  # [1, 3, 2]

for w in sorted_keys:
    sorted_dict[w] = orders_by_rider[w]



print(len(sorted_dict))


plt.bar(range(len(sorted_dict)), list(sorted_dict.values()), align='center')
plt.xticks(range(len(sorted_dict)), list(sorted_dict.keys()), rotation='vertical')

plt.show()
