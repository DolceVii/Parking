# -*- coding: utf-8 -*-
"""Στοιχεία MySQL μόνο στη μνήμη κατά τη διάρκεια της εκτέλεσης."""
import tkinter as tk
from getpass import getpass
import mysql.connector

MYSQL_HOST = "127.0.0.1"
MYSQL_DATABASE = "parking"
MYSQL_PORT = 3306
_session = None


def check_credentials(username, password):
    """Πραγματικός μη καταστροφικός έλεγχος σύνδεσης."""
    if not username or not password:
        raise ValueError("Συμπλήρωσε όνομα χρήστη και κωδικό.")
    db = None
    cur = None
    try:
        db = mysql.connector.connect(
            host=MYSQL_HOST, port=MYSQL_PORT, database=MYSQL_DATABASE,
            user=username, password=password, connection_timeout=5)
        cur = db.cursor()
        cur.execute("SELECT remaneplaces FROM places WHERE id = 1")
        if cur.fetchone() is None:
            raise ValueError("Δεν βρέθηκε η εγγραφή places.id = 1.")
    finally:
        if cur is not None:
            cur.close()
        if db is not None:
            db.close()


def _friendly_error(exc):
    if isinstance(exc, ValueError):
        return str(exc)
    if isinstance(exc, mysql.connector.Error):
        return {
            1045: "Λάθος όνομα χρήστη ή κωδικός MySQL.",
            1044: "Δεν επιτρέπεται η πρόσβαση στη βάση parking.",
            1049: "Δεν βρέθηκε η βάση parking.",
            1142: "Δεν υπάρχει δικαίωμα ανάγνωσης από τον πίνακα places.",
            2003: "Δεν υπάρχει σύνδεση με τη MySQL (127.0.0.1:3306).",
            2005: "Ο MySQL server δεν βρέθηκε.",
        }.get(getattr(exc, 'errno', None),
              "Σφάλμα MySQL (" + str(getattr(exc, 'errno', '?')) + ").")
    return "Αδυναμία ελέγχου σύνδεσης MySQL."


