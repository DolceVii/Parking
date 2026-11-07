# -*- coding: utf-8 -*-
"""Ενιαία modal παράθυρα στο οπτικό ύφος του Project Parking.

Διατηρούν τα API/τιμές επιστροφής των tkinter.messagebox και
 tkinter.simpledialog, ώστε οι υπάρχοντες handlers να μη μεταβληθούν.
Δεν μεταβάλλουν κανένα widget του κύριου GUI.
"""

import os
import tkinter as tk
from tkinter import messagebox, simpledialog

# Κοινή παλέτα με το κύριο Parking και τη φόρμα εισόδου MySQL.
BACKGROUND = "#8080ff"
PANEL = "#c0c0c0"
CONTROL = "#d9d9d9"
RED = "#f0001b"
BLACK = "#000000"
GREEN = "#80ff80"
ERROR = "#ff8080"
YELLOW = "#ffff80"

_originals = {}
_root = None


def _parent_of(requested=None):
    """Γονικό παράθυρο: προηγείται το ενεργό modal/παράθυρο εργασίας."""
    parent = requested
    if parent is not None:
        try:
            if parent.winfo_exists():
                return parent.winfo_toplevel()
        except (AttributeError, tk.TclError):
            pass

    base = _root
    if base is None:
        return None
    try:
        if not base.winfo_exists():
            return None
        focused = base.focus_get()
        if focused is not None and focused.winfo_exists():
            return focused.winfo_toplevel()
        return base
    except tk.TclError:
        return None


