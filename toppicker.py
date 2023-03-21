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

url = 'https://prod-api.gorillas.io/api/market/orders/list'


startTime = datetime(2023,3,2)
endTime = datetime(2023,3,2)
delta = (endTime - startTime).days + 1
timePeriods = math.floor(delta/14)
leftover = delta % 14
if leftover != 0:
    timePeriods += 1


orders_by_picker = {}
picking_time_by_picker = {}
items_by_picker = {}

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

        count = len(res['items'])

        for j in range(count):
                if 'pickerName' in res['items'][j]['orderDetails']['pickData']:
                    name = res['items'][j]['orderDetails']['pickData']['pickerName']
                else:
                    name = 'None'
                if name in orders_by_picker:
                    orders_by_picker[name] += 1
                else:
                    orders_by_picker[name] = 1
                
                rootPath = res['items'][j]['workflowData']['postOrderStates'][3]
                if rootPath['completedOn'] != None:
                    pickingTime = (rootPath['completedOn'] - rootPath['startedOn'])/1000
                #pickingTime = res['items'][j]['orderDetails']['pickData']['pickTime']
                print(name)
                print(pickingTime)
            
                if name in picking_time_by_picker:
                    picking_time_by_picker[name] += pickingTime
                else:
                    picking_time_by_picker[name] = pickingTime

                numberOfItems = res['items'][j]['orderDetails']['numberOfItems']
                if name in items_by_picker:
                    items_by_picker[name] += numberOfItems
                else:
                    items_by_picker[name] = numberOfItems

#print(orders_by_rider)
print(picking_time_by_picker)
for p in picking_time_by_picker:
    picking_time_by_picker[p] = picking_time_by_picker[p]/items_by_picker[p]
print(picking_time_by_picker)

sorted_dict1 = {}
sorted_keys1 = sorted(orders_by_picker, key=orders_by_picker.get, reverse=True)  # [1, 3, 2]

sorted_dict2 = {}
sorted_keys2 = sorted(picking_time_by_picker, key=picking_time_by_picker.get)  # [1, 3, 2]

for w in sorted_keys1:
    sorted_dict1[w] = orders_by_picker[w]

for w in sorted_keys2:
    sorted_dict2[w] = picking_time_by_picker[w]

print(sorted_dict1)

print(sorted_dict2)
total = 0
for picker in orders_by_picker:
    total += orders_by_picker[picker]

print(total)

plt.bar(range(len(sorted_dict1)), list(sorted_dict1.values()), align='center')
plt.xticks(range(len(sorted_dict1)), list(sorted_dict1.keys()), rotation='vertical')

plt.show()

plt.bar(range(len(sorted_dict2)), list(sorted_dict2.values()), align='center')
plt.xticks(range(len(sorted_dict2)), list(sorted_dict2.keys()), rotation='vertical')

plt.show()
