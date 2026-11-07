"""Διαχείριση συνδρομών."""
import datetime
import re
from parking_modules import subscription_services


def _date_display(value):
    """Εμφάνιση ελληνικής ημερομηνίας, ανεξάρτητα από τη MySQL/locale."""
    if isinstance(value, datetime.datetime):
        value = value.date()
    if isinstance(value, datetime.date):
        return value.strftime("%d/%m/%Y")
    return datetime.datetime.strptime(str(value)[:10], "%Y-%m-%d").strftime("%d/%m/%Y")


def _european_date(value):
    """Έλεγχος αυστηρής μορφής ΗΗ/ΜΜ/ΕΕΕΕ, χωρίς αμφισημία ημέρας/μήνα."""
    if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", value.strip()):
        raise ValueError("Η ημερομηνία πρέπει να είναι ΗΗ/ΜΜ/ΕΕΕΕ.")
    return datetime.datetime.strptime(value.strip(), "%d/%m/%Y").date()


def create_handlers(self, top, handlers):
    """Επιστρέφει callbacks με κοινό περιβάλλον, χωρίς μεταβολή λογικής GUI."""

    def subdaysSelection(event):
        """Επιλογή διάρκειας από τις επιτρεπόμενες τιμές του τιμοκαταλόγου."""
        global my_subdays_namess
        global subdaysDropdown
        global my_subdays_names
        selection = subdaysDropdown.get().strip()
        my_subdays_namess = selection if selection in [str(v) for v in my_subdays_names] else 0

    def button3():
        self._selected_subscription_id = None
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
        global ids
        global subdaysDropdown
        global my_subdays_names
        global subcostlistbox
        global subcostlistbox2
        global passwords
        global hosts
        global users
        global base
        global scrollbarresult2
        global myresult

        self.Frame1.place_forget()
        self.Frame2.place_forget()
        self.Frame4.place_forget()
        self.Frame5.place_forget()
        self.Frame3.place(relx=0.009, rely=0.074, relheight=0.853, relwidth=0.979)

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
            self.Label20133.place_forget()
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

        # Clear and disable Buttons Labels and Entries in Frame 3

        self.Entry1100.configure(state = 'normal')
        self.Entry1111.configure(state = 'normal')
        self.Entry1110.configure(state = 'normal')
        self.Entry1112.configure(state = 'normal')
        self.Entry1100.delete(0, 'end')
        self.Entry1111.delete(0, 'end')
        self.Entry1110.delete(0, 'end')
        self.Entry1112.delete(0, 'end')
        self.Label1333.configure(text = '''0.0''' + '€')
        self.Label10011.configure(text = ''' ''')
        self.Label10012.configure(text = ''' ''')
        self.Label2011.configure(text = ''' ''')
        self.Label2013.configure(text = ''' ''')

        # disable
        self.Button7772.configure(state = "disabled")
        self.Button7773.configure(state = "disabled")
        self.Button7775.configure(state = "disabled")
        self.Button7774.configure(state = "disabled")
        self.Button7771.configure(state = "disabled")

        # enable
        self.Button7777.configure(state = "normal")

        # Calendar in Frame 3
        try:
            if cal == 0:
                myday = datetime.datetime.now()
                year = myday.strftime('%Y')
                month = myday.strftime('%m')
                day = myday.strftime('%d')
                cal = Calendar(self.Frame3, font="Arial 12", cursor = "hand1", selectmode = 'day', year = int(year),
                    month = int(month), day = int(day), locale = 'el_GR', selectbackground = '#ff8040',
                    selectforeground = '#ffff00', background = 'black', date_pattern = "dd/mm/yyyy")
                cal.pack(side = "left", fill = "none", expand = False, padx = 250, pady = 122,
                    ipadx = 7, ipady = 29, anchor = 'ne')
            else:
                pass
        except:
            pass

        # Drop menu dayssub costsub in Frame 3
        # Check id
        cnx = None
        mycursor = None
        try:
            cnx = mysql.connector.connect(user = users,
                                          password = passwords,
                                          host = hosts,
                                          database = base,
                                          connect_timeout = 5)
            mycursor = cnx.cursor()

            # Check subcost. Δεν βασιζόμαστε στα id ώστε διαγραμμένες εγγραφές να μην
            # δημιουργούν κενά/IndexError στο Combobox.
            sql = ("SELECT subdays FROM costsub WHERE id >= '0' ORDER BY id ASC")
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            my_subdays_names = [str(row[0]) for row in myresult]
            if not my_subdays_names:
                my_subdays_names = ["0"]
            ids = len(my_subdays_names) - 1

            style = ttk.Style()
            style.configure("TCombobox", foreground = "blue")
            subdaysDropdown = ttk.Combobox(root, state = "disable", style = "TCombobox", font = "Arial 16 bold", justify = "center", width = "3", values = my_subdays_names, cursor="hand1")
            subdaysDropdown.current(0)
            subdaysDropdown.bind("<<ComboboxSelected>>", subdaysSelection)
            subdaysDropdown.grid(padx = 793, pady = 175)
        except Exception as exc:
            tk.messagebox.showerror('Ανάκτηση τιμοκαταλόγου συνδρομών',str(exc))
        finally:
            if mycursor is not None:
                try: mycursor.close()
                except Exception: pass
            if cnx is not None:
                try: cnx.close()
                except Exception: pass

    def searchsubcar():
        global placenumbersearchsub
        global firstname
        global lastname
        global phone
        global startdaysubresult
        global stopdaysubresult
        global costmoney
        global myresult
        global result
        global subdateend
        global subdtimeend
        global dateend
        global timeendsub
        global passwords
        global hosts
        global users
        global base
        global myresult
        global Myfpa
        firstname = ""
        lastname = ""
        phone = ""
        placenumbersearchsub = ""
        myresult = ""
        result = []
        self._selected_subscription_id = None
        cnx = None
        mycursor = None
        self.Button7772.configure(state='disabled')
        self.Button7773.configure(state='disabled')

        # Ψάχνει αν υπάρχει συνδρομή
        # Check for english
        placenumbersearchsub = self.Entry1100.get().upper()
        firstname = self.Entry1110.get()
        lastname = self.Entry1111.get()
        phone = self.Entry1112.get()
        myresult = placenumbersearchsub.isascii()
        if myresult == False:
            self.Label1.configure(text = "Εισάγατε τον αριθμό πινακίδας οχήματος στα Ελληνικά.")
            tk.messagebox.showerror(title = "Δεν έγινε εισαγωγή αριθμού πινακίδας.",
                        message = "Προσοχή! Δώστε αριθμό πινακίδας στα Αγγλικά για εύρεση αυτοκινήτου.")
            self.Entry1100.delete(0, 'end')
            self.Label155.configure(text = " ")
            self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
            self.Label2011.configure(text = " ")
            self.Label2013.configure(text = " ")
            self.Label10011.configure(text = " ")
            self.Label10012.configure(text = " ")
            self.Label1333.configure(text = "0.0€")
        else:
            try:
                cnx = mysql.connector.connect(user = users,
                                          password = passwords,
                                          host = hosts,
                                          database = base,
                                          connect_timeout = 5)
                mycursor = cnx.cursor()

                # Εμφάνιση συνδρομής
                sql = ("SELECT * FROM subscription WHERE placenumber = %s AND id > 0 ORDER BY id DESC LIMIT 1")
                val = [(placenumbersearchsub)]
                mycursor.execute(sql, val)
                myresult = mycursor.fetchall()
                if myresult == []:
                    sql = ("SELECT * FROM subscription WHERE firstname = %s AND id > 0 ORDER BY id DESC LIMIT 1")
                    val = [(firstname)]
                    mycursor.execute(sql, val)
                    myresult = mycursor.fetchall()
                    if myresult == []:
                        sql = ("SELECT * FROM subscription WHERE lastname = %s AND id > 0 ORDER BY id DESC LIMIT 1")
                        val = [(lastname)]
                        mycursor.execute(sql, val)
                        myresult = mycursor.fetchall()
                        if myresult == []:
                            if phone.isnumeric() or phone == "":
                                sql = ("SELECT * FROM subscription WHERE phone = %s AND id > 0 ORDER BY id DESC LIMIT 1")
                                val = [(phone)]
                                mycursor.execute(sql, val)
                                myresult = mycursor.fetchall()
                                if myresult == [] and placenumbersearchsub != "":
                                    self.Label1.configure(text = "Δεν βρέθηκε συνδρομή.")
                                    tk.messagebox.showinfo(title = "Δεν βρέθηκε συνδρομή για το όχημα.",
                                                 message = "Δεν υπάρχει συνδρομή οχήματος.")
                                    self.Button7777.configure(state = "disabled")
                                    
                                    self.Label155.configure(text = " ")
                                    self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
                                    self.Label2011.configure(text = " ")
                                    self.Label2013.configure(text = " ")
                                    self.Label10011.configure(text = " ")
                                    self.Label10012.configure(text = " ")
                                    self.Label1333.configure(text = "0.0€")
                                    self.Button7774.configure(state = 'normal')
                                elif myresult == [] and phone != "":
                                    self.Label1.configure(text = "Δεν βρέθηκε συνδρομή.")
                                    tk.messagebox.showinfo(title = "Δεν βρέθηκε συνδρομή για το όχημα.",
                                                 message = "Δεν υπάρχει συνδρομή οχήματος.")
                                    self.Label155.configure(text = " ")
                                    self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
                                    self.Label2011.configure(text = " ")
                                    self.Label2013.configure(text = " ")
                                    self.Label10011.configure(text = " ")
                                    self.Label10012.configure(text = " ")
                                    self.Label1333.configure(text = "0.0€")
                                elif myresult == [] and firstname != "":
                                    self.Label1.configure(text = "Δεν βρέθηκε συνδρομή.")
                                    tk.messagebox.showinfo(title = "Δεν βρέθηκε συνδρομή για το όχημα.",
                                                 message = "Δεν υπάρχει συνδρομή οχήματος.")
                                    self.Label155.configure(text = " ")
                                    self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
                                    self.Label2011.configure(text = " ")
                                    self.Label2013.configure(text = " ")
                                    self.Label10011.configure(text = " ")
                                    self.Label10012.configure(text = " ")
                                    self.Label1333.configure(text = "0.0€")
                                elif myresult == [] and lastname != "":
                                    self.Label1.configure(text = "Δεν βρέθηκε συνδρομή.")
                                    tk.messagebox.showinfo(title = "Δεν βρέθηκε συνδρομή για το όχημα.",
                                                 message = "Δεν υπάρχει συνδρομή οχήματος.")
                                    self.Label155.configure(text = " ")
                                    self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
                                    self.Label2011.configure(text = " ")
                                    self.Label2013.configure(text = " ")
                                    self.Label10011.configure(text = " ")
                                    self.Label10012.configure(text = " ")
                                    self.Label1333.configure(text = "0.0€")
                                else:
                                    pass
                            else:
                                self.Label1.configure(text = "Δεν εισάγατε σωστό αριθμό τηλεφώνου.")
                                tk.messagebox.showerror(title = "Δεν έγινε σωστή εισαγωγή αριθμού τηλεφώνου.",
                                                message = "Προσοχή! Δώστε σωστό αριθμό τηλεφώνου \
για εύρεση αυτοκινήτου.")
                                self.Entry1112.delete(0, 'end')
                                self.Label155.configure(text = " ")
                                self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
                                self.Label2011.configure(text = " ")
                                self.Label2013.configure(text = " ")
                                self.Label10011.configure(text = " ")
                                self.Label10012.configure(text = " ")
                                self.Label1333.configure(text = "0.0€")
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
                if not myresult:
                    self._selected_subscription_id = None
                    self.Button7772.configure(state='disabled')
                    self.Button7773.configure(state='disabled')
                    return
                for x in myresult:
                    result = x
                # Επιλογή ιστορικής συνδρομής για την ίδια πινακίδα, χωρίς νέο widget.
                mycursor.execute("SELECT id,datestart,dateend FROM subscription "
                                 "WHERE placenumber=%s AND id>0 ORDER BY id DESC", (result[4],))
                history = mycursor.fetchall()
                if len(history) > 1:
                    from tkinter import simpledialog
                    info = "\n".join("#{}: {} έως {}".format(r[0], _date_display(r[1]),
                                        _date_display(r[2])) for r in history[:15])
                    choice = simpledialog.askinteger("Ιστορικό συνδρομών",
                        "Επιλέξτε αριθμό ID για προβολή/διόρθωση.\n"
                        "Άκυρο = νεότερη συνδρομή.\n\n" + info,
                        initialvalue=int(result[0]), parent=self.Frame3)
                    if choice is not None:
                        if choice not in [int(row[0]) for row in history]:
                            raise ValueError("Το ID δεν ανήκει στις συνδρομές της πινακίδας.")
                        mycursor.execute("SELECT * FROM subscription WHERE id=%s AND id>0", (choice,))
                        result = mycursor.fetchone()
                if result[4] != []:   
                    self.Entry1100.delete(0, 'end')
                else:
                    pass
                self.Entry1110.delete(0, 'end')
                self.Entry1111.delete(0, 'end')
                self.Entry1112.delete(0, 'end')

                # Όνομα
                self.Entry1110.insert(0, result[1])

                # Επίθετο
                self.Entry1111.insert(0, result[2])

                # Τηλέφωνο
                self.Entry1112.insert(0, result[3])

                # Πινακίδα
                self.Entry1100.insert(0, result[4])

                # Ευρωπαϊκή εμφάνιση: ημερομηνία και ώρα έναρξης / λήξης.
                startdaysubresult = _date_display(result[5])
                stopdaysubresult = _date_display(result[6])
                self.Label10011.configure(text = str(startdaysubresult) + "    " + str(result[7]))
                self.Label10012.configure(text = str(stopdaysubresult) + "    " + str(result[8]))

                # Μέρες συνδρομής
                self.Label2013.configure(text = result[9])

                # Κόστος
                self.Label1333.configure(text = str(result[10]) + "€")

                # Φ.Π.Α
                Myfpa = str(result[11])

                # Έλεγχος αν υπάρχει οποιαδήποτε ενεργή συνδρομή για την πινακίδα αυτή τη στιγμή.
                # Δεν αρκεί μόνο η πιο πρόσφατη εγγραφή: μπορεί να έχει προστεθεί μελλοντική
                # συνδρομή ενώ μια παλαιότερη παραμένει ακόμη ενεργή.
                sql = ("SELECT datestart, timestart, dateend, timeend "
                       "FROM subscription WHERE placenumber = %s AND id > 0")
                val = [(result[4])]
                mycursor.execute(sql, val)
                subscription_rows = mycursor.fetchall()
                time_now2 = datetime.datetime.now()
                subscription_active = False

                for subscription_row in subscription_rows:
                    try:
                        subdtimestart = _combine_mysql_datetime(subscription_row[0], subscription_row[1])
                        subdtimeend = _combine_mysql_datetime(subscription_row[2], subscription_row[3])
                        if subdtimestart <= time_now2 < subdtimeend:
                            subscription_active = True
                            break
                    except (TypeError, ValueError):
                        # Μη έγκυρη παλιά εγγραφή δεν πρέπει να ακυρώνει τον έλεγχο των υπόλοιπων.
                        continue

                self.Label2011.configure(text = "ΝΑΙ" if subscription_active else "ΟΧΙ")
                self._selected_subscription_id = int(result[0])
                self.Button7772.configure(state = 'normal' if int(result[0]) > 0 else 'disabled')
                self.Button7773.configure(state = 'normal' if int(result[0]) > 0 else 'disabled')
                self.Button7774.configure(state = 'normal')
                # Αν είχε αποτύχει η έκδοση PDF μετά το commit, η αναζήτηση
                # επαναδημιουργεί ΜΟΝΟ το παραστατικό, ποτέ νέα συνδρομή.
                if int(result[0]) > 0:
                    try:
                        pdf_path, image_path = parking_subscriptions.subscription_services.receipt_paths(
                            os.path.dirname(os.path.abspath(__file__)), result[4], int(result[0]))
                        if not pdf_path.is_file() or not image_path.is_file():
                            mycursor.execute('SELECT * FROM company WHERE id=1')
                            receipt_company = mycursor.fetchone()
                            if receipt_company is None:
                                raise ValueError('Λείπουν τα στοιχεία επιχείρησης για την επανέκδοση.')
                            parking_subscriptions.subscription_services.issue_receipt(
                                result, receipt_company, os.path.dirname(os.path.abspath(__file__)))
                            tk.messagebox.showinfo('Επανέκδοση συνδρομής',
                                'Το ελλείπον παραστατικό επανεκδόθηκε για το ID #{}.'.format(result[0]))
                    except Exception as reprint_error:
                        from parking_modules.receipt_safety import report_receipt_failure
                        report_receipt_failure(self, 'ΣΥΝΔΡΟΜΗ', int(result[0]), result[4], reprint_error)
            except Exception as exc:
                if firstname == "" and lastname == "" and phone == "" and placenumbersearchsub == "":
                    self.Label1.configure(text = "Δεν εισάγατε δεδομένα.")
                    tk.messagebox.showerror(title = "Δεν έγινε εισαγωγή δεδομένων.",
                            message = "Προσοχή! Πρέπει να εισάγετε δεδομένα για εύρεση συνδρομής.")
                    self.Entry1100.delete(0, 'end')
                    self.Entry1110.delete(0, 'end')
                    self.Entry1111.delete(0, 'end')
                    self.Entry1112.delete(0, 'end')
                    self.Label155.configure(text = " ")
                    self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
                    self.Label2011.configure(text = " ")
                    self.Label2013.configure(text = " ")
                    self.Label10011.configure(text = " ")
                    self.Label10012.configure(text = " ")
                    self.Label1333.configure(text = "0.0€")
                else:
                    tk.messagebox.showerror(title="Σφάλμα αναζήτησης συνδρομής",
                        message=str(exc))
                    self.Label1.configure(text="Σφάλμα αναζήτησης συνδρομής.")
            finally:
                if mycursor is not None:
                    try: mycursor.close()
                    except Exception: pass
                if cnx is not None:
                    try: cnx.close()
                    except Exception: pass

    def savesubcar():
        """Μοναδική συναλλαγή νέας συνδρομής με αποκλεισμό επικαλύψεων.

        Το commit ολοκληρώνεται πριν την έκδοση PDF, αλλά αποτυχία PDF
        αναφέρεται ως τέτοια — ποτέ ως αποτυχία SQL ή λόγος νέας εγγραφής.
        """
        global my_subdays_namess_out, subdaysDropdown, cal
        global mycursor, cnx
        global firstname, lastname, phone, placenumbersearchsub
        connection = cursor = None
        committed_id = None
        commit_started = False
        try:
            plate = self.Entry1100.get().strip().upper()
            firstname = self.Entry1110.get().strip() or '×××'
            lastname = self.Entry1111.get().strip() or '×××'
            phone = self.Entry1112.get().strip() or '0'
            # Το όνομα αρχείου παραστατικού πρέπει να μην περιέχει path separators.
            parking_subscriptions.subscription_services.receipt_paths(os.path.dirname(os.path.abspath(__file__)),
                                                                      plate, 1)
            if not re.fullmatch(r'[0-9]+', phone):
                raise ValueError('Ο αριθμός τηλεφώνου πρέπει να περιέχει μόνο ψηφία.')
            if not str(my_subdays_namess_out).isdigit() or int(my_subdays_namess_out) <= 0:
                raise ValueError('Επιλέξτε έγκυρη διάρκεια συνδρομής από τον τιμοκατάλογο.')
            days = int(my_subdays_namess_out)
            start_date = _european_date(cal.get_date())
            start_time = datetime.datetime.now().time().replace(microsecond=0)
            start = datetime.datetime.combine(start_date, start_time)
            end = start + datetime.timedelta(days=days)
            parking_subscriptions.subscription_services.check_period(start, end)
            connection = mysql.connector.connect(user=users, password=passwords,
                           host=hosts, database=base, connect_timeout=5)
            cursor = connection.cursor()
            connection.start_transaction()
            # Σταθερό row lock ώστε δύο instances να μην εισάγουν
            # παράλληλα επικαλυπτόμενες περιόδους της ίδιας πινακίδας.
            cursor.execute("SELECT id FROM company WHERE id=1 FOR UPDATE")
            if cursor.fetchone() is None:
                raise ValueError('Δεν υπάρχουν στοιχεία επιχείρησης (company.id=1).')
            cursor.execute("SELECT datestart,timestart,dateend,timeend FROM subscription "
                           "WHERE placenumber=%s AND id>0 FOR UPDATE", (plate,))
            if parking_subscriptions.subscription_services.has_overlap(start, end, cursor.fetchall()):
                raise ValueError('Η ζητούμενη περίοδος επικαλύπτει υπάρχουσα συνδρομή.')
            cursor.execute("SELECT paysub FROM costsub WHERE subdays=%s AND subdays>0 LIMIT 1", (days,))
            tariff = cursor.fetchone()
            if tariff is None:
                raise ValueError('Δεν υπάρχει τιμοκατάλογος για {} ημέρες.'.format(days))
            cursor.execute("SELECT costfpa FROM fpa WHERE id=1")
            vat = cursor.fetchone()
            if vat is None:
                raise ValueError('Δεν έχει οριστεί ΦΠΑ στη βάση.')
            gross = parking_subscriptions.subscription_services.gross_amount(tariff[0], vat[0])
            cursor.execute("INSERT INTO subscription(firstname,lastname,phone,placenumber,"
                           "datestart,dateend,timestart,timeend,costsub,cost,fpa,comments) "
                           "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           (firstname,lastname,phone,plate,start.date(),end.date(),
                            start.time(),end.time(),days,float(gross),int(vat[0]),''))
            committed_id = int(cursor.lastrowid)
            if committed_id <= 0:
                raise ValueError('Δεν εκδόθηκε έγκυρος αριθμός συνδρομής.')
            commit_started = True
            connection.commit()
        except Exception as exc:
            if connection is not None and committed_id is None:
                try: connection.rollback()
                except Exception: pass
            elif connection is not None:
                # Σε αμφιβολία για την κατάσταση COMMIT, αποφεύγουμε νέα εισαγωγή.
                try: connection.rollback()
                except Exception: pass
            if commit_started:
                self.Button7771.configure(state='disabled')
                self.Button7777.configure(state='normal')
                tk.messagebox.showerror(title='Αβέβαιη κατάσταση συναλλαγής',
                    message='Το COMMIT δεν επιβεβαιώθηκε για το ID #{}.\n'
                            'ΜΗΝ επαναλάβετε την καταχώριση. Ελέγξτε τη βάση '
                            'και αναζητήστε τη συνδρομή.\n{}'.format(committed_id,exc))
            else:
                tk.messagebox.showerror(title='Δεν έγινε εισαγωγή συνδρομής', message=str(exc))
            return
        finally:
            if cursor is not None:
                try: cursor.close()
                except Exception: pass
            if connection is not None:
                try: connection.close()
                except Exception: pass

        # Διαφορετικό στάδιο: δεν επιτρέπεται δεύτερο INSERT εάν αποτύχει το PDF.
        self.Button7771.configure(state='disabled')
        self.Button7777.configure(state='normal')
        try:
            # Νέα ανάγνωση της ακριβούς committed εγγραφής (ID, όχι τελευταία πινακίδα).
            connection = mysql.connector.connect(user=users,password=passwords,
                                host=hosts,database=base,connect_timeout=5)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM subscription WHERE id=%s", (committed_id,))
            record = cursor.fetchone()
            cursor.execute("SELECT * FROM company WHERE id=1")
            company = cursor.fetchone()
            if record is None or company is None:
                raise ValueError('Δεν βρέθηκαν τα δεδομένα για την επανέκδοση παραστατικού.')
            parking_subscriptions.subscription_services.issue_receipt(
                record, company, os.path.dirname(os.path.abspath(__file__)))
        except Exception as exc:
            from parking_modules.receipt_safety import report_receipt_failure
            report_receipt_failure(self, 'ΣΥΝΔΡΟΜΗ', committed_id, plate, exc)
            return
        finally:
            if cursor is not None:
                try: cursor.close()
                except Exception: pass
            if connection is not None:
                try: connection.close()
                except Exception: pass

        # Επαναφορά των ίδιων controls και της ίδιας γεωμετρίας UI.
        self._selected_subscription_id = None
        for entry in (self.Entry1100,self.Entry1110,self.Entry1111,self.Entry1112):
            entry.configure(state='normal')
            entry.delete(0,'end')
        for label in (self.Label2011,self.Label2013,self.Label10011,self.Label10012):
            label.configure(text=' ')
        self.Label1333.configure(text='0.0€')
        self.Label20133.configure(text=' ')
        self.Label20133.place_forget()
        cal.configure(state='normal')
        try:
            subdaysDropdown.destroy()
            style = ttk.Style()
            style.configure('TCombobox', foreground='blue')
            subdaysDropdown = ttk.Combobox(root, state='disable', style='TCombobox',
                font='Arial 16 bold',justify='center',width='3',values=my_subdays_names)
            subdaysDropdown.current(0)
            subdaysDropdown.bind('<<ComboboxSelected>>',subdaysSelection)
            subdaysDropdown.grid(padx=793,pady=175)
        except Exception:
            pass
        my_subdays_namess_out = 0
        tk.messagebox.showinfo('Συνδρομή',
            'Η συνδρομή #{} καταχωρίστηκε και το παραστατικό αποθηκεύτηκε.'.format(committed_id))

    def editsubcar():
        """Αλλαγή συγκεκριμένου ID με αναπροσαρμογή ποσού και έκδοση ενημερωμένου PDF."""
        from tkinter import simpledialog
        sub_id = getattr(self, '_selected_subscription_id', None)
        if sub_id is None:
            tk.messagebox.showwarning('Συνδρομή', 'Πρώτα αναζητήστε συγκεκριμένη συνδρομή.')
            return
        if int(sub_id) <= 0:
            tk.messagebox.showerror('Προστασία', 'Η αρχική εγγραφή id=0 δεν τροποποιείται.')
            return
        connection = cursor = None
        committed = False
        commit_started = False
        record = None
        try:
            connection = mysql.connector.connect(user=users,password=passwords,
                                host=hosts,database=base,connect_timeout=5)
            cursor = connection.cursor()
            connection.start_transaction()
            cursor.execute('SELECT id FROM company WHERE id=1 FOR UPDATE')
            if cursor.fetchone() is None:
                raise ValueError('Λείπει η εγγραφή επιχείρησης.')
            cursor.execute('SELECT * FROM subscription WHERE id=%s AND id>0 FOR UPDATE',(sub_id,))
            record = cursor.fetchone()
            if record is None:
                raise ValueError('Η συνδρομή δεν υπάρχει πλέον.')
            if not tk.messagebox.askyesno('Διόρθωση συνδρομής',
                    'Διόρθωση εγγραφής #{} για {};\nΤο αρχικό PDF θα αρχειοθετηθεί. Συνέχεια;'.format(sub_id,record[4])):
                return
            updates={}
            for label,index in [('Όνομα',1),('Επώνυμο',2),('Τηλέφωνο',3),('Πινακίδα',4)]:
                value=simpledialog.askstring('Διόρθωση #{}'.format(sub_id),label,
                              initialvalue=str(record[index]),parent=self.Frame3)
                if value is None: return
                value=value.strip().upper() if index==4 else value.strip()
                if not value: raise ValueError('Κενό πεδίο: '+label)
                if index==3 and not re.fullmatch(r'[0-9]+',value):
                    raise ValueError('Το τηλέφωνο πρέπει να περιέχει ψηφία.')
                if index==4:
                    parking_subscriptions.subscription_services.receipt_paths(
                        os.path.dirname(os.path.abspath(__file__)),value,1)
                updates[index]=value
            dates={}
            for label,index in [('Έναρξη (ΗΗ/ΜΜ/ΕΕΕΕ)',5),('Λήξη (ΗΗ/ΜΜ/ΕΕΕΕ)',6)]:
                value=simpledialog.askstring('Διόρθωση #{}'.format(sub_id),label,
                              initialvalue=_date_display(record[index]),parent=self.Frame3)
                if value is None:return
                dates[index]=_european_date(value)
            start=parking_subscriptions.subscription_services.as_datetime(dates[5],record[7])
            end=parking_subscriptions.subscription_services.as_datetime(dates[6],record[8])
            parking_subscriptions.subscription_services.check_period(start,end)
            # Οι ώρες δεν μεταβάλλονται στο υπάρχον UI. Μόνο πλήρεις ημερήσιες διάρκειες.
            if start.time()!=end.time():
                raise ValueError('Οι ώρες αρχής/λήξης δεν είναι ίδιες. Απαιτείται νέα συνδρομή.')
            days=(end.date()-start.date()).days
            if days<=0:
                raise ValueError('Η διάρκεια πρέπει να είναι τουλάχιστον μία ημέρα.')
            if days == int(record[9]):
                # Αλλαγή μόνο στοιχείων/περιόδου χωρίς αλλαγή διάρκειας:
                # δεν επανατιμολογείται παλιά πώληση με τον σημερινό τιμοκατάλογο.
                new_cost=parking_subscriptions.subscription_services.money(record[10])
            else:
                cursor.execute('SELECT paysub FROM costsub WHERE subdays=%s AND subdays>0 LIMIT 1',(days,))
                tariff=cursor.fetchone()
                if tariff is None:
                    raise ValueError('Δεν υπάρχει τιμή συνδρομής για {} ημέρες.'.format(days))
                new_cost=parking_subscriptions.subscription_services.gross_amount(tariff[0],record[11])
            cursor.execute('SELECT datestart,timestart,dateend,timeend FROM subscription '
                           'WHERE placenumber=%s AND id<>%s AND id>0 FOR UPDATE',(updates[4],sub_id))
            if parking_subscriptions.subscription_services.has_overlap(start,end,cursor.fetchall()):
                raise ValueError('Η νέα περίοδος επικαλύπτει άλλη συνδρομή της πινακίδας.')
            if not tk.messagebox.askyesno('Επιβεβαίωση διόρθωσης',
                'ID #{}\nΔιάρκεια: {} ημέρες\nΠαλαιό ποσό: {} €\nΝέο ποσό: {} €\n'
                'Η διόρθωση θα καταγραφεί. Αποθήκευση;'.format(sub_id,days,record[10],new_cost)):
                return
            trace='[Διόρθωση {}: διάρκεια {}→{}, ποσό {}→{}]'.format(
                datetime.datetime.now().strftime('%d/%m/%Y %H:%M'),record[9],days,record[10],new_cost)
            comments=(str(record[12] or '')+'\n'+trace).strip()
            cursor.execute('UPDATE subscription SET firstname=%s,lastname=%s,phone=%s,'
                           'placenumber=%s,datestart=%s,dateend=%s,costsub=%s,cost=%s,comments=%s '
                           'WHERE id=%s AND id>0',
                           (updates[1],updates[2],updates[3],updates[4],dates[5],dates[6],
                            days,float(new_cost),comments,sub_id))
            if cursor.rowcount != 1:
                raise ValueError('Η ενημέρωση δεν επηρέασε ακριβώς μία εγγραφή.')
            commit_started=True
            connection.commit()
            committed=True
        except Exception as exc:
            if commit_started:
                tk.messagebox.showerror('Αβέβαιη κατάσταση διόρθωσης',
                    'Δεν επιβεβαιώθηκε η συναλλαγή #{}. ΜΗΝ επαναλάβετε τη διόρθωση '
                    'χωρίς να ελέγξετε τη βάση.\n{}'.format(sub_id,exc))
            else:
                tk.messagebox.showerror('Σφάλμα διόρθωσης συνδρομής',str(exc))
            return
        finally:
            if not committed and connection is not None:
                try:connection.rollback()
                except Exception:pass
            if cursor is not None:
                try:cursor.close()
                except Exception:pass
            if connection is not None:
                try:connection.close()
                except Exception:pass
        # SQL committed. Re-issue, preserving the old PDF as an archive.
        try:
            connection=mysql.connector.connect(user=users,password=passwords,
                       host=hosts,database=base,connect_timeout=5)
            cursor=connection.cursor()
            cursor.execute('SELECT * FROM subscription WHERE id=%s',(sub_id,))
            changed=cursor.fetchone()
            cursor.execute('SELECT * FROM company WHERE id=1')
            company=cursor.fetchone()
            if not changed or not company:
                raise ValueError('Η ενημερωμένη εγγραφή δεν είναι διαθέσιμη.')
            if str(record[4]) != str(changed[4]):
                # Αρχειοθέτηση του προηγούμενου ονόματος αρχείου όταν άλλαξε η πινακίδα.
                import shutil
                old_pdf, old_png = parking_subscriptions.subscription_services.receipt_paths(
                    os.path.dirname(os.path.abspath(__file__)), record[4], int(sub_id))
                for old_file in (old_pdf, old_png):
                    if old_file.is_file():
                        archive=old_file.parent/'archive'
                        archive.mkdir(parents=True, exist_ok=True)
                        stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                        shutil.copy2(old_file, archive/(old_file.stem+'_'+stamp+old_file.suffix))
            parking_subscriptions.subscription_services.issue_receipt(
                changed,company,os.path.dirname(os.path.abspath(__file__)),archive_previous=True)
            tk.messagebox.showinfo('Συνδρομή','Η διόρθωση και το ενημερωμένο PDF αποθηκεύτηκαν.')
        except Exception as exc:
            from parking_modules.receipt_safety import report_receipt_failure
            report_receipt_failure(self,'ΔΙΟΡΘΩΣΗ ΣΥΝΔΡΟΜΗΣ',sub_id,record[4],exc)
        finally:
            if cursor is not None:
                try:cursor.close()
                except Exception:pass
            if connection is not None:
                try:connection.close()
                except Exception:pass
            self._selected_subscription_id=None
            self.Button7772.configure(state='disabled')
            self.Button7773.configure(state='disabled')

    def deletesubcar():
        """Διαγράφει ακριβώς το id που επιλέχθηκε, μετά από διπλή επιβεβαίωση."""
        sub_id = getattr(self, '_selected_subscription_id', None)
        if sub_id is None:
            tk.messagebox.showwarning("Συνδρομή", "Πρώτα αναζητήστε συγκεκριμένη συνδρομή.")
            return
        if int(sub_id) <= 0:
            tk.messagebox.showerror("Προστασία", "Η αρχική εγγραφή id=0 δεν διαγράφεται.")
            return
        connection = None
        cursor = None
        commit_started = False
        committed = False
        try:
            connection = mysql.connector.connect(user=users, password=passwords,
                         host=hosts, database=base, connect_timeout=5)
            connection.start_transaction()
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM company WHERE id=1 FOR UPDATE")
            if cursor.fetchone() is None:
                raise ValueError("Λείπει η εγγραφή επιχείρησης.")
            cursor.execute("SELECT placenumber,datestart,dateend FROM subscription WHERE id=%s AND id>0 FOR UPDATE", (sub_id,))
            record = cursor.fetchone()
            if record is None:
                raise ValueError("Η συνδρομή δεν υπάρχει πλέον.")
            if not tk.messagebox.askyesno("Διαγραφή συνδρομής",
                      "Διαγραφή εγγραφής #{} - {} ({} έως {});\n"
                      "Η διαγραφή μπορεί να επηρεάσει μελλοντικές χρεώσεις. Συνέχεια;".format(
                      sub_id, record[0],_date_display(record[1]),_date_display(record[2]))):
                connection.rollback()
                return
            if not tk.messagebox.askyesno("ΟΡΙΣΤΙΚΗ ΕΠΙΒΕΒΑΙΩΣΗ",
                      "Να διαγραφεί ΟΡΙΣΤΙΚΑ η συνδρομή #{};".format(sub_id)):
                connection.rollback()
                return
            cursor.execute("DELETE FROM subscription WHERE id=%s AND id>0", (sub_id,))
            if cursor.rowcount != 1:
                raise ValueError("Η διαγραφή δεν επηρέασε ακριβώς μία εγγραφή.")
            commit_started = True
            connection.commit()
            committed = True
            self._selected_subscription_id = None
            self.Button7772.configure(state='disabled')
            self.Button7773.configure(state='disabled')
            tk.messagebox.showinfo("Συνδρομή", "Η συνδρομή διαγράφηκε. Κάντε νέα αναζήτηση.")
        except Exception as exc:
            if connection and not committed:
                try: connection.rollback()
                except Exception: pass
            if commit_started and not committed:
                tk.messagebox.showerror("Αβέβαιη διαγραφή",
                    "Η κατάσταση της διαγραφής #{} δεν επιβεβαιώθηκε. "
                    "Ελέγξτε τη βάση πριν ξαναδοκιμάσετε.\n{}".format(sub_id,exc))
            elif not committed:
                tk.messagebox.showerror("Σφάλμα διαγραφής", str(exc))
            else:
                tk.messagebox.showerror("Ειδοποίηση διαγραφής", str(exc))
        finally:
            if cursor: cursor.close()
            if connection: connection.close()

    def startdaysubcar():
        global subdaysDropdown
        global my_subdays_names
        global my_subdays_namess
        global cal
        subdaysDropdown.destroy()
        self.Button7774.configure(state = "disabled")
        self.Button7777.configure(state = "disabled")
        self.Button7775.configure(state = "normal")
        style = ttk.Style()
        style.configure("TCombobox", foreground = "blue")
        subdaysDropdown = ttk.Combobox(root, state = "enable", style = "TCombobox", font = "Arial 16 bold", justify = "center", width = "3", values = my_subdays_names)
        subdaysDropdown.current(0)
        my_subdays_namess = subdaysDropdown.get()
        subdaysDropdown.bind("<<ComboboxSelected>>", subdaysSelection)
        subdaysDropdown.grid(padx = 793, pady = 175)
        self.Button7771.configure(state = "disabled")
        cal.configure(state = 'disabled')

    def endsubdaycar():
        global subdaysDropdown
        global my_subdays_namess
        global my_subdays_namess_out
        if not str(my_subdays_namess).isdigit() or int(my_subdays_namess) <= 0:
            self.Label1.configure(text = "Δεν εισάγατε αριθμό ημερών διάρκειας συνδρομής.")
            tk.messagebox.showerror(title = "Δεν έγινε εισαγωγή συνδρομής.",
                            message = "Προσοχή! Πρέπει να εισάγετε αριθμό ημερών διάρκειας συνδρομής.")
            self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
        else:    
            subdaysDropdown.destroy()
            self.Button7775.configure(state = "disabled")
            self.Label20133.place(relx = 0.684, rely = 0.212, height = 31, width = 57)
            self.Label20133.configure(text = str(my_subdays_namess))
            my_subdays_namess_out = my_subdays_namess
            my_subdays_namess = 0
            self.Button7771.configure(state = "normal")
            self.Entry1100.configure(state = "disabled")
            self.Entry1110.configure(state = "disabled")
            self.Entry1111.configure(state = "disabled")
            self.Entry1112.configure(state = "disabled")

    return {
        'subdaysSelection': subdaysSelection,
        'button3': button3,
        'searchsubcar': searchsubcar,
        'savesubcar': savesubcar,
        'editsubcar': editsubcar,
        'deletesubcar': deletesubcar,
        'startdaysubcar': startdaysubcar,
        'endsubdaycar': endsubdaycar,
    }
