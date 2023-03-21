import requests
import matplotlib.pyplot as plt
import json
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


data = {'pageNumber':1,
    'recordsPerPage':'300',
    'orderStatus':['COMPLETE'],
    'storeIds':[storeId]}

r = requests.post(url, headers=headers, json=data)
res = r.json()
totalOrders = res['totalRecords']
pages = res['totalPages']
leftover = totalOrders % 300
print(res['totalRecords'])

print('leftover: ' + str(leftover))

orders_by_rider = {}

for i in range(pages):
    print('page ' + str(i+1))
    data = {'pageNumber':i+1,
    'recordsPerPage':'300',
    'orderStatus':['COMPLETE'],
    'storeIds':[storeId]}

    r = requests.post(url, headers=headers, json=data)
    res = r.json()

    if i != pages - 1:
        count = 300
    else:
        count = leftover

    for j in range(count):
            name = res['items'][j]['dispatch']['activeWorker']['name']
            if name in orders_by_rider:
                orders_by_rider[name] += 1
            else:
                orders_by_rider[name] = 1

print(orders_by_rider)
total = 0
for rider in orders_by_rider:
    total += orders_by_rider[rider]

print(total)

plt.bar(range(len(orders_by_rider)), list(orders_by_rider.values()), align='center')
plt.xticks(range(len(orders_by_rider)), list(orders_by_rider.keys()), rotation='vertical')

plt.show()

with open('orders.json', 'w') as fp:
    json.dump(orders_by_rider, fp)