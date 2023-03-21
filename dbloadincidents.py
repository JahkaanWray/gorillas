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
    'Authorization': 'Bearer ' + config.gorillas_api_key
}
baseURL = 'https://prod-api.gorillas.io/api/market/admin/tickets/list'






aTime = datetime(2022,11,23)
bTime = datetime(2022,12,1)



orders_by_rider = {}

products = []

startTimeCode = aTime.strftime('%Y') + '-' + aTime.strftime('%m') + '-' + aTime.strftime('%d') + 'T' + aTime.strftime('%H') + ':' + aTime.strftime('%M') + ':' + aTime.strftime('%S') +'.000Z'
endTimeCode = bTime.strftime('%Y') + '-' + bTime.strftime('%m') + '-' + bTime.strftime('%d') + 'T' + bTime.strftime('%H') + ':' + bTime.strftime('%M') + ':' + bTime.strftime('%S') +'.000Z'


mydb =  mariadb.connect(
  host=config.dbInfo['host'],
  user=config.dbInfo['user'],
  password=config.dbInfo['password'],
  database=config.dbInfo['database']
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
  host=config.dbInfo['host'],
  user=config.dbInfo['user'],
  password=config.dbInfo['password'],
  database=config.dbInfo['database']
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