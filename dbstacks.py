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