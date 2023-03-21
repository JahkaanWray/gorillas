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

baseURL = 'https://prod-api.gorillas.io/api/market/products/'






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


baseURL = baseURL + '?storeId=' + storeId + '&getInventory=true&recordsPerPage=800'

r = requests.get(baseURL, headers=headers)
print(r)
res = r.json()

pages = res['pages']
print(pages)
  
    

    

for i in range(int(pages)):

    mydb =  mariadb.connect(
      host="sql904.main-hosting.eu",
      user="u883725273_Jahkaan",
      password="@Lbrighton26",
      database="u883725273_DB"
    )


    cur = mydb.cursor()

    URL = baseURL + '&pageNumber=' + str(i+1)


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

        

        product = (name,productId,sku,zone,published, quantity,0,0,0,0)

        print(product)

        products.append(product)

      

              

    #print(products)
    print(len(products))
    if len(products) != 0:
      cur.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", products)
    mydb.commit()
    mydb.close()
    print('orders inserted')
    products = []


#print(orders_by_rider)

#print(len(orders))




#print(mydb)