import mysql.connector
from parking_modules.mysql_login import console_connect
from mysql.connector import errorcode
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from datetime import timedelta
from datetime import datetime

placenumberout = 'EBK2129'

try:
    plt.style.use('seaborn-v0_8')
except OSError:
    pass
plt.figure(figsize=(12, 6))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
plt.gca().yaxis.set_major_formatter(mdates.DateFormatter('%#H:%M:%S'))
plt.gcf().autofmt_xdate()

plt.xlabel('Ημέρες αρχής και λήξης συνδρομών οχήματος')
plt.ylabel('Ώρες αρχής και λήξης συνδρομών οχήματος')
plt.suptitle('Συνγκεντροτικός πίνακας συνδρομών του οχήματος: ' + placenumberout)


cnx = console_connect()
mycursor = cnx.cursor()

sql = ("SELECT datestart, dateend, timestart, timeend FROM subscription WHERE placenumber = %s")
val = [(placenumberout)]
mycursor.execute(sql, val)
myresult = mycursor.fetchall()
for x in myresult:
    suball = x
    x = [suball[0], suball[1]]
    y = [datetime.strptime(str(suball[2]), '%H:%M:%S'), datetime.strptime(str(suball[3]), '%H:%M:%S')]
    plt.plot(x,  y)

mycursor.close()
cnx.close()

plt.tight_layout()
plt.show()
