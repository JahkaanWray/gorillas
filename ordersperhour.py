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

mydb =  mariadb.connect(
      host="sql904.main-hosting.eu",
      user="u883725273_Jahkaan",
      password="@Lbrighton26",
      database="u883725273_DB"
    )

cur = mydb.cursor()

startTime = 1672617600000

orders = []
sum = 0
ophsum = 0

ridersum = 0

for i in range(24):
    startTime = 1672963200000 + i*60*60*1000
    mydb =  mariadb.connect(
      host="sql904.main-hosting.eu",
      user="u883725273_Jahkaan",
      password="@Lbrighton26",
      database="u883725273_DB"
    )

    cur = mydb.cursor()

    endTime = startTime + 60*60*1000 - 1

    cur.execute("SELECT COUNT(DISTINCT rider) FROM orders WHERE createdOn BETWEEN " + str(startTime) + " AND " + str(endTime))


    
    rows = cur.fetchall()
    riders = rows[0][0]
    ridersum += riders
    #print(rows[0][0])
    #sum += rows[0][0]

    cur.execute("SELECT COUNT(rider) FROM orders WHERE createdOn BETWEEN " + str(startTime) + " AND " + str(endTime))
    rows = cur.fetchall()
    o = rows[0][0]
    sum += o

    if riders == 0:
        oph = 0
        #orders.append(0)
    else:
        oph = o/riders
        #orders.append(o/riders)
    ophsum += oph
    print(oph)
    orders.append(o)


    #plt.show()

print(sum/ridersum)
print(sum)
y=[]
#for i in range(24):
 ##   n=20
   # if i < n:
    #    y.append(0)
    #else:
     #   sum=0
      #  for j in range(n+1):
       #     sum += orders[i-j]
        #y.append(sum/(n+1))
#print(sum)
x = np.arange(24)

plt.bar(x,orders, color=(0,0,1,0.5))
#plt.show()
#plt.plot(x,y)
#plt.bar(x,[0,0,0,0,0,0,0,0,5,6,12,7,14,10,2,12,14,16,16,23,16,8,16,5], color=(1,0,0,0.5))
plt.show()
#fig = plt.figure()
#animator = FuncAnimation(fig, animate, frames = 550, interval=100, repeat=False)
#plt.show()
#
#writer = PillowWriter(fps=30)
#animator.save("toprider.gif", writer=writer)#

mydb.commit()
mydb.close()