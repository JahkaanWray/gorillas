import requests
import matplotlib.pyplot as plt
import json
from datetime import datetime
from datetime import timedelta
import math
import numpy as np
import mariadb


startDate = datetime(2022,11,1)
endDate = datetime(2022,12,3)

delta = (endDate - startDate).days + 1

for i in range(delta):
    date = startDate + timedelta(days=i)

    dateCode = date.strftime('%Y') + '-' + date.strftime('%m') + '-' + date.strftime('%d')#
    print(dateCode)
    mydb =  mariadb.connect(
      host="sql904.main-hosting.eu",
      user="u883725273_Jahkaan",
      password="@Lbrighton26",
      database="u883725273_DB"
    )

    cur = mydb.cursor()

    cur.execute('SELECT store, REC, points FROM leaderboard WHERE date = "' + dateCode + '" ORDER BY REC ASC')

    rows = cur.fetchall()

    wh = rows[0][0]

    points = rows[0][2]

    sql = "UPDATE leaderboard SET points = " + str(10) + " WHERE store = '" + wh + "' AND date = " + dateCode

    print(sql)

    cur.execute("UPDATE leaderboard SET points = " + str(points + 1) + " WHERE store = '" + wh + "' AND date = '" + dateCode + "'")

    cur.execute('SELECT store, OPH, points FROM leaderboard WHERE date = "' + dateCode + '" ORDER BY OPH DESC')

    rows = cur.fetchall()

    wh = rows[0][0]

    points = rows[0][2]

    sql = "UPDATE leaderboard SET points = " + str(points + 1) + " WHERE store = '" + wh + "' AND date = " + dateCode

    print(sql)

    cur.execute("UPDATE leaderboard SET points = " + str(points + 1) + " WHERE store = '" + wh + "' AND date = '" + dateCode + "'")


    mydb.commit()
    mydb.close()

    print(wh)