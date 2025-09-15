from pathlib import Path
import tempfile
from tools.logbook_generator.cli_logbook_generator import main

def test_cli_generates_pdf(tmp_path):
    # Use a temporary output path
    output_pdf = tmp_path / "test_logbook.pdf"
    project_root = Path(__file__).resolve().parent.parent  # Adjust if needed
    name = "Test User"
    main(project_root=project_root, name=name, output=str(output_pdf))
    assert output_pdf.exists()
    # Check that the file is a PDF
    with open(output_pdf, "rb") as f:
        assert f.read(4) == b"%PDF"

def test_cli_invalid_name(tmp_path, capsys):
    output_pdf = tmp_path / "test_logbook.pdf"
    project_root = Path(__file__).resolve().parent.parent
    name = "Invalid/Name"
    main(project_root=project_root, name=name, output=str(output_pdf))
    # Should not create a PDF
    assert not output_pdf.exists()
    # Should print an error message
    captured = capsys.readouterr()
    assert "Invalid name" in captured.out or "無効な名前" in captured.out