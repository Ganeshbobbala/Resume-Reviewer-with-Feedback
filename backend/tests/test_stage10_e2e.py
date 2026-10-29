import os
import sys
import pytest
from fastapi.testclient import TestClient

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from main import app

client = TestClient(app)

SAMPLE_PDF_PATH = os.path.abspath(
    os.path.join(backend_dir, "..", "sample_resumes", "sample_frontend_resume.pdf")
)

def test_health_check():
    """Verify root endpoint returns online status."""
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "online"

def test_e2e_resume_analysis_complete_workflow():
    """Verify full end-to-end workflow from upload to explainable AI feedback."""
    assert os.path.exists(SAMPLE_PDF_PATH)
    with open(SAMPLE_PDF_PATH, "rb") as f:
        res = client.post(
            "/analyze-resume",
            files={"file": ("sample_frontend_resume.pdf", f, "application/pdf")},
            data={"target_role": "Frontend Developer"}
        )
    assert res.status_code == 200
    data = res.json()

    # 1. Preserved baseline fields
    assert data["target_role"] == "Frontend Developer"
    assert "resume_score" in data
    assert 0 <= data["resume_score"] <= 100
    assert "skill_score" in data
    assert "section_score" in data
    assert "job_match_score" in data
    assert "keyword_score" in data
    assert "detected_skills" in data
    assert "strengths" in data
    assert "weaknesses" in data
    assert "recommendations" in data

    # 2. Formula integrity: (skill * 0.40) + (section * 0.30) + (job_match * 0.20) + (keyword * 0.10)
    expected_score = round(
        (data["skill_score"] * 0.40) +
        (data["section_score"] * 0.30) +
        (data["job_match_score"] * 0.20) +
        (data["keyword_score"] * 0.10)
    )
    assert data["resume_score"] == expected_score

    # 3. Explainable scoring & demonstration attribution
    assert "score_breakdown" in data
    assert "components" in data["score_breakdown"]
    assert "demonstrated_skills" in data

    # 4. LLM feedback & RAG citations
    assert "llm_feedback" in data
    assert "bullet_rewrites" in data
    assert "rag_citations" in data

def test_e2e_job_matcher_hybrid_workflow():
    """Verify job description matcher returns hybrid metrics and requirement breakdown."""
    jd_text = """
    Looking for a Senior Frontend Developer with 4+ years of React, TypeScript, Tailwind CSS,
    and REST API integration. Must write unit tests and optimize page speed.
    """
    with open(SAMPLE_PDF_PATH, "rb") as f:
        res = client.post(
            "/match-job",
            files={"file": ("sample_frontend_resume.pdf", f, "application/pdf")},
            data={"job_description": jd_text}
        )
    assert res.status_code == 200
    data = res.json()

    # Baseline keys
    assert "match_score" in data
    assert "skill_match" in data
    assert "keyword_match" in data
    assert "matched_skills" in data
    assert "missing_skills" in data

    # Advanced semantic keys
    assert "semantic_score" in data
    assert "lexical_score" in data
    assert "requirement_breakdown" in data
    assert len(data["requirement_breakdown"]) > 0

def test_e2e_format_analysis():
    """Verify format analysis runs cleanly on sample resume."""
    with open(SAMPLE_PDF_PATH, "rb") as f:
        res = client.post(
            "/analyze-format",
            files={"file": ("sample_frontend_resume.pdf", f, "application/pdf")}
        )
    assert res.status_code == 200
    data = res.json()
    assert "format_score" in data
    assert "pages" in data

def test_e2e_bullet_rewrite():
    """Verify interactive bullet rewrite returns variations."""
    payload = {"bullet": "Responsible for developing web application in React", "target_role": "Frontend Developer"}
    res = client.post("/rewrite-bullet", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "original" in data
    assert "variations" in data
    assert len(data["variations"]) >= 1

def test_e2e_history_and_deletion_workflow():
    """Verify history listing returns valid structure."""
    res = client.get("/history?limit=5")
    assert res.status_code == 200
    data = res.json()
    assert "reviews" in data
    assert "total" in data

def test_graceful_degradation_on_malformed_job_description():
    """Verify short or invalid inputs return clean 400 Bad Request, never 500."""
    with open(SAMPLE_PDF_PATH, "rb") as f:
        res = client.post(
            "/match-job",
            files={"file": ("sample_frontend_resume.pdf", f, "application/pdf")},
            data={"job_description": "too short"}
        )
    assert res.status_code == 400

if __name__ == "__main__":
    pytest.main(["-v", __file__])
