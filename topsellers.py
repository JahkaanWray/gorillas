import requests
import matplotlib.pyplot as plt
import json

storeId = '604a2f5d17be050a2fbbf95a'

headers = {'Content-Type':'application/json',
    'Cookie':'JSESSIONID=CoTqtMsP-LnSrU0pdJdKeClvXHwClE1XeLBF2VxI',
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Connection':'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Authorization': 'Bearer eyJhbGciOiJIUzM4NCJ9.eyJzdWIiOiJhcHBsaWNhdGlvbiIsImlzcyI6ImdvcmlsbGFzLW1vbm9saXRoIiwidWlkIjoiZ1FKRDEyUjVRbVd0Sy16akVFZ0xMdyIsInRhZ3MiOlsiSU5WRU5UT1JZX0VESVRfUVVBTlRJVFkiLCJVU0VSX0VESVQiLCJSSURFUl9FRElUIiwiSU5WRU5UT1JZX0xJU1RfUFVSQ0hBU0VfT1JERVJTIiwiUklERVJfTElTVCIsIk9SREVSX0NPTkZJUk0iLCJJTlZFTlRPUllfTElTVF9ERUxJVkVSWV9OT1RFUyIsIklOVkVOVE9SWV9FRElUX1pPTkUiLCJURUFNX0RFTEVURSIsIlJJREVSX0RFTEVURSIsIklOVkVOVE9SWV9ERUxJVkVSX0RFTElWRVJZIiwiUFJPTU9fTElTVCIsIklOVkVOVE9SWV9SRVBMRU5JU0hfREVMSVZFUlkiLCJUSUNLRVRfTElTVCIsIklOVkVOVE9SWV9DT1VOVF9ERUxJVkVSWSIsIlRFQU1fRURJVCIsIklOVkVOVE9SWV9WSUVXX0RFTElWRVJZX05PVEUiLCJURUFNX0xJU1QiLCJVU0VSX0NSRUFURSIsIlZFTkRPUlNfTElTVCIsIk9SREVSX0NBTkNFTCIsIklOVkVOVE9SWV9WSUVXX1BVUkNIQVNFX09SREVSIiwiT1JERVJfTElTVCIsIlVTRVJfTElTVCIsIklOVkVOVE9SWV9FRElUIiwiT1JERVJfQ09NUExFVEUiLCJJTlZFTlRPUllfTElTVCIsIk9SREVSX0FTU0lHTiIsIk9SREVSX0VESVQiLCJJTlZFTlRPUllfUkVDRUlWRV9ERUxJVkVSWSIsIlBPUlRBTF9VU0VSIl0sImFwaVR5cGUiOiJQT1JUQUwiLCJpYXQiOjE2NjE5MTEwNzcsInVzZXJJZCI6IjYyM2RmMTc0YjZlMjk4MzI5NDM1ODlmYiIsInN0b3JlSWQiOiI2MDRhMmY1ZDE3YmUwNTBhMmZiYmY5NWEiLCJyb2xlcyI6WyJVU0VSIiwiQVBJX1VTRVIiXSwidGVuYW50IjoiWnpSbUJnazNTSnFBRUZadzFQNWNkQSJ9.i4jLW0mG5OOld8W7oBB-XGkFlhKayNi0GPIbZxT54qyxRZc94TVZY9Pu6mpADiF2'}

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

