from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200

    assert response.json()["status"] == "running"


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


def test_generate():

    payload = {
        "document_type": "NDA",
        "title": "Simple NDA",
        "jurisdiction": "India",
        "language": "English",
        "parties": "Party A and Party B",
        "key_terms": (
            "Confidential business information "
            "must be protected."
        ),
        "additional_instructions": "",
    }

    response = client.post(
        "/generate",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["document"]

    assert "disclaimer" in data


def test_export_txt():

    payload = {
        "filename": "test",
        "title": "Test Document",
        "document": "# Hello\n\nThis is a test.",
    }

    response = client.post(
        "/export/txt",
        json=payload
    )

    assert response.status_code == 200

    assert b"Hello" in response.content


def test_export_docx():

    payload = {
        "filename": "test",
        "title": "Test Document",
        "document": "# Hello\n\nThis is a test.",
    }

    response = client.post(
        "/export/docx",
        json=payload
    )

    assert response.status_code == 200

    assert response.headers[
        "content-type"
    ].startswith(
        "application/vnd.openxmlformats"
    )


def test_export_pdf():

    payload = {
        "filename": "test",
        "title": "Test Document",
        "document": "# Hello\n\nThis is a test.",
    }

    response = client.post(
        "/export/pdf",
        json=payload
    )

    assert response.status_code == 200

    assert (
        response.headers["content-type"]
        == "application/pdf"
    )
def test_basic():
    assert True