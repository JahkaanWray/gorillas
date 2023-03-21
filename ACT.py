import requests
import matplotlib.pyplot as plt
import json
from datetime import datetime
from datetime import timedelta
import math
import numpy as np

storeId = '604a2f5d17be050a2fbbf95a'

headers = {'Content-Type':'application/json',
    'Cookie':'JSESSIONID=CoTqtMsP-LnSrU0pdJdKeClvXHwClE1XeLBF2VxI',
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Connection':'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Authorization': 'Bearer eyJhbGciOiJIUzM4NCJ9.eyJzdWIiOiJhcHBsaWNhdGlvbiIsImlzcyI6ImdvcmlsbGFzLW1vbm9saXRoIiwidWlkIjoiZ1FKRDEyUjVRbVd0Sy16akVFZ0xMdyIsInRhZ3MiOlsiSU5WRU5UT1JZX0VESVRfUVVBTlRJVFkiLCJVU0VSX0VESVQiLCJSSURFUl9FRElUIiwiSU5WRU5UT1JZX0xJU1RfUFVSQ0hBU0VfT1JERVJTIiwiUklERVJfTElTVCIsIk9SREVSX0NPTkZJUk0iLCJJTlZFTlRPUllfTElTVF9ERUxJVkVSWV9OT1RFUyIsIklOVkVOVE9SWV9FRElUX1pPTkUiLCJURUFNX0RFTEVURSIsIlJJREVSX0RFTEVURSIsIklOVkVOVE9SWV9ERUxJVkVSX0RFTElWRVJZIiwiUFJPTU9fTElTVCIsIklOVkVOVE9SWV9SRVBMRU5JU0hfREVMSVZFUlkiLCJUSUNLRVRfTElTVCIsIklOVkVOVE9SWV9DT1VOVF9ERUxJVkVSWSIsIlRFQU1fRURJVCIsIklOVkVOVE9SWV9WSUVXX0RFTElWRVJZX05PVEUiLCJURUFNX0xJU1QiLCJVU0VSX0NSRUFURSIsIlZFTkRPUlNfTElTVCIsIk9SREVSX0NBTkNFTCIsIklOVkVOVE9SWV9WSUVXX1BVUkNIQVNFX09SREVSIiwiT1JERVJfTElTVCIsIlVTRVJfTElTVCIsIklOVkVOVE9SWV9FRElUIiwiT1JERVJfQ09NUExFVEUiLCJJTlZFTlRPUllfTElTVCIsIk9SREVSX0FTU0lHTiIsIk9SREVSX0VESVQiLCJJTlZFTlRPUllfUkVDRUlWRV9ERUxJVkVSWSIsIlBPUlRBTF9VU0VSIl0sImFwaVR5cGUiOiJQT1JUQUwiLCJpYXQiOjE2NjE5MTEwNzcsInVzZXJJZCI6IjYyM2RmMTc0YjZlMjk4MzI5NDM1ODlmYiIsInN0b3JlSWQiOiI2MDRhMmY1ZDE3YmUwNTBhMmZiYmY5NWEiLCJyb2xlcyI6WyJVU0VSIiwiQVBJX1VTRVIiXSwidGVuYW50IjoiWnpSbUJnazNTSnFBRUZadzFQNWNkQSJ9.i4jLW0mG5OOld8W7oBB-XGkFlhKayNi0GPIbZxT54qyxRZc94TVZY9Pu6mpADiF2'}

url = 'https://prod-api.gorillas.io/api/market/orders/list'

aTime = datetime(2023,3,14)
bTime = aTime + timedelta(days=1) - timedelta(seconds=1)

startTimeCode = aTime.strftime('%Y') + '-' + aTime.strftime('%m') + '-' + aTime.strftime('%d') + 'T' + aTime.strftime('%H') + ':' + aTime.strftime('%M') + ':' + aTime.strftime('%S') +'.000Z'
endTimeCode = bTime.strftime('%Y') + '-' + bTime.strftime('%m') + '-' + bTime.strftime('%d') + 'T' + bTime.strftime('%H') + ':' + bTime.strftime('%M') + ':' + bTime.strftime('%S') +'.000Z'


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

timestamps = []
completionTimes = []
avgCompletionTimes = []
completionTimeSums = []
completionTimeSum = 0
numOverSL = 0

ghostRides = 0

SL = []
k = 1
for i in range(pages):
    print('page ' + str(i+1))
    data = {'pageNumber':i+1,
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

    for j in range(count):

        if len(res['items'][j]['workflowData']['events']) < 6:
            ghostRides += 1
        
        rootPath = res['items'][j]['workflowData']['postOrderStates'][0]
        #print('completedOn' in rootPath)
        if rootPath['completedOn'] != None:
            completionTime = (rootPath['completedOn'] - rootPath['startedOn'])
            timestamps.append((rootPath['startedOn']-1665788400000)/3600000)
            promiseTime = res['items'][j]['promiseDate']
        
        
            completionTimeSum += completionTime
            completionTimeSums.append(completionTimeSum)
            print(res['items'][j]['dailySequence'])

            completionTimes.append(completionTime/60000)

            print(completionTime/60000)

            if completionTime > 20*60000:
                numOverSL += 1

            SL.append(numOverSL/k)

            print(rootPath['completedOn'])
            avgCompletionTimes.append(completionTimeSum/(k*60000))

        k+=1

    

print('Ghost Rides: ' + str(ghostRides))

#vagCompletionTimes = avgCompletionTimes / 60000



print(completionTimeSum/(60000*len(timestamps)))
plt.plot(timestamps,avgCompletionTimes)
plt.plot(timestamps,completionTimes)
#plt.plot(completionTimeSums)

SLLine = 20 * np.ones(len(timestamps))
plt.plot(timestamps, SLLine)

plt.show()

plt.plot(timestamps,SL)

plt.show()

plt.plot(timestamps,np.arange(len(timestamps)))
plt.plot(np.linspace(8,24,len(timestamps)),np.arange(len(timestamps)))
plt.show()


