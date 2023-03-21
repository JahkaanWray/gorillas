import requests
import matplotlib.pyplot as plt
import json

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

top_sellers = {}

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

            numberOfProducts = len(res['items'][j]['orderDetails']['items'])

            for k in range(numberOfProducts):
                if res['items'][j]['orderDetails']['items'][k]['bin'] is not None:
                    zone = res['items'][j]['orderDetails']['items'][k]['bin']['zone']
                product = res['items'][j]['orderDetails']['items'][k]['name']
                quantity = res['items'][j]['orderDetails']['items'][k]['quantity']
                if zone == 'B1':
                    if product in top_sellers:
                        top_sellers[product] += quantity
                    else:
                        top_sellers[product] = quantity

print(top_sellers)
total = 0

sorted_dict = {}
sorted_keys = sorted(top_sellers, key=top_sellers.get, reverse=True)  # [1, 3, 2]

for w in sorted_keys:
    sorted_dict[w] = top_sellers[w]

plt.bar(range(len(sorted_dict)), list(sorted_dict.values()), align='center')
plt.xticks(range(len(sorted_dict)), list(sorted_dict.keys()), rotation='vertical')

plt.show()