def _modal(title, message, *, parent=None, kind="info", initialvalue=None,
           value_type=None, minvalue=None, maxvalue=None, show=None):
    """Κοινός μηχανισμός για πληροφορίες, ερωτήσεις και εισαγωγή τιμών."""
    owner = _parent_of(parent)
    if owner is None:
        raise tk.TclError("Δεν υπάρχει ενεργό παράθυρο Tkinter")

    title = str(title or "Ειδοποίηση")
    message = str(message or "")
    is_input = value_type is not None
    is_question = kind in ("yesno", "yesnocancel", "okcancel", "retrycancel", "question")
    default_result = None if is_input or kind == "yesnocancel" else (
        "no" if kind == "question" else False if is_question else "ok")
    answer = [default_result]
    finished = [False]

    dialog = tk.Toplevel(owner)
    dialog.withdraw()  # Τοποθέτηση πριν εμφανιστεί, χωρίς αναλαμπές στην οθόνη.
    dialog.title("Πάρκινγκ - " + title)
    dialog.configure(background=BACKGROUND)
    dialog.resizable(False, False)
    try:
        icon = os.path.join(os.path.dirname(os.path.dirname(__file__)), "p.ico")
        if os.path.isfile(icon):
            dialog.iconbitmap(icon)
    except (OSError, tk.TclError):
        pass

    # Η κόκκινη ζώνη και τα ανάγλυφα πλαίσια είναι ίδιας αισθητικής με το Parking.
    header = tk.Frame(dialog, background=RED, height=38)
    header.pack(side="top", fill="x")
    header.pack_propagate(False)
    tk.Label(header, text="Πάρκινγκ  •  " + title,
             background=RED, foreground="white", anchor="w",
             font=("Rockwell Nova", 11, "bold"), padx=14).pack(fill="both", expand=True)

    panel = tk.Frame(dialog, background=PANEL, relief="raised", borderwidth=2)
    panel.pack(side="top", fill="both", expand=True, padx=15, pady=(13, 11))

    kind_title = "Επεξεργασία στοιχείων" if is_input else {
        "error": "Σφάλμα", "warning": "Προειδοποίηση",
        "info": "Πληροφορία", "yesno": "Επιβεβαίωση",
        "yesnocancel": "Επιβεβαίωση", "question": "Ερώτηση",
        "okcancel": "Επιβεβαίωση", "retrycancel": "Επανάληψη",
    }.get(kind, "Ειδοποίηση")
    tk.Label(panel, text=kind_title, background=BLACK, foreground="white",
             font=("Rockwell Nova", 14, "bold"), anchor="center",
             relief="raised", borderwidth=1).pack(fill="x", padx=13,
                                                   pady=(12, 10), ipady=3)
    inner = tk.Frame(panel, background=PANEL)
    inner.pack(fill="both", expand=True, padx=16, pady=(0, 13))

    # Μακριές περιγραφές / ιστορικό συνδρομών χωρίς κομμένο περιεχόμενο.
    lines = message.splitlines() or [""]
    maxlen = max(map(len, lines))
    long_text = len(lines) > 7 or len(message) > 490
    if long_text:
        area = tk.Frame(inner, background=PANEL)
        area.pack(fill="both", expand=True)
        height = min(12, max(4, len(lines)))
        text = tk.Text(area, font=("Rockwell Nova", 11), background=PANEL,
                       foreground="black", relief="flat", highlightthickness=0,
                       height=height, width=64, wrap="word", cursor="arrow")
        bar = tk.Scrollbar(area, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=bar.set)
        text.insert("1.0", message)
        text.configure(state="disabled")
        text.pack(side="left", fill="both", expand=True)
        bar.pack(side="right", fill="y")
    else:
        symbol = "✎" if is_input else {"error": "×", "warning": "!", "info": "i",
                  "yesno": "?", "question": "?", "yesnocancel": "?",
                  "okcancel": "?", "retrycancel": "?"}.get(kind, "i")
        row = tk.Frame(inner, background=PANEL)
        row.pack(fill="x")
        tk.Label(row, text=symbol, background=RED if kind == "error" else BACKGROUND,
                 foreground="white", font=("Rockwell Nova", 15, "bold"),
                 width=3, relief="raised", borderwidth=1).pack(side="left", anchor="n",
                                                               padx=(0, 12), pady=(0, 3))
        label = tk.Label(row, text=message, background=PANEL, foreground="black",
                         justify="left", anchor="w", wraplength=475,
                         font=("Rockwell Nova", 11))
        label.pack(side="left", fill="both", expand=True)

    variable = None
    entry = None
    status = tk.StringVar(master=dialog, value="")
    if is_input:
        variable = tk.StringVar(master=dialog, value="" if initialvalue is None else str(initialvalue))
        entry = tk.Entry(inner, textvariable=variable, background="white",
                         foreground="black", relief="sunken", borderwidth=2,
                         font=("Segoe UI", 12), show=show or "", width=48)
        entry.pack(fill="x", pady=(12, 4), ipady=3)
        tk.Label(inner, textvariable=status, background=PANEL, foreground="#9b0019",
                 anchor="w", font=("Segoe UI", 9), wraplength=500).pack(fill="x")

    actions = tk.Frame(dialog, background=BACKGROUND)
    actions.pack(side="bottom", fill="x", padx=15, pady=(0, 14))
    buttons = tk.Frame(actions, background=BACKGROUND)
    buttons.pack(anchor="center")

    def finish(value):
        if finished[0]:
            return
        finished[0] = True
        answer[0] = value
        try:
            dialog.grab_release()
        except tk.TclError:
            pass
        dialog.destroy()

    def cancel(event=None):
        finish(default_result)

    def submit(event=None):
        if not is_input:
            finish("ok")
            return
        raw = variable.get().strip() if value_type != "string" else variable.get()
        try:
            if value_type == "integer":
                value = int(raw)
            elif value_type == "float":
                value = float(raw)
            else:
                value = raw
            if minvalue is not None and value < minvalue:
                raise ValueError("Η τιμή πρέπει να είναι ≥ {}.".format(minvalue))
            if maxvalue is not None and value > maxvalue:
                raise ValueError("Η τιμή πρέπει να είναι ≤ {}.".format(maxvalue))
        except (TypeError, ValueError) as exc:
            status.set(str(exc) if str(exc).startswith("Η τιμή") else
                       "Πληκτρολογήστε έγκυρο αριθμό.")
            entry.focus_set()
            entry.selection_range(0, "end")
            return
        finish(value)

    def add_button(text, value, *, primary=False):
        tk.Button(buttons, text=text, command=lambda: finish(value),
                  background=CONTROL, foreground="black", relief="raised",
                  activebackground=GREEN if primary else ERROR,
                  font=("Rockwell Nova", 11), borderwidth=2, width=13,
                  cursor="hand2", default="active" if primary else "normal"
                  ).pack(side="left", padx=6, ipady=3)

    if is_input:
        tk.Button(buttons, text="OK", command=submit, background=CONTROL,
                  relief="raised", borderwidth=2, width=13,
                  activebackground=GREEN, cursor="hand2",
                  font=("Rockwell Nova", 11), default="active").pack(side="left", padx=6, ipady=3)
        add_button("Ακύρωση", None)
    elif kind in ("yesno", "question", "yesnocancel"):
        add_button("Ναι", "yes" if kind == "question" else True, primary=True)
        add_button("Όχι", "no" if kind == "question" else False)
        if kind == "yesnocancel":
            add_button("Ακύρωση", None)
    elif kind == "okcancel":
        add_button("OK", True, primary=True)
        add_button("Ακύρωση", False)
    elif kind == "retrycancel":
        add_button("Επανάληψη", True, primary=True)
        add_button("Ακύρωση", False)
    else:
        add_button("OK", "ok", primary=True)

    # Στο messagebox το Enter επιβεβαιώνει την προεπιλεγμένη ενέργεια.
    if is_input:
        dialog.bind("<Return>", submit)
    elif kind in ("yesno", "question", "yesnocancel", "okcancel", "retrycancel"):
        positive = "yes" if kind == "question" else True
        dialog.bind("<Return>", lambda event: finish(positive))
    else:
        dialog.bind("<Return>", lambda event: finish("ok"))
    dialog.bind("<Escape>", cancel)
    dialog.protocol("WM_DELETE_WINDOW", cancel)

    dialog.update_idletasks()
    width = max(390, min(690, max(dialog.winfo_reqwidth(), 480)))
    height = max(215, min(650, dialog.winfo_reqheight()))
    try:
        # Κεντράρισμα πάνω στο ενεργό παράθυρο και όχι στην οθόνη Windows.
        owner.update_idletasks()
        px, py = owner.winfo_rootx(), owner.winfo_rooty()
        pw, ph = owner.winfo_width(), owner.winfo_height()
        if pw <= 1 or ph <= 1:
            raise ValueError
        x = px + (pw - width) // 2
        y = py + (ph - height) // 2
    except (ValueError, tk.TclError):
        x = (dialog.winfo_screenwidth() - width) // 2
        y = (dialog.winfo_screenheight() - height) // 2
    x = max(0, min(x, dialog.winfo_screenwidth() - width))
    y = max(0, min(y, dialog.winfo_screenheight() - height))
    dialog.geometry("{}x{}+{}+{}".format(width, height, x, y))
    try:
        dialog.transient(owner)
    except tk.TclError:
        pass
    dialog.deiconify()
    dialog.lift()
    previous_grab = dialog.grab_current()
    dialog.grab_set()
    if entry is not None:
        entry.focus_set()
        entry.selection_range(0, "end")
    else:
        dialog.focus_set()
    try:
        dialog.wait_window()
    finally:
        # Αν εμφανίστηκε δεύτερο modal πάνω από ήδη ενεργό, επαναφορά grab.
        try:
            if previous_grab is not None and previous_grab.winfo_exists():
                previous_grab.grab_set()
        except tk.TclError:
            pass
    return answer[0]


