import pytest
from services.logbook.flask_logbook_service import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index_page_english(client):
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"Messier Log Book Generator" in rv.data

def test_index_page_japanese(client):
    rv = client.get("/?lang=ja")
    assert rv.status_code == 200
    # Check for Japanese title (UTF-8 bytes)
    assert "メシエログブックジェネレーター".encode("utf-8") in rv.data

def test_generate_pdf_success(client):
    rv = client.post("/generate", data={"name": "Test User"})
    assert rv.status_code == 200
    assert rv.mimetype == "application/pdf"
    assert rv.data[:4] == b"%PDF"  # PDF magic number

def test_generate_pdf_invalid_name(client):
    rv = client.post("/generate", data={"name": "Name/With/Slash"})
    assert rv.status_code == 400
    assert b"Invalid name" in rv.data or "無効な名前".encode("utf-8") in rv.data