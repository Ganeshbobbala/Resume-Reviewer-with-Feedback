import os
import sys
import pytest

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from services.semantic_matcher import (
    compute_semantic_matching,
    chunk_job_requirements,
    chunk_resume_passages,
    embedding_service
)
from services.job_matcher import analyze_job_match

SAMPLE_RESUME = """
Jane Doe — Senior React Frontend Engineer
Email: jane.doe@example.com | GitHub: github.com/janedoe

TECHNICAL SKILLS:
React, TypeScript, JavaScript, HTML5, CSS3, Tailwind CSS, Redux, REST API, Git, Jest

WORK EXPERIENCE:
Senior Frontend Developer — Acme Corp (2021 - Present)
• Architected scalable web dashboards with React and TypeScript, serving 250k monthly active users.
• Reduced initial page load bundle size by 35% through dynamic code-splitting and memoization.
• Integrated secure REST APIs and implemented responsive UI styling using Tailwind CSS.
• Maintained 90% automated unit test coverage with Jest and React Testing Library.

EDUCATION:
Bachelor of Science in Computer Science, University of Technology
"""

SAMPLE_JD = """
Job Title: Senior Frontend Developer
Requirements:
• 4+ years of professional experience building responsive web applications using React and TypeScript.
• Deep understanding of Tailwind CSS, Redux, and modern JavaScript (ES6+).
• Experience integrating REST APIs and writing automated tests with Jest.
• Proven ability to optimize web performance and page load metrics.
"""

def test_semantic_matching_output_schema():
    """Verify semantic matching produces all backward-compatible and advanced fields."""
    res = compute_semantic_matching(SAMPLE_RESUME, SAMPLE_JD)

    # Backward compatible fields
    assert "match_score" in res
    assert "skill_match" in res
    assert "keyword_match" in res
    assert "experience_match" in res
    assert "education_match" in res
    assert "role_similarity" in res
    assert "matched_skills" in res
    assert "missing_skills" in res
    assert "recommendations" in res

    # Advanced semantic fields
    assert "semantic_score" in res
    assert "lexical_score" in res
    assert "hybrid_score" in res
    assert "requirement_breakdown" in res
    assert len(res["requirement_breakdown"]) > 0
    assert "status" in res["requirement_breakdown"][0]
    assert "supporting_excerpt" in res["requirement_breakdown"][0]

def test_evidence_attribution_and_skill_grounding():
    """Verify evidence attribution associates requirements with resume excerpts."""
    res = compute_semantic_matching(SAMPLE_RESUME, SAMPLE_JD)
    matched_reqs = [r for r in res["requirement_breakdown"] if r["status"] == "matched"]
    assert len(matched_reqs) > 0
    # The first matched requirement should cite supporting excerpt
    first = matched_reqs[0]
    assert len(first["supporting_excerpt"]) > 10
    assert "React" in first["supporting_excerpt"] or "TypeScript" in first["supporting_excerpt"]

def test_job_matcher_integration_backward_compatibility():
    """Verify analyze_job_match transparently returns enriched semantic payload."""
    res = analyze_job_match(SAMPLE_RESUME, SAMPLE_JD)
    assert res["match_score"] >= 70
    assert "semantic_score" in res
    assert "requirement_breakdown" in res

def test_empty_inputs_handling():
    """Verify empty inputs raise graceful ValueErrors without unhandled crashes."""
    with pytest.raises(ValueError):
        compute_semantic_matching("", SAMPLE_JD)
    with pytest.raises(ValueError):
        compute_semantic_matching(SAMPLE_RESUME, "")

if __name__ == "__main__":
    pytest.main(["-v", __file__])

