"""Ευρετήριο οχημάτων και αναζητήσεις."""

def create_handlers(self, top, handlers):
    """Επιστρέφει callbacks με κοινό περιβάλλον, χωρίς μεταβολή λογικής GUI."""

    def button5():
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
        global listboxresult
        global scrollbarresult
        global scrollbarresult2

        self.EntryS1.delete(0, 'end')
        self.Buttonplot1.configure(state = "disabled")
        self.Buttonplot2.configure(state = "disabled")
        self.Buttonresults.configure(state = "disabled")
        self.Frame1.place_forget()
        self.Frame2.place_forget()
        self.Frame3.place_forget()
        self.Frame4.place_forget()
        self.Frame5.place(relx=0.009, rely=0.074, relheight=0.853, relwidth=0.979)

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
            listboxresult.destroy()
        except:
            pass
        try:
            scrollbarresult.destroy()
        except:
            pass
        try:
            scrollbarresult2.destroy()
        except:
            pass
        try:
            subdaysDropdown.destroy()
        except:
            pass

        # Αποτελέσματα Frame 5
        listboxresult = Listbox(self.Frame5)
        listboxresult.configure(font = "-family {Rockwell Nova} -size 12")
        listboxresult.configure(cursor = "hand1")
        listboxresult.pack(side = LEFT, padx = 10, pady = 80, ipadx = 455, ipady = 20, anchor = 'se')
        scrollbarresult = Scrollbar(self.Frame5)
        scrollbarresult.pack(side = RIGHT, padx = 5, pady = 80, ipady = 112, anchor = 'se')
        scrollbarresult.config(command = listboxresult.yview, cursor = "hand1")
        listboxresult.config(yscrollcommand = scrollbarresult.set)
        scrollbarresult2 = Scrollbar(top)
        scrollbarresult2.pack(side = BOTTOM, padx = 230, pady = 110, ipady = 0, fill = X)
        scrollbarresult2.config(command = listboxresult.xview, cursor = "hand1", orient = HORIZONTAL)
        listboxresult.config(xscrollcommand = scrollbarresult2.set)
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

    def searchsubcar2():
        global passwords
        global users
        global hosts
        global base
        global listboxresult
        global subscriptionall
        global inputall
        global outputall
        global placenumbersearch2
        global cnx
        global mycursor
        global myresult
        subscriptionall = 0
        inputall = 0
        outputall = 0

        placenumbersearch2 = self.EntryS1.get().upper()
        myresult = placenumbersearch2.isascii()
        if myresult == False:
            self.Label1.configure(text = "Εισάγατε τον αριθμό πινακίδας οχήματος στα Ελληνικά.")
            tk.messagebox.showerror(title = "Δεν έγινε εισαγωγή αριθμού πινακίδας.",
                        message = "Προσοχή! Δώστε αριθμό πινακίδας στα Αγγλικά για εύρεση αυτοκινήτου.")
            time.sleep(1)
            self.EntryS1.delete(0, 'end')
            self.Label155.configure(text = " ")
            self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
            self.Label2011.configure(text = " ")
            self.Label2013.configure(text = " ")
            self.Label10011.configure(text = " ")
            self.Label10012.configure(text = " ")
            self.Label1333.configure(text = "0.0€")
            listboxresult.delete(0, 'end')
        elif placenumbersearch2 == "":
            self.Label1.configure(text = "Δεν εισάγατε τον αριθμό πινακίδας οχήματος.")
            tk.messagebox.showerror(title = "Δεν έγινε εισαγωγή αριθμού πινακίδας.",
                        message = "Προσοχή! Δεν δώσατε αριθμό πινακίδας για εύρεση αυτοκινήτου.")
            time.sleep(1)
            self.EntryS1.delete(0, 'end')
            self.Text11.delete("1.0", "end")
            self.Label155.configure(text = " ")
            self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
            self.Label1001.configure(text = " ")
            self.Label110.configure(text = " ")
            self.Label201.configure(text = " ")
            self.Text11.configure(state = "disable")
            listboxresult.delete(0, 'end')
        else:
            try:
                listboxresult.delete(0, 'end')
                cnx = mysql.connector.connect(user = users,
                                          password = passwords,
                                          host = hosts,
                                          database = base,
                                          connect_timeout = 5)
                mycursor = cnx.cursor()

                # Αποτελέσματα και Plot
                # Βρήσκει το οχημα αν είναι μέσα ή έξω ή αν έχει συνδρομή γενικές πληροφορίες (στατιστικά - plot*)
                # input car
                try:
                    sql = ("SELECT * FROM inputcar WHERE placenumber = %s")
                    val = [(placenumbersearch2)]
                    mycursor.execute(sql, val)
                    myresult = mycursor.fetchall()
                    listboxresult.insert(END, "Είσοδοι για το " + placenumbersearch2)
                    for x in myresult:
                        inputall = x
                        listboxresult.insert(END, "Αριθμός εισόδου: " + str(inputall[0]) + \
                                             ". Αριθμος εισητηρίου: " + str(inputall[1]) + \
                                             ". Ημερομηνία εισόδου: " + str(inputall[2].strftime('%d-%m-%Y')) + \
                                             " " + str(inputall[3]) + \
                                             ". Σχόλια: " + str(inputall[5]))
                    listboxresult.insert(END, " ")
                    self.Buttonplot2.configure(state = "normal")
                    self.Buttonresults.configure(state = "normal")
                    if inputall == 0:
                        self.Buttonplot2.configure(state = "disabled")
                    else:
                        pass
                except:
                    self.Buttonplot2.configure(state = "disabled")

                # output car
                try:
                    sql = ("SELECT * FROM outputcar WHERE placenumber = %s")
                    val = [(placenumbersearch2)]
                    mycursor.execute(sql, val)
                    myresult = mycursor.fetchall()
                    listboxresult.insert(END, "Έξοδοι για το " + placenumbersearch2)
                    for x in myresult:
                        outputall = x
                        listboxresult.insert(END, "Αριθμός εξόδου: " + str(outputall[0]) + \
                                             ". Αριθμος εισητηρίου: " + str(outputall[1]) + \
                                             ". Ημερομηνία εξόδου: " + str(outputall[2].strftime('%d-%m-%Y')) + \
                                             " " + str(outputall[3]) + \
                                             ". Κόστος: " + str(outputall[5]) + "€" + \
                                             ". Σχόλια: " + str(outputall[7])) 
                    listboxresult.insert(END, " ")
                    self.Buttonplot2.configure(state = "normal")
                    self.Buttonresults.configure(state = "normal")
                    if outputall == 0:
                        self.Buttonplot2.configure(state = "disabled")
                    else:
                        pass
                except:
                    self.Buttonplot2.configure(state = "disabled")

                # subscription
                try:
                    sql = ("SELECT * FROM subscription WHERE placenumber = %s")
                    val = [(placenumbersearch2)]
                    mycursor.execute(sql, val)
                    myresult = mycursor.fetchall()
                    listboxresult.insert(END, "Συνδρομές για το " + placenumbersearch2)
                    for x in myresult:
                        subscriptionall = x
                        listboxresult.insert(END, "Αριθμός συνδρομής: " + str(subscriptionall[0]) + \
                                             ". Ονοματεπώνυμο: " + str(subscriptionall[1]) + \
                                             " " + str(subscriptionall[2]) + \
                                             ". Τηλέφωνο: " + str(subscriptionall[3]) + \
                                             ". Ημερομηνία αρχής: " + str(subscriptionall[5].strftime('%d-%m-%Y')) + \
                                             " " + str(subscriptionall[7]) + \
                                             ". Ημερομηνία λήξης: " + str(subscriptionall[6].strftime('%d-%m-%Y')) + \
                                             " " + str(subscriptionall[8]) + ". Ημέρες: " + str(subscriptionall[9]) + \
                                             ". Κόστος: " + str(subscriptionall[10]) + "€" + ". (Με Φ.Π.Α.: " + str(subscriptionall[11]) + "%)")
                    self.Buttonplot1.configure(state = "normal")
                    self.Buttonresults.configure(state = "normal")
                    if subscriptionall == 0:
                        self.Buttonplot1.configure(state = "disabled")
                    else:
                        pass
                except:
                    self.Buttonplot1.configure(state = "disabled")
                if subscriptionall == 0 and outputall == 0 and inputall == 0:
                    self.Buttonresults.configure(state = "disabled")
                    self.Label1.configure(text = "Δεν βρέθηκε το όχημα.")
                    tk.messagebox.showinfo(title = "Δεν βρέθηκαν δεδομένα για το όχημα.",
                                            message = "Δεν υπάρχουν δεδομένα οχήματος.")
                    time.sleep(1)
                    self.EntryS1.delete(0, 'end')
                    listboxresult.delete(0, 'end')
                    self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
                else:
                    pass
            except:
                self.Buttonplot1.configure(state = "disabled")
                self.Buttonplot2.configure(state = "disabled")
                self.Buttonresults.configure(state = "disabled")
                self.Label1.configure(text='''Γενικό σφάλμα συστήματος βάσης. Παρακαλώ επανεκκινήστε την βάση και το πρόγραμμα.''')

    return {
        'button5': button5,
        'searchsubcar2': searchsubcar2,
    }
