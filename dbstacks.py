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


mydb =  mariadb.connect(
      host="sql904.main-hosting.eu",
      user="u883725273_Jahkaan",
      password="@Lbrighton26",
      database="u883725273_DB"
)


cur = mydb.cursor()

cur.execute("SELECT * FROM orders WHERE createdOn <= 1672531200000 AND createdOn > 1667260800000 ORDER BY createdOn ASC")

rows = cur.fetchall()

print(len(rows))


for i in range(len(rows)):
    row = rows[i]
    orderId = row[0]
    rider = row[1]
    createdOn = row[7]
    assignedOn = row[10]
    startedOn = row[11]
    completedOn = row[12]
    #print("SELECT COUNT(orderId) FROM orders WHERE rider = '" + rider + "' AND assignedOn  < " + str(completedOn) + " AND completedOn > " + str(completedOn) + " AND assignedOn != 0")
    cur.execute("SELECT COUNT(orderId) FROM orders WHERE rider = '" + rider + "' AND assignedOn  < " + str(completedOn) + " AND completedOn > " + str(completedOn) + " AND assignedOn != 0")

    rows2 = cur.fetchall()

    #print(completedOn)
    #print(rows2[0][0])
    a = rows2[0][0]
    cur.execute("SELECT COUNT(orderId) FROM orders WHERE rider = '" + rider + "' AND assignedOn < " + str(startedOn) + " AND completedOn > " + str(startedOn) + " AND assignedOn != 0")
    rows2 = cur.fetchall()
    b = rows2[0][0]
    
    cur.execute("UPDATE orders SET stack = " + str(b-a) + " WHERE orderId = '" + str(orderId)+"'")
    mydb.commit()
    print(i/len(rows))

mydb.close()