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






startTime = datetime(2022,2,2)
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

    orders = []


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

            if 'activeWorker' in res['items'][j]['dispatch']:
                rider = res['items'][j]['dispatch']['activeWorker']['name']
                if rider == None:
                    rider = 'None'
            else:
                rider = 'None'

            if 'pickerName' in res['items'][j]['orderDetails']['pickData']:
                picker = res['items'][j]['orderDetails']['pickData']['pickerName']
                if picker == None:
                    picker = 'None'
            else:
                picker = 'None'

            print(rider)
            
            orderId = res['items'][j]['id']

            customer = res['items'][j]['customer']['name']
            seq = res['items'][j]['customer']['sequence']

            createdOn = res['items'][j]['createdOn']
            completedOn = res['items'][j]['completedOn']
            if completedOn == None:
                completedOn = 0

            createdOn = 0
            pickedOn = 0
            confirmedOn = 0
            assignedOn = 0
            startedOn = 0
            createdOn = 0

            events = res['items'][j]['workflowData']['events']

            for k in range(len(events)):
                eventType = events[k]['event']
                if eventType == 'START':
                    createdOn = events[k]['timestamp']
                elif eventType == 'PROCESS':
                    pickedOn = events[k]['timestamp']
                elif eventType == 'CONFIRM':
                    confirmedOn = events[k]['timestamp']
                elif eventType == 'ASSIGN':
                    assignedOn = events[k]['timestamp']
                elif eventType == 'START_TRIP':
                    startedOn = events[k]['timestamp']
                elif eventType == 'COMPLETE_TRIP':
                    completedOn = events[k]['timestamp']

            latitude = res['items'][j]['dispatch']['dropOff']['address']['coordinates']['lat']
            longitude = res['items'][j]['dispatch']['dropOff']['address']['coordinates']['lon']

            #distance = res['items'][j]['travelDistance']
            distance = 0
    


            print(distance)
                  
            orders.append((orderId,rider,picker,customer,latitude,longitude,distance,createdOn,pickedOn,confirmedOn,assignedOn,startedOn,completedOn,seq))

                  

        #print(orders)
        print(len(orders))
        if len(orders) != 0:
          cur.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", orders)
        mydb.commit()
        mydb.close()
        print('orders inserted')
        orders = []


#print(orders_by_rider)

#print(len(orders))




#print(mydb)