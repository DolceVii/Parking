"""Αναφορά αποτυχίας έκδοσης παραστατικού μετά από επιτυχή SQL commit.

Δεν αλλάζει την κατάσταση της συναλλαγής και δεν επικοινωνεί με την μπάρα.
"""
import logging
from pathlib import Path
from tkinter import messagebox


_logger = logging.getLogger("parking.receipts")


def report_receipt_failure(gui, operation, ticket, plate, error):
    """Ειδοποιεί ότι η κίνηση ολοκληρώθηκε αλλά δεν εκδόθηκε παραστατικό.

    Το αρχείο σφαλμάτων περιέχει μόνο τον αριθμό εισιτηρίου, όχι την πινακίδα.
    """
    ticket_text = str(ticket)
    msg = (f"Η {operation.lower()} έχει ήδη καταχωριστεί στη βάση δεδομένων.\n"
           f"Δεν εκδόθηκε το PDF για το εισιτήριο {ticket_text}.\n\n"
           "ΜΗΝ επαναλάβετε την καταχώριση. Ελέγξτε τον φάκελο παραστατικών "
           "και αποκαταστήστε το πρόβλημα εκτύπωσης.")
    try:
        gui.Label1.configure(text=f"{operation}: αποτυχία παραστατικού, ticket {ticket_text}")
    except Exception:
        pass
    try:
        messagebox.showerror(title="Η καταχώριση αποθηκεύτηκε — αποτυχία PDF", message=msg)
    finally:
        # Καταγραφή επιπλέον τεχνικών λεπτομερειών, ακόμη και αν το GUI είναι μη διαθέσιμο.
        _logger.error("%s ticket=%s PDF failure: %s", operation, ticket_text, error)
        try:
            logfile = Path(__file__).resolve().parent.parent / "parking_errors.log"
            with logfile.open("a", encoding="utf-8") as handle:
                from datetime import datetime
                handle.write(f"{datetime.now().isoformat(timespec='seconds')} | {operation} | "
                             f"ticket={ticket_text} | {type(error).__name__}: {error}\n")
        except OSError:
            _logger.exception("Cannot write parking_errors.log")
