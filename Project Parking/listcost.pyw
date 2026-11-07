import mysql.connector
from parking_modules.mysql_login import gui_connect
import datetime
import time
from datetime import date
from dateutil import parser as dt_parser

from tkinter import *

root = Tk()
root.withdraw()
db = gui_connect(root)
if db is None:
    root.destroy()
    raise SystemExit(0)
root.title("listbox")
root.geometry("200x350")
root.deiconify()

mycursor=db.cursor()

subcostlistbox = Listbox(root)
# List box
# Check subcost
sql = ("SELECT subdays, paysub FROM costsub WHERE id >= '1'")
mycursor.execute(sql)
myresult = mycursor.fetchall()
myresult = str(myresult)
myresult = myresult.replace("[(", "").replace("), (", "-").replace(", ", " Κόστος: ").replace(")]", "")
myresult = list(myresult.split("-"))
for x in myresult:
    dayscost = x
    subcostlistbox.insert(END, "Ημέρες: " + str(dayscost) + "€")
subcostlistbox.pack(pady = 5, padx = 5, ipadx = 25, ipady = 1)

subcostlistbox2 = Listbox(root)
# Check Cost
c = 0
sql = ("SELECT timecost, moneycost FROM costs WHERE id >= '1'")
mycursor.execute(sql)
myresult = mycursor.fetchall()
for x in myresult:
    c = c + 1
    costdate = str(x)
    costdate = costdate.replace("(datetime.timedelta(seconds=", "").replace("),)", "").replace("), ", " ").replace(")", "")
    costdate = costdate.split(" ")
    costdate1 = datetime.timedelta(seconds = int(costdate[0]))
    costdate2 = costdate[1]
    subcostlistbox2.insert(END, "Φάση " + str(c) + "η: " + str(costdate1) + " Κόστος: " + str(costdate2) + "€")
subcostlistbox2.pack(pady = 1, padx = 1, ipadx = 25, ipady = 1)

db.close()

root.mainloop()
