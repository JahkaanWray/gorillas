import requests
import matplotlib.pyplot as plt
import json
from datetime import datetime
from datetime import timedelta

storeId = config.storeId

headers = {'Content-Type':'application/json',
    'Cookie':'JSESSIONID=CoTqtMsP-LnSrU0pdJdKeClvXHwClE1XeLBF2VxI',
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Connection':'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Authorization': 'Bearer ' + config.gorillas_api_key}

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