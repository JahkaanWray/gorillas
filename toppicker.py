import requests
import matplotlib.pyplot as plt
import json
from datetime import datetime
from datetime import timedelta
import math

storeId = '604a2f5d17be050a2fbbf95a'

headers = {'Content-Type':'application/json',
    'Cookie':'JSESSIONID=CoTqtMsP-LnSrU0pdJdKeClvXHwClE1XeLBF2VxI',
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Connection':'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Authorization': 'Bearer eyJhbGciOiJIUzM4NCJ9.eyJzdWIiOiJhcHBsaWNhdGlvbiIsImlzcyI6ImdvcmlsbGFzLW1vbm9saXRoIiwidWlkIjoiZ1FKRDEyUjVRbVd0Sy16akVFZ0xMdyIsInRhZ3MiOlsiSU5WRU5UT1JZX0VESVRfUVVBTlRJVFkiLCJVU0VSX0VESVQiLCJSSURFUl9FRElUIiwiSU5WRU5UT1JZX0xJU1RfUFVSQ0hBU0VfT1JERVJTIiwiUklERVJfTElTVCIsIk9SREVSX0NPTkZJUk0iLCJJTlZFTlRPUllfTElTVF9ERUxJVkVSWV9OT1RFUyIsIklOVkVOVE9SWV9FRElUX1pPTkUiLCJURUFNX0RFTEVURSIsIlJJREVSX0RFTEVURSIsIklOVkVOVE9SWV9ERUxJVkVSX0RFTElWRVJZIiwiUFJPTU9fTElTVCIsIklOVkVOVE9SWV9SRVBMRU5JU0hfREVMSVZFUlkiLCJUSUNLRVRfTElTVCIsIklOVkVOVE9SWV9DT1VOVF9ERUxJVkVSWSIsIlRFQU1fRURJVCIsIklOVkVOVE9SWV9WSUVXX0RFTElWRVJZX05PVEUiLCJURUFNX0xJU1QiLCJVU0VSX0NSRUFURSIsIlZFTkRPUlNfTElTVCIsIk9SREVSX0NBTkNFTCIsIklOVkVOVE9SWV9WSUVXX1BVUkNIQVNFX09SREVSIiwiT1JERVJfTElTVCIsIlVTRVJfTElTVCIsIklOVkVOVE9SWV9FRElUIiwiT1JERVJfQ09NUExFVEUiLCJJTlZFTlRPUllfTElTVCIsIk9SREVSX0FTU0lHTiIsIk9SREVSX0VESVQiLCJJTlZFTlRPUllfUkVDRUlWRV9ERUxJVkVSWSIsIlBPUlRBTF9VU0VSIl0sImFwaVR5cGUiOiJQT1JUQUwiLCJpYXQiOjE2NjE5MTEwNzcsInVzZXJJZCI6IjYyM2RmMTc0YjZlMjk4MzI5NDM1ODlmYiIsInN0b3JlSWQiOiI2MDRhMmY1ZDE3YmUwNTBhMmZiYmY5NWEiLCJyb2xlcyI6WyJVU0VSIiwiQVBJX1VTRVIiXSwidGVuYW50IjoiWnpSbUJnazNTSnFBRUZadzFQNWNkQSJ9.i4jLW0mG5OOld8W7oBB-XGkFlhKayNi0GPIbZxT54qyxRZc94TVZY9Pu6mpADiF2'}

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
