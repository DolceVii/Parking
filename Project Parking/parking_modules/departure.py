"""Έξοδος οχημάτων και αποδείξεις."""

def create_handlers(self, top, handlers):
    """Επιστρέφει callbacks με κοινό περιβάλλον, χωρίς μεταβολή λογικής GUI."""

    def searchout():
        global subscription
        global ticketnumberout
        global idbase
        global totalcost
        global totaltime
        global countidbase
        global inputs
        global err
        global timein
        global datein
        global datein2
        global fpa
        global totalcostfba
        global dateendsub
        global timeendsub
        global subdateend
        global subdtimeend
        global payfpa
        global myresult
        global compinedatein
        global compinetimein
        global timedatesub
        global totalsubdatetimein
        global text
        global subdaysDropdown
        global cal
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
        global placenumberout
        text = "ΟΧΙ"
        ticketnumber = '0'
        subscription = '0'
        self.Text11.configure(state = "normal")
        self.Text11.delete("1.0", "end")
        pay = '0.0'
        totalcost = 0
        totaltime = 0

        cnx = None
        try:
            cnx = mysql.connector.connect(user = users,
                                          password = passwords,
                                          host = hosts,
                                          database = base,
                                          connect_timeout = 5)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.Label1.configure(text = '''Λάθος όνομα χρήστη ή κωδικός στην βάση δεδομένων.''')
                self.Button1.configure(state = "disabled")
                self.Button2.configure(state = "disabled")
                self.Button3.configure(state = "disabled")
                self.Button4.configure(state = "disabled")
                self.Button5.configure(state = "disabled")
                self.Frame1.place_forget()
                self.Frame2.place_forget()
                self.Frame3.place_forget()
                self.Frame4.place_forget()
                self.Frame5.place_forget()
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
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                self.Label1.configure(text = '''Η βάση δεδομένων δεν υπάρχει.''')
                self.Button1.configure(state = "disabled")
                self.Button2.configure(state = "disabled")
                self.Button3.configure(state = "disabled")
                self.Button4.configure(state = "disabled")
                self.Button5.configure(state = "disabled")
                self.Frame1.place_forget()
                self.Frame2.place_forget()
                self.Frame3.place_forget()
                self.Frame4.place_forget()
                self.Frame5.place_forget()
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
            elif err.errno == errorcode.CR_CONN_HOST_ERROR:
                self.Label1.configure(text = '''Δεν υπάρχει σύνδεση με την βάση δεδομένων. Επανεκκινήστε την βάση και το πρόγραμμα.''')
                self.Button1.configure(state = "disabled")
                self.Button2.configure(state = "disabled")
                self.Button3.configure(state = "disabled")
                self.Button4.configure(state = "disabled")
                self.Button5.configure(state = "disabled")
                self.Frame1.place_forget()
                self.Frame2.place_forget()
                self.Frame3.place_forget()
                self.Frame4.place_forget()
                self.Frame5.place_forget()
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
            else:
                self.Label1.configure(text='''Γενικό σφάλμα συστήματος.''' + str(err))
                self.Button1.configure(state = "disabled")
                self.Button2.configure(state = "disabled")
                self.Button3.configure(state = "disabled")
                self.Button4.configure(state = "disabled")
                self.Button5.configure(state = "disabled")
                self.Frame1.place_forget()
                self.Frame2.place_forget()
                self.Frame3.place_forget()
                self.Frame4.place_forget()
                self.Frame5.place_forget()
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
        if cnx is None or not cnx.is_connected():
            return
        mycursor = cnx.cursor()
        placenumberout = self.Entry11.get().upper()

        # Check for english
        myresult = placenumberout.isascii()
        if myresult == False:
            placenumberout = "×××"
        else:
            pass
        if placenumberout == "":
            self.Label1.configure(text = "Δεν εισάγατε τον αριθμό πινακίδας οχήματος.")
            tk.messagebox.showerror(title = "Δεν έγινε εισαγωγή αριθμού πινακίδας.",
                                message = "Προσοχή! Δεν δώσατε αριθμό πινακίδας για εξαγωγή αυτοκινήτου.")
            time.sleep(1)
            self.Entry11.delete(0, 'end')
            self.Text11.delete("1.0", "end")
            self.Label155.configure(text = " ")
            self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
            self.Label1001.configure(text = " ")
            self.Label110.configure(text = " ")
            self.Label201.configure(text = " ")
            self.Text11.configure(state = "disable")
        elif placenumberout == "×××":
            self.Label1.configure(text = "Εισάγατε τον αριθμό πινακίδας οχήματος στα Ελληνικά.")
            tk.messagebox.showerror(title = "Δεν έγινε εισαγωγή αριθμού πινακίδας.",
                                message = "Προσοχή! Δώστε αριθμό πινακίδας στα Αγγλικά για εξαγωγή αυτοκινήτου.")
            time.sleep(1)
            self.Entry11.delete(0, 'end')
            self.Text11.delete("1.0", "end")
            self.Label155.configure(text = " ")
            self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
            self.Label1001.configure(text = " ")
            self.Label110.configure(text = " ")
            self.Label201.configure(text = " ")
            self.Text11.configure(state = "disable")
            placenumberout = ""
        else:
            try:
                # Διαβάζουμε την ενεργή είσοδο ως μία ενιαία εγγραφή, ώστε ticket/ώρα/σχόλια
                # να ανήκουν πάντοτε στην ίδια είσοδο ακόμη και αν υπάρχουν παλιά διπλά δεδομένα.
                sql = ("SELECT ticketnumber, comments, datein, timein FROM inputcar "
                       "WHERE placenumber = %s AND isout = %s "
                       "ORDER BY inputnumber DESC LIMIT 1")
                val = [(placenumberout), ('0')]
                mycursor.execute(sql, val)
                active_input = mycursor.fetchone()
                if active_input is None:
                    raise LookupError("Δεν βρέθηκε ενεργή είσοδος για το όχημα.")

                ticketnumberout, comments, datein, timein = active_input
                self.Label155.configure(text = ticketnumberout)
                self.Label110.configure(text = comments)
                datein2 = datetime.datetime.strptime(str(datein), "%Y-%m-%d").strftime("%d/%m/%Y")
                self.Label1001.configure(text = str(datein2) + "  " + str(timein))
                self.Button77.configure(state = "normal")
                self.Button777.configure(state = "disabled")
                self.Entry11.configure(state = "disabled")

                # combine and find total parking time (συνδιάζει μέρα και ώρα για να βγάλει τον χρόνο πάρκινγκ)
                dbindate =(datetime.datetime.min + timein).time()
                indate = datetime.datetime.combine(datein, dbindate)
                nowdate = datetime.datetime.today()
                totaltime = nowdate - indate

                # Read phase and costs (διαβάζει φάσεις και κόστη)
                sql = ("SELECT id, timecost, moneycost FROM costs ORDER BY id ASC")
                mycursor.execute(sql)
                inputs = mycursor.fetchall()
                idbase = inputs[-1][0] if inputs else 0
                countidbase = 0

                # Read ΦΠΑ
                sql = ("SELECT costfpa FROM fpa ORDER BY id DESC LIMIT 1")
                mycursor.execute(sql)
                myresult = mycursor.fetchone()
                for x in myresult:
                    fpa = x
            except:
                self.Label1.configure(text = "Το αυτοκίνητο με αριθμό: " + placenumberout + " δεν είναι μέσα στο \
πάρκινγκ.")
                tk.messagebox.showerror(title = "Το αυτοκίνητο " + placenumberout + " δεν είναι μέσα στο πάρκινγ.",
                                    message = "Προσοχή! Δώσατε εξαγωγή αυτοκινήτου με αριθμό \
" + placenumberout + " το οποίο δεν είναι μέσα στο πάρκινγ.")
                time.sleep(1)
                self.Entry11.delete(0, 'end')
                self.Text11.delete("1.0", "end")
                self.Label201.configure(text = " ")
                self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
                self.Label155.configure(text = " ")
                self.Label1001.configure(text = " ")
                self.Text11.configure(state = "disable")
                self.Button77.configure(state = "disabled")
                placenumberout = ""

            # Check subscription and calculate the chargeable duration exactly once.
            try:
                if placenumberout == "":
                    self.Label201.configure(text = " ")
                    text = " "
                    subscription = '0'
                    totalcost = 0
                    totaltime = datetime.timedelta(0)
                    self.Label133.configure(text = "0.0€")
                else:
                    parking_start = indate
                    parking_end = datetime.datetime.now()
                    parking_duration = max(parking_end - parking_start, datetime.timedelta(0))

                    # Όλες οι συνδρομές του οχήματος λαμβάνονται υπόψη ώστε ανανεώσεις/επικαλύψεις
                    # να μην δημιουργούν λάθος χρέωση.
                    sql = ("SELECT datestart, timestart, dateend, timeend FROM subscription "
                           "WHERE placenumber = %s ORDER BY datestart ASC, timestart ASC, id ASC")
                    val = [(placenumberout)]
                    mycursor.execute(sql, val)
                    subscription_rows = mycursor.fetchall()

                    covered_duration = _covered_subscription_duration(
                        parking_start, parking_end, subscription_rows)
                    if covered_duration > parking_duration:
                        covered_duration = parking_duration
                    charge_duration = parking_duration - covered_duration

                    if parking_duration == datetime.timedelta(0):
                        active_now = False
                        for sub_row in subscription_rows:
                            try:
                                sub_start_now = _combine_mysql_datetime(sub_row[0], sub_row[1])
                                sub_end_now = _combine_mysql_datetime(sub_row[2], sub_row[3])
                                if sub_start_now <= parking_end <= sub_end_now:
                                    active_now = True
                                    break
                            except (TypeError, ValueError):
                                pass
                        full_coverage = active_now
                    else:
                        full_coverage = covered_duration >= parking_duration

                    if full_coverage:
                        self.Label201.configure(text = "ΝΑΙ")
                        text = "ΝΑΙ"
                        subscription = '1'
                        charge_duration = datetime.timedelta(0)
                    elif covered_duration > datetime.timedelta(0):
                        self.Label201.configure(text = "ΟΧΙ*")
                        text = "ΟΧΙ*"
                        subscription = '0'
                    else:
                        self.Label201.configure(text = "ΟΧΙ")
                        text = "ΟΧΙ"
                        subscription = '0'

                    totaltime = charge_duration
                    totalcost = _calculate_parking_cost(totaltime, inputs)
                    totalcostfba = round(totalcost * fpa / 100 + totalcost, 2)
                    self.Label133.configure(text = str(totalcostfba) + "€")
            except:
                self.Label1.configure(text='''Γενικό σφάλμα συστήματος.''')
                self.Button1.configure(state = "disabled")
                self.Button2.configure(state = "disabled")
                self.Button3.configure(state = "disabled")
                self.Button4.configure(state = "disabled")
                self.Button5.configure(state = "disabled")
                self.Frame1.place_forget()
                self.Frame2.place_forget()
                self.Frame3.place_forget()
                self.Frame4.place_forget()
                self.Frame5.place_forget()
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

    def saveoutreceipt():
        global subscription
        global ticketnumberout
        global remaneplaces
        global idbase
        global totalcost
        global totaltime
        global countidbase
        global inputs
        global pay
        global err
        global time_string
        global timein
        global datein
        global placenumberout
        global rv
        global input_data
        global bargodelogo
        global datein2
        global fpa
        global dateendsub
        global timeendsub
        global subdateend
        global subdtimeend
        global payfpa
        global myresult
        global compinedatein
        global compinetimein
        global timedatesub
        global totalsubdatetimein
        global totalcostfba
        global subdaysDropdown
        global cal
        global subcostlistbox
        global subcostlistbox2
        global passwords
        global hosts
        global users
        global base
        global scrollbarresult2
        global cnx
        global mycursor
        global city
        global title1
        global title2
        global address
        global telephone
        global afm
        global doy
        pay = '0.0'

        cnx = None
        try:
            cnx = mysql.connector.connect(user = users,
                                          password = passwords,
                                          host = hosts,
                                          database = base,
                                          connect_timeout = 5)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.Label1.configure(text = '''Λάθος όνομα χρήστη ή κωδικός στην βάση δεδομένων.''')
                self.Button1.configure(state = "disabled")
                self.Button2.configure(state = "disabled")
                self.Button3.configure(state = "disabled")
                self.Button4.configure(state = "disabled")
                self.Button5.configure(state = "disabled")
                self.Frame1.place_forget()
                self.Frame2.place_forget()
                self.Frame3.place_forget()
                self.Frame4.place_forget()
                self.Frame5.place_forget()
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
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                self.Label1.configure(text = '''Η βάση δεδομένων δεν υπάρχει.''')
                self.Button1.configure(state = "disabled")
                self.Button2.configure(state = "disabled")
                self.Button3.configure(state = "disabled")
                self.Button4.configure(state = "disabled")
                self.Button5.configure(state = "disabled")
                self.Frame1.place_forget()
                self.Frame2.place_forget()
                self.Frame3.place_forget()
                self.Frame4.place_forget()
                self.Frame5.place_forget()
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
            elif err.errno == errorcode.CR_CONN_HOST_ERROR:
                self.Label1.configure(text = '''Δεν υπάρχει σύνδεση με την βάση δεδομένων. Επανεκκινήστε την βάση και το πρόγραμμα.''')
                self.Button1.configure(state = "disabled")
                self.Button2.configure(state = "disabled")
                self.Button3.configure(state = "disabled")
                self.Button4.configure(state = "disabled")
                self.Button5.configure(state = "disabled")
                self.Frame1.place_forget()
                self.Frame2.place_forget()
                self.Frame3.place_forget()
                self.Frame4.place_forget()
                self.Frame5.place_forget()
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
            else:
                self.Label1.configure(text='''Γενικό σφάλμα συστήματος.''' + str(err))
                self.Button1.configure(state = "disabled")
                self.Button2.configure(state = "disabled")
                self.Button3.configure(state = "disabled")
                self.Button4.configure(state = "disabled")
                self.Button5.configure(state = "disabled")
                self.Frame1.place_forget()
                self.Frame2.place_forget()
                self.Frame3.place_forget()
                self.Frame4.place_forget()
                self.Frame5.place_forget()
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
        if cnx is None or not cnx.is_connected():
            return
        try:
            mycursor = cnx.cursor()
            placenumberout = self.Entry11.get().upper()
            comments = self.Text11.get("1.0","end-1c")
        except:
            self.Label1.configure(text='''Γενικό σφάλμα συστήματος.''')
            self.Button1.configure(state = "disabled")
            self.Button2.configure(state = "disabled")
            self.Button3.configure(state = "disabled")
            self.Button4.configure(state = "disabled")
            self.Button5.configure(state = "disabled")
            self.Frame1.place_forget()
            self.Frame2.place_forget()
            self.Frame3.place_forget()
            self.Frame4.place_forget()
            self.Frame5.place_forget()
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
        transaction_committed = False
        try:
            pay = totalcost
  
            # Read ΦΠΑ
            sql = ("SELECT costfpa FROM fpa ORDER BY id DESC LIMIT 1")
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            for x in myresult:
                fpa = x
            payfpa = round(pay * fpa/100 + pay, 2)

            # Κλειδώνουμε τις διαθέσιμες θέσεις και ολοκληρώνουμε την έξοδο ως μία συναλλαγή.
            mycursor.execute("SELECT remaneplaces FROM places WHERE id = %s FOR UPDATE", (1,))
            places_row = mycursor.fetchone()
            current_free_places = int(places_row[0]) if places_row else 0

            # DATA update inputcar isout 1 (ενημερώνει ότι βγήκε το αυτοκίνητο)
            sql = '''UPDATE inputcar SET isout = %s WHERE ticketnumber = %s AND placenumber = %s AND isout = %s'''
            val = [('1'), (ticketnumberout), (placenumberout), ('0')]
            mycursor.execute(sql, val)
            if mycursor.rowcount != 1:
                cnx.rollback()
                raise RuntimeError("Δεν βρέθηκε μοναδική ενεργή είσοδος για το συγκεκριμένο εισιτήριο.")

            # DATA input to outputcar (σώζει την έξοδο του αυτοκινήτου με χρέωση κτλπ)
            sql = '''INSERT INTO outputcar(ticketnumber, dateout, timeout,
                placenumber, pay, subscription, comments) VALUES(%s, %s, %s, %s, %s, %s, %s)'''
            val = [(ticketnumberout, time_string5, time_string2, placenumberout, payfpa, subscription, comments)]
            mycursor.executemany(sql, val)

            # DATA update places + 1 (προσθέτει την θέση που άδειασε)
            remaneplaces = current_free_places + 1
            sql = '''UPDATE places SET remaneplaces = %s where id = %s'''
            val = [(remaneplaces, '1')]
            mycursor.executemany(sql, val)
            cnx.commit()
            transaction_committed = True
            self.Label1.configure(text = "To σύστημα είναι έτοιμο για νέα χαταχώρηση εξόδου.")
            self.Label13.configure(text = remaneplaces)

            # Η SQL συναλλαγή έχει ήδη γίνει commit. Εάν αποτύχει η έκδοση PDF,
            # δεν ισχυριζόμαστε ότι απέτυχε η καταχώριση (κίνδυνος διπλής κίνησης).
            try:
                # Read - Δεδομένα από SQL στοιχεία της εταιρείας (company)
                # ΑΦΜ
                sql = ("SELECT afm FROM company ORDER BY id DESC LIMIT 1")
                mycursor.execute(sql)
                myresult = mycursor.fetchone()
                for x in myresult:
                    afm = x

                # ΔΟΥ
                sql = ("SELECT doy FROM company ORDER BY id DESC LIMIT 1")
                mycursor.execute(sql)
                myresult = mycursor.fetchone()
                for x in myresult:
                    doy = x

                # Διεύθυνση
                sql = ("SELECT address FROM company ORDER BY id DESC LIMIT 1")
                mycursor.execute(sql)
                myresult = mycursor.fetchone()
                for x in myresult:
                    address = x

                # Πόλη
                sql = ("SELECT city FROM company ORDER BY id DESC LIMIT 1")
                mycursor.execute(sql)
                myresult = mycursor.fetchone()
                for x in myresult:
                    city = x

                # Τηλέφωνο
                sql = ("SELECT telephone FROM company ORDER BY id DESC LIMIT 1")
                mycursor.execute(sql)
                myresult = mycursor.fetchone()
                for x in myresult:
                    telephone = x

                # Τίτλος 1
                sql = ("SELECT title1 FROM company ORDER BY id DESC LIMIT 1")
                mycursor.execute(sql)
                myresult = mycursor.fetchone()
                for x in myresult:
                    title1 = x

                # Τίτλος 2
                sql = ("SELECT title2 FROM company ORDER BY id DESC LIMIT 1")
                mycursor.execute(sql)
                myresult = mycursor.fetchone()
                for x in myresult:
                    title2 = x

                # Write pdf EAN13 barcode  (ετοιμασία για την απόδειξη)
                # print to a file-like object:
                rv = BytesIO()

                # Link on barcode
                input_data = str(ticketnumberout)
                input_data = input_data.zfill(12)
                EAN13 = barcode.get_barcode_class('code128')
                EAN13(input_data, writer = ImageWriter()).write(rv)

                # save file:
                with open('IMs/OUT/barcode_' + str(placenumberout) + "_" + input_data + ".png", 'wb') as f:
                    EAN13(input_data, writer = ImageWriter()).write(f)
                bargodelogo = 'IMs/OUT/barcode_' + str(placenumberout) + "_" + input_data + ".png"
                c = canvas.Canvas("OUTs/" + str(placenumberout) + "_" + input_data + ".pdf")
                c.setFont('Arial', 12)
                c.drawImage(bargodelogo, 50, 735, width = 120, height = 80, mask = 'auto')
                c.drawString(45, 720, "ΑΠΟΔΕΙΞΗ - RECEIPT")
                c.drawString(10, 705, str(title1) + ".")
                c.drawString(10, 693, str(title2) + " " + str(address) + " " + str(city))
                c.drawString(10, 680, "Α.Φ.Μ. :")
                c.drawString(90, 680, str(afm))
                c.drawString(10, 669, "ΔΟΥ :")
                c.drawString(90, 669, str(doy))
                c.drawString(10, 657, "ΤΗΛ :")
                c.drawString(90, 657, str(telephone))
                c.line(5, 654, 215, 654)
                c.drawString(10, 641, "ΕΙΣΟΔΟΣ :")          
                c.drawString(90, 641, str(datein2) + "   " + " " + str(timein))
                c.drawString(10, 631, "ΈΞΟΔΟΣ :")
                c.drawString(90, 631, str(time_string))
                c.drawString(10, 621, "ΑΡ. ΕΙΣΙΤΗΡΙΟΥ :")
                c.drawString(120, 621, str(input_data))
                c.drawString(10, 611, "ΑΡ. ΚΥΚΛΟΦΟΡΙΑΣ :")
                c.drawString(140, 611, str(placenumberout))
                c.line(5, 607, 215, 607)
                c.drawString(10, 595, "ΚΑΘΑΡΗ ΑΞΙΑ :")
                c.drawString(140, 595, str(pay) + "€")
                c.drawString(10, 585, "Φ.Π.Α. " + str(fpa) + "%" + " :")
                c.drawString(140, 585, str(round(pay * fpa/100, 2)) + "€")
                c.drawString(10, 575, "ΠΛΗΡΩΤΕΟ ΠΟΣΟ :")
                c.drawString(140, 575, str(round(pay * fpa/100 + pay, 2)) + "€")
                c.drawString(65, 555, "ΕΥΧΑΡΙΣΤΟΥΜΕ")
                c.showPage()
                c.save()
                #os.remove("IMs/OUT/barcode_" + str(placenumberout) + "_" + input_data + ".png")

                # delay
                time.sleep(0.5)
                self.Entry11.configure(state = "normal")
                self.Entry11.delete(0, 'end')
                self.Button77.configure(state = "disabled")
                self.Button777.configure(state = "normal")
                pay = '0.0'
                totalcost = 0
                totaltime = 0

            except Exception as receipt_error:
                from parking_modules.receipt_safety import report_receipt_failure
                report_receipt_failure(self, "ΕΞΟΔΟΣ",
                                       ticketnumberout, placenumberout, receipt_error)
                return

            # Dongle Door OUT
            try:
                sql = '''UPDATE door SET stageout = %s'''
                val = [(1)]
                mycursor.execute(sql, val)
                cnx.commit()
                time.sleep(1)
                sql = '''UPDATE door SET stageout = %s'''
                val = [(0)]
                mycursor.execute(sql, val)
                cnx.commit()
                time.sleep(1)
            except:
                self.Label1.configure(text = "Πρόβλημα με την πόρτα εξόδου.")
                tk.messagebox.showerror(title = "Πρόβλημα με την πόρτα εξόδου.",
                            message = "Προσοχή! Δεν άνοιξε η πόρτα εξόδου.")
                time.sleep(1)
                self.Label1.configure(text = "To σύστημα είναι έτοιμο.")
        except Exception as err:
            if transaction_committed:
                from parking_modules.receipt_safety import report_receipt_failure
                report_receipt_failure(self, "ΕΞΟΔΟΣ", ticketnumberout, placenumberout, err)
                return
            try:
                cnx.rollback()
            except:
                pass
            self.Label1.configure(text='''Γενικό σφάλμα συστήματος.''' + str(err))
            self.Button1.configure(state = "disabled")
            self.Button2.configure(state = "disabled")
            self.Button3.configure(state = "disabled")
            self.Button4.configure(state = "disabled")
            self.Button5.configure(state = "disabled")
            self.Frame1.place_forget()
            self.Frame2.place_forget()
            self.Frame3.place_forget()
            self.Frame4.place_forget()
            self.Frame5.place_forget()
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
        self.Button77.configure(state = "disabled")
        self.Entry11.delete(0, 'end')
        self.Text11.delete("1.0", "end")
        self.Label155.configure(text = " ")
        self.Label110.configure(text = " ")
        self.Label133.configure(text = "0.0" + "€")
        self.Label1001.configure(text = ''' ''')
        self.Label201.configure(text = ''' ''')

    def button2():
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
        global scrollbarresult2

        self.Frame1.place_forget()
        self.Frame3.place_forget()
        self.Frame4.place_forget()
        self.Frame5.place_forget()
        self.Entry11.delete(0, 'end')
        self.Text11.delete("1.0", "end")
        self.Label155.configure(text = " ")
        self.Label110.configure(text = " ")
        self.Label133.configure(text = "0.0" + "€")
        self.Label1001.configure(text = ''' ''')
        self.Label201.configure(text = ''' ''')
        self.Text11.configure(state = "disable")
        self.Button77.configure(state = "disabled")
        self.Button777.configure(state = "normal")
        self.Entry11.configure(state = "normal")
        self.Entry11.delete(0, 'end')
        self.Frame2.place(relx=0.009, rely=0.074, relheight=0.853, relwidth=0.979)

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

    return {
        'searchout': searchout,
        'saveoutreceipt': saveoutreceipt,
        'button2': button2,
    }
