"""MySQL, έξοδος και ενημέρωση ρολογιού."""

def create_handlers(self, top, handlers):
    """Επιστρέφει callbacks με κοινό περιβάλλον, χωρίς μεταβολή λογικής GUI."""

    def msqlconnect():
        global threadmemory2
        global threadmemory
        global ticketnumber
        global inputnumber
        global remaneplaces
        global cnx
        global mycursor
        global myresult
        global subdaysDropdown
        global subcostlistbox
        global subcostlistbox2
        global cal
        global passwords
        global hosts
        global users
        global base
        global scrollbarresult2
        threadmemory2 = 0

        cnx = None
        try:
            cnx = mysql.connector.connect(user = users,
                                          password = passwords,
                                          host = hosts,
                                          database = base,
                                          connect_timeout = 5)
            mycursor = cnx.cursor()

            # Read remaneplaces
            mycursor.execute("SELECT remaneplaces FROM places")
            myresult = mycursor.fetchone()
            for x in myresult:
                remaneplaces = x
                self.Label13.configure(text = remaneplaces)
            if remaneplaces <= 0:
                self.Label13.configure(text = '0')
                self.Label1.configure(text = '''Δεν υπάρχουν διαθέσημες θέσεις πάρκινγκ. 0 θέσεις πάρκινγκ.''')
                self.Button7.configure(state = "disabled")
                self.Entry1.configure(state = "disabled")
                self.Text1.configure(state = "disabled")
            else:
                pass

            # Read inputnumber @ last and add + 1
            sql = ("SELECT inputnumber FROM inputcar ORDER BY inputnumber DESC LIMIT 1")
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            for x in myresult:
                inputnumber = x + 1
            self.Label5.configure(text = inputnumber)

            # Read ticketnumber @ last and add + 1
            sql = ("SELECT ticketnumber FROM inputcar ORDER BY inputnumber DESC LIMIT 1")
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            for x in myresult:
                ticketnumber = x + 1
            self.Label15.configure(text = ticketnumber)
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
                self.Label1.configure(text='''Γενικό σφάλμα συστήματος. ''' + str(err))
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

        # Αν απέτυχε η αρχική σύνδεση, η συνάρτηση έχει ήδη εμφανίσει το σφάλμα.
        # Δεν συνεχίζουμε με μη έγκυρο cnx.
        if cnx is None or not cnx.is_connected():
            return

        # Η αρχική σύνδεση γίνεται αποκλειστική σύνδεση επιτήρησης.
        # Κάθε callback (συνδρομές, είσοδος, έξοδος κ.λπ.) μπορεί να δημιουργεί
        # ή να κλείνει τις δικές του συνδέσεις χωρίς να επηρεάζει τον έλεγχο SQL.
        health_connection = cnx
        self._parking_health_connection = health_connection
        try:
            mycursor.close()
        except Exception:
            pass
        mycursor = None
        cnx = None

        def thread_sql():
            global threadmemory2
            global CheckSQL
            CheckSQL = globals().get("CheckSQL", 0)
            if threadmemory2 != True:
                return

            # Το health_connection δεν είναι global: δεν μπορεί να αντικατασταθεί
            # από τις ενέργειες του χρήστη (π.χ. άνοιγμα συνδρομών).
            try:
                if not health_connection.is_connected():
                    health_connection.ping(reconnect=True, attempts=1, delay=0)
                connected = health_connection.is_connected()
            except mysql.connector.Error:
                connected = False
            except (OSError, RuntimeError):
                connected = False

            if connected:
                if CheckSQL == 1:
                    CheckSQL = 0
                    self.Label1.configure(text='Το σύστημα είναι έτοιμο.')
            else:
                if CheckSQL != 1:
                    self.Label1.configure(
                        text='Προσωρινή απώλεια σύνδεσης MySQL. Έλεγχος επανασύνδεσης...')
                CheckSQL = 1
                # ΜΗΝ καταστρέφετε ή αποκρύπτετε το GUI. Ένα προσωρινό σφάλμα
                # MySQL δεν πρέπει να σβήνει δεδομένα από τις φόρμες.

            if threadmemory2 == True:
                root.after(2000, thread_sql)

        # Μόνο ένα περιοδικό callback. Δεν χρησιμοποιεί κοινή cnx/mycursor.
        if threadmemory2 == 0:
            threadmemory2 = 1
            root.after(2000, thread_sql)

    def buttonexit():
        global subdaysDropdown
        global threadmemory2
        global threadmemory
        global cnx
        global mycursor
        global myresult
        threadmemory = 0
        threadmemory2 = 0

        # Ασφαλές κλείσιμο της ανεξάρτητης σύνδεσης ελέγχου.
        try:
            health_connection = getattr(self, '_parking_health_connection', None)
            if health_connection is not None:
                health_connection.close()
        except Exception:
            pass
        try:
            if mycursor is not None:
                mycursor.close()
            if cnx is not None:
                cnx.close()
        except Exception:
            pass
        time.sleep(1)
        exit()

    def thread_time():
        global subdaysDropdown
        global time_string5
        global time_string4
        global time_string2
        global time_string

        if threadmemory != True:
            return
        time_now = time.localtime()
        time_string = time.strftime("%d/%m/%Y    %#H:%M:%S", time_now)
        time_string2 = time.strftime("%#H:%M:%S", time_now)
        time_string3 = time.strftime("%A, %d %B %Y", time_now)
        time_string4 = time.strftime("%Y/%m/%d", time_now)
        time_string5 = time.strftime("%Y-%m-%d", time_now)
        self.Label2.configure(text = time_string)
        self.Label11.configure(text = time_string2)
        self.Label111.configure(text = time_string2)
        self.Label9.configure(text = time_string3)
        self.Label19.configure(text = time_string3)
        self.Label11000.configure(text = time_string2)
        root.after(1000, thread_time)

    return {
        'msqlconnect': msqlconnect,
        'buttonexit': buttonexit,
        'thread_time': thread_time,
    }
