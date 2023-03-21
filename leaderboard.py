import requests
import matplotlib.pyplot as plt
import json
from datetime import datetime
from datetime import timedelta
import math
import numpy as np
import mariadb

url = "https://prod-api.gorillas.io/api/market/admin/settings/users/stores"

payload={}
headers = {'Content-Type':'application/json',
    'Cookie':'JSESSIONID=CoTqtMsP-LnSrU0pdJdKeClvXHwClE1XeLBF2VxI',
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Connection':'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Authorization': 'Bearer eyJhbGciOiJIUzM4NCJ9.eyJzdWIiOiJhcHBsaWNhdGlvbiIsImlzcyI6ImdvcmlsbGFzLW1vbm9saXRoIiwidWlkIjoiZ1FKRDEyUjVRbVd0Sy16akVFZ0xMdyIsInRhZ3MiOlsiSU5WRU5UT1JZX0VESVRfUVVBTlRJVFkiLCJVU0VSX0VESVQiLCJSSURFUl9FRElUIiwiSU5WRU5UT1JZX0xJU1RfUFVSQ0hBU0VfT1JERVJTIiwiUklERVJfTElTVCIsIk9SREVSX0NPTkZJUk0iLCJJTlZFTlRPUllfTElTVF9ERUxJVkVSWV9OT1RFUyIsIklOVkVOVE9SWV9FRElUX1pPTkUiLCJURUFNX0RFTEVURSIsIlJJREVSX0RFTEVURSIsIklOVkVOVE9SWV9ERUxJVkVSX0RFTElWRVJZIiwiUFJPTU9fTElTVCIsIklOVkVOVE9SWV9SRVBMRU5JU0hfREVMSVZFUlkiLCJUSUNLRVRfTElTVCIsIklOVkVOVE9SWV9DT1VOVF9ERUxJVkVSWSIsIlRFQU1fRURJVCIsIklOVkVOVE9SWV9WSUVXX0RFTElWRVJZX05PVEUiLCJURUFNX0xJU1QiLCJVU0VSX0NSRUFURSIsIlZFTkRPUlNfTElTVCIsIk9SREVSX0NBTkNFTCIsIklOVkVOVE9SWV9WSUVXX1BVUkNIQVNFX09SREVSIiwiT1JERVJfTElTVCIsIlVTRVJfTElTVCIsIklOVkVOVE9SWV9FRElUIiwiT1JERVJfQ09NUExFVEUiLCJJTlZFTlRPUllfTElTVCIsIk9SREVSX0FTU0lHTiIsIk9SREVSX0VESVQiLCJJTlZFTlRPUllfUkVDRUlWRV9ERUxJVkVSWSIsIlBPUlRBTF9VU0VSIl0sImFwaVR5cGUiOiJQT1JUQUwiLCJpYXQiOjE2NjE5MTEwNzcsInVzZXJJZCI6IjYyM2RmMTc0YjZlMjk4MzI5NDM1ODlmYiIsInN0b3JlSWQiOiI2MDRhMmY1ZDE3YmUwNTBhMmZiYmY5NWEiLCJyb2xlcyI6WyJVU0VSIiwiQVBJX1VTRVIiXSwidGVuYW50IjoiWnpSbUJnazNTSnFBRUZadzFQNWNkQSJ9.i4jLW0mG5OOld8W7oBB-XGkFlhKayNi0GPIbZxT54qyxRZc94TVZY9Pu6mpADiF2'}


r = requests.request("GET", url, headers=headers, data=payload)
res = r.json()
#print(res)

stores = []



for i in range(len(res)):
    print(i)
    #print(res[i]['value'][-6:])
    if res[i]['value'][-6:] == 'London':
        #print(res[i]['value'])
        stores.append((res[i]['value'],res[i]['key']))

print(stores)

startTime = datetime(2022,11,4)
endTime = datetime(2022,12,3)
timestamp = datetime.timestamp(startTime)
delta = (endTime - startTime).days
print(delta)

leaderboardData = []

#Loop through each day in time period
for i in range(delta + 1):
    a = startTime + timedelta(days=i) + timedelta(hours=1)
    b = a + timedelta(days=1) - timedelta(seconds=1)
    startTimeCode = a.strftime('%Y') + '-' + a.strftime('%m') + '-' + a.strftime('%d') + 'T' + a.strftime('%H') + ':' + a.strftime('%M') + ':' + a.strftime('%S') +'.000Z'
    endTimeCode = b.strftime('%Y') + '-' + b.strftime('%m') + '-' + b.strftime('%d') + 'T' + b.strftime('%H') + ':' + b.strftime('%M') + ':' + b.strftime('%S') +'.000Z'
    #Loop throught each WH

    startTimestamp = datetime.timestamp(a)*1000
    print(startTimestamp)
    for j in range(len(stores)):
        storeId = stores[j][1]
        #Get order data for specific WH and day
        url = 'https://prod-api.gorillas.io/api/market/orders/list'
        
        headers = {'Content-Type':'application/json',
        'Cookie':'JSESSIONID=CoTqtMsP-LnSrU0pdJdKeClvXHwClE1XeLBF2VxI',
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Connection':'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Authorization': 'Bearer eyJhbGciOiJIUzM4NCJ9.eyJzdWIiOiJhcHBsaWNhdGlvbiIsImlzcyI6ImdvcmlsbGFzLW1vbm9saXRoIiwidWlkIjoiZ1FKRDEyUjVRbVd0Sy16akVFZ0xMdyIsInRhZ3MiOlsiSU5WRU5UT1JZX0VESVRfUVVBTlRJVFkiLCJVU0VSX0VESVQiLCJSSURFUl9FRElUIiwiSU5WRU5UT1JZX0xJU1RfUFVSQ0hBU0VfT1JERVJTIiwiUklERVJfTElTVCIsIk9SREVSX0NPTkZJUk0iLCJJTlZFTlRPUllfTElTVF9ERUxJVkVSWV9OT1RFUyIsIklOVkVOVE9SWV9FRElUX1pPTkUiLCJURUFNX0RFTEVURSIsIlJJREVSX0RFTEVURSIsIklOVkVOVE9SWV9ERUxJVkVSX0RFTElWRVJZIiwiUFJPTU9fTElTVCIsIklOVkVOVE9SWV9SRVBMRU5JU0hfREVMSVZFUlkiLCJUSUNLRVRfTElTVCIsIklOVkVOVE9SWV9DT1VOVF9ERUxJVkVSWSIsIlRFQU1fRURJVCIsIklOVkVOVE9SWV9WSUVXX0RFTElWRVJZX05PVEUiLCJURUFNX0xJU1QiLCJVU0VSX0NSRUFURSIsIlZFTkRPUlNfTElTVCIsIk9SREVSX0NBTkNFTCIsIklOVkVOVE9SWV9WSUVXX1BVUkNIQVNFX09SREVSIiwiT1JERVJfTElTVCIsIlVTRVJfTElTVCIsIklOVkVOVE9SWV9FRElUIiwiT1JERVJfQ09NUExFVEUiLCJJTlZFTlRPUllfTElTVCIsIk9SREVSX0FTU0lHTiIsIk9SREVSX0VESVQiLCJJTlZFTlRPUllfUkVDRUlWRV9ERUxJVkVSWSIsIlBPUlRBTF9VU0VSIl0sImFwaVR5cGUiOiJQT1JUQUwiLCJpYXQiOjE2NjE5MTEwNzcsInVzZXJJZCI6IjYyM2RmMTc0YjZlMjk4MzI5NDM1ODlmYiIsInN0b3JlSWQiOiI2MDRhMmY1ZDE3YmUwNTBhMmZiYmY5NWEiLCJyb2xlcyI6WyJVU0VSIiwiQVBJX1VTRVIiXSwidGVuYW50IjoiWnpSbUJnazNTSnFBRUZadzFQNWNkQSJ9.i4jLW0mG5OOld8W7oBB-XGkFlhKayNi0GPIbZxT54qyxRZc94TVZY9Pu6mpADiF2'}
        
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

        print(totalOrders)
        completionTimeSum = 0

        orders = []
        activeRiders = []
        for index in range(24):
            orders.append(0)
            activeRiders.append([])

        for k in range(pages):
            print(stores[j][0])
            #print(timeCode)
            print('page ' + str(k+1))
            data = {'pageNumber':k+1,
            'recordsPerPage':'300',
            'orderStatus':['COMPLETE'],
            'storeIds':[storeId],
            'createdAfter':startTimeCode,
            'createdBefore':endTimeCode,
            "sortDirection":"ASC",
            "sortBy":"createdOn"}

            r = requests.post(url, headers=headers, json=data)
            res = r.json()

            count = len(res['items'])

            for l in range(count):
                
                rootPath = res['items'][l]['workflowData']['postOrderStates'][0]
                #print('completedOn' in rootPath)
                if rootPath['completedOn'] != None:
                    completionTime = (rootPath['completedOn'] - rootPath['startedOn'])
                    promiseTime = res['items'][l]['promiseDate']
                
                
                    completionTimeSum += completionTime
                print(rootPath['startedOn'])
                for m in range(24):

                    if rootPath['startedOn'] < startTimestamp + m*60*60*1000:
                        orders[m] += 1
                        if 'activeWorker' in res['items'][l]['dispatch']:
                            
                            name = res['items'][l]['dispatch']['activeWorker']['name']
                            #print(name)
                            if (name in activeRiders[m]) == False:
                                activeRiders[m].append(name)
                        
                        break
                    

        if totalOrders != 0:
            ACT = completionTimeSum/(totalOrders*60*1000)
        else:
            ACT = 0

        #print(orders)
        #print(activeRiders)
        totalRiders = 0
        for index in range(len(activeRiders)):
            totalRiders += len(activeRiders[index])
        if totalRiders != 0:
            OPH = totalOrders/totalRiders
        else: 
            OPH = 0

        if OPH == 0:
            REC = 0
        else:
            REC = ACT/OPH

        if totalOrders != 0:
            leaderboardData.append((stores[j][0],stores[j][1],ACT,OPH,REC,a.strftime('%Y') + '-' + a.strftime('%m') + '-' + a.strftime('%d')))

        

        print((stores[j][0],stores[j][1],ACT,OPH,REC,a.strftime('%Y') + '-' + a.strftime('%m') + '-' + a.strftime('%d')))

        #cur.execute('INSERT INTO leaderboard (store, storeId, ACT, OPH, REC, date) VALUES (?,?,?,?,?,?)',(stores[j][0],stores[j][1],ACT,OPH,REC,a.strftime('%Y') + '-' + a.strftime('%m') + '-' + a.strftime('%d')))     

        

                   




print(leaderboardData)

mydb =  mariadb.connect(
      host="sql904.main-hosting.eu",
      user="u883725273_Jahkaan",
      password="@Lbrighton26",
      database="u883725273_DB"
    )


cur = mydb.cursor()

cur.executemany('INSERT INTO leaderboard VALUES (?,?,?,?,?,?)', leaderboardData)
mydb.commit()
mydb.close()

