from tkinter import *
from tkinter import ttk
import mysql.connector
from parking_modules.mysql_login import gui_connect

import re

screen = Tk()
screen.withdraw()
db = gui_connect(screen)
if db is None:
    screen.destroy()
    raise SystemExit(0)

mycursor=db.cursor()

# Check subcost without assuming contiguous database IDs.
sql = ("SELECT subdays FROM costsub WHERE id >= 0 ORDER BY id ASC")
mycursor.execute(sql)
myresult = mycursor.fetchall()
my_weekdays_names = [str(row[0]) for row in myresult] or ["0"]
ids = len(my_weekdays_names) - 1

screen.deiconify()


def weekdaySelection(event):
   for x in range(ids + 1):
      if weekdaysDropdown.get() == my_weekdays_names[x]:
         print(my_weekdays_names[x])
          
          
weekdaysDropdown = ttk.Combobox(screen, values = my_weekdays_names)
weekdaysDropdown.current(0)
weekdaysDropdown.bind("<<ComboboxSelected>>", weekdaySelection)
weekdaysDropdown.grid()

# Εκκίνηση του Tk event loop.
screen.mainloop()

try:
   mycursor.close()
   db.close()
except:
   pass
