import asyncio
import aiohttp
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


results = []

total = 0



startTime = datetime(2023,1,1)
endTime = datetime(2023,1,30)
delta = (endTime - startTime).days + 1
timePeriods = math.floor(delta/14)
leftover = delta % 14
if leftover != 0:
    timePeriods += 1

print(timePeriods) 

def get_tasks(pages, startTimeCode, endTimeCode, session):
    tasks = []
    pages = 100
    for i in range(pages):
        print(i)
        data = {'pageNumber':i+1,
            'recordsPerPage':'300',
            'orderStatus':['COMPLETE'],
            'storeIds':["60795bb8e0c68e33318a303d","6022876dd2c6b32791f92b94","607e97429bcc9e3242a2b747","604698bff57d8a636b8ddf80","60c1c3842842e843d452330c","604a2f5d17be050a2fbbf95a","60e8615c53a1ca1f95b51ddf","60ccc09c8eac0d15b5c1a48d","607ded82aaf59e18e79b9d84","613f88aa0e51165231a23c2b","623c8a9e01768871d1cb844f","60f97af0c8b5640d78e83548","64143a343bfb373e305ea71d","6256b46f99753e53002dc958","6194e5684318ea4126de039e","604697cb3c49672892854437","612e44f6936e315fd2fe03b6","60468968c7ee951c47bb11d4","609b945d1620cc6739e51bb8","619bbf29b4c22b4869bb36bf","6246f0e86e0fc4599930c5cb","6246fa5cdfb08315fac49c01","62472868ac9224320312a720","618bbabdd359a8553d224806","609bfe9c4a581e14ac61133f","61b9fd8a8a85e63c2918c13e","607d9b22a5190770ce9ae150","62a0a461953cb76c6acd56fa","6271641f3b131523c81b48ad","60cf68e8707060600518cf6c","601bd862abed3143952a8049","61019d249c42dd0fe73f5087","60917884131bca3e3d625841","61a89e5483fd67700d1155b8","6171a01de6e8c805d9eefa86","622fa376d32d3c369d59cbcb","619bc156fc573a057529252c","61656aa8687fb43745116be2","6083bfc7b309d43032455fef","614a103bfd6c186e67dc7e13","60c43fd6b3e01b5ee00f77ec","60a506c2097d492747516f66","60a6919a685dad25b437e635","627e8467a83278649aa3bde6"],
            'createdAfter':startTimeCode,
            'createdBefore':endTimeCode
        }
        tasks.append(asyncio.create_task(session.post(url, json=data, headers=headers)))
    return tasks



async def getOrders(pages, startTimeCode, endTimeCode):
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(pages, startTimeCode, endTimeCode, session)

        responses = await asyncio.gather(*tasks)

        print(responses)

        for i in range(len(responses)):
            print(i)
            results.append(await responses[i].json())

        
        #print(json.dumps(results[0]))

def parseResponse(response):
    parsedResponse = []
    for item in response['items']:

        if 'activeWorker' in item['dispatch']:
            rider = item['dispatch']['activeWorker']['name']
            if rider == None:
                rider = 'None'
        else:
            rider = 'None'

        if 'pickerName' in item['orderDetails']['pickData']:
            picker = item['orderDetails']['pickData']['pickerName']
            if picker == None:
                picker = 'None'
        else:
            picker = 'None'



        orderId = item['id']
        storeId = item['store']['id']
        customer = item['customer']['name']
        seq = item['customer']['sequence']

        createdOn = item['createdOn']
        completedOn = item['completedOn']
        if completedOn == None:
            completedOn = 0

        createdOn = 0
        pickedOn = 0
        confirmedOn = 0
        assignedOn = 0
        startedOn = 0
        createdOn = 0

        events = item['workflowData']['events']

        for k in range(len(events)):
            eventType = events[k]['event']
            if eventType == 'START':
                createdOn = events[k]['timestamp']
            elif eventType == 'PROCESS':
                pickedOn = events[k]['timestamp']
            elif eventType == 'CONFIRM':
                confirmedOn = events[k]['timestamp']
            elif eventType == 'ASSIGN':
                assignedOn = events[k]['timestamp']
            elif eventType == 'START_TRIP':
                startedOn = events[k]['timestamp']
            elif eventType == 'COMPLETE_TRIP':
                completedOn = events[k]['timestamp']

        latitude = item['dispatch']['dropOff']['address']['coordinates']['lat']
        longitude = item['dispatch']['dropOff']['address']['coordinates']['lon']

        distance = item['travelDistance']

        distance = 0

        parsedResponse.append((orderId,storeId,rider,picker,customer,latitude,longitude,distance,createdOn,pickedOn,confirmedOn,assignedOn,startedOn,completedOn,seq,0))
        

    return parsedResponse

