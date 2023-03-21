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

baseURL = 'https://prod-api.gorillas.io/api/market/products/'






aTime = datetime(2022,10,4)
bTime = datetime(2022,10,7)



orders_by_rider = {}

products = []

startTimeCode = aTime.strftime('%Y') + '-' + aTime.strftime('%m') + '-' + aTime.strftime('%d') + 'T' + aTime.strftime('%H') + ':' + aTime.strftime('%M') + ':' + aTime.strftime('%S') +'.000Z'
endTimeCode = bTime.strftime('%Y') + '-' + bTime.strftime('%m') + '-' + bTime.strftime('%d') + 'T' + bTime.strftime('%H') + ':' + bTime.strftime('%M') + ':' + bTime.strftime('%S') +'.000Z'


mydb =  mariadb.connect(
  host="localhost",
  user="root",
  password="",
  database="Gorillas"
)


cur = mydb.cursor()


baseURL2 = baseURL + '?storeId=' + storeId + '&getInventory=true&recordsPerPage=800'

r = requests.get(baseURL2, headers=headers)
res = r.json()

pages = res['pages']
print(pages)
  
    

    

for i in range(int(pages)):

    mydb =  mariadb.connect(
      host="localhost",
      user="root",
      password="",
      database="Gorillas"
    )


    cur = mydb.cursor()

    URL = baseURL2 + '&pageNumber=' + str(i+1)


    r = requests.get(URL, headers=headers)
    #print(r)
    res = r.json()

    count = len(res['productsList'])

    print(count)
    #print(res['productsList'])

    for j in range(count):

        
        name = res['productsList'][j]['label']
        
        productId = res['productsList'][j]['id']

        sku = res['productsList'][j]['sku']
        #print(name)
        if 'productInventory' in res['productsList'][j].keys():
          #print(res['productsList'][j]['productInventory'])
          if res['productsList'][j]['productInventory']['bin'] != None:

              zone = res['productsList'][j]['productInventory']['bin']['name']
              
              #print(zone)
          else:
              zone = '-'
              #print('-')

          quantity = res['productsList'][j]['productInventory']['quantity']
        else:
          zone = '-'
          quantity = 0

        published = res['productsList'][j]['isPublished']

        

        product = (name,productId,sku,zone,published, quantity)

        URL = baseURL + productId
        print(URL)

        payload = json.dumps({
          "quantity": quantity,
          "sku": sku,
          "storeId": storeId
        })
        print(payload)

        response = requests.request("PUT", URL, headers=headers, data=payload)

        products.append(product)

              

    #print(products)
    #print(len(products))
    if len(products) != 0:
      cur.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)", products)
    mydb.commit()
    mydb.close()
    #print('orders inserted')
    products = []


#print(orders_by_rider)

#print(len(orders))




#print(mydb)