"""Στατιστικά, γραφήματα και αναφορές."""

def create_handlers(self, top, handlers):
    """Επιστρέφει callbacks με κοινό περιβάλλον, χωρίς μεταβολή λογικής GUI."""

    def statsplot1():
        global passwords
        global users
        global hosts
        global base
        global placenumbersearch2
        global cnx
        global mycursor
        global myresult

        plt.style.use('Solarize_Light2') # Solarize_Light2, dark_background, seaborn-poster
        plt.figure(figsize=(12, 6))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
        plt.gca().yaxis.set_major_formatter(mdates.DateFormatter('%#H:%M:%S'))
        plt.gcf().autofmt_xdate()
        plt.xlabel('Ημέρες αρχής και λήξης συνδρομών οχήματος')
        plt.ylabel('Ώρες αρχής και λήξης συνδρομών οχήματος')
        plt.suptitle('Συνγκεντροτικός πίνακας συνδρομών του οχήματος: ' + placenumbersearch2)

        try:
            cnx = mysql.connector.connect(user = users,
                    password = passwords,
                    host = hosts,
                    database = base,
                    connect_timeout = 5)
            mycursor = cnx.cursor()
            
            sql = ("SELECT datestart, dateend, timestart, timeend FROM subscription WHERE placenumber = %s")
            val = [(placenumbersearch2)]
            mycursor.execute(sql, val)
            myresult = mycursor.fetchall()
            for x in myresult:
                suball = x
                x = [suball[0], suball[1]]
                y = [datetime.datetime.strptime(str(suball[2]), '%H:%M:%S'),datetime.datetime.strptime(str(suball[3]), '%H:%M:%S')]
                plt.plot(x, y, linewidth = 4.0)
            plt.autoscale(enable = True, axis = 'both', tight = True)
            #mng = plt.get_current_fig_manager()
            #mng.window.state("zoomed")
            plt.show()
        except Exception as exc:
            import traceback
            traceback.print_exc()
            self.Label1.configure(text="Πρόβλημα στη δημιουργία γραφήματος.")
            tk.messagebox.showerror(
                title="Σφάλμα στατιστικού γραφήματος",
                message="Δεν ήταν δυνατή η δημιουργία του γραφήματος.\n" + str(exc),
            )
            plt.close()
        finally:
            if 'mycursor' in locals():
                try:
                    mycursor.close()
                except Exception:
                    pass
            if 'cnx' in locals():
                try:
                    cnx.close()
                except Exception:
                    pass

    def statsplot2():
        global passwords
        global users
        global hosts
        global base
        global placenumbersearch2
        global l
        global m
        global cnx
        global mycursor
        global myresult
        l = 1
        m = 1

        plt.style.use('Solarize_Light2') # Solarize_Light2, dark_background, seaborn-poster
        plt.figure(figsize=(12, 6))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
        plt.gca().yaxis.set_major_formatter(mdates.DateFormatter('%#H:%M:%S'))
        plt.gcf().autofmt_xdate()
        plt.xlabel('Ημέρες εισόδων / εξόδων οχήματος')
        plt.ylabel('Ώρες εισόδων / εξόδων οχήματος')
        plt.suptitle('Συνγκεντροτικός πίνακας εισόδων / εξόδων οχήματος: ' + placenumbersearch2)

        try:
            cnx = mysql.connector.connect(user = users,
                    password = passwords,
                    host = hosts,
                    database = base,
                    connect_timeout = 5)
            mycursor = cnx.cursor()

            sql1 = ("SELECT datein, timein FROM inputcar WHERE placenumber = %s")
            val1 = [(placenumbersearch2)]
            mycursor.execute(sql1, val1)
            myresult1 = mycursor.fetchall()
            for x in myresult1:
                suball = x
                plt.text(suball[0], datetime.datetime.strptime(str(suball[1]), '%H:%M:%S'), ('Είσοδος ' + str(l)), ha = 'center')
                plt.scatter(suball[0], datetime.datetime.strptime(str(suball[1]), '%H:%M:%S'), linewidth = 4.0, color = "cyan")
                l = l + 1

            sql2 = ("SELECT dateout, timeout FROM outputcar WHERE placenumber = %s")
            val2 = [(placenumbersearch2)]
            mycursor.execute(sql2, val2)
            myresult2 = mycursor.fetchall()
            for i in myresult2:
                suballs = i
                plt.text(suballs[0], datetime.datetime.strptime(str(suballs[1]), '%H:%M:%S'), ('Έξοδος ' + str(m)), ha = 'center')
                plt.scatter(suballs[0], datetime.datetime.strptime(str(suballs[1]), '%H:%M:%S'), linewidth = 4.0, color = "orange")
                m = m + 1

            plt.autoscale(enable = True, axis = 'both', tight = True)
            #mng = plt.get_current_fig_manager()
            #mng.window.state("zoomed")
            plt.show()
        except Exception as exc:
            import traceback
            traceback.print_exc()
            self.Label1.configure(text="Πρόβλημα στη δημιουργία γραφήματος.")
            tk.messagebox.showerror(
                title="Σφάλμα στατιστικού γραφήματος",
                message="Δεν ήταν δυνατή η δημιουργία του γραφήματος.\n" + str(exc),
            )
            plt.close()
        finally:
            if 'mycursor' in locals():
                try:
                    mycursor.close()
                except Exception:
                    pass
            if 'cnx' in locals():
                try:
                    cnx.close()
                except Exception:
                    pass

    def printresult():
        """Εξαγωγή όλων των εισόδων/εξόδων από τους ίδιους πίνακες με το Ευρετήριο."""
        global passwords, users, hosts, base, placenumbersearch2
        global pagepdf, writeover3

        writeover3 = 530
        pagepdf = 1
        plate = str(placenumbersearch2).strip().upper()
        safe_plate = re.sub(r"[^A-Za-z0-9_-]", "_", plate)
        stats_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "STATs")
        os.makedirs(stats_dir, exist_ok=True)

        def date_text(value):
            if hasattr(value, "strftime"):
                return value.strftime("%d/%m/%Y")
            try:
                return datetime.date.fromisoformat(str(value)).strftime("%d/%m/%Y")
            except (TypeError, ValueError):
                return str(value)

        def time_text(value):
            if isinstance(value, datetime.timedelta):
                sec = int(value.total_seconds())
                if 0 <= sec < 24 * 3600:
                    hours, rest = divmod(sec, 3600)
                    minutes, seconds = divmod(rest, 60)
                    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            if hasattr(value, "strftime"):
                return value.strftime("%H:%M:%S")
            return str(value)

        def mysql_datetime(date_value, time_value):
            """Για ασφαλή αντιστοίχιση επαναλαμβανόμενων εισιτηρίων."""
            try:
                raw_time = time_text(time_value)
                raw_date = date_text(date_value)
                return datetime.datetime.strptime(raw_date + " " + raw_time,
                                                  "%d/%m/%Y %H:%M:%S")
            except (TypeError, ValueError):
                return None

        def money_text(value):
            try:
                return ("%.2f" % float(value)).replace(".", ",") + " €"
            except (TypeError, ValueError):
                return "-" if value is None else str(value) + " €"

        def heading(pdf, number):
            pdf.setFont("Arial", 11)
            pdf.drawString(15, 806, "Συγκεντρωτικά στοιχεία εισόδου / εξόδου: " + plate)
            pdf.setFont("Arial", 9)
            pdf.drawString(20, 780, "Πινακίδα / Ticket")
            pdf.drawString(130, 780, "Ημερομηνία και ώρα εισόδου")
            pdf.drawString(325, 780, "Ημερομηνία και ώρα εξόδου")
            pdf.drawString(550, 780, "Κόστος")
            pdf.line(20, 772, 592, 772)
            pdf.drawString(15, 30, "Σελίδα " + str(number))
            return 755

        connection = None
        cursor = None
        try:
            connection = mysql.connector.connect(
                user=users, password=passwords, host=hosts,
                database=base, connect_timeout=5,
            )
            cursor = connection.cursor()

            # Τα ίδια πραγματικά πεδία που καταχωρίζουν οι saveandprint()/saveoutreceipt().
            # ΔΕΝ φιλτράρουμε τις εξόδους με βάση ticket ή το flag isout:
            # διαφορετικά μια καταχωρισμένη έξοδος μπορεί να εξαφανιστεί από το PDF.
            # Το TRIM/UPPER καλύπτει τυχόν παλιά δεδομένα με κενά/μικρά γράμματα.
            cursor.execute(
                "SELECT inputnumber, ticketnumber, datein, timein, isout "
                "FROM inputcar WHERE UPPER(TRIM(placenumber)) = %s "
                "AND inputnumber > 0 ORDER BY datein, timein, inputnumber",
                (plate,),
            )
            entrances = cursor.fetchall()
            cursor.execute(
                "SELECT id, ticketnumber, dateout, timeout, pay "
                "FROM outputcar WHERE UPPER(TRIM(placenumber)) = %s "
                "AND id > 0 ORDER BY dateout, timeout, id",
                (plate,),
            )
            departures = cursor.fetchall()

            # Η σύνδεση γίνεται μόνο για παρουσίαση, δεν αλλάζει τίποτα στη MySQL.
            # Σε περίπτωση επαναχρησιμοποίησης ticket από παλιά δεδομένα,
            # χρησιμοποιούμε αποκλειστικά έξοδο μετά την αντίστοιχη είσοδο.
            used_output_ids = set()
            records = []
            for input_id, ticket, date_in, time_in, is_out in entrances:
                in_dt = mysql_datetime(date_in, time_in)
                valid = []
                for exit_row in departures:
                    exit_id, exit_ticket, date_out, time_out, amount = exit_row
                    if exit_id in used_output_ids or exit_ticket != ticket:
                        continue
                    out_dt = mysql_datetime(date_out, time_out)
                    if in_dt is not None and out_dt is not None and out_dt < in_dt:
                        continue
                    valid.append(exit_row)
                if valid:
                    matched = valid[0]  # ORDER BY dateout, timeout, id
                    used_output_ids.add(matched[0])
                    records.append((ticket, date_in, time_in,
                                    matched[2], matched[3], matched[4], "OK"))
                else:
                    state = "MISSING_EXIT" if int(is_out) == 1 else "STILL_IN_DB"
                    records.append((ticket, date_in, time_in, None, None, None, state))

            # Ακόμη και με λάθος ticket, η πραγματική έξοδος εμφανίζεται
            # αυτούσια, σε ξεχωριστή γραμμή και με ένδειξη ασυμφωνίας.
            for exit_id, ticket, date_out, time_out, amount in departures:
                if exit_id not in used_output_ids:
                    records.append((ticket, None, None, date_out, time_out,
                                    amount, "UNMATCHED_EXIT"))

            # Το παλιό σταθερό PDF μπορεί να είναι ανοιχτό στον PDF viewer.
            # Νέο όνομα σε κάθε εκτύπωση: δεν γίνεται ποτέ προβολή παλιού PDF.
            stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            fresh_filename = os.path.join(
                stats_dir, "PrintResult_" + safe_plate + "_" + stamp + ".pdf")
            legacy_filename = os.path.join(stats_dir, "PrintResult_" + safe_plate + ".pdf")
            pdf = canvas.Canvas(fresh_filename)
            page_number = 1
            y = heading(pdf, page_number)
            if not records:
                pdf.setFont("Arial", 10)
                pdf.drawString(20, y, "Δεν υπάρχουν κινήσεις για την πινακίδα.")
            for ticket, d_in, t_in, d_out, t_out, amount, status in records:
                height = 27 if status == "UNMATCHED_EXIT" else 18
                if y - height < 65:
                    pdf.showPage()
                    page_number += 1
                    y = heading(pdf, page_number)
                pdf.setFont("Arial", 8.5)
                pdf.drawString(20, y, plate + "  #" + str(ticket))
                in_label = (date_text(d_in) + "  " + time_text(t_in)) if d_in is not None else "-"
                pdf.drawString(130, y, in_label)
                if status in ("OK", "UNMATCHED_EXIT"):
                    exit_label = date_text(d_out) + "  " + time_text(t_out)
                    cost_label = money_text(amount)
                elif status == "MISSING_EXIT":
                    exit_label = "ΛΕΙΠΕΙ ΕΓΓΡΑΦΗ ΕΞΟΔΟΥ"
                    cost_label = "-"
                else:
                    exit_label = "ΣΤΗ ΒΑΣΗ: ΕΝΤΟΣ PARKING"
                    cost_label = "-"
                pdf.drawString(325, y, exit_label)
                pdf.drawRightString(590, y, cost_label)
                if status == "UNMATCHED_EXIT":
                    pdf.setFont("Arial", 7.5)
                    pdf.drawString(130, y - 11,
                                   "ΕΞΟΔΟΣ ΧΩΡΙΣ ΑΝΤΙΣΤΟΙΧΙΣΜΕΝΗ ΕΙΣΟΔΟ - ελέγξτε το ticket")
                y -= height
            pdf.save()

            # Συμβατότητα με το παλιό σταθερό όνομα αρχείου.
            # Αν είναι κλειδωμένο από PDFGear, το νέο PDF παραμένει άθικτο.
            import shutil
            try:
                shutil.copyfile(fresh_filename, legacy_filename)
            except OSError as copy_error:
                import logging
                logging.warning("Δεν ενημερώθηκε το παλιό PDF %s: %s",
                                legacy_filename, copy_error)
            self.Label1.configure(text="Νέα αναφορά: " + os.path.basename(fresh_filename))

            # Στα Windows, το κουμπί ανοίγει ακριβώς το νέο PDF και όχι
            # την παλιότερη έκδοση που μπορεί να διατηρεί στη μνήμη ο viewer.
            if top is not None and os.name == "nt":
                try:
                    os.startfile(fresh_filename)
                except OSError as open_error:
                    import logging
                    logging.warning("Δεν άνοιξε το νέο PDF: %s", open_error)
        except Exception as exc:
            import traceback
            traceback.print_exc()
            self.Label1.configure(text="Πρόβλημα στην εκτύπωση.")
            tk.messagebox.showerror(
                title="Σφάλμα αναφοράς εισόδων/εξόδων",
                message="Αποτυχία δημιουργίας PDF ιστορικού οχήματος.\n" + str(exc),
            )
        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass
            if connection is not None:
                try:
                    connection.close()
                except Exception:
                    pass

        # Read Συνδρομές SQL
        # Συνδρομές και Κόστος
        sub_connection = None
        sub_cursor = None
        try:
            stats_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "STATs")
            os.makedirs(stats_dir, exist_ok=True)
            safe_plate = re.sub(r"[^A-Za-z0-9_-]", "_", str(placenumbersearch2))
            pagepdf = 1
            sub_connection = mysql.connector.connect(user = users,
                    password = passwords,
                    host = hosts,
                    database = base,
                    connect_timeout = 5)
            sub_cursor = sub_connection.cursor()

            c = canvas.Canvas(os.path.join(stats_dir, "PrintSub_" + safe_plate + ".pdf"), pagesize = landscape(letter))
            c.setFont('Arial', 12)
            c.drawString(15, 570, "Συγκεντρωτικά στατιστικά στοιχεία συνδρομών για το όχημα: " + placenumbersearch2)
            c.drawString(15, 550, "   Πινακίδα   " + "         Ονοματεπώνυμο         " + \
                         "      Τηλέφωνο      " + "        Ημερομηνία αρχής       " + \
                         "        Ημερομηνία λήξης        " + "    Ημέρες    "  + "    Κόστος    ")
            c.drawString(15, 20, "Σελίδα " + str(pagepdf))

            sql = ("SELECT firstname, lastname, phone, datestart, timestart, dateend, timeend, costsub, cost FROM subscription WHERE placenumber = %s")
            val = [(placenumbersearch2)]
            sub_cursor.execute(sql, val)
            myresult = sub_cursor.fetchall()
            for s in myresult:
                subscriptions = s
                c.drawString(15, writeover3, "  " + placenumbersearch2 + "        " + str(subscriptions[0]) + "  " + \
                             str(subscriptions[1]) + "          " + str(subscriptions[2]) + "          " + \
                             str((subscriptions[3]).strftime('%d/%m/%Y')) + "  " + str(subscriptions[4]) + "            " + \
                             str((subscriptions[5]).strftime('%d/%m/%Y')) + "  " + str(subscriptions[6]) + "               " + \
                             str(subscriptions[7]) + "               " + str(subscriptions[8]) + "€")
                writeover3 = writeover3 - 11

                if writeover3 < 40:
                    c.showPage()
                    c.setFont('Arial', 12)
                    writeover3 = 529
                    c.drawString(15, 550, "   Πινακίδα   " + "         Ονοματεπώνυμο         " + \
                         "      Τηλέφωνο      " + "        Ημερομηνία αρχής       " + \
                         "        Ημερομηνία λήξης        " + "    Ημέρες    "  + "    Κόστος    ")
                    pagepdf = pagepdf + 1
                    c.drawString(15, 20, "Σελίδα " + str(pagepdf))
                else:
                    pass
            c.save()

        except Exception as exc:
            import traceback
            traceback.print_exc()
            self.Label1.configure(text = "Πρόβλημα στην εκτύπωση.")
            tk.messagebox.showinfo(title = "Δημιουργήθηκε πρόβλημα στην εκτύπωση.",
                                        message = "Δημιουργήθηκε πρόβλημα στην εκτύπωση στατιστικών συνδρομών του οχήματος.\n" + str(exc))
        finally:
            if sub_cursor is not None:
                try:
                    sub_cursor.close()
                except Exception:
                    pass
            if sub_connection is not None:
                try:
                    sub_connection.close()
                except Exception:
                    pass

    def opensub():
        global passwords
        global users
        global hosts
        global base
        global listboxresult
        global countcarssub
        global cnx
        global mycursor
        global myresult
        countcarssub = 0

        try:
            cnx = mysql.connector.connect(user = users,
                    password = passwords,
                    host = hosts,
                    database = base,
                    connect_timeout = 5)
            mycursor = cnx.cursor()

            listboxresult.delete(0, 'end')
            self.EntryS1.delete(0, 'end')

            # local time
            timenow = datetime.datetime.now()

            # Ενεργή συνδρομή = η τρέχουσα ώρα βρίσκεται ανάμεσα στην έναρξη και τη λήξη
            # της ΙΔΙΑΣ εγγραφής συνδρομής.
            sql = ("SELECT datestart, timestart, dateend, timeend, placenumber FROM subscription")
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            for datesub in myresult:
                try:
                    datestart_active = _combine_mysql_datetime(datesub[0], datesub[1])
                    dateend_active = _combine_mysql_datetime(datesub[2], datesub[3])
                    if datestart_active <= timenow <= dateend_active:
                        countcarssub = countcarssub + 1
                        listboxresult.insert(END, "Το όχημα με αριθμό πινακίδας: " + str(datesub[4]) + " είναι σε συνδρομή.")
                except (TypeError, ValueError):
                    pass

            listboxresult.insert(END, "")
            listboxresult.insert(END, "--------------------------------------------------------------------")
            listboxresult.insert(END, " Σύνολο οχημάτων σε συνδρομή αυτήν την ώρα: " + str(countcarssub))
            self.Buttonplot1.configure(state = "disabled")
            self.Buttonplot2.configure(state = "disabled")
            self.Buttonresults.configure(state = "disabled")
        except:
            self.Label1.configure(text = "Πρόβλημα στην βάση.")
            tk.messagebox.showinfo(title = "Δημιουργήθηκε πρόβλημα στην βάση.",
                                message = "Δημιουργήθηκε πρόβλημα στην βάση στατιστικών.")
            time.sleep(1)
            self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
            self.Buttonplot1.configure(state = "disabled")
            self.Buttonplot2.configure(state = "disabled")
            self.Buttonresults.configure(state = "disabled")

    def openpark():
        global passwords
        global users
        global hosts
        global base
        global listboxresult
        global countcars
        global cnx
        global mycursor
        global myresult
        countcars = 0

        try:
            cnx = mysql.connector.connect(user = users,
                    password = passwords,
                    host = hosts,
                    database = base,
                    connect_timeout = 5)
            mycursor = cnx.cursor()

            listboxresult.delete(0, 'end')
            self.EntryS1.delete(0, 'end')

            sql = ("SELECT placenumber FROM inputcar WHERE isout = 0")
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            for x in myresult:
                carsinpark = x
                countcars = countcars + 1
                carsinpark = str(carsinpark)
                carsinpark = carsinpark.replace("('", "").replace("',)", "")
                listboxresult.insert(END, "Το όχημα με αριθμό πινακίδας: " + str(carsinpark) + " είναι στο πάρκινγκ.")
            listboxresult.insert(END, "")
            listboxresult.insert(END, "----------------------------------------------------------------------------")
            listboxresult.insert(END, " Σύνολο οχημάτων μέσα στο πάρκινγκ αυτήν την ώρα: " + str(countcars))
            self.Buttonplot1.configure(state = "disabled")
            self.Buttonplot2.configure(state = "disabled")
            self.Buttonresults.configure(state = "disabled")
        except:
            self.Label1.configure(text = "Πρόβλημα στην βάση.")
            tk.messagebox.showinfo(title = "Δημιουργήθηκε πρόβλημα στην βάση.",
                                message = "Δημιουργήθηκε πρόβλημα στην βάση στατιστικών.")
            time.sleep(1)
            self.Label1.configure(text = "Το σύστημα είναι έτοιμο.")
            self.Buttonplot1.configure(state = "disabled")
            self.Buttonplot2.configure(state = "disabled")
            self.Buttonresults.configure(state = "disabled")

    return {
        'statsplot1': statsplot1,
        'statsplot2': statsplot2,
        'printresult': printresult,
        'opensub': opensub,
        'openpark': openpark,
    }
