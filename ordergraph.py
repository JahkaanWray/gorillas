import requests
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
import matplotlib
import numpy as np
import json
from datetime import datetime
from datetime import timedelta
import math
import mariadb
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from random import random
import config

mydb =  mariadb.connect(
        host="localhost",
        user="root",
        password="",
        database="Gorillas"
    )

cur = mydb.cursor()

startTime = 1617058800000

orders_by_rider = {}

colours = {}

def animate(i):
    startTime = 1617058800000 + i*24*60*60*1000
    mydb =  mariadb.connect(
        host="localhost",
        user="root",
        password="",
        database="Gorillas"
    )

    cur = mydb.cursor()

    endTime = startTime + 24*60*60*1000 - 1

    cur.execute("SELECT rider FROM orders WHERE timestamp BETWEEN " + str(startTime) + " AND " + str(endTime))

    rows = cur.fetchall()
    for row in rows:
        rider = row[0]
        if rider == "Curtis (Agency)":
            rider = "Curtis A"
        if rider == "Adam Peter Thomas":
            rider = "Adam Thomas "
        if rider not in orders_by_rider:
            orders_by_rider[rider] = 1
            colours[rider] = [math.floor(255*random()),math.floor(255*random()),math.floor(255*random())]
        else: 
            orders_by_rider[rider] += 1

    
    sorted_dict = {}
    sorted_keys = sorted(orders_by_rider, key=orders_by_rider.get, reverse=True)  # [1, 3, 2]

    for w in sorted_keys:
        sorted_dict[w] = orders_by_rider[w]
    
    startTime = endTime + 1
    print(i)
    print(sorted_dict)
    top10riders = {k: sorted_dict[k] for k in list(sorted_dict)[:18]}
    plt.bar(range(len(top10riders)), list(top10riders.values()), align='center',color=(0.2, 0.4, 0.6, 1))
    plt.xticks(range(len(top10riders)), list(top10riders.keys()), rotation='vertical')

    data = 255*np.ones((1080, 1920, 3), dtype=np.uint8)
    max_rides = list(top10riders.values())[0]
    for j in range(len(list(top10riders.keys()))):
        width = math.floor(1720*list(top10riders.values())[j]/max_rides)
        #print(width)
        data[60*j:60*j + 45, 0:width] = colours[list(top10riders.keys())[j]]
    img = Image.fromarray(data, 'RGB')
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype("abel-regular.ttf", 32)
    #    draw.text((x, y),"Sample Text",(r,g,b))
    for j in range(len(list(top10riders.keys()))):
        width = math.floor(1720*list(top10riders.values())[j]/max_rides)
        #print(width)
        #data[100*j:100*j + 80, 0:width] = colours[list(top10riders.keys())[j]]
        draw.text((0, 60*j),list(top10riders.keys())[j],(255,255,255),font=font)
        draw.text((width + 40, 60*j),str(list(top10riders.values())[j]),(0,0,0),font=font)
    img.save('images/img' + str(i) + '.jpeg')
    

    #plt.show()


for i in range(800):
    animate(i)



mydb.commit()
mydb.close()