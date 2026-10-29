import os
import sys
import pytest
from fastapi.testclient import TestClient

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from main import app
from services.schemas import LLMFeedbackResponse
from services.llm_provider import RuleBasedLLMProvider, MockLLMProvider, get_llm_provider
from services.llm_feedback import generate_enhanced_llm_feedback, extract_resume_bullets

client = TestClient(app)

SAMPLE_PDF_PATH = os.path.abspath(
    os.path.join(backend_dir, "..", "sample_resumes", "sample_frontend_resume.pdf")
)

def test_pydantic_schema_validation():
    """Verify LLMFeedbackResponse schema accepts and validates valid payload."""
    provider = RuleBasedLLMProvider()
    prompt_data = {
        "target_role": "Frontend Developer",
        "matched_skills": ["React", "JavaScript", "HTML", "CSS"],
        "missing_skills": ["TypeScript", "Next.js"],
        "demonstrated_skills": ["React", "JavaScript"],
        "insufficiently_demonstrated": ["HTML"],
        "sections": {"contact": True, "skills": True, "experience": True, "projects": True},
        "bullets": ["Developed responsive customer dashboard using React and Tailwind."],
        "rag_citations": [{"title": "Harvard OCS Guide", "section": "Action Verbs", "content": "Start with active verbs."}]
    }

    raw = provider.generate_feedback(prompt_data)
    validated = LLMFeedbackResponse(**raw)
    assert validated.resume_summary
    assert len(validated.verified_strengths) > 0
    assert len(validated.skill_gaps) > 0
    assert len(validated.bullet_rewrites) > 0
    assert len(validated.rag_citations) > 0

def test_non_fabrication_metric_placeholders():
    """Verify bullet rewrites do not fabricate unverified statistics, providing clear user placeholders."""
    provider = RuleBasedLLMProvider()
    prompt_data = {
        "target_role": "Backend Developer",
        "matched_skills": ["Python", "FastAPI"],
        "missing_skills": ["Redis"],
        "bullets": ["Wrote backend code for user authentication."]
    }
    raw = provider.generate_feedback(prompt_data)
    rewrite = raw["bullet_rewrites"][0]

    # Verify placeholder is present for unverified metrics
    assert "metric_placeholder" in rewrite
    assert rewrite["metric_placeholder"] is not None
    assert "[" in rewrite["improved_bullet"] and "]" in rewrite["improved_bullet"]

def test_bullet_point_extractor():
    """Verify action-oriented bullets are cleanly extracted from raw text."""
    sample_text = """
    EXPERIENCE
    • Architected microservices with Python and Docker.
    • Built interactive client application with React.
    • Spearheaded database migration to PostgreSQL.
    """
    bullets = extract_resume_bullets(sample_text)
    assert len(bullets) >= 2
    assert any("Architected" in b for b in bullets)

def test_end_to_end_analyze_resume_llm_fields():
    """Verify /analyze-resume response contains enriched LLM feedback and RAG citations."""
    with open(SAMPLE_PDF_PATH, "rb") as f:
        response = client.post(
            "/analyze-resume",
            files={"file": ("sample_frontend_resume.pdf", f, "application/pdf")},
            data={"target_role": "Frontend Developer"}
        )
    assert response.status_code == 200
    data = response.json()

    assert "llm_feedback" in data
    llm = data["llm_feedback"]
    assert "resume_summary" in llm
    assert "verified_strengths" in llm
    assert "skill_gaps" in llm
    assert "bullet_rewrites" in llm
    assert "rag_citations" in llm
    assert "prioritized_next_steps" in llm

def test_end_to_end_analyze_text_llm_fields():
    """Verify /analyze-text response contains enriched LLM feedback."""
    payload = {
        "resume_text": "Experienced Python Backend Developer with FastAPI, PostgreSQL, Docker, Redis, and Git. Built high-scale REST APIs.",
        "target_role": "Backend Developer"
    }
    response = client.post("/analyze-text", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "llm_feedback" in data
    assert len(data["llm_feedback"]["verified_strengths"]) > 0

if __name__ == "__main__":
    pytest.main(["-v", __file__])
