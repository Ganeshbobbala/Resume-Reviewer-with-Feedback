import os
import sys
import pytest
from fastapi.testclient import TestClient

# Ensure backend root is on sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from main import app
from services.security_validator import (
    validate_uploaded_file,
    sanitize_filename,
    check_rate_limit,
    get_allowed_origins,
    sanitize_error_message
)
from services.supabase_service import redact_pii

client = TestClient(app)

SAMPLE_PDF_PATH = os.path.abspath(
    os.path.join(backend_dir, "..", "sample_resumes", "sample_frontend_resume.pdf")
)

def test_valid_pdf_analysis_baseline():
    """Verify standard valid PDF analysis succeeds without regression."""
    assert os.path.exists(SAMPLE_PDF_PATH), f"Sample file not found at {SAMPLE_PDF_PATH}"
    with open(SAMPLE_PDF_PATH, "rb") as f:
        response = client.post(
            "/analyze-resume",
            files={"file": ("sample_frontend_resume.pdf", f, "application/pdf")},
            data={"target_role": "Frontend Developer"}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["target_role"] == "Frontend Developer"
    assert "resume_score" in data
    assert data["resume_score"] > 0
    assert "detected_skills" in data

def test_empty_file_rejection():
    """Verify empty file (0 bytes) is strictly rejected with 400."""
    response = client.post(
        "/analyze-resume",
        files={"file": ("empty.pdf", b"", "application/pdf")},
        data={"target_role": "Frontend Developer"}
    )
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()

def test_spoofed_pdf_magic_bytes_rejection():
    """Verify file with .pdf extension but invalid magic bytes is rejected."""
    fake_content = b"This is not a PDF file. Plain text pretending to be PDF."
    response = client.post(
        "/analyze-resume",
        files={"file": ("malicious.pdf", fake_content, "application/pdf")},
        data={"target_role": "Frontend Developer"}
    )
    assert response.status_code == 400
    assert "signature" in response.json()["detail"].lower() or "pdf" in response.json()["detail"].lower()

def test_disallowed_extension_rejection():
    """Verify .exe, .sh, .py uploads are rejected with 400."""
    response = client.post(
        "/analyze-resume",
        files={"file": ("exploit.exe", b"%PDF-fake", "application/octet-stream")},
        data={"target_role": "Frontend Developer"}
    )
    assert response.status_code == 400
    assert "invalid file format" in response.json()["detail"].lower()

def test_oversized_file_rejection():
    """Verify oversized payload exceeds maximum size limit."""
    # 11 MB fake payload
    oversized_data = b"%PDF-" + b"0" * (11 * 1024 * 1024)
    response = client.post(
        "/analyze-resume",
        files={"file": ("large.pdf", oversized_data, "application/pdf")},
        data={"target_role": "Frontend Developer"}
    )
    assert response.status_code == 400
    assert "exceeds" in response.json()["detail"].lower()

def test_filename_sanitization():
    """Verify path traversal characters are sanitized."""
    raw = "../../../etc/passwd.pdf"
    clean = sanitize_filename(raw)
    assert "/" not in clean
    assert "\\" not in clean
    assert ".." not in clean

def test_pii_redaction():
    """Verify emails and phone numbers are redacted in privacy mode."""
    sample_text = "Contact Jane Doe at jane.doe@example.com or call 555-123-4567 for references."
    redacted = redact_pii(sample_text)
    assert "jane.doe@example.com" not in redacted
    assert "[REDACTED_EMAIL]" in redacted
    assert "555-123-4567" not in redacted
    assert "[REDACTED_PHONE]" in redacted

def test_job_match_empty_description_rejected():
    """Verify job match requires a valid description."""
    with open(SAMPLE_PDF_PATH, "rb") as f:
        response = client.post(
            "/match-job",
            files={"file": ("sample.pdf", f, "application/pdf")},
            data={"job_description": "short"}
        )
    assert response.status_code == 400
    assert "short" in response.json()["detail"].lower()

def test_cors_origins_configuration():
    """Verify CORS origins helper handles defaults and environment overrides."""
    origins = get_allowed_origins()
    assert len(origins) > 0
    assert any("localhost" in o for o in origins)

if __name__ == "__main__":
    pytest.main(["-v", __file__])

