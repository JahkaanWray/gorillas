import requests
import matplotlib.pyplot as plt
import json
from datetime import datetime
from datetime import timedelta

storeId = '604a2f5d17be050a2fbbf95a'

headers = {'Content-Type':'application/json',
    'Cookie':'JSESSIONID=CoTqtMsP-LnSrU0pdJdKeClvXHwClE1XeLBF2VxI',
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Connection':'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Authorization': 'Bearer eyJhbGciOiJIUzM4NCJ9.eyJzdWIiOiJhcHBsaWNhdGlvbiIsImlzcyI6ImdvcmlsbGFzLW1vbm9saXRoIiwidWlkIjoiZ1FKRDEyUjVRbVd0Sy16akVFZ0xMdyIsInRhZ3MiOlsiSU5WRU5UT1JZX0VESVRfUVVBTlRJVFkiLCJVU0VSX0VESVQiLCJSSURFUl9FRElUIiwiSU5WRU5UT1JZX0xJU1RfUFVSQ0hBU0VfT1JERVJTIiwiUklERVJfTElTVCIsIk9SREVSX0NPTkZJUk0iLCJJTlZFTlRPUllfTElTVF9ERUxJVkVSWV9OT1RFUyIsIklOVkVOVE9SWV9FRElUX1pPTkUiLCJURUFNX0RFTEVURSIsIlJJREVSX0RFTEVURSIsIklOVkVOVE9SWV9ERUxJVkVSX0RFTElWRVJZIiwiUFJPTU9fTElTVCIsIklOVkVOVE9SWV9SRVBMRU5JU0hfREVMSVZFUlkiLCJUSUNLRVRfTElTVCIsIklOVkVOVE9SWV9DT1VOVF9ERUxJVkVSWSIsIlRFQU1fRURJVCIsIklOVkVOVE9SWV9WSUVXX0RFTElWRVJZX05PVEUiLCJURUFNX0xJU1QiLCJVU0VSX0NSRUFURSIsIlZFTkRPUlNfTElTVCIsIk9SREVSX0NBTkNFTCIsIklOVkVOVE9SWV9WSUVXX1BVUkNIQVNFX09SREVSIiwiT1JERVJfTElTVCIsIlVTRVJfTElTVCIsIklOVkVOVE9SWV9FRElUIiwiT1JERVJfQ09NUExFVEUiLCJJTlZFTlRPUllfTElTVCIsIk9SREVSX0FTU0lHTiIsIk9SREVSX0VESVQiLCJJTlZFTlRPUllfUkVDRUlWRV9ERUxJVkVSWSIsIlBPUlRBTF9VU0VSIl0sImFwaVR5cGUiOiJQT1JUQUwiLCJpYXQiOjE2NjE5MTEwNzcsInVzZXJJZCI6IjYyM2RmMTc0YjZlMjk4MzI5NDM1ODlmYiIsInN0b3JlSWQiOiI2MDRhMmY1ZDE3YmUwNTBhMmZiYmY5NWEiLCJyb2xlcyI6WyJVU0VSIiwiQVBJX1VTRVIiXSwidGVuYW50IjoiWnpSbUJnazNTSnFBRUZadzFQNWNkQSJ9.i4jLW0mG5OOld8W7oBB-XGkFlhKayNi0GPIbZxT54qyxRZc94TVZY9Pu6mpADiF2'}

url = 'https://prod-api.gorillas.io/api/market/orders/list'

startTime = datetime(2022,7,15)
endTime = startTime + timedelta(days=1) - timedelta(seconds=1)

k = 0

while k < 14:
    startTimeCode = startTime.strftime('%Y') + '-' + startTime.strftime('%m') + '-' + startTime.strftime('%d') + 'T' + startTime.strftime('%H') + ':' + startTime.strftime('%M') + ':' + startTime.strftime('%S') +'.000Z'
    endTimeCode = endTime.strftime('%Y') + '-' + endTime.strftime('%m') + '-' + endTime.strftime('%d') + 'T' + endTime.strftime('%H') + ':' + endTime.strftime('%M') + ':' + endTime.strftime('%S') +'.000Z'

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

    orders_by_rider = {}

    orders = []

    for i in range(pages):
        print('page ' + str(i+1))
        data = {'pageNumber':i+1,
        'recordsPerPage':'300',
        'orderStatus':['COMPLETE'],
        'storeIds':[storeId],
        'createdAfter':startTimeCode,
        'createdBefore':endTimeCode
        }

        r = requests.post(url, headers=headers, json=data)
        res = r.json()

        if i != pages - 1:
            count = 300
        else:
            count = leftover

        for j in range(count):
                
                order = res['items'][j]
                print(order['dailySequence'])
                orderId = order['id']
                customerId = order['customer']['userId']
                customerSequence = order['customer']['sequence']

                workflowData = order['workflowData']
                if 'activeWorker' in order['dispatch']:
                    print(order['dispatch']['activeWorker']['name'])
                    rider = order['dispatch']['activeWorker']['name']
                else:
                    rider = 'None'

                orderDetails = order['dispatch']['orderDetails']
                sequence = order['dailySequence']
                

                item = {'orderId': orderId,
                    'customer':{
                        'customerId':customerId,
                        'customerSequence':customerSequence
                    },
                    'workflowData':workflowData,
                    'rider':rider,
                    'orderDetails':orderDetails,
                    'sequence': sequence
                    }

                orders.append(item)

    #print(orders)

    with open('orders.json') as fp:
        data = json.load(fp)

    orderList = data['orders']

    orderList.append(orders)

    with open('orders.json', 'w') as fp:
        json.dump({'orders': orderList}, fp)

    startTime = startTime - timedelta(days=1)
    endTime = startTime + timedelta(days=1) - timedelta(seconds=1)
    k += 1