async def getOrderData(startTimeCode, endTimeCode, page, session):
    data = {'pageNumber':page,
            'recordsPerPage':'300',
            'orderStatus':['COMPLETE'],
            'storeIds':["60795bb8e0c68e33318a303d","6022876dd2c6b32791f92b94","607e97429bcc9e3242a2b747","604698bff57d8a636b8ddf80","60c1c3842842e843d452330c","604a2f5d17be050a2fbbf95a","60e8615c53a1ca1f95b51ddf","60ccc09c8eac0d15b5c1a48d","607ded82aaf59e18e79b9d84","613f88aa0e51165231a23c2b","623c8a9e01768871d1cb844f","60f97af0c8b5640d78e83548","64143a343bfb373e305ea71d","6256b46f99753e53002dc958","6194e5684318ea4126de039e","604697cb3c49672892854437","612e44f6936e315fd2fe03b6","60468968c7ee951c47bb11d4","609b945d1620cc6739e51bb8","619bbf29b4c22b4869bb36bf","6246f0e86e0fc4599930c5cb","6246fa5cdfb08315fac49c01","62472868ac9224320312a720","618bbabdd359a8553d224806","609bfe9c4a581e14ac61133f","61b9fd8a8a85e63c2918c13e","607d9b22a5190770ce9ae150","62a0a461953cb76c6acd56fa","6271641f3b131523c81b48ad","60cf68e8707060600518cf6c","601bd862abed3143952a8049","61019d249c42dd0fe73f5087","60917884131bca3e3d625841","61a89e5483fd67700d1155b8","6171a01de6e8c805d9eefa86","622fa376d32d3c369d59cbcb","619bc156fc573a057529252c","61656aa8687fb43745116be2","6083bfc7b309d43032455fef","614a103bfd6c186e67dc7e13","60c43fd6b3e01b5ee00f77ec","60a506c2097d492747516f66","60a6919a685dad25b437e635","627e8467a83278649aa3bde6"],
            'createdAfter':startTimeCode,
            'createdBefore':endTimeCode
        }
    response = await session.post(url, json=data, headers=headers)
    print(response.status)
    responseJSON = await response.json()

    print(len(responseJSON['items']))

    return responseJSON

async def runProgram(startTimeCode, endTimeCode, page, session):
    response = await getOrderData(startTimeCode, endTimeCode, page, session)
    parsedResponse = parseResponse(response)
    return parsedResponse
    #print(json.dumps(response))

            
async def main(startTimeCode, endTimeCode, startPage, endPage):
    async with aiohttp.ClientSession() as session:
        parsedResponses = await asyncio.gather(*[runProgram(startTimeCode, endTimeCode, page, session) for page in range(startPage, endPage + 1)])

        return parsedResponses

def insertIntoDB(data):
    flatList = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            flatList.append(data[i][j])


    mydb =  mariadb.connect(
        host="sql904.main-hosting.eu",
        user="u883725273_Jahkaan",
        password="@Lbrighton26",
        database="u883725273_DB"
    )


    cur = mydb.cursor()

    cur.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", flatList)
    mydb.commit()
    mydb.close()
    print(str(len(flatList)) + ' orders inserted')
        



for j in range(timePeriods):

    aTime = startTime + timedelta(days=14*j)
    if j == timePeriods - 1:
        bTime = endTime + timedelta(days=1) - timedelta(seconds=1)
    else:
        bTime = startTime + timedelta(days=14*(j+1)) - timedelta(seconds=1)

    startTimeCode = aTime.strftime('%Y') + '-' + aTime.strftime('%m') + '-' + aTime.strftime('%d') + 'T' + aTime.strftime('%H') + ':' + aTime.strftime('%M') + ':' + aTime.strftime('%S') +'.000Z'
    endTimeCode = bTime.strftime('%Y') + '-' + bTime.strftime('%m') + '-' + bTime.strftime('%d') + 'T' + bTime.strftime('%H') + ':' + bTime.strftime('%M') + ':' + bTime.strftime('%S') +'.000Z'


    
    data = {'pageNumber':1,
        'recordsPerPage':'300',
        'orderStatus':['COMPLETE'],
        'storeIds':["60795bb8e0c68e33318a303d","6022876dd2c6b32791f92b94","607e97429bcc9e3242a2b747","604698bff57d8a636b8ddf80","60c1c3842842e843d452330c","604a2f5d17be050a2fbbf95a","60e8615c53a1ca1f95b51ddf","60ccc09c8eac0d15b5c1a48d","607ded82aaf59e18e79b9d84","613f88aa0e51165231a23c2b","623c8a9e01768871d1cb844f","60f97af0c8b5640d78e83548","64143a343bfb373e305ea71d","6256b46f99753e53002dc958","6194e5684318ea4126de039e","604697cb3c49672892854437","612e44f6936e315fd2fe03b6","60468968c7ee951c47bb11d4","609b945d1620cc6739e51bb8","619bbf29b4c22b4869bb36bf","6246f0e86e0fc4599930c5cb","6246fa5cdfb08315fac49c01","62472868ac9224320312a720","618bbabdd359a8553d224806","609bfe9c4a581e14ac61133f","61b9fd8a8a85e63c2918c13e","607d9b22a5190770ce9ae150","62a0a461953cb76c6acd56fa","6271641f3b131523c81b48ad","60cf68e8707060600518cf6c","601bd862abed3143952a8049","61019d249c42dd0fe73f5087","60917884131bca3e3d625841","61a89e5483fd67700d1155b8","6171a01de6e8c805d9eefa86","622fa376d32d3c369d59cbcb","619bc156fc573a057529252c","61656aa8687fb43745116be2","6083bfc7b309d43032455fef","614a103bfd6c186e67dc7e13","60c43fd6b3e01b5ee00f77ec","60a506c2097d492747516f66","60a6919a685dad25b437e635","627e8467a83278649aa3bde6"],
        'createdAfter':startTimeCode,
        'createdBefore':endTimeCode}

    r = requests.post(url, headers=headers, json=data)
    res = r.json()

    pages = res['totalPages']

    #print(startTimeCode)
    #print(endTimeCode)
    #print(pages)

    numRequestsBlocks = math.floor(pages/100) + 1

    for i in range(numRequestsBlocks):
        startPage = 100*i + 1
        if (i+1 == numRequestsBlocks):
            endPage = pages
        else:
            endPage = startPage + 99

        
        print(startTimeCode)
        print(endTimeCode)
        print('p' + str(startPage) + ' - ' + 'p' + str(endPage))
        
        parsedResponses = asyncio.run(main(startTimeCode, endTimeCode, startPage, endPage))
        insertIntoDB(parsedResponses)
        




      
        

    