def _message_wrapper(kind):
    def invoke(title=None, message=None, **options):
        parent = options.pop("parent", None)
        # Διατηρούμε το standard API. Οι ανυποστήρικτες από το style
        # παράμετροι (icon/default/detail) δεν επηρεάζουν την επιστροφή.
        detail = options.pop("detail", None)
        if detail:
            message = "{}\n\n{}".format(message or "", detail)
        # Προστασία για χρήση χωρίς ενεργό Tk (π.χ. CLI helpers).
        if _parent_of(parent) is None:
            return _originals[("message", kind)](title, message, parent=parent) if parent else _originals[("message", kind)](title, message)
        return _modal(title, message, parent=parent, kind=kind)
    return invoke


def _input_wrapper(value_type):
    def invoke(title, prompt, **options):
        parent = options.pop("parent", None)
        if _parent_of(parent) is None:
            return _originals[("input", value_type)](title, prompt, parent=parent, **options) if parent else _originals[("input", value_type)](title, prompt, **options)
        return _modal(title, prompt, parent=parent, value_type=value_type,
                      initialvalue=options.get("initialvalue"),
                      minvalue=options.get("minvalue"), maxvalue=options.get("maxvalue"),
                      show=options.get("show"))
    return invoke


def install(root):
    """Ενεργοποίηση ΜΙΑ φορά στο κύριο Tk. Δεν επηρεάζει τη φόρμα Login."""
    global _root
    _root = root
    if _originals:
        return
    for kind in ("showinfo", "showwarning", "showerror", "askyesno",
                 "askyesnocancel", "askokcancel", "askretrycancel", "askquestion"):
        _originals[("message", kind)] = getattr(messagebox, kind)
        translated = kind.removeprefix("show").removeprefix("ask")
        setattr(messagebox, kind, _message_wrapper(translated))
    for name, value_type in (("askstring", "string"), ("askinteger", "integer"),
                             ("askfloat", "float")):
        _originals[("input", value_type)] = getattr(simpledialog, name)
        setattr(simpledialog, name, _input_wrapper(value_type))


def uninstall():
    """Επαναφορά των built-in συναρτήσεων (χρήσιμο στα αυτοματοποιημένα tests)."""
    global _root
    for (family, name), original in list(_originals.items()):
        if family == "message":
            public_name = "show" + name if name in ("info", "warning", "error") else "ask" + name
            setattr(messagebox, public_name, original)
        else:
            setattr(simpledialog, "ask" + name, original)
    _originals.clear()
    _root = None
