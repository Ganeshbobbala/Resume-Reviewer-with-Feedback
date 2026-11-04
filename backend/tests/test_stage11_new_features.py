import os
import sys
import io
import pytest
from fastapi.testclient import TestClient
import docx

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from main import app
from services.resume_parser import (
    extract_text_from_docx,
    extract_text_from_document,
    extract_contact_info
)
from services.local_db import (
    save_local_review,
    get_local_reviews,
    get_local_review_by_id,
    delete_local_review
)
from services.cover_letter_service import generate_tailored_cover_letter

client = TestClient(app)

def create_sample_docx(text_paragraphs):
    doc = docx.Document()
    for p in text_paragraphs:
        doc.add_paragraph(p)
    f = io.BytesIO()
    doc.save(f)
    return f.getvalue()

def test_extract_text_from_docx():
    paragraphs = [
        "Jane Doe - Full Stack Developer",
        "Email: jane.doe@example.com | Phone: 555-0199",
        "LinkedIn: https://linkedin.com/in/janedoe | GitHub: https://github.com/janedoe",
        "Skills: React, Python, FastAPI, PostgreSQL, Docker",
        "Experience: Engineered scalable microservices improving query latency by 40%."
    ]
    docx_bytes = create_sample_docx(paragraphs)
    text, err = extract_text_from_docx(docx_bytes)
    assert err is None
    assert "Jane Doe" in text
    assert "FastAPI" in text

def test_extract_contact_info():
    sample_text = """
    Alex Rivera
    alex.rivera@techfirm.io | (415) 555-2671
    https://linkedin.com/in/alex-rivera-dev
    https://github.com/arivera-code
    https://alexrivera.dev
    Summary: Experienced Backend Engineer with 5 years in Python and Distributed Systems.
    """
    contact = extract_contact_info(sample_text)
    assert contact["email"] == "alex.rivera@techfirm.io"
    assert "555-2671" in contact["phone"]
    assert "linkedin.com/in/alex-rivera-dev" in contact["linkedin"]
    assert "github.com/arivera-code" in contact["github"]
    assert contact["portfolio"] is not None

def test_local_sqlite_history_crud():
    sample_review = {
        "filename": "candidate_alex.docx",
        "target_role": "Backend Developer",
        "predicted_category": "Backend Developer",
        "overall_score": 88,
        "detected_skills": ["Python", "FastAPI", "PostgreSQL"],
        "missing_skills": ["Kubernetes"],
        "strengths": ["Strong systems fundamentals"],
        "weaknesses": ["Needs more metrics"],
        "recommendations": ["Highlight cloud deployment experience"],
        "raw_text": "Experienced Python developer with FastAPI.",
        "user_id": "test_user_123"
    }

    saved = save_local_review(sample_review)
    assert saved is not None
    assert "id" in saved
    review_id = saved["id"]

    # Fetch
    reviews = get_local_reviews(limit=10, user_id="test_user_123")
    assert any(r["id"] == review_id for r in reviews)

    # Fetch by ID
    single = get_local_review_by_id(review_id, user_id="test_user_123")
    assert single is not None
    assert single["filename"] == "candidate_alex.docx"

    # Delete
    deleted = delete_local_review(review_id, user_id="test_user_123")
    assert deleted is True

    # Confirm deletion
    after_del = get_local_review_by_id(review_id)
    assert after_del is None

def test_cover_letter_generator_endpoint():
    response = client.post(
        "/generate-cover-letter",
        json={
            "resume_text": "Experienced Frontend Engineer with React, TypeScript, and Tailwind CSS. Built responsive web apps.",
            "job_description": "We are seeking a Frontend Developer proficient in React, TypeScript, and UI optimization for our SaaS platform.",
            "candidate_name": "Taylor Swift",
            "company_name": "Stripe"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "cover_letter" in data
    assert "Stripe" in data["cover_letter"]
    assert "Taylor Swift" in data["cover_letter"]
    assert "React" in data["cover_letter"] or "TypeScript" in data["cover_letter"]

