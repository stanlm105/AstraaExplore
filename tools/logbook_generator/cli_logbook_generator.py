"""
CLI tool for generating personalized Messier Log Book PDFs.
"""

from pathlib import Path
from pypdf import PdfReader, PdfWriter
from utils.pdf_helpers import build_overlay, flatten_forms
from utils.validation import validate_name

def main(project_root: Path, name: str, output: str = None):
    """
    Generate a personalized Messier Log Book PDF.

    Args:
        project_root (Path): The root directory of the project.
        name (str): The name to personalize the logbook with.
        output (str, optional): The output PDF file path. If None, a default path is used.

    Returns:
        None. Writes the generated PDF to the specified output path.
    """
    try:
        name = validate_name(name)
    except ValueError as e:
        print(f"Invalid name: {e}")
        return

    template_pdf = project_root / "assets" / "templates" / "messier_logbook_template_final-6.pdf"
    output_pdf = Path(output) if output else (project_root / "output" / f"LogBook_{name}.pdf")
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    if output_pdf.exists():
        output_pdf.unlink()
        
    try:
        reader = PdfReader(str(template_pdf))
        writer = PdfWriter()
        p0 = reader.pages[0]
        overlay = build_overlay(float(p0.mediabox.width), float(p0.mediabox.height), name)
        p0.merge_page(overlay)
        writer.add_page(p0)
        for i in range(1, len(reader.pages)):
            writer.add_page(reader.pages[i])
        flatten_forms(writer)
        with open(output_pdf, "wb") as f:
            writer.write(f)
        print(f"PDF generated at {output_pdf}")
    except Exception as e:
        print(f"Failed to generate PDF: {e}")