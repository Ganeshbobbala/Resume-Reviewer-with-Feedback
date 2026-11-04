import os
import sys
import pytest

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from services.skill_taxonomy import extract_skills_detailed, extract_canonical_skills, SKILL_TAXONOMY
from services.skill_extractor import extract_skills
from services.scorer import calculate_scores

def test_alias_normalization():
    """Verify common aliases are resolved to canonical skill names."""
    text = "Proficient in JS, TS, Postgres, ReactJS, and K8s."
    canonical = extract_canonical_skills(text)
    assert "JavaScript" in canonical
    assert "TypeScript" in canonical
    assert "PostgreSQL" in canonical
    assert "React" in canonical
    assert "Kubernetes" in canonical

def test_substring_boundary_safety():
    """Verify Java does not falsely match JavaScript, and Go requires context."""
    text_js = "Expert in JavaScript and modern web frameworks."
    skills_js = extract_canonical_skills(text_js)
    assert "JavaScript" in skills_js
    assert "Java" not in skills_js

    text_regular_go = "I like to go for a run every morning."
    skills_go = extract_canonical_skills(text_regular_go)
    assert "Go" not in skills_go

    text_golang = "Backend engineer writing Golang microservices."
    skills_golang = extract_canonical_skills(text_golang)
    assert "Go" in skills_golang

def test_demonstrated_vs_mentioned_classification():
    """Verify skills with action verbs and metrics in experience are classified as demonstrated."""
    sample_resume = """
    EXPERIENCE:
    Senior Software Engineer
    • Architected high-throughput microservices using Python and Redis, reducing p99 latency by 45%.
    • Designed responsive dashboard in React.

    SKILLS:
    Docker, Kubernetes, AWS, C++
    """
    detailed = extract_skills_detailed(sample_resume)
    skill_map = {d["canonical_name"]: d for d in detailed}

    # Python and Redis have action verb 'Architected' and metric '45%' in Experience
    assert "Python" in skill_map
    assert skill_map["Python"]["status"] == "demonstrated"
    assert skill_map["Redis"]["status"] == "demonstrated"

    # Docker is only mentioned in skills list
    assert "Docker" in skill_map
    assert skill_map["Docker"]["status"] == "mentioned"

def test_explainable_score_breakdown_structure():
    """Verify score breakdown returns components, weights, contributions, and non-ATS disclaimer."""
    detected = ["React", "JavaScript", "HTML", "CSS", "Git", "TypeScript"]
    raw_text = """
    Jane Doe
    jane@example.com
    SUMMARY: Frontend Developer with React experience.
    SKILLS: React, JavaScript, HTML, CSS, Git, TypeScript
    EXPERIENCE:
    • Built responsive web app in React, serving 50k users.
    PROJECTS:
    • Personal portfolio in TypeScript.
    EDUCATION:
    BS Computer Science
    """
    scores = calculate_scores(detected, raw_text, "Frontend Developer")

    assert "score_breakdown" in scores
    breakdown = scores["score_breakdown"]

    assert "components" in breakdown
    components = breakdown["components"]
    assert "skill_match" in components
    assert "resume_structure" in components
    assert "role_alignment" in components
    assert "impact_keywords" in components

    # Verify component weights
    assert components["skill_match"]["weight"] == 0.40
    assert components["resume_structure"]["weight"] == 0.30
    assert components["role_alignment"]["weight"] == 0.20
    assert components["impact_keywords"]["weight"] == 0.10

    # Verify disclaimer avoids deceptive ATS claims
    assert "not an official ats score" in breakdown["disclaimer"].lower()

    # Verify missing evidence & actionable suggestions exist
    assert "missing_evidence" in breakdown
    assert "actionable_suggestions" in breakdown

def test_empty_resume_scoring_boundaries():
    """Verify empty/minimal inputs produce valid 0-100 scores without crashing."""
    scores = calculate_scores([], "", "Frontend Developer")
    assert 0 <= scores["resume_score"] <= 100
    assert scores["resume_score"] < 50
    assert "missing_evidence" in scores["score_breakdown"]

if __name__ == "__main__":
    pytest.main(["-v", __file__])

