"""Είσοδος οχημάτων και έκδοση εισιτηρίων."""

def create_handlers(self, top, handlers):
    """Επιστρέφει callbacks με κοινό περιβάλλον, χωρίς μεταβολή λογικής GUI."""

    def saveandprint():
        global placenumber
        global texter
        global remaneplaces
        global ticketnumber
        global subdaysDropdown
        global subcostlistbox
        global subcostlistbox2
        global passwords
        global hosts
        global users
        global base
        global scrollbarresult2
        global mycursor
        global myresult
        global doy
        global city
        global afm
        global address
        global title1
        global title2
        global telephone

        placenumber = self.Entry1.get().upper()
        # Check for english
        myresult = placenumber.isascii()
        if myresult == False:
            placenumber = "×××"
            self.Entry1.delete(0, 'end')
            self.Text1.delete("1.0", "end")
        else:
            texter = self.Text1.get("1.0","end-1c")
        
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
        # Σε αποτυχία σύνδεσης δεν επιχειρούμε καμία εγγραφή.
        if cnx is None or not cnx.is_connected():
            return
        mycursor = cnx.cursor()
        if placenumber == "":
            self.Label1.configure(text = "Δεν εισάγατε τον αριθμό πινακίδας οχήματος.")
            tk.messagebox.showerror(title = "Δεν έγινε εισαγωγή αριθμού πινακίδας.",
                                    message = "Προσοχή! Δεν δώσατε αριθμό πινακίδας \
για την εισαγωγή αυτοκινήτου.")
            time.sleep(1)
            self.Text1.delete("1.0", "end")
            self.Label1.configure(text = "To σύστημα είναι έτοιμο.")
        elif placenumber == "×××":
            self.Label1.configure(text = "Εισάγατε τον αριθμό πινακίδας οχήματος στα Ελληνικά.")
            tk.messagebox.showerror(title = "Δεν έγινε εισαγωγή αριθμού πινακίδας.",
                                    message = "Προσοχή! Δώστε αριθμό πινακίδας στα Αγγλικά \
για την εισαγωγή αυτοκινήτου.")
            time.sleep(1)
            self.Text1.delete("1.0", "end")
            self.Label1.configure(text = "To σύστημα είναι έτοιμο.")
        else:
            try:
                # Read placenumber @ All for check (αριθμός πινακίδας)
                sql = ("SELECT placenumber FROM inputcar WHERE EXISTS(SELECT \
placenumber FROM inputcar WHERE placenumber = %s AND isout = %s)")
                val = [(placenumber), ('0')]
                mycursor.execute(sql, val)
                myresult = mycursor.fetchone()
                for x in myresult:
                    placenumbercheck = 0
            except:
                placenumbercheck = 1
            if placenumbercheck == 0:
                self.Label1.configure(text = "Το αυτοκίνητο με αριθμό: " + placenumber + " είναι μέσα στο πάρκινγκ.")
                tk.messagebox.showerror(title = "Το αυτοκίνητο " + placenumber + " είναι μέσα στο πάρκινγ.",
                                        message = "Προσοχή! Δώσατε \
εισαγωγή αυτοκινήτου με αριθμό " + placenumber + " το οποίο είναι μέσα στο πάρκινγ.")
                time.sleep(1)
                self.Entry1.delete(0, 'end')
                self.Text1.delete("1.0", "end")
                self.Label1.configure(text = "To σύστημα είναι έτοιμο.")
            else:
                # Διαβάζουμε ξανά τις διαθέσιμες θέσεις και κλειδώνουμε τη γραμμή μέχρι το commit.
                # Έτσι δύο ταυτόχρονες εισαγωγές δεν μπορούν να δημιουργήσουν αρνητικό υπόλοιπο.
                mycursor.execute("SELECT remaneplaces FROM places WHERE id = %s FOR UPDATE", (1,))
                places_row = mycursor.fetchone()
                remaneplaces = int(places_row[0]) if places_row else 0
                self.Label13.configure(text = max(remaneplaces, 0))

                # Επαναληπτικός έλεγχος της πινακίδας μέσα στην ίδια συναλλαγή.
                # Το lock της places σειριοποιεί τις παράλληλες εισαγωγές.
                sql = ("SELECT 1 FROM inputcar WHERE placenumber = %s AND isout = %s LIMIT 1")
                val = [(placenumber), ('0')]
                mycursor.execute(sql, val)
                if mycursor.fetchone() is not None:
                    cnx.rollback()
                    self.Label1.configure(text = "Το αυτοκίνητο με αριθμό: " + placenumber + " είναι μέσα στο πάρκινγκ.")
                    tk.messagebox.showerror(title = "Το αυτοκίνητο " + placenumber + " είναι μέσα στο πάρκινγ.",
                                            message = "Προσοχή! Το όχημα υπάρχει ήδη ως ενεργή είσοδος.")
                    self.Entry1.delete(0, 'end')
                    self.Text1.delete("1.0", "end")
                    return

                if remaneplaces <= 0:
                    cnx.rollback()
                    self.Label13.configure(text = '0')
                    self.Label1.configure(text='''Δεν υπάρχουν διαθέσημες θέσεις πάρκινγκ. 0 θέσεις πάρκινγκ.''')
                    self.Button7.configure(state = "disabled")
                    self.Entry1.delete(0, 'end')
                    self.Entry1.configure(state = "disabled")
                    self.Text1.configure(state = "disabled")
                    return

                # Νέος αριθμός εισιτηρίου αφού αποκτήθηκε το lock, για αποφυγή διπλού αριθμού
                # σε ταυτόχρονες εισαγωγές από δύο instances.
                mycursor.execute("SELECT ticketnumber FROM inputcar ORDER BY inputnumber DESC LIMIT 1")
                ticket_row = mycursor.fetchone()
                ticketnumber = int(ticket_row[0]) + 1 if ticket_row else 1
                # Κρατάμε το ticket που εκδόθηκε σε αυτή ακριβώς τη συναλλαγή. Μετά το commit
                # μπορεί άλλο instance να δημιουργήσει νέο ticket πριν τυπωθεί το PDF.
                issued_ticketnumber = ticketnumber
                self.Label15.configure(text = ticketnumber)

                # DATA input (είσοδος αυτοκινήτου)
                sql = '''INSERT INTO inputcar(ticketnumber, datein, timein,
                    placenumber, comments, isout) VALUES(%s, %s, %s, %s, %s, %s)'''
                val = [(ticketnumber, time_string4, time_string2, placenumber, texter, '0')]
                mycursor.executemany(sql, val)
                self.Label1.configure(text = "To σύστημα είναι έτοιμο για νέα χαταχώρηση.")

                # Decrease renameplaces 1 (αφαιρεση μιας θέσης στο πάρκινγ)
                remaneplaces = remaneplaces - 1
                sql = '''UPDATE places SET remaneplaces = %s where id = %s'''
                val = [(remaneplaces, '1')]
                mycursor.executemany(sql, val)
                cnx.commit()
                self.Label13.configure(text = remaneplaces)
                self.Entry1.delete(0, 'end')
                self.Text1.delete("1.0", "end")
                if remaneplaces <= 0:
                    self.Label13.configure(text = "0")
                    self.Label1.configure(text = '''Δεν υπάρχουν διαθέσημες θέσεις πάρκινγκ. 0 θέσεις πάρκινγκ.''')
                    self.Button7.configure(state = "disabled")
                    self.Entry1.delete(0, 'end')
                    self.Entry1.configure(state = "disabled")
                    self.Text1.configure(state = "disabled")
                else:
                    pass

                # Η SQL συναλλαγή έχει ήδη γίνει commit. Εάν αποτύχει η έκδοση PDF,
                # δεν ισχυριζόμαστε ότι απέτυχε η καταχώριση (κίνδυνος διπλής κίνησης).
                try:
                    # Read inputnumber @ last and add + 1 (Αριθμός εισόδου)
                    sql = ("SELECT inputnumber FROM inputcar ORDER BY inputnumber DESC LIMIT 1")
                    mycursor.execute(sql)
                    myresult = mycursor.fetchone()
                    for x in myresult:
                        inputnumber = x + 1
                    self.Label5.configure(text = inputnumber)

                    # Read ticketnumber @ last and add + 1 (Αριθμός εισιτηρίου)
                    sql = ("SELECT ticketnumber FROM inputcar ORDER BY inputnumber DESC LIMIT 1")
                    mycursor.execute(sql)
                    myresult = mycursor.fetchone()
                    for x in myresult:
                        ticketnumber = x + 1
                    self.Label15.configure(text = ticketnumber)

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

                    # in Data fill 12 digitis + '7'
                    input_data = str(issued_ticketnumber)
                    input_data = input_data.zfill(12)
                    input_data = str(input_data)

                    #Creating an instance of qrcode (δημιουργία qrcode)
                    qr = qrcode.QRCode(version = 1, box_size = 10, border = 5)
                    qr.add_data(input_data)
                    qr.make(fit = True)
                    img = qr.make_image(fill = 'black', back_color = 'white')
                    img.save('IMs/IN/qrcode_' + placenumber + '_' + str(issued_ticketnumber) + '.png')

                    # Write to pdf (Εκτύπωση pdf εισιρτηρίου)
                    PartnerLogo = 'IMs/IN/qrcode_' + placenumber + '_' + str(issued_ticketnumber) + '.png'
                    c = canvas.Canvas("INs/grcode_" + placenumber + "_" + str(issued_ticketnumber) + ".pdf")
                    c.drawImage(PartnerLogo, -10,675, width = 100, height = 100, mask = 'auto')
                    c.setFont('Arial', 12)
                    c.drawString(5, 803, "ΕΙΣΙΤΗΡΙΟ - TICKET")
                    c.drawString(5, 792, str(title1) + "." + " " + " " + str(address) + " " + str(city))
                    c.drawString(5, 779, "Α.Φ.Μ. : " + str(afm) + " " + "ΔΟΥ " + str(doy))
                    c.drawString(5, 767, "ΟΥΔΕΜΙΑ ΕΥΘΥΝΗ ΦΕΡΟΥΜΕ ΓΙΑ ΦΘΟΡΑ ΤΟΥ ΑΥΤΟΚΙΝΗΤΟΥ")
                    c.drawString(102, 750, "ΑΡ. ΕΙΣΙΤΗΡΙΟΥ")
                    c.drawString(210, 750, ":  " + input_data)
                    c.drawString(102, 738, "ΗΜ/ΝΙΑ ΕΚΔΟΣΗΣ")
                    c.drawString(210, 738, ":  " + time_string)
                    c.drawString(102, 726, "ΑΡ. ΠΙΝΑΚΙΔΑΣ")
                    c.drawString(210, 726, ":  " + placenumber)
                    c.drawString(102, 709, "ΕΥΧΑΡΙΣΤΟΥΜΕ")
                    c.line(102, 705, 296, 705)
                    c.drawString(102, 692, "TΗΛΕΦΩΝΟ")
                    c.drawString(210, 692, ":  " + str(telephone))
                    c.showPage()
                    c.save()
                    #os.remove("IMs/IN/qrcode_" + placenumber + "_" + str(issued_ticketnumber) + ".png")
                    time.sleep(0.7)

                except Exception as receipt_error:
                    from parking_modules.receipt_safety import report_receipt_failure
                    report_receipt_failure(self, "ΕΙΣΟΔΟΣ",
                                           issued_ticketnumber, placenumber, receipt_error)
                    return

                # Dongle Door IN
                try:
                    sql = '''UPDATE door SET stagein = %s'''
                    val = [(1)]
                    mycursor.execute(sql, val)
                    cnx.commit()
                    time.sleep(1)
                    sql = '''UPDATE door SET stagein = %s'''
                    val = [(0)]
                    mycursor.execute(sql, val)
                    cnx.commit()
                    time.sleep(1)
                except:
                    self.Label1.configure(text = "Πρόβλημα με την πόρτα εισόδου.")
                    tk.messagebox.showerror(title = "Πρόβλημα με την πόρτα εισόδου.",
                                message = "Προσοχή! Δεν άνοιξε η πόρτα εισόδου.")
                    time.sleep(1)
                    self.Label1.configure(text = "To σύστημα είναι έτοιμο.")

    def button1():
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
        global remaneplaces

        self.Frame2.place_forget()
        self.Frame3.place_forget()
        self.Frame4.place_forget()
        self.Frame5.place_forget()
        self.Entry1.delete(0, 'end')
        self.Text1.delete("1.0", "end")
        self.Frame1.place(relx=0.009, rely=0.074, relheight=0.853, relwidth=0.979)

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
        if remaneplaces > 0:
            self.Button7.configure(state = 'normal')
            self.Entry1.configure(state = 'normal')
        else:
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

        # Read Places
        try:
            cnx = mysql.connector.connect(user = users,
                                          password = passwords,
                                          host = hosts,
                                          database = base,
                                          connect_timeout = 5)
            mycursor = cnx.cursor()

            sql = ("SELECT remaneplaces FROM places")
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            for n in myresult:
               placenumbers = n
            remaneplaces = int(placenumbers)
            self.Label13.configure(text = remaneplaces)
            self.Entry1.delete(0, 'end')
            self.Entry1.configure(state = "normal")
            self.Text1.configure(state = "normal")
            self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
            if placenumbers <= 0:
                self.Label13.configure(text = "0")
                self.Label1.configure(text = '''Δεν υπάρχουν διαθέσημες θέσεις πάρκινγκ. 0 θέσεις πάρκινγκ.''')
                self.Button7.configure(state = "disabled")
                self.Entry1.delete(0, 'end')
                self.Entry1.configure(state = "disabled")
                self.Text1.configure(state = "disabled")
            else:
                self.Button7.configure(state = "normal")
                self.Entry1.configure(state = "normal")
                self.Text1.configure(state = "normal")
        except:
            pass

    return {
        'saveandprint': saveandprint,
        'button1': button1,
    }
