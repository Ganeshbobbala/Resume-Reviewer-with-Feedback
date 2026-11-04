import os
import sys
import json
import pytest

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from train_classifier import train_and_evaluate, load_and_validate_dataset
from services.scorer import calculate_scores

def test_dataset_loading_and_deduplication():
    data_path = os.path.join(backend_dir, "data", "resumes_corpus.json")
    texts, labels, metadata = load_and_validate_dataset(data_path)
    assert len(texts) > 0
    assert len(texts) == len(labels) == len(metadata)
    # Check no duplicate texts
    assert len(texts) == len(set(texts))

def test_classifier_training_metrics_saved():
    metrics = train_and_evaluate(random_seed=42, save_artifacts=False)
    assert "dataset_metadata" in metrics
    assert "multinomial_nb_baseline" in metrics
    assert "linearsvc_enhanced" in metrics
    assert "accuracy" in metrics["multinomial_nb_baseline"]
    assert "macro_f1" in metrics["multinomial_nb_baseline"]
    assert "confusion_matrix" in metrics["multinomial_nb_baseline"]

def test_scoring_formula_preservation():
    """
    CRITICAL: Verify the verified scoring formula remains exactly:
    skills 40%, structure 30%, job match 20%, keywords 10%
    """
    sample_skills = ["React", "JavaScript", "HTML", "CSS", "Git", "TypeScript"]
    sample_text = "Experienced Frontend Developer. Skills: React, JavaScript, HTML, CSS. Education: BS CS. Experience: Built apps. Projects: Dashboard."
    target_role = "Frontend Developer"

    scores = calculate_scores(sample_skills, sample_text, target_role)

    skill_score = scores["skill_score"]
    section_score = scores["section_score"]
    job_match_score = scores["job_match_score"]
    keyword_score = scores["keyword_score"]

    expected_final = round(
        (skill_score * 0.40) +
        (section_score * 0.30) +
        (job_match_score * 0.20) +
        (keyword_score * 0.10)
    )

    assert scores["resume_score"] == expected_final, (
        f"Score formula violated! Expected {expected_final}, got {scores['resume_score']}"
    )

if __name__ == "__main__":
    pytest.main(["-v", __file__])

