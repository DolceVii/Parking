"""Pure validation, monetary computations and repeatable subscription PDF issuance.

No database or barrier writes occur here. All dates stored in SQL remain DATE/TIME;
Greek dates are used only for display/print.
"""
from datetime import date, datetime, time, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from io import BytesIO
import os
import shutil
import tempfile


def as_datetime(date_value, time_value):
    if isinstance(date_value, datetime):
        date_value = date_value.date()
    if isinstance(date_value, str):
        date_value = date.fromisoformat(date_value[:10])
    if isinstance(time_value, timedelta):
        seconds = time_value.total_seconds()
        if seconds < 0 or seconds >= 86400:
            raise ValueError("Μη έγκυρη ώρα συνδρομής")
        time_value = (datetime.min + timedelta(seconds=seconds)).time()
    elif isinstance(time_value, str):
        time_value = time.fromisoformat(time_value)
    if not isinstance(date_value, date) or not isinstance(time_value, time):
        raise ValueError("Μη έγκυρη ημερομηνία/ώρα συνδρομής")
    return datetime.combine(date_value, time_value)


def check_period(start, end):
    if end <= start:
        raise ValueError("Η λήξη πρέπει να είναι μεταγενέστερη της έναρξης.")
    return start, end


def has_overlap(start, end, rows):
    check_period(start, end)
    for r in rows:
        # Row shape: datestart, timestart, dateend, timeend.
        left = as_datetime(r[0], r[1])
        right = as_datetime(r[2], r[3])
        if left >= right:
            continue  # Αρχική/κενή εγγραφή· δεν δεσμεύει περίοδο.
        if left < end and right > start:
            return True
    return False