def prompt_login(root):
    """Παράθυρο σύνδεσης με την ίδια χρωματική ταυτότητα του Parking.

    Επιστρέφει (username, password) ή None. Δεν αποθηκεύει στοιχεία στον δίσκο.
    Το κυρίως GUI και η διαδικασία επαλήθευσης MySQL δεν τροποποιούνται.
    """
    # Χρώματα και αισθητική ίδια με το κύριο GUI (PAGE / Tkinter).
    background = "#8080ff"
    panel_color = "#c0c0c0"
    control_color = "#d9d9d9"
    title_color = "#000000"
    title_text_color = "#ffffff"
    header_red = "#f0001b"
    status_ok = "#80ff80"
    status_error = "#ff8080"
    status_busy = "#ffff80"

    dialog = tk.Toplevel(root)
    dialog.withdraw()  # Αποφεύγει την εμφάνιση σε λάθος θέση πριν από το κεντράρισμα.
    dialog.title("Project Parking — Σύνδεση χρήστη")
    dialog.resizable(False, False)
    dialog.configure(background=background)
    dialog.geometry("600x390")

    # Ίδιο εικονίδιο με το κεντρικό παράθυρο, όπου υποστηρίζεται.
    try:
        import os
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "p.ico")
        if os.path.isfile(icon_path):
            dialog.iconbitmap(icon_path)
    except (OSError, tk.TclError):
        pass

    result = [None]
    processing = [False]
    username = tk.StringVar(master=dialog)
    password = tk.StringVar(master=dialog)
    status = tk.StringVar(master=dialog, value="Συμπληρώστε τα στοιχεία σύνδεσης MySQL.")

    # Κόκκινη επάνω ζώνη, όπως η μπάρα του κυρίως Parking στα Windows.
    topbar = tk.Frame(dialog, background=header_red, height=43)
    topbar.pack(side="top", fill="x")
    topbar.pack_propagate(False)
    tk.Label(
        topbar, text="Πάρκινγκ  •  Σύνδεση χρήστη", background=header_red,
        foreground="white", font=("Rockwell Nova", 12, "bold"),
        anchor="w", padx=16
    ).pack(fill="both", expand=True)

    # Κεντρικό γκρίζο πλαίσιο: η ίδια σχεδίαση με τις καρτέλες του Parking.
    main = tk.Frame(dialog, background=panel_color, relief="raised", borderwidth=2)
    main.pack(side="top", fill="x", padx=20, pady=(17, 12))
    heading = tk.Label(
        main, text="Σύνδεση στη βάση δεδομένων", background=title_color,
        foreground=title_text_color, font=("Rockwell Nova", 16, "bold"),
        relief="raised", borderwidth=1, anchor="center"
    )
    heading.pack(fill="x", padx=14, pady=(13, 14), ipady=5)

    fields = tk.Frame(main, background=panel_color)
    fields.pack(fill="x", padx=23)
    fields.grid_columnconfigure(1, weight=1)
    label_font = ("Rockwell Nova", 12)
    entry_font = ("Segoe UI", 12)

    tk.Label(fields, text="Όνομα χρήστη:", background=panel_color,
             foreground="black", font=label_font, anchor="w").grid(
                 row=0, column=0, sticky="w", padx=(0, 16), pady=(0, 11))
    euser = tk.Entry(fields, textvariable=username, font=entry_font,
                     relief="sunken", borderwidth=2, width=27,
                     background="white", foreground="#000000")
    euser.grid(row=0, column=1, sticky="ew", pady=(0, 11), ipady=3)

    tk.Label(fields, text="Κωδικός:", background=panel_color,
             foreground="black", font=label_font, anchor="w").grid(
                 row=1, column=0, sticky="w", padx=(0, 16))
    epass = tk.Entry(fields, textvariable=password, font=entry_font,
                     relief="sunken", borderwidth=2, width=27,
                     background="white", foreground="#000000", show="*")
    epass.grid(row=1, column=1, sticky="ew", ipady=3)

    tk.Label(
        main, text=f"MySQL: {MYSQL_HOST}:{MYSQL_PORT}    |    Βάση: {MYSQL_DATABASE}",
        background=panel_color, foreground="#333333",
        font=("Segoe UI", 9), anchor="w"
    ).pack(fill="x", padx=25, pady=(13, 13))

    # Ενέργειες με τα ίδια ανάγλυφα, ανοιχτόχρωμα κουμπιά του κυρίως GUI.
    actions = tk.Frame(dialog, background=background)
    actions.pack(fill="x", padx=20, pady=(1, 12))
    actions.grid_columnconfigure(0, weight=1)
    actions.grid_columnconfigure(3, weight=1)

    def set_status(message, color):
        status.set(message)
        status_label.configure(background=color)

    def cancel():
        if processing[0]:
            return
        password.set("")
        dialog.destroy()

    def submit(event=None):
        if processing[0]:
            return
        processing[0] = True
        u, p = username.get().strip(), password.get()
        connect_button.configure(state="disabled")
        set_status("Έλεγχος σύνδεσης με τη MySQL...", status_busy)
        dialog.update_idletasks()
        try:
            check_credentials(u, p)
        except (mysql.connector.Error, ValueError, OSError) as exc:
            set_status(_friendly_error(exc), status_error)
            password.set("")
            epass.focus_set()
            processing[0] = False
            connect_button.configure(state="normal")
        except Exception:
            # Μη αναμενόμενο σφάλμα: δεν εμφανίζουμε δεδομένα σύνδεσης.
            set_status("Δεν ήταν δυνατός ο έλεγχος σύνδεσης στη MySQL.", status_error)
            password.set("")
            epass.focus_set()
            processing[0] = False
            connect_button.configure(state="normal")
        else:
            result[0] = (u, p)
            password.set("")
            dialog.destroy()

    button_font = ("Rockwell Nova", 12)
    connect_button = tk.Button(
        actions, text="Σύνδεση", command=submit, background=control_color,
        activebackground="#80dfbf", foreground="black", activeforeground="black",
        font=button_font, relief="raised", borderwidth=2,
        width=15, cursor="hand2", default="active"
    )
    connect_button.grid(row=0, column=1, padx=(0, 12), ipady=4)
    tk.Button(
        actions, text="Ακύρωση", command=cancel, background=control_color,
        activebackground=status_error, foreground="black", activeforeground="black",
        font=button_font, relief="raised", borderwidth=2,
        width=15, cursor="hand2"
    ).grid(row=0, column=2, ipady=4)

    # Κάτω μπάρα μηνυμάτων: ίδια λογική με την πράσινη ένδειξη κυρίως GUI.
    status_label = tk.Label(
        dialog, textvariable=status, background=status_ok,
        foreground="black", font=("Rockwell Nova", 10),
        relief="sunken", borderwidth=2, anchor="w", padx=10,
        wraplength=550
    )
    status_label.pack(side="bottom", fill="x", padx=20, pady=(0, 13), ipady=5)

    dialog.protocol("WM_DELETE_WINDOW", cancel)
    dialog.bind("<Return>", submit)
    dialog.bind("<Escape>", lambda event: cancel())
    dialog.update_idletasks()
    width, height = 600, 390
    x = max(0, (dialog.winfo_screenwidth() - width) // 2)
    y = max(0, (dialog.winfo_screenheight() - height) // 2)
    dialog.geometry(f"{width}x{height}+{x}+{y}")
    dialog.deiconify()
    dialog.grab_set()
    euser.focus_set()
    root.wait_window(dialog)
    return result[0]


def set_session(credentials):
    global _session
    if not credentials or len(credentials) != 2 or not all(credentials):
        raise ValueError("Δεν έχουν δοθεί στοιχεία MySQL.")
    _session = credentials


def get_session():
    if _session is None:
        raise RuntimeError("Απαιτείται είσοδος στη MySQL.")
    return _session


def has_session():
    return _session is not None


def clear_session():
    global _session
    _session = None


def console_connect():
    """Βοηθητικά CLI scripts: είσοδος σε κάθε εκτέλεση."""
    user = input('MySQL χρήστης: ').strip()
    passwd = getpass('MySQL κωδικός: ')
    check_credentials(user, passwd)
    return mysql.connector.connect(host=MYSQL_HOST, port=MYSQL_PORT,
                                   database=MYSQL_DATABASE, user=user,
                                   password=passwd, connection_timeout=5)


def gui_connect(root):
    """Παλιά βοηθητικά GUI scripts: ίδια φόρμα εισόδου."""
    credentials = prompt_login(root)
    if credentials is None:
        return None
    user, passwd = credentials
    return mysql.connector.connect(host=MYSQL_HOST, port=MYSQL_PORT,
                                   database=MYSQL_DATABASE, user=user,
                                   password=passwd, connection_timeout=5)
