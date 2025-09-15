"""
Helper functions for PDF manipulation and overlay creation.
"""

from io import BytesIO
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, BooleanObject, ArrayObject
from pypdf._page import PageObject
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch

def build_overlay(
    page_width: float,
    page_height: float,
    text: str,
    font: str = "Helvetica-Oblique",
    size: int = 26,
    y_top_in: float = 2.9
) -> PageObject:
    """
    Build a PDF overlay page with the given name.

    Args:
        width (float): Width of the PDF page.
        height (float): Height of the PDF page.
        name (str): Name to overlay on the PDF.

    Returns:
        PdfPage: A PDF page object with the overlay.
    """
    buf = BytesIO()
    c = Canvas(buf, pagesize=(page_width, page_height))
    y = page_height - (y_top_in * inch) + 0.18 * inch
    c.setFont(font, size)
    c.drawCentredString(page_width / 2.0, y, text)
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]

def flatten_forms(writer: PdfWriter) -> None:
    """
    Flatten form fields in a PDF writer object.

    Args:
        writer (PdfWriter): The PDF writer object.

    Returns:
        None. Modifies the writer in place.
    """
    root = writer._root_object
    if "/AcroForm" in root:
        acro = root["/AcroForm"]
        acro[NameObject("/NeedAppearances")] = BooleanObject(False)
        acro[NameObject("/Fields")] = ArrayObject()