def money(value):
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError("Μη έγκυρη τιμή τιμοκαταλόγου")
    if not result.is_finite() or result < 0:
        raise ValueError("Αρνητικό ή μη πεπερασμένο ποσό")
    return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def gross_amount(net, vat):
    price = money(net)
    vat_rate = Decimal(str(vat))
    if not vat_rate.is_finite() or vat_rate < 0 or vat_rate > 100:
        raise ValueError("Μη έγκυρος συντελεστής ΦΠΑ")
    gross = (price * (Decimal('1') + vat_rate / Decimal('100')))
    return gross.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def split_gross(gross, vat):
    total = money(gross)
    rate = Decimal(str(vat))
    if not rate.is_finite() or rate < 0 or rate > 100:
        raise ValueError("Μη έγκυρος συντελεστής ΦΠΑ")
    net = (total / (1 + rate / 100)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return net, total - net, total


def receipt_code(sub_id):
    if not isinstance(sub_id, int) or sub_id <= 0:
        raise ValueError("Η εγγραφή αρχικοποίησης δεν εκδίδει παραστατικό")
    if sub_id > 99999999999:
        raise ValueError("Πολύ μεγάλος αριθμός συνδρομής")
    return '9' + str(sub_id).zfill(11)


def receipt_paths(project_root, plate, sub_id):
    import re
    plate = str(plate).strip().upper()
    if not plate or not plate.isascii() or not re.fullmatch(r'[A-Z0-9_-]+', plate):
        raise ValueError("Μη έγκυρος αριθμός πινακίδας για όνομα αρχείου")
    root = Path(project_root)
    stem = f'sub_{plate}_{receipt_code(int(sub_id))}'
    return root / 'SUBs' / (stem + '.pdf'), root / 'IMs' / 'SUB' / (stem + '.png')


def issue_receipt(record, company, project_root, archive_previous=False):
    """Produce real Code128 PNG and PDF from a committed subscription row.

    record = SELECT * FROM subscription row, company = SELECT * FROM company row.
    Repeatable by subscription ID; errors never write to SQL. Existing documents
    are kept until the replacement PDF has been completely generated.
    """
    from barcode import get_barcode_class
    from barcode.writer import ImageWriter
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    sub_id, plate = int(record[0]), str(record[4])
    pdf_path, image_path = receipt_paths(project_root, plate, sub_id)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    image_path.parent.mkdir(parents=True, exist_ok=True)
    code = receipt_code(sub_id)
    buffer = BytesIO()
    get_barcode_class('code128')(code, writer=ImageWriter()).write(buffer)
    image_bytes = buffer.getvalue()
    if not image_bytes:
        raise OSError("Δεν δημιουργήθηκε barcode συνδρομής")
    start, end = as_datetime(record[5], record[7]), as_datetime(record[6], record[8])
    check_period(start, end)
    net, tax, total = split_gross(record[10], record[11])
    image_tmp = pdf_tmp = None
    try:
        with tempfile.NamedTemporaryFile(mode='wb', dir=image_path.parent, suffix='.png', delete=False) as f:
            image_tmp = Path(f.name)
            f.write(image_bytes)
        with tempfile.NamedTemporaryFile(mode='wb', dir=pdf_path.parent, suffix='.pdf', delete=False) as f:
            pdf_tmp = Path(f.name)
        c = canvas.Canvas(str(pdf_tmp))
        c.setFont('Arial', 12)
        c.drawImage(ImageReader(BytesIO(image_bytes)), 50, 735, width=120, height=80, mask='auto')
        c.drawString(45, 720, '  ΑΠΟΔΕΙΞΗ Συνδρομής   ')
        c.drawString(10, 705, str(company[6]) + '.')
        c.drawString(10, 693, f'{company[7]} {company[3]} {company[4]}')
        c.drawString(10, 680, 'Α.Φ.Μ. :')
        c.drawString(90, 680, str(company[1]))
        c.drawString(10, 669, 'ΔΟΥ :')
        c.drawString(90, 669, str(company[2]))
        c.drawString(10, 657, 'ΤΗΛ :')
        c.drawString(90, 657, str(company[5]))
        c.line(5, 654, 215, 654)
        c.drawString(10, 641, 'ΑΡΧΗ :')
        c.drawString(90, 641, start.strftime('%d/%m/%Y   %H:%M:%S'))
        c.drawString(10, 631, 'ΛΗΞΗ :')
        c.drawString(90, 631, end.strftime('%d/%m/%Y   %H:%M:%S'))
        c.drawString(10, 621, 'ΑΡ. ΣΥΝΔΡΟΜΗΣ :')
        c.drawString(120, 621, code)
        c.drawString(10, 611, 'ΑΡ. ΚΥΚΛΟΦΟΡΙΑΣ :')
        c.drawString(140, 611, plate)
        c.line(5, 607, 215, 607)
        c.drawString(10, 595, 'ΚΑΘΑΡΗ ΑΞΙΑ :')
        c.drawString(140, 595, f'{net}€')
        c.drawString(10, 585, f'Φ.Π.Α. {record[11]}% :')
        c.drawString(140, 585, f'{tax}€')
        c.drawString(10, 575, 'ΠΛΗΡΩΤΕΟ ΠΟΣΟ :')
        c.drawString(140, 575, f'{total}€')
        c.drawString(65, 555, 'ΕΥΧΑΡΙΣΤΟΥΜΕ')
        c.showPage()
        c.save()
        if pdf_tmp.stat().st_size <= 200 or image_tmp.stat().st_size <= 100:
            raise OSError("Κενό ή ελλιπές παραστατικό")
        if archive_previous and pdf_path.is_file():
            archive = pdf_path.parent / 'archive'
            archive.mkdir(exist_ok=True)
            stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            shutil.copy2(pdf_path, archive / (pdf_path.stem + '_' + stamp + '.pdf'))
        # Atomically replace both output files. The SQL record is never modified here.
        os.replace(str(image_tmp), str(image_path))
        image_tmp = None
        os.replace(str(pdf_tmp), str(pdf_path))
        pdf_tmp = None
        return pdf_path, image_path
    finally:
        for pending in (image_tmp, pdf_tmp):
            if pending is not None:
                try: pending.unlink(missing_ok=True)
                except OSError: pass
