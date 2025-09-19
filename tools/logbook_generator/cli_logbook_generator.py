"""
CLI tool for generating personalized Messier Log Book PDFs.

This script overlays a user-provided name onto the cover page of a Messier logbook PDF template,
then writes the personalized PDF to disk.
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
    # Validate the provided name
    try:
        name = validate_name(name)
    except ValueError as e:
        print(f"Invalid name: {e}")
        return

    # Define template and output paths
    template_pdf = project_root / "assets" / "templates" / "messier_logbook_template_final-6.pdf"
    output_pdf = Path(output) if output else (project_root / "output" / f"LogBook_{name}.pdf")
    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    # Remove existing output file if present
    if output_pdf.exists():
        output_pdf.unlink()
        
    try:
        # Read template and create writer
        reader = PdfReader(str(template_pdf))
        writer = PdfWriter()

        # Overlay name on cover page
        p0 = reader.pages[0]
        overlay = build_overlay(float(p0.mediabox.width), float(p0.mediabox.height), name)
        p0.merge_page(overlay)
        writer.add_page(p0)

        # Add remaining pages
        for i in range(1, len(reader.pages)):
            writer.add_page(reader.pages[i])

        # Flatten form fields for compatibility
        flatten_forms(writer)

        # Write the personalized PDF to disk
        with open(output_pdf, "wb") as f:
            writer.write(f)
        print(f"PDF generated at {output_pdf}")
    except Exception as e:
        print(f"Failed to generate PDF: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate a personalized Messier Log Book PDF.")
    parser.add_argument("name", help="Name to personalize the logbook with")
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parent.parent.parent,
                        help="Root directory of the project (default: repo root)")
    parser.add_argument("--output", type=str, default=None, help="Output PDF file path")
    args = parser.parse_args()
    main(args.project_root, args.name, args.output)