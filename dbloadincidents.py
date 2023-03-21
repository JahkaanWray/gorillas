import requests
import matplotlib.pyplot as plt
import json
from datetime import datetime
from datetime import timedelta
import math
import mariadb

storeId = '604a2f5d17be050a2fbbf95a'

headers = {'Content-Type':'application/json',
    'Cookie':'JSESSIONID=CoTqtMsP-LnSrU0pdJdKeClvXHwClE1XeLBF2VxI',
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Connection':'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Authorization': 'Bearer eyJhbGciOiJIUzM4NCJ9.eyJzdWIiOiJhcHBsaWNhdGlvbiIsImlzcyI6ImdvcmlsbGFzLW1vbm9saXRoIiwidWlkIjoiZ1FKRDEyUjVRbVd0Sy16akVFZ0xMdyIsInRhZ3MiOlsiSU5WRU5UT1JZX0VESVRfUVVBTlRJVFkiLCJVU0VSX0VESVQiLCJSSURFUl9FRElUIiwiSU5WRU5UT1JZX0xJU1RfUFVSQ0hBU0VfT1JERVJTIiwiUklERVJfTElTVCIsIk9SREVSX0NPTkZJUk0iLCJJTlZFTlRPUllfTElTVF9ERUxJVkVSWV9OT1RFUyIsIklOVkVOVE9SWV9FRElUX1pPTkUiLCJURUFNX0RFTEVURSIsIlJJREVSX0RFTEVURSIsIklOVkVOVE9SWV9ERUxJVkVSX0RFTElWRVJZIiwiUFJPTU9fTElTVCIsIklOVkVOVE9SWV9SRVBMRU5JU0hfREVMSVZFUlkiLCJUSUNLRVRfTElTVCIsIklOVkVOVE9SWV9DT1VOVF9ERUxJVkVSWSIsIlRFQU1fRURJVCIsIklOVkVOVE9SWV9WSUVXX0RFTElWRVJZX05PVEUiLCJURUFNX0xJU1QiLCJVU0VSX0NSRUFURSIsIlZFTkRPUlNfTElTVCIsIk9SREVSX0NBTkNFTCIsIklOVkVOVE9SWV9WSUVXX1BVUkNIQVNFX09SREVSIiwiT1JERVJfTElTVCIsIlVTRVJfTElTVCIsIklOVkVOVE9SWV9FRElUIiwiT1JERVJfQ09NUExFVEUiLCJJTlZFTlRPUllfTElTVCIsIk9SREVSX0FTU0lHTiIsIk9SREVSX0VESVQiLCJJTlZFTlRPUllfUkVDRUlWRV9ERUxJVkVSWSIsIlBPUlRBTF9VU0VSIl0sImFwaVR5cGUiOiJQT1JUQUwiLCJpYXQiOjE2NjE5MTEwNzcsInVzZXJJZCI6IjYyM2RmMTc0YjZlMjk4MzI5NDM1ODlmYiIsInN0b3JlSWQiOiI2MDRhMmY1ZDE3YmUwNTBhMmZiYmY5NWEiLCJyb2xlcyI6WyJVU0VSIiwiQVBJX1VTRVIiXSwidGVuYW50IjoiWnpSbUJnazNTSnFBRUZadzFQNWNkQSJ9.i4jLW0mG5OOld8W7oBB-XGkFlhKayNi0GPIbZxT54qyxRZc94TVZY9Pu6mpADiF2'}

baseURL = 'https://prod-api.gorillas.io/api/market/admin/tickets/list'






aTime = datetime(2022,10,4)
bTime = datetime(2022,10,7)



orders_by_rider = {}

products = []

startTimeCode = aTime.strftime('%Y') + '-' + aTime.strftime('%m') + '-' + aTime.strftime('%d') + 'T' + aTime.strftime('%H') + ':' + aTime.strftime('%M') + ':' + aTime.strftime('%S') +'.000Z'
endTimeCode = bTime.strftime('%Y') + '-' + bTime.strftime('%m') + '-' + bTime.strftime('%d') + 'T' + bTime.strftime('%H') + ':' + bTime.strftime('%M') + ':' + bTime.strftime('%S') +'.000Z'


mydb =  mariadb.connect(
  host="sql904.main-hosting.eu",
  user="u883725273_Jahkaan",
  password="@Lbrighton26",
  database="u883725273_DB"
)


cur = mydb.cursor()


#baseURL = baseURL + '?storeId=' + storeId + '&getInventory=true&recordsPerPage=800'
data = {'pageNumber':1,
        'recordsPerPage':'100',
        'orderStatus':['COMPLETE'],
        'statusList':['RESOLVED']}

r = requests.post(baseURL, headers=headers, json=data)
res = r.json()

pages = res['totalPages']
print(pages)
  
    

    

for i in range(int(pages)):

    mydb =  mariadb.connect(
      host="sql904.main-hosting.eu",
      user="u883725273_Jahkaan",
      password="@Lbrighton26",
      database="u883725273_DB"
    )


    cur = mydb.cursor()

    URL = baseURL

    data = {'pageNumber':i+1,
        'recordsPerPage':'100',
        'orderStatus':['COMPLETE'],
        'statusList':['RESOLVED']}

    r = requests.post(URL, headers=headers, json=data)
    #print(r)
    res = r.json()

    count = len(res['items'])

    print(count)
    #print(res['productsList'])

    for j in range(count):

        
        cat = res['items'][j]['category']
        
        subcat = res['items'][j]['subCategory']

        comments = res['items'][j]['comments']
        if comments == None:
            comments = ''
        #print(name)
        if 'compensateAmount' in res['items'][j]:
            if 'price' in res['items'][j]['compensateAmount']:

                compensateAmount = res['items'][j]['compensateAmount']['price']

        createdOn = res['items'][j]['createdOn']

        orderId = res['items'][j]['orderData']['id']

        

        incident = (cat,subcat,compensateAmount,orderId,createdOn,comments)

        print(incident)

        products.append(incident)

      

              

    #print(products)
    print(len(products))
    if len(products) != 0:
      cur.executemany("INSERT INTO incidents VALUES (?, ?, ?, ?, ?, ?)", products)
    mydb.commit()
    mydb.close()
    print('orders inserted')
    products = []


#print(orders_by_rider)

#print(len(orders))




#print(mydb)