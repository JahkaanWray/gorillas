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


baseURL = baseURL + '?storeId=' + storeId + '&getInventory=true&recordsPerPage=100'

r = requests.get(baseURL, headers=headers)
res = r.json()

pages = res['pages']
print(pages)
  
    

data = []

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

        #print(product)

        products.append(product)

        url = "https://prod-api.gorillas.io/api/v1/market/inventory/logs"

        payload = json.dumps({
            "storeId": config.storeId,
            "productId": productId,
            "startDate": "2023-02-05T00:00:00.000Z",
            "endDate": "2023-02-07T00:00:00.000Z",
            "action": [
                "BULK_UPDATE",
                "UPDATE",
                "REPLENISHED",
                "SCRAPPED",
                "COUNTING"
            ],
            "recordsPerPage": 1000,
            "pageNumber": 1
        })

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response)
        logs = response.json()

        print(i*100 + j)

        for k in range(len(logs)):
            valid = False
            label = logs[k]['label']
            timestamp = logs[k]['createdOn']
            print(label)
            if "UPDATE" in label and "BIN" not in label and "RESET" not in label and "PUBLISH" not in label:
                valid = True
                action = "UPDATE"
                a = label.find("QTY")
                b = label.find("TO")
                startval = int(label[a+4:b-1])
                endval = int(label[b+3:])
                qty = endval - startval

                d = label.find("UPDATE")

                picker = label[:d-1]
            if "REPLENISHED" in label:
                valid = True
                action = "REPLENISHED"
                a = label.find("QTY")
                b = label.find("FROM")
                c = label.find("TO")

                qty = int(label[a+4:b-1])
                startval = int(label[b+5:c-1])
                endval = int(label[c+3:])

                d = label.find("REPLENISHED")

                picker = label[7:d-1]
            if "COUNTING" in label:
                valid = True
                action = "COUNTING"
                a = label.find("QTY")
                b = label.find("FROM")
                c = label.find("TO")

                qty = int(label[a+4:b-1])
                startval = int(label[b+5:c-1])
                endval = int(label[c+3:])

                d = label.find("COUNTING")

                picker = label[7:d-1]
                
            if "SCRAPPED" in label:
                valid = True
                action = "SCRAPPED"
                a = label.find("QTY")
                b = label.find("FROM")
                c = label.find("TO")

                qty = int(label[a+4:b-1])
                startval = int(label[b+5:c-1])
                endval = int(label[c+3:])

                d = label.find("SCRAPPED")

                picker = label[7:d-1]
            print(picker)
            
            if valid:
                data.append((productId,picker,label,action,qty,startval,endval,timestamp))
      

              

    #print(products)
    print(len(data))
    if len(data) != 0:
      cur.executemany("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
    mydb.commit()
    mydb.close()
    #print('orders inserted')
    data = []


#print(orders_by_rider)

#print(len(orders))




#print(mydb)