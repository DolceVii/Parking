"""Χρεώσεις, τιμοκατάλογος, στοιχεία εταιρείας και θέσεις."""

def create_handlers(self, top, handlers):
    """Επιστρέφει callbacks με κοινό περιβάλλον, χωρίς μεταβολή λογικής GUI."""

    def CurSelect1(event):
        global COSTpDAY
        try:
            self.EntryDAY.delete(0, 'end')
            self.EntryCOST.delete(0, 'end')
            widget = event.widget
            selection = widget.curselection()
            COSTpDAY = widget.get(selection[0])
            COSTpDAY = re.findall(r'\d+.+', COSTpDAY)
            COSTpDAY = str(COSTpDAY)
            COSTpDAY = COSTpDAY.replace("['", "").replace(" Κόστος: ", " ").replace("€']", "")
            COSTpDAY = list(COSTpDAY.split(" "))
            self.EntryDAY.insert(0, COSTpDAY[0])
            self.EntryCOST.insert(0, COSTpDAY[1])
        except:
            pass

    def CurSelect2(event):
        global COSTpTIME
        try:
            self.EntryTIMEs.delete(0, 'end')
            self.EntryCOSTs.delete(0, 'end')
            widget = event.widget
            selection = widget.curselection()
            COSTpTIME = widget.get(selection[0])
            COSTpTIME = re.findall(r'\d+.+', COSTpTIME)
            COSTpTIME = str(COSTpTIME)
            COSTpTIME = COSTpTIME.replace("['", "").replace(" Κόστος: ", " ").replace("€']", "")
            COSTpTIME = list(COSTpTIME.split(" "))
            self.EntryTIMEs.insert(0, COSTpTIME[1])
            self.EntryCOSTs.insert(0, COSTpTIME[2])
        except:
            pass

    def button4():
        gc.collect()
        global totaltime
        global pay
        global myresult
        global subdateend
        global subdtimeend
        global dateendsub
        global timeendsub
        global payfpa
        global fpa
        global totalcost
        global myday
        global year
        global month
        global day
        global cal
        global subdaysDropdown
        global subcostlistbox
        global subcostlistbox2
        global passwords
        global hosts
        global users
        global base
        global scrollbarresult2
        global cnx
        global mycursor
        global myresult
        global c

        self.Frame1.place_forget()
        self.Frame2.place_forget()
        self.Frame3.place_forget()
        self.Frame5.place_forget()
        self.Frame4.place(relx=0.009, rely=0.074, relheight=0.853, relwidth=0.979)

        totaltime = 0
        pay = 0
        myresult = 0
        subdateend = 0
        subdtimeend = 0
        dateendsub = 0
        timeendsub = 0
        payfpa = 0
        fpa = 0
        totalcost = 0
        self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
        try:
            cal.destroy()
            cal = 0
        except:
            pass
        try:
            subdaysDropdown.destroy()
        except:
            pass
        try:
            subcostlistbox.destroy()
        except:
            pass
        try:
            subcostlistbox2.destroy()
        except:
            pass
        try:
            scrollbarresult2.destroy()
        except:
            pass

        # Clear Entries
        self.Entry11121.delete(0, 'end')
        self.Entry11122.delete(0, 'end')
        self.Entry11123.delete(0, 'end')
        self.Entry11124.delete(0, 'end')
        self.Entry11125.delete(0, 'end')
        self.Entry11126.delete(0, 'end')
        self.Entry11127.delete(0, 'end')
        self.Entry11128.delete(0, 'end')
        self.EntryDAY.delete(0, 'end')
        self.EntryTIMEs.delete(0, 'end')
        self.EntryCOST.delete(0, 'end')
        self.EntryCOSTs.delete(0, 'end')
        self.EntryplacesU.delete(0, 'end')

        #Company mySQL Data
        try:
            cnx = mysql.connector.connect(user = users,
                                          password = passwords,
                                          host = hosts,
                                          database = base,
                                          connect_timeout = 5)
            mycursor = cnx.cursor()

            # Listbox 1 ----------------------------------------------------------------------------------------
            subcostlistbox = Listbox(self.Frame4, font = 'Arial 12', borderwidth = 4, highlightthickness = 0, width = 26, height = 10, cursor="hand1")
            sql = ("SELECT subdays, paysub FROM costsub WHERE id >= '1'")
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            myresult = str(myresult)
            if str(myresult) != "[]":
                myresult = myresult.replace("[(", "").replace("), (", "-").replace(", ", " Κόστος: ").replace(")]", "")
                myresult = list(myresult.split("-"))
                for x in myresult:
                    dayscost = x
                    subcostlistbox.insert(END, "Ημέρες: " + str(dayscost) + "€")
                subcostlistbox.pack(pady = 46, padx = 230, anchor = 'nw')
                subcostlistbox.bind('<<ListboxSelect>>', CurSelect1)
            else:
                subcostlistbox.pack(pady = 46, padx = 230, anchor = 'nw')
                subcostlistbox.bind('<<ListboxSelect>>', CurSelect1)

            # Listpox 2 -----------------------------------------------------------------------------------------
            subcostlistbox2 = Listbox(self.Frame4, font = 'Arial 12', borderwidth = 4, highlightthickness = 0, width = 26, height = 13, cursor="hand1")
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
            subcostlistbox2.pack(pady = 23, padx = 230, anchor = 'nw')
            subcostlistbox2.bind('<<ListboxSelect>>', CurSelect2)

            # ΑΦΜ
            sql = ("SELECT afm FROM company")
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            for f in myresult:
               afm1 = f
            self.Entry11126.insert(0, afm1)

            # ΔΟΥ
            sql = ("SELECT doy FROM company")
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            for f in myresult:
               doy1 = f
            self.Entry11127.insert(0, doy1)

            # Διεύθυνση
            sql = ("SELECT address FROM company")
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            for f in myresult:
               address1 = f
            self.Entry11123.insert(0, address1)

            # Πόλη
            sql = ("SELECT city FROM company")
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            for f in myresult:
               city1 = f
            self.Entry11125.insert(0, city1)

            # Τηλέφωνο
            sql = ("SELECT telephone FROM company")
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            for f in myresult:
               telephone1 = f
            self.Entry11124.insert(0, telephone1)

            # Τίτλος 1
            sql = ("SELECT title1 FROM company")
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            for f in myresult:
               title11 = f
            self.Entry11121.insert(0, title11)

            # Τίτλος 2
            sql = ("SELECT title2 FROM company")
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            for f in myresult:
               title21 = f
            self.Entry11122.insert(0, title21)

            # Φ.Π.Α.
            sql = ("SELECT costfpa FROM fpa")
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            for f in myresult:
               fpa1 = f               
            self.Entry11128.insert(0, fpa1)

            # Θέσεις πάρκινγκ
            sql = ("SELECT remaneplaces FROM places")
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            for f in myresult:
               park1 = f               
            self.EntryplacesU.insert(0, park1)
        except:
            pass

        # Check if set for fist time places and company
        try:
            cnx = mysql.connector.connect(user = users,
                                          password = passwords,
                                          host = hosts,
                                          database = base,
                                          connect_timeout = 5)
            mycursor = cnx.cursor()

            sql = ("SELECT lockout FROM lockm")
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            for x in myresult:
                lockplace = x
            if lockplace == 0:
                self.Buttonplaces.configure(state = "normal")
                self.EntryplacesU.configure(state = "normal")
            else:
                self.Buttonplaces.configure(state = "disabled")
                self.EntryplacesU.configure(state = "disabled")

            sql = ("SELECT lockout2 FROM lockm")
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            for x in myresult:
                lockplace2 = x
            if lockplace2 == 0:
                self.Button77775.configure(state = "normal")
                self.Entry11121.configure(state = "normal")
                self.Entry11122.configure(state = "normal")
                self.Entry11123.configure(state = "normal")
                self.Entry11124.configure(state = "normal")
                self.Entry11125.configure(state = "normal")
                self.Entry11126.configure(state = "normal")
                self.Entry11127.configure(state = "normal")
                self.Entry11128.configure(state = "normal")
            else:
                self.Button77775.configure(state = "disabled")
                self.Entry11121.configure(state = "disabled")
                self.Entry11122.configure(state = "disabled")
                self.Entry11123.configure(state = "disabled")
                self.Entry11124.configure(state = "disabled")
                self.Entry11125.configure(state = "disabled")
                self.Entry11126.configure(state = "disabled")
                self.Entry11127.configure(state = "disabled")
                self.Entry11128.configure(state = "disabled")
        except:
            self.Buttonplaces.configure(state = "disabled")
            self.Button77775.configure(state = "disabled")
            self.EntryplacesU.configure(state = "disabled")
            self.Entry11121.configure(state = "disabled")
            self.Entry11122.configure(state = "disabled")
            self.Entry11123.configure(state = "disabled")
            self.Entry11124.configure(state = "disabled")
            self.Entry11125.configure(state = "disabled")
            self.Entry11126.configure(state = "disabled")
            self.Entry11127.configure(state = "disabled")
            self.Entry11128.configure(state = "disabled")

    def updatedatacompany():
        global passwords
        global hosts
        global users
        global base
        global cnx
        global mycursor
        global myresult

        try:
            cnx = mysql.connector.connect(user = users,
                                          password = passwords,
                                          host = hosts,
                                          database = base,
                                          connect_timeout = 5)
            mycursor = cnx.cursor()

            afm1 = self.Entry11126.get()
            telephone1 = self.Entry11124.get()
            fpa1 = self.Entry11128.get()
            if afm1.isnumeric() and telephone1.isnumeric() and fpa1.isnumeric() and validate_afm(afm1) == True:
                if self.Entry11121.get() != "" and self.Entry11123.get() != "" \
                and self.Entry11124.get() != "" and self.Entry11125.get() != "" \
                and self.Entry11126.get() != "" and self.Entry11127.get() != "" and self.Entry11128.get() != "":
                    # Check and lock from SQL company. Frame 4
                    sql = '''UPDATE lockm SET lockout2 = %s where id = %s'''
                    val = [('1', '1')]
                    mycursor.executemany(sql, val)
                    cnx.commit()
                    self.Button77775.configure(state = "disabled")
                    self.Entry11121.configure(state = "disabled")
                    self.Entry11122.configure(state = "disabled")
                    self.Entry11123.configure(state = "disabled")
                    self.Entry11124.configure(state = "disabled")
                    self.Entry11125.configure(state = "disabled")
                    self.Entry11126.configure(state = "disabled")
                    self.Entry11127.configure(state = "disabled")
                    self.Entry11128.configure(state = "disabled")
                else:
                    pass
            else:
                pass
        except:
            self.Button77775.configure(state = "disabled")
            self.Entry11121.configure(state = "disabled")
            self.Entry11122.configure(state = "disabled")
            self.Entry11123.configure(state = "disabled")
            self.Entry11124.configure(state = "disabled")
            self.Entry11125.configure(state = "disabled")
            self.Entry11126.configure(state = "disabled")
            self.Entry11127.configure(state = "disabled")
            self.Entry11128.configure(state = "disabled")

        # Chek if entry is empty and numeric
        afm1 = self.Entry11126.get()
        telephone1 = self.Entry11124.get()
        fpa1 = self.Entry11128.get()
        if afm1.isnumeric() and telephone1.isnumeric() and fpa1.isnumeric() and validate_afm(afm1) == True:
            if self.Entry11121.get() != "" and self.Entry11123.get() != "" \
            and self.Entry11124.get() != "" and self.Entry11125.get() != "" \
            and self.Entry11126.get() != "" and self.Entry11127.get() != "" and self.Entry11128.get() != "":
                try:
                    cnx = mysql.connector.connect(user = users,
                                          password = passwords,
                                          host = hosts,
                                          database = base,
                                          connect_timeout = 5)
                    mycursor = cnx.cursor()

                    # Ανανέωση στοιχείων της εταιρείας + Φ.Π.Α.
                    # ΑΦΜ check only numbers - not empty
                    afm1 = self.Entry11126.get()
                    sql = '''UPDATE company SET afm = %s where id = %s'''
                    val = [(afm1, '1')]
                    mycursor.executemany(sql, val)
                    cnx.commit()

                    # ΔΟΥ - not empty
                    doy1 = self.Entry11127.get()
                    sql = '''UPDATE company SET doy = %s where id = %s'''
                    val = [(doy1, '1')]
                    mycursor.executemany(sql, val)
                    cnx.commit()

                    # Διεύθυνση - not empty
                    address1 = self.Entry11123.get()
                    sql = '''UPDATE company SET address = %s where id = %s'''
                    val = [(address1, '1')]
                    mycursor.executemany(sql, val)
                    cnx.commit()

                    # Πόλη - not empty
                    city1 = self.Entry11125.get()
                    sql = '''UPDATE company SET city = %s where id = %s'''
                    val = [(city1, '1')]
                    mycursor.executemany(sql, val)
                    cnx.commit()

                    # Τηλέφωνο check only numbers - not empty
                    telephone1 = self.Entry11124.get()
                    sql = '''UPDATE company SET telephone = %s where id = %s'''
                    val = [(telephone1, '1')]
                    mycursor.executemany(sql, val)
                    cnx.commit()

                    # Τίτλος 1 - not empty
                    title11 = self.Entry11121.get()
                    sql = '''UPDATE company SET title1 = %s where id = %s'''
                    val = [(title11, '1')]
                    mycursor.executemany(sql, val)
                    cnx.commit()

                    # Τίτλος 2
                    title21 = self.Entry11122.get()
                    sql = '''UPDATE company SET title2 = %s where id = %s'''
                    val = [(title21, '1')]
                    mycursor.executemany(sql, val)
                    cnx.commit()

                    # Φ.Π.Α. check only numbers - not empty
                    fpa1 = self.Entry11128.get()
                    sql = '''UPDATE fpa SET costfpa = %s where id = %s'''
                    val = [(fpa1, '1')]
                    mycursor.executemany(sql, val)
                    cnx.commit()
                except:
                    self.Label1.configure(text = "Δεν εισάγατε όλα τα δεδομένα.")
                    tk.messagebox.showerror(title = "Δεν έγινε εισαγωγή όλων των δεδομένων.",
                    message = "Προσοχή! Πρέπει να εισάγετε όλα τα δεδομένα για την εταιρεία.")
                    time.sleep(1)
                    self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
            else:
                self.Label1.configure(text = "Δεν εισάγατε όλα τα δεδομένα.")
                tk.messagebox.showerror(title = "Δεν έγινε εισαγωγή όλων των δεδομένων.",
                message = "Προσοχή! Πρέπει να εισάγετε όλα τα δεδομένα για την εταιρεία.")
                time.sleep(1)
                self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
        else:
            self.Label1.configure(text = "Δεν εισάγατε σωστά τα δεδομένα.")
            tk.messagebox.showerror(title = "Δεν έγινε σωστά η εισαγωγή όλων των δεδομένων.",
            message = "Προσοχή! Πρέπει να εισάγετε σωστά όλα τα δεδομένα για την εταιρεία.")
            time.sleep(1)
            self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
            if afm1.isnumeric() == False:
                    self.Entry11126.delete(0, 'end')
            else:
                pass
            if validate_afm(afm1) == False:
                    self.Entry11126.delete(0, 'end')
            else:
                pass
            if telephone1.isnumeric() == False:
                self.Entry11124.delete(0, 'end')
            else:
                pass
            if fpa1.isnumeric() == False:
                self.Entry11128.delete(0, 'end')
            else:
                pass

    def savedatacostd():
        global MyDay
        global MyCostDay
        global passwords
        global hosts
        global base
        global users
        global subcostlistbox2
        global subcostlistbox
        global cnx
        global mycursor
        global myresult
        global c
        global countcarssub
        countcarssub = 0

        # Ημέρες
        MyDay = self.EntryDAY.get()
        if not MyDay.isascii() or not MyDay.isdecimal() or int(MyDay) <= 0:
            self.Label1.configure(text = "Δεν ειναι σωστή η μέρα.")
            tk.messagebox.showerror(title = "Δεν εισάγατε σωστά τις ημέρες.",
                                    message = "Δεν εισάγατε σωστά τον αριθμό ημερών.")
            time.sleep(1)
            self.EntryDAY.delete(0, 'end')
            self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
        else:
            # Κόστος
            MyCostDay = self.EntryCOST.get()
            try:
                MyCostDay = float(MyCostDay)
                from math import isfinite
                if not isfinite(MyCostDay) or MyCostDay < 0:
                    raise ValueError('Μη έγκυρο κόστος συνδρομής.')
                cnx = mysql.connector.connect(user = users,
                                    password = passwords,
                                    host = hosts,
                                    database = base,
                                    connect_timeout = 5)
                mycursor = cnx.cursor()

                # Check if any car is @ Subscription
                timenow = datetime.datetime.now()
                sql = ("SELECT datestart, timestart, dateend, timeend, placenumber FROM subscription WHERE id>0")
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                for datesub in myresult:
                    try:
                        datestart_active = _combine_mysql_datetime(datesub[0], datesub[1])
                        dateend_active = _combine_mysql_datetime(datesub[2], datesub[3])
                        if datestart_active <= timenow < dateend_active:
                            countcarssub = countcarssub + 1
                    except (TypeError, ValueError):
                        pass

                # Check Subscription days and costs
                try:
                    if countcarssub == 0:
                        sql = ("SELECT * FROM costsub WHERE (subdays = %s OR paysub = %s) AND id>0")
                        val = [(MyDay), (MyCostDay)]
                        mycursor.execute(sql, val)
                        myresult = mycursor.fetchall()
                        if myresult != []:
                            for x in myresult:
                                costsubsall = x
                            if costsubsall[1] != [] or costsubsall[2] != []:   
                                self.Label1.configure(text = "Υπάρχει ημέρα ή κόστος.")
                                tk.messagebox.showerror(title = "Το κόστος ή ημέρες που εισάγατε υπάρχουν.",
                                    message = "Εισάγατε ημέρες ή κόστος που υπάρχει.")
                                time.sleep(1)
                                self.EntryCOST.delete(0, 'end')
                                self.EntryDAY.delete(0, 'end')
                                self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
                            else:
                                pass
                        else:
                            # Save New Subscription days and costs
                            sql = '''INSERT INTO costsub(subdays, paysub, comments) VALUES (%s, %s, %s)'''
                            val = [(MyDay, MyCostDay, '')]
                            mycursor.executemany(sql, val)
                            cnx.commit()
                            time.sleep(0.2)
                            subcostlistbox2.destroy()
                            subcostlistbox.destroy()
                            time.sleep(0.2)

                            # Listbox 1 Update -----------------------------------------------------------------------------------------------------------------------
                            subcostlistbox.destroy()
                            subcostlistbox = Listbox(self.Frame4, font = 'Arial 12', borderwidth = 4, highlightthickness = 0, width = 26, height = 10, cursor="hand1")
                            sql = ("SELECT subdays, paysub FROM costsub WHERE id >= '1'")
                            mycursor.execute(sql)
                            myresult = mycursor.fetchall()
                            myresult = str(myresult)
                            if str(myresult) != "[]":
                                myresult = myresult.replace("[(", "").replace("), (", "-").replace(", ", " Κόστος: ").replace(")]", "")
                                myresult = list(myresult.split("-"))
                                for x in myresult:
                                    dayscost = x
                                    subcostlistbox.insert(END, "Ημέρες: " + str(dayscost) + "€")
                                subcostlistbox.pack(pady = 46, padx = 230, anchor = 'nw')
                                subcostlistbox.bind('<<ListboxSelect>>', CurSelect1)
                            else:
                                subcostlistbox.pack(pady = 46, padx = 230, anchor = 'nw')
                                subcostlistbox.bind('<<ListboxSelect>>', CurSelect1)
                        
                            # Listpox 2 -----------------------------------------------------------------------------------------
                            subcostlistbox2.destroy()
                            subcostlistbox2 = Listbox(self.Frame4, font = 'Arial 12', borderwidth = 4, highlightthickness = 0, width = 26, height = 13, cursor="hand1")
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
                            subcostlistbox2.pack(pady = 23, padx = 230, anchor = 'nw')
                            subcostlistbox2.bind('<<ListboxSelect>>', CurSelect2)
                            self.EntryCOST.delete(0, 'end')
                            self.EntryDAY.delete(0, 'end')
                    else:
                        self.Label1.configure(text = "Υπάρχη όχημα σε συνδρομή.")
                        tk.messagebox.showerror(title = "Υπάρχη όχημα σε συνδρομή.",
                                    message = "Υπάρχη όχημα σε ενεργή συνδρομή.")
                        time.sleep(1)
                        self.EntryCOST.delete(0, 'end')
                        self.EntryDAY.delete(0, 'end')
                        self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
                except:
                    self.Label1.configure(text = "Πρόβλημα στην βάση.")
                    tk.messagebox.showerror(title = "Δεν εισάγατε σωστά ημέρες και το κόστος.",
                                    message = "Δεν εισάγατε σωστά ημέρες και το κόστος σε €.")
                    time.sleep(1)
                    self.EntryCOST.delete(0, 'end')
                    self.EntryDAY.delete(0, 'end')
                    self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
            except:
                self.Label1.configure(text = "Δεν είναι σωστό το κόστος.")
                tk.messagebox.showerror(title = "Δεν εισάγατε σωστά το κόστος.",
                                    message = "Δεν εισάγατε σωστά το κόστος σε €.")
                time.sleep(1)
                self.EntryCOST.delete(0, 'end')
                self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")

    def editdatacostd():
        global COSTpDAY
        global MyDay
        global MyCostDay
        global passwords
        global hosts
        global base
        global users
        global subcostlistbox2
        global subcostlistbox
        global cnx
        global mycursor
        global myresult
        global c
        global countcarssub
        countcarssub = 0

        # Ημέρες
        MyDay = self.EntryDAY.get()
        if not MyDay.isascii() or not MyDay.isdecimal() or int(MyDay) <= 0:
            self.Label1.configure(text = "Δεν ειναι σωστή η μέρα.")
            tk.messagebox.showerror(title = "Δεν εισάγατε σωστά τις ημέρες.",
                                    message = "Δεν εισάγατε σωστά τον αριθμό ημερών.")
            time.sleep(1)
            self.EntryDAY.delete(0, 'end')
            self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
        else:
            # Κόστος
            MyCostDay = self.EntryCOST.get()
            try:
                MyCostDay = float(MyCostDay)
                from math import isfinite
                if not isfinite(MyCostDay) or MyCostDay < 0:
                    raise ValueError('Μη έγκυρο κόστος συνδρομής.')
                cnx = mysql.connector.connect(user = users,
                                    password = passwords,
                                    host = hosts,
                                    database = base,
                                    connect_timeout = 5)
                mycursor = cnx.cursor()

                # Check if any car is @ Subscription
                timenow = datetime.datetime.now()
                sql = ("SELECT datestart, timestart, dateend, timeend, placenumber FROM subscription WHERE id>0")
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                for datesub in myresult:
                    try:
                        datestart_active = _combine_mysql_datetime(datesub[0], datesub[1])
                        dateend_active = _combine_mysql_datetime(datesub[2], datesub[3])
                        if datestart_active <= timenow < dateend_active:
                            countcarssub = countcarssub + 1
                    except (TypeError, ValueError):
                        pass

                if countcarssub == 0:
                    # Check For Edit
                    # Επεξεργασία μόνο της σειράς που επέλεξε ο χρήστης.
                    # Διαχωρίζουμε την αρχική διάρκεια από τη νέα τιμή στα πεδία.
                    if not isinstance(COSTpDAY, list) or len(COSTpDAY) < 2:
                        raise ValueError('Επιλέξτε πρώτα εγγραφή από τη λίστα συνδρομών.')
                    sql = ("SELECT * FROM costsub WHERE subdays = %s AND id>0")
                    mycursor.execute(sql, (COSTpDAY[0],))
                    myresult = mycursor.fetchall()
                    if len(myresult) != 1:
                        raise ValueError('Δεν βρέθηκε μοναδική εγγραφή για διόρθωση.')
                    DataEdit = myresult[0]
                    mycursor.execute("SELECT id FROM costsub WHERE subdays=%s AND id<>%s AND id>0",
                                     (MyDay,DataEdit[0]))
                    if mycursor.fetchone() is not None:
                        raise ValueError('Υπάρχει ήδη τιμοκατάλογος αυτής της διάρκειας.')
                    if int(DataEdit[0]) > 0:
                        # Update Base
                        sql = '''UPDATE costsub SET subdays = %s, paysub = %s WHERE id = %s AND id>0'''
                        val = [(MyDay, MyCostDay, DataEdit[0])]
                        mycursor.executemany(sql, val)
                        cnx.commit()
                        time.sleep(0.2)
                        subcostlistbox2.destroy()
                        subcostlistbox.destroy()
                        time.sleep(0.2)

                        # Listbox 1 Update -----------------------------------------------------------------------------------------------------------------------
                        subcostlistbox.destroy()
                        subcostlistbox = Listbox(self.Frame4, font = 'Arial 12', borderwidth = 4, highlightthickness = 0, width = 26, height = 10, cursor="hand1")
                        sql = ("SELECT subdays, paysub FROM costsub WHERE id >= '1'")
                        mycursor.execute(sql)
                        myresult = mycursor.fetchall()
                        myresult = str(myresult)
                        if str(myresult) != "[]":
                            myresult = myresult.replace("[(", "").replace("), (", "-").replace(", ", " Κόστος: ").replace(")]", "")
                            myresult = list(myresult.split("-"))
                            for x in myresult:
                                dayscost = x
                                subcostlistbox.insert(END, "Ημέρες: " + str(dayscost) + "€")
                            subcostlistbox.pack(pady = 46, padx = 230, anchor = 'nw')
                            subcostlistbox.bind('<<ListboxSelect>>', CurSelect1)
                        else:
                            subcostlistbox.pack(pady = 46, padx = 230, anchor = 'nw')
                            subcostlistbox.bind('<<ListboxSelect>>', CurSelect1)

                        # Listpox 2 -----------------------------------------------------------------------------------------
                        subcostlistbox2.destroy()
                        subcostlistbox2 = Listbox(self.Frame4, font = 'Arial 12', borderwidth = 4, highlightthickness = 0, width = 26, height = 13, cursor="hand1")
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
                        subcostlistbox2.pack(pady = 23, padx = 230, anchor = 'nw')
                        subcostlistbox2.bind('<<ListboxSelect>>', CurSelect2)
                        self.EntryCOST.delete(0, 'end')
                        self.EntryDAY.delete(0, 'end')
                    else:
                        pass
                else:
                    self.Label1.configure(text = "Υπάρχη όχημα σε συνδρομή.")
                    tk.messagebox.showerror(title = "Υπάρχη όχημα σε συνδρομή.",
                                    message = "Υπάρχη όχημα σε ενεργή συνδρομή.")
                    time.sleep(1)
                    self.EntryCOST.delete(0, 'end')
                    self.EntryDAY.delete(0, 'end')
                    self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
            except:
                self.Label1.configure(text = "Δεν έγινε σωστή εισαγωγή.")
                tk.messagebox.showerror(title = "Δεν εισάγατε σωστά τα δεδομένα.",
                                    message = "Δεν εισάγατε σωστά τα δεδομένα για το κόστος.")
                time.sleep(1)
                self.EntryCOST.delete(0, 'end')
                self.EntryDAY.delete(0, 'end')
                self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")

    def deletedatacostd():
        global MyDay
        global MyCostDay
        global passwords
        global hosts
        global base
        global users
        global subcostlistbox2
        global subcostlistbox
        global cnx
        global mycursor
        global myresult
        global c
        global countcarssub
        countcarssub = 0

        # Ημέρες
        MyDay = self.EntryDAY.get()
        if not MyDay.isascii() or not MyDay.isdecimal() or int(MyDay) <= 0:
            self.Label1.configure(text = "Δεν ειναι σωστή η μέρα.")
            tk.messagebox.showerror(title = "Δεν εισάγατε σωστά τις ημέρες.",
                                    message = "Δεν εισάγατε σωστά τον αριθμό ημερών.")
            time.sleep(1)
            self.EntryDAY.delete(0, 'end')
            self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
        else:
            # Κόστος
            MyCostDay = self.EntryCOST.get()
            try:
                MyCostDay = float(MyCostDay)
                from math import isfinite
                if not isfinite(MyCostDay) or MyCostDay < 0:
                    raise ValueError('Μη έγκυρο κόστος συνδρομής.')
                cnx = mysql.connector.connect(user = users,
                                    password = passwords,
                                    host = hosts,
                                    database = base,
                                    connect_timeout = 5)
                mycursor = cnx.cursor()

                # Check if any car is @ Subscription
                timenow = datetime.datetime.now()
                sql = ("SELECT datestart, timestart, dateend, timeend, placenumber FROM subscription WHERE id>0")
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                for datesub in myresult:
                    try:
                        datestart_active = _combine_mysql_datetime(datesub[0], datesub[1])
                        dateend_active = _combine_mysql_datetime(datesub[2], datesub[3])
                        if datestart_active <= timenow < dateend_active:
                            countcarssub = countcarssub + 1
                    except (TypeError, ValueError):
                        pass

                if countcarssub == 0:
                    try:
                        sql = ("SELECT * FROM costsub WHERE subdays = %s AND paysub = %s AND id>0")
                        val = [(MyDay), (MyCostDay)]
                        mycursor.execute(sql, val)
                        myresult = mycursor.fetchall()
                        for x in myresult:
                            datafordelete = x
                        if str(datafordelete[1]) == str(MyDay) and str(datafordelete[2]) == str(MyCostDay):
                            sql = ("DELETE FROM costsub WHERE subdays = %s AND paysub = %s AND id>0")
                            val = [(MyDay, MyCostDay)]
                            mycursor.executemany(sql, val)
                            cnx.commit()
                            time.sleep(0.2)
                            subcostlistbox2.destroy()
                            subcostlistbox.destroy()
                            time.sleep(0.2)

                            # Listbox 1 Update -----------------------------------------------------------------------------------------------------------------------
                            subcostlistbox.destroy()
                            subcostlistbox = Listbox(self.Frame4, font = 'Arial 12', borderwidth = 4, highlightthickness = 0, width = 26, height = 10, cursor="hand1")
                            sql = ("SELECT subdays, paysub FROM costsub WHERE id >= '1'")
                            mycursor.execute(sql)
                            myresult = mycursor.fetchall()
                            myresult = str(myresult)
                            if str(myresult) != "[]":
                                myresult = myresult.replace("[(", "").replace("), (", "-").replace(", ", " Κόστος: ").replace(")]", "")
                                myresult = list(myresult.split("-"))
                                for x in myresult:
                                    dayscost = x
                                    subcostlistbox.insert(END, "Ημέρες: " + str(dayscost) + "€")
                                subcostlistbox.pack(pady = 46, padx = 230, anchor = 'nw')
                                subcostlistbox.bind('<<ListboxSelect>>', CurSelect1)
                            else:
                                subcostlistbox.pack(pady = 46, padx = 230, anchor = 'nw')
                                subcostlistbox.bind('<<ListboxSelect>>', CurSelect1)

                            # Listpox 2 -----------------------------------------------------------------------------------------
                            subcostlistbox2.destroy()
                            subcostlistbox2 = Listbox(self.Frame4, font = 'Arial 12', borderwidth = 4, highlightthickness = 0, width = 26, height = 13, cursor="hand1")
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
                            subcostlistbox2.pack(pady = 23, padx = 230, anchor = 'nw')
                            subcostlistbox2.bind('<<ListboxSelect>>', CurSelect2)
                            self.EntryCOST.delete(0, 'end')
                            self.EntryDAY.delete(0, 'end')

                            # Δεν επαναριθμούμε PRIMARY KEY IDs: το AUTO_INCREMENT
                            # διατηρεί ασφαλώς τα σταθερά αναγνωριστικά τιμοκαταλόγου.
                        else:
                            pass
                    except:
                        self.Label1.configure(text = "Δεν υπάρχουν δεδομένα για διαγραφή.")
                        tk.messagebox.showerror(title = "Δεν υπάρχουν δεδομένα για διαγραφή.",
                                    message = "Δεν εισάγατε σωστά δεδομένα για διαγραφή.")
                        time.sleep(1)
                        self.EntryCOST.delete(0, 'end')
                        self.EntryDAY.delete(0, 'end')
                        self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
                else:
                    self.Label1.configure(text = "Υπάρχη όχημα σε συνδρομή.")
                    tk.messagebox.showerror(title = "Υπάρχη όχημα σε συνδρομή.",
                                    message = "Υπάρχη όχημα σε ενεργή συνδρομή.")
                    time.sleep(1)
                    self.EntryCOST.delete(0, 'end')
                    self.EntryDAY.delete(0, 'end')
                    self.Label1.configure(text = "Το σύστημα είναι έτοιμο.") 
            except:
                self.Label1.configure(text = "Δεν είναι σωστό το κόστος.")
                tk.messagebox.showerror(title = "Δεν εισάγατε σωστά το κόστος.",
                                    message = "Δεν εισάγατε σωστά το κόστος σε €.")
                time.sleep(1)
                self.EntryCOST.delete(0, 'end')
                self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")

    def isTimeFormat(input):
        global MyTime
        try:
            time.strptime(input, '%H:%M:%S')
            return True
        except ValueError:
            return False

    def savedatacosts():
        global MyTime
        global MyCost
        global passwords
        global hosts
        global base
        global users
        global subcostlistbox2
        global subcostlistbox
        global cnx
        global mycursor
        global myresult
        global c
        global countcars
        countcars = 0

        # Ώρα
        MyTime = self.EntryTIMEs.get()
        if isTimeFormat(MyTime) == False or MyTime == '00:00:00':
            self.Label1.configure(text = "Δεν ειναι σωστή η ώρα.")
            tk.messagebox.showerror(title = "Δεν εισάγατε σωστά την ώρα.",
                                    message = "Δεν εισάγατε σωστά την ώρα.")
            time.sleep(1)
            self.EntryTIMEs.delete(0, 'end')
            self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
        else:
            # Κόστος
            MyCost = self.EntryCOSTs.get()
            try:
                MyCost = float(MyCost)
                from math import isfinite
                if not isfinite(MyCost) or MyCost < 0:
                    raise ValueError('Μη έγκυρη τιμή στάθμευσης.')
                cnx = mysql.connector.connect(user = users,
                                    password = passwords,
                                    host = hosts,
                                    database = base,
                                    connect_timeout = 5)
                mycursor = cnx.cursor()

                sql = ("SELECT placenumber FROM inputcar WHERE isout = 0 AND inputnumber > 0")
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                for x in myresult:
                    carsinpark = x
                    countcars = countcars + 1

                if countcars == 0:
                    # Check
                    sql = ("SELECT timecost FROM costs WHERE timecost = %s")
                    val = [(MyTime)]
                    mycursor.execute(sql, val)
                    myresult = mycursor.fetchall()
                    if myresult == []:
                        sql = '''INSERT INTO costs(timecost, moneycost, comments) VALUES (%s, %s, %s)'''
                        val = [(MyTime, MyCost, '')]
                        mycursor.executemany(sql, val)
                        cnx.commit()
                        time.sleep(0.2)
                        subcostlistbox2.destroy()
                        subcostlistbox.destroy()
                        time.sleep(0.2)
                    else:
                        self.Label1.configure(text = "Υπάρχη καταχώρηση.")
                        tk.messagebox.showerror(title = "Υπάρχη η καταχώρηση.",
                                    message = "Υπάρχη η καταχώρηση. Δώστε σωστά τα δεδομένα.")
                        time.sleep(1)
                        self.EntryCOSTs.delete(0, 'end')
                        self.EntryTIMEs.delete(0, 'end')
                        self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")

                    # Listbox 1 Update -----------------------------------------------------------------------------------------------------------------------
                    subcostlistbox.destroy()
                    subcostlistbox = Listbox(self.Frame4, font = 'Arial 12', borderwidth = 4, highlightthickness = 0, width = 26, height = 10, cursor="hand1")
                    sql = ("SELECT subdays, paysub FROM costsub WHERE id >= '1'")
                    mycursor.execute(sql)
                    myresult = mycursor.fetchall()
                    myresult = str(myresult)
                    if str(myresult) != "[]":
                        myresult = myresult.replace("[(", "").replace("), (", "-").replace(", ", " Κόστος: ").replace(")]", "")
                        myresult = list(myresult.split("-"))
                        for x in myresult:
                            dayscost = x
                            subcostlistbox.insert(END, "Ημέρες: " + str(dayscost) + "€")
                        subcostlistbox.pack(pady = 46, padx = 230, anchor = 'nw')
                        subcostlistbox.bind('<<ListboxSelect>>', CurSelect1)
                    else:
                        subcostlistbox.pack(pady = 46, padx = 230, anchor = 'nw')
                        subcostlistbox.bind('<<ListboxSelect>>', CurSelect1)

                    # Listpox 2 -----------------------------------------------------------------------------------------
                    subcostlistbox2.destroy()
                    subcostlistbox2 = Listbox(self.Frame4, font = 'Arial 12', borderwidth = 4, highlightthickness = 0, width = 26, height = 13, cursor="hand1")
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
                    subcostlistbox2.pack(pady = 23, padx = 230, anchor = 'nw')
                    subcostlistbox2.bind('<<ListboxSelect>>', CurSelect2)
                    self.EntryTIMEs.delete(0, 'end')
                    self.EntryCOSTs.delete(0, 'end')
                else:
                    self.Label1.configure(text = "Υπάρχη όχημα στο πάρκινγκ.")
                    tk.messagebox.showerror(title = "Υπάρχη όχημα στο πάρκινγκ.",
                                    message = "Υπάρχη όχημα μέσα στο πάρκινγκ.")
                    time.sleep(1)
                    self.EntryCOSTs.delete(0, 'end')
                    self.EntryTIMEs.delete(0, 'end')
                    self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
            except:
                self.Label1.configure(text = "Δεν είναι σωστό το κόστος.")
                tk.messagebox.showerror(title = "Δεν εισάγατε σωστά το κόστος.",
                                    message = "Δεν εισάγατε σωστά το κόστος σε €.")
                time.sleep(1)
                self.EntryCOSTs.delete(0, 'end')
                self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")

    def editdatacosts():
        global COSTpTIME
        global MyTime
        global MyCost
        global passwords
        global users
        global hosts
        global base
        global subcostlistbox2
        global subcostlistbox
        global cnx
        global mycursor
        global myresult
        global c
        global countcars
        countcars = 0

        # Ώρα
        MyTime = self.EntryTIMEs.get()
        if isTimeFormat(MyTime) == False or MyTime == '00:00:00':
            self.Label1.configure(text = "Δεν ειναι σωστή η ώρα.")
            tk.messagebox.showerror(title = "Δεν εισάγατε σωστά την ώρα.",
                                    message = "Δεν εισάγατε σωστά την ώρα.")
            time.sleep(1)
            self.EntryTIMEs.delete(0, 'end')
            self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
        else:
            # Κόστος
            MyCost = self.EntryCOSTs.get()
            try:
                MyCost = float(MyCost)
                from math import isfinite
                if not isfinite(MyCost) or MyCost < 0:
                    raise ValueError('Μη έγκυρη τιμή στάθμευσης.')
                cnx = mysql.connector.connect(user = users,
                                    password = passwords,
                                    host = hosts,
                                    database = base,
                                    connect_timeout = 5)
                mycursor = cnx.cursor()

                sql = ("SELECT placenumber FROM inputcar WHERE isout = 0 AND inputnumber > 0")
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                for x in myresult:
                    carsinpark = x
                    countcars = countcars + 1
                if countcars == 0:
                    try:
                        # Check For Edit
                        # Προηγούμενη επιλογή από τη λίστα: ένα μοναδικό timecost.
                        if not isinstance(COSTpTIME, list) or len(COSTpTIME) < 3:
                            raise ValueError('Επιλέξτε πρώτα εγγραφή τιμοκαταλόγου.')
                        sql = ("SELECT id,timecost,moneycost FROM costs WHERE timecost=%s AND id>0")
                        mycursor.execute(sql, (COSTpTIME[1],))
                        myresult = mycursor.fetchall()
                        if len(myresult) != 1:
                            raise ValueError('Δεν βρέθηκε μοναδική φάση χρέωσης.')
                        DataEdit = myresult[0]
                        mycursor.execute("SELECT id FROM costs WHERE timecost=%s AND id<>%s AND id>0",
                                         (MyTime,DataEdit[0]))
                        if mycursor.fetchone() is not None:
                            raise ValueError('Υπάρχει ήδη τιμολογιακή φάση ίδιας διάρκειας.')
                        if int(DataEdit[0]) > 0:
                            # Update Base
                            sql = '''UPDATE costs SET timecost = %s, moneycost = %s WHERE id = %s AND id>0'''
                            val = [(MyTime, MyCost, DataEdit[0])]
                            mycursor.executemany(sql, val)
                            cnx.commit()
                            time.sleep(0.2)
                            subcostlistbox2.destroy()
                            subcostlistbox.destroy()
                            time.sleep(0.2)
                        else:
                            pass
                    except:
                        self.Label1.configure(text = "Δεν είναι σωστά τα δεδομένα που εισάγατε.")
                        tk.messagebox.showerror(title = "Δεν εισάγατε σωστά τα δεδομένα.",
                                    message = "Δεν εισάγατε σωστά τα δεδομένα Υπάρχει λάθος.")
                        time.sleep(1)
                        self.EntryCOSTs.delete(0, 'end')
                        self.EntryTIMEs.delete(0, 'end')
                        self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")

                    # Listbox 1 Update -----------------------------------------------------------------------------------------------------------------------
                    subcostlistbox.destroy()
                    subcostlistbox = Listbox(self.Frame4, font = 'Arial 12', borderwidth = 4, highlightthickness = 0, width = 26, height = 10, cursor="hand1")
                    sql = ("SELECT subdays, paysub FROM costsub WHERE id >= '1'")
                    mycursor.execute(sql)
                    myresult = mycursor.fetchall()
                    myresult = str(myresult)
                    if str(myresult) != "[]":
                        myresult = myresult.replace("[(", "").replace("), (", "-").replace(", ", " Κόστος: ").replace(")]", "")
                        myresult = list(myresult.split("-"))
                        for x in myresult:
                            dayscost = x
                            subcostlistbox.insert(END, "Ημέρες: " + str(dayscost) + "€")
                        subcostlistbox.pack(pady = 46, padx = 230, anchor = 'nw')
                        subcostlistbox.bind('<<ListboxSelect>>', CurSelect1)
                    else:
                        subcostlistbox.pack(pady = 46, padx = 230, anchor = 'nw')
                        subcostlistbox.bind('<<ListboxSelect>>', CurSelect1)

                    # Listpox 2 -----------------------------------------------------------------------------------------
                    subcostlistbox2.destroy()
                    subcostlistbox2 = Listbox(self.Frame4, font = 'Arial 12', borderwidth = 4, highlightthickness = 0, width = 26, height = 13, cursor="hand1")
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
                    subcostlistbox2.pack(pady = 23, padx = 230, anchor = 'nw')
                    subcostlistbox2.bind('<<ListboxSelect>>', CurSelect2)
                    self.EntryTIMEs.delete(0, 'end')
                    self.EntryCOSTs.delete(0, 'end')
                else:
                    self.Label1.configure(text = "Υπάρχη όχημα στο πάρκινγκ.")
                    tk.messagebox.showerror(title = "Υπάρχη όχημα στο πάρκινγκ.",
                                    message = "Υπάρχη όχημα μέσα στο πάρκινγκ.")
                    time.sleep(1)
                    self.EntryCOSTs.delete(0, 'end')
                    self.EntryTIMEs.delete(0, 'end')
                    self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
            except:
                self.Label1.configure(text = "Δεν είναι σωστό το κόστος.")
                tk.messagebox.showerror(title = "Δεν εισάγατε σωστά το κόστος.",
                                    message = "Δεν εισάγατε σωστά το κόστος σε €.")
                time.sleep(1)
                self.EntryCOSTs.delete(0, 'end')
                self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")

    def deletedatacosts():
        global MyTime
        global MyCost
        global MyTime
        global MyCost
        global passwords
        global users
        global hosts
        global base
        global subcostlistbox
        global subcostlistbox2
        global cnx
        global mycursor
        global myresult
        global c
        global countcars
        countcars = 0

        # Ώρα
        MyTime = self.EntryTIMEs.get()
        if isTimeFormat(MyTime) == False or MyTime == '00:00:00':
            self.Label1.configure(text = "Δεν ειναι σωστή η ώρα.")
            tk.messagebox.showerror(title = "Δεν εισάγατε σωστά την ώρα.",
                                    message = "Δεν εισάγατε σωστά την ώρα.")
            time.sleep(1)
            self.EntryTIMEs.delete(0, 'end')
            self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
        else:
            # Κόστος
            MyCost = self.EntryCOSTs.get()
            try:
                MyCost = float(MyCost)
                from math import isfinite
                if not isfinite(MyCost) or MyCost < 0:
                    raise ValueError('Μη έγκυρη τιμή στάθμευσης.')
                cnx = mysql.connector.connect(user = users,
                                    password = passwords,
                                    host = hosts,
                                    database = base,
                                    connect_timeout = 5)
                mycursor = cnx.cursor()

                sql = ("SELECT placenumber FROM inputcar WHERE isout = 0 AND inputnumber > 0")
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                for x in myresult:
                    carsinpark = x
                    countcars = countcars + 1
                if countcars == 0:
                    try:
                        sql = ("SELECT * FROM costs WHERE timecost = %s AND moneycost = %s AND id>0")
                        val = [(MyTime), (MyCost)]
                        mycursor.execute(sql, val)
                        myresult = mycursor.fetchall()
                        for x in myresult:
                            datafordelete = x
                        if str(datafordelete[1]) == str(MyTime) and str(datafordelete[2]) == str(MyCost):
                            sql = ("DELETE FROM costs WHERE timecost = %s AND moneycost = %s AND id>0")
                            val = [(MyTime, MyCost)]
                            mycursor.executemany(sql, val)
                            cnx.commit()
                            time.sleep(0.2)
                            subcostlistbox2.destroy()
                            subcostlistbox.destroy()
                            time.sleep(0.2)

                            # Listbox 1 Update -----------------------------------------------------------------------------------------------------------------------
                            subcostlistbox.destroy()
                            subcostlistbox = Listbox(self.Frame4, font = 'Arial 12', borderwidth = 4, highlightthickness = 0, width = 26, height = 10, cursor="hand1")
                            sql = ("SELECT subdays, paysub FROM costsub WHERE id >= '1'")
                            mycursor.execute(sql)
                            myresult = mycursor.fetchall()
                            myresult = str(myresult)
                            if str(myresult) != "[]":
                                myresult = myresult.replace("[(", "").replace("), (", "-").replace(", ", " Κόστος: ").replace(")]", "")
                                myresult = list(myresult.split("-"))
                                for x in myresult:
                                    dayscost = x
                                    subcostlistbox.insert(END, "Ημέρες: " + str(dayscost) + "€")
                                subcostlistbox.pack(pady = 46, padx = 230, anchor = 'nw')
                                subcostlistbox.bind('<<ListboxSelect>>', CurSelect1)
                            else:
                                subcostlistbox.pack(pady = 46, padx = 230, anchor = 'nw')
                                subcostlistbox.bind('<<ListboxSelect>>', CurSelect1)

                            # Listpox 2 -----------------------------------------------------------------------------------------
                            subcostlistbox2.destroy()
                            subcostlistbox2 = Listbox(self.Frame4, font = 'Arial 12', borderwidth = 4, highlightthickness = 0, width = 26, height = 13, cursor="hand1")
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
                            subcostlistbox2.pack(pady = 23, padx = 230, anchor = 'nw')
                            subcostlistbox2.bind('<<ListboxSelect>>', CurSelect2)
                            self.EntryCOSTs.delete(0, 'end')
                            self.EntryTIMEs.delete(0, 'end')

                            # Σταθερά PRIMARY KEY IDs, χωρίς μαζική επαναρίθμηση.
                        else:
                            pass
                    except:
                        self.Label1.configure(text = "Δεν υπάρχουν δεδομένα για διαγραφή.")
                        tk.messagebox.showerror(title = "Δεν υπάρχουν δεδομένα για διαγραφή.",
                                    message = "Δεν εισάγατε σωστά δεδομένα για διαγραφή.")
                        time.sleep(1)
                        self.EntryCOSTs.delete(0, 'end')
                        self.EntryTIMEs.delete(0, 'end')
                        self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
                else:
                    self.Label1.configure(text = "Υπάρχη όχημα στο πάρκινγκ.")
                    tk.messagebox.showerror(title = "Υπάρχη όχημα στο πάρκινγκ.",
                                    message = "Υπάρχη όχημα μέσα στο πάρκινγκ.")
                    time.sleep(1)
                    self.EntryCOSTs.delete(0, 'end')
                    self.EntryTIMEs.delete(0, 'end')
                    self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
            except:
                self.Label1.configure(text = "Δεν είναι σωστό το κόστος.")
                tk.messagebox.showerror(title = "Δεν εισάγατε σωστά το κόστος.",
                                    message = "Δεν εισάγατε σωστά το κόστος σε €.")
                time.sleep(1)
                self.EntryCOSTs.delete(0, 'end')
                self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")

    def updateplaces():
        global passwords
        global hosts
        global users
        global base
        global cnx
        global mycursor
        global myresult
        global remaneplaces

        # Check for lock places and company
        try:
            cnx = mysql.connector.connect(user = users,
                                    password = passwords,
                                    host = hosts,
                                    database = base,
                                    connect_timeout = 5)
            mycursor = cnx.cursor()

            park1 = self.EntryplacesU.get()
            if park1.isnumeric() and park1 != "":
                # Check and lock from SQL place. Frame 4
                sql = '''UPDATE lockm SET lockout = %s where id = %s'''
                val = [('1', '1')]
                mycursor.executemany(sql, val)
                cnx.commit()
                self.Buttonplaces.configure(state = "disabled")
                self.EntryplacesU.configure(state = "disabled")
            else:
                pass
        except:
            self.Buttonplaces.configure(state = "disabled")
            self.EntryplacesU.configure(state = "disabled")

        park1 = self.EntryplacesU.get()
        if park1.isnumeric() and park1 != "":
            try:
                cnx = mysql.connector.connect(user = users,
                                        password = passwords,
                                        host = hosts,
                                        database = base,
                                        connect_timeout = 5)
                mycursor = cnx.cursor()

                # Ανανέωση θέσων πάρκινγ στο Frame 4.
                sql = '''UPDATE places SET remaneplaces = %s where id = %s'''
                val = [(park1, '1')]
                mycursor.executemany(sql, val)
                cnx.commit()
                remaneplaces = int(park1)
                self.Label13.configure(text = remaneplaces)
                if int(park1) >= 1:
                    self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
                else:
                    self.Label1.configure(text = "Δεν υπάρχουν διαθέσημες θέσεις πάρκινγκ. 0 θέσεις πάρκινγκ.")
            except:
                self.Label1.configure(text = "Πρόβλημα με τις θέσεις πάρκινγκ.")
                tk.messagebox.showerror(title = "Δεν έγινε σωστά εισαγωγή θέσεων πάρκινγκ.",
                message = "Προσοχή! Πρέπει να προσπαθήσετε να εισάγετε ξανά τις θέσεις πάρκινγκ.")
                time.sleep(1)
                self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
                self.EntryplacesU.delete(0, 'end')
        else:
            self.Label1.configure(text = "Δεν εισάγατε σωστά θέσεις πάρκινγκ.")
            tk.messagebox.showerror(title = "Δεν έγινε σωστά εισαγωγή θέσεων πάρκινγκ.",
            message = "Προσοχή! Πρέπει να εισάγετε σωστά τις θέσεις πάρκινγκ.")
            time.sleep(1)
            self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
            self.EntryplacesU.delete(0, 'end')

    return {
        'CurSelect1': CurSelect1,
        'CurSelect2': CurSelect2,
        'button4': button4,
        'updatedatacompany': updatedatacompany,
        'savedatacostd': savedatacostd,
        'editdatacostd': editdatacostd,
        'deletedatacostd': deletedatacostd,
        'isTimeFormat': isTimeFormat,
        'savedatacosts': savedatacosts,
        'editdatacosts': editdatacosts,
        'deletedatacosts': deletedatacosts,
        'updateplaces': updateplaces,
    }
