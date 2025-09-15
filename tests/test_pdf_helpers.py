from io import BytesIO
from pypdf import PdfReader, PdfWriter
from utils.pdf_helpers import build_overlay, flatten_forms

def test_build_overlay_returns_pdf_page():
    width, height = 595, 842  # A4 size in points
    name = "Test User"
    overlay = build_overlay(width, height, name)
    assert overlay is not None
    # Overlay should have mediabox with correct dimensions
    assert float(overlay.mediabox.width) == width
    assert float(overlay.mediabox.height) == height

def test_flatten_forms_on_writer(tmp_path):
    # Create a PDF with one page (overlay)
    width, height = 595, 842
    name = "Test User"
    overlay = build_overlay(width, height, name)
    writer = PdfWriter()
    writer.add_page(overlay)
    # Should not raise
    flatten_forms(writer)
    # Write to BytesIO and check it's a valid PDF
    pdf_bytes = BytesIO()
    writer.write(pdf_bytes)
    pdf_bytes.seek(0)
    reader = PdfReader(pdf_bytes)
    assert len(reader.pages) == 1