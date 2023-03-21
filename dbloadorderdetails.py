import requests
import matplotlib.pyplot as plt
import json
from datetime import datetime
from datetime import timedelta
import math
import mariadb
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






startTime = datetime(2022,11,22)
endTime = datetime(2023,2,15)
delta = (endTime - startTime).days + 1
timePeriods = math.floor(delta/14)
leftover = delta % 14
if leftover != 0:
    timePeriods += 1


for j in range(timePeriods):

    aTime = startTime + timedelta(days=14*j)
    if j == timePeriods - 1:
        bTime = endTime + timedelta(days=1) - timedelta(seconds=1)
    else:
        bTime = startTime + timedelta(days=14*(j+1)) - timedelta(seconds=1)

    startTimeCode = aTime.strftime('%Y') + '-' + aTime.strftime('%m') + '-' + aTime.strftime('%d') + 'T' + aTime.strftime('%H') + ':' + aTime.strftime('%M') + ':' + aTime.strftime('%S') +'.000Z'
    endTimeCode = bTime.strftime('%Y') + '-' + bTime.strftime('%m') + '-' + bTime.strftime('%d') + 'T' + bTime.strftime('%H') + ':' + bTime.strftime('%M') + ':' + bTime.strftime('%S') +'.000Z'





    orders_by_rider = {}

    orderDetails = []


    mydb =  mariadb.connect(
      host="sql904.main-hosting.eu",
      user="u883725273_Jahkaan",
      password="@Lbrighton26",
      database="u883725273_DB"
    )


    cur = mydb.cursor()

    data = {'pageNumber':1,
        'recordsPerPage':'300',
        'orderStatus':['COMPLETE'],
        'storeIds':[storeId],
        'createdAfter':startTimeCode,
        'createdBefore':endTimeCode}

    r = requests.post(url, headers=headers, json=data)
    res = r.json()

    pages = res['totalPages']
    print(pages)
      
        

        

    for i in range(pages):

        mydb =  mariadb.connect(
          host="sql904.main-hosting.eu",
          user="u883725273_Jahkaan",
          password="@Lbrighton26",
          database="u883725273_DB"
        )


        cur = mydb.cursor()

        data = {'pageNumber':i+1,
        'recordsPerPage':'300',
        'orderStatus':['COMPLETE'],
        'storeIds':[storeId],
        'createdAfter':startTimeCode,
        'createdBefore':endTimeCode}

        r = requests.post(url, headers=headers, json=data)
        print(r)
        res = r.json()

        count = len(res['items'])

        print(count)

        for j in range(count):

            orderId = res['items'][j]['id']

            createdOn = res['items'][j]['createdOn']
            completedOn = res['items'][j]['completedOn']
            if completedOn == None:
                completedOn = 0

            for k in range(len(res['items'][j]['orderDetails']['items'])):
                productId = res['items'][j]['orderDetails']['items'][k]['id']
                productName = res['items'][j]['orderDetails']['items'][k]['name']
                quantity = res['items'][j]['orderDetails']['items'][k]['quantity']
                orderDetails.append((orderId,productName,productId,quantity,createdOn))

                  

        #print(orders)
        print(len(orderDetails))
        if len(orderDetails) != 0:
          cur.executemany("INSERT INTO orderDetails VALUES (?, ?, ?, ?, ?)", orderDetails)
        mydb.commit()
        mydb.close()
        print('order details inserted')
        orderDetails = []


#print(orders_by_rider)

#print(len(orders))




#print(mydb)