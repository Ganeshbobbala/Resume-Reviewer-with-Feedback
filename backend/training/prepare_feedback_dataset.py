import os
import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger("prepare_dataset")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

TRAINING_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(TRAINING_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Curated, permissioned instruction tuning examples with verified evidence-based recommendations
RAW_FEEDBACK_EXAMPLES: List[Dict[str, Any]] = [
    {
        "id": "sft_001",
        "instruction": "Analyze this Frontend Developer resume excerpt and generate structured feedback.",
        "input": "Target Role: Frontend Developer\nResume Text: Frontend Developer with experience in HTML, CSS, JavaScript, React. Built responsive single page apps and integrated REST APIs.\nJob Requirements: React, TypeScript, Tailwind CSS, REST APIs, Web Vitals.",
        "output": {
            "resume_summary": "Junior to mid-level frontend developer with foundational experience in React and JavaScript.",
            "verified_strengths": [
                {
                    "strength": "Direct experience building React single-page applications",
                    "supporting_excerpt": "Built responsive single page apps and integrated REST APIs.",
                    "relevance": "Directly matches core React component requirements."
                }
            ],
            "skill_gaps": [
                {
                    "skill": "TypeScript",
                    "status": "missing",
                    "recommendation": "Migrate an existing React project to TypeScript to demonstrate strong typing proficiency."
                },
                {
                    "skill": "Tailwind CSS",
                    "status": "missing",
                    "recommendation": "Adopt Tailwind CSS for utility-first responsive styling."
                }
            ],
            "job_specific_recommendations": [
                "Incorporate TypeScript type interfaces across API request and response data.",
                "Detail page load optimization techniques and Core Web Vitals achievements."
            ],
            "section_suggestions": [
                {
                    "section": "Professional Experience",
                    "critique": "Lacks quantified impact numbers.",
                    "recommendation": "Quantify outcomes with percentages or user scale."
                }
            ],
            "bullet_rewrites": [
                {
                    "original_bullet": "Built responsive single page apps and integrated REST APIs.",
                    "improved_bullet": "Architected responsive React single page applications integrating RESTful endpoints, improving initial page load by [insert metric, e.g. 28%].",
                    "framework_used": "Action-Context-Result",
                    "metric_placeholder": "[specify latency or bundle reduction %]"
                }
            ],
            "supporting_evidence": ["Confirmed skills: React, JavaScript, HTML, CSS, REST APIs."],
            "rag_citations": [
                {
                    "source_title": "Harvard OCS Resume Principles",
                    "section": "Action Verbs",
                    "key_principle": "Begin bullet points with active verbs like Architected or Engineered."
                }
            ],
            "prioritized_next_steps": [
                "1. Add TypeScript to projects.",
                "2. Add quantified metrics to experience bullets.",
                "3. Include GitHub links for verification."
            ],
            "limitations_and_uncertainty": "Evaluation based on text excerpt; does not assess live application code quality.",
            "provider_used": "lora_supervised_tuning"
        }
    },
    {
        "id": "sft_002",
        "instruction": "Analyze this Backend Developer resume excerpt and generate structured feedback.",
        "input": "Target Role: Backend Developer\nResume Text: Backend Engineer with Python, FastAPI, and PostgreSQL experience. Maintained web servers and created database tables.\nJob Requirements: Python, FastAPI, PostgreSQL, Redis, Docker, Microservices, CI/CD.",
        "output": {
            "resume_summary": "Backend developer with direct Python FastAPI and relational database experience.",
            "verified_strengths": [
                {
                    "strength": "Hands-on experience with FastAPI and PostgreSQL",
                    "supporting_excerpt": "Backend Engineer with Python, FastAPI, and PostgreSQL experience.",
                    "relevance": "Directly satisfies primary service stack requirements."
                }
            ],
            "skill_gaps": [
                {
                    "skill": "Redis",
                    "status": "missing",
                    "recommendation": "Introduce a Redis caching layer to demonstrate endpoint acceleration."
                },
                {
                    "skill": "Docker",
                    "status": "missing",
                    "recommendation": "Containerize backend services with Docker and Docker Compose."
                }
            ],
            "job_specific_recommendations": [
                "Document throughput numbers (QPS) and query optimization results.",
                "Highlight microservice communication patterns."
            ],
            "section_suggestions": [
                {
                    "section": "Experience",
                    "critique": "Bullet points are passive ('Maintained web servers').",
                    "recommendation": "Replace with proactive engineering accomplishments."
                }
            ],
            "bullet_rewrites": [
                {
                    "original_bullet": "Maintained web servers and created database tables.",
                    "improved_bullet": "Engineered high-throughput FastAPI REST microservices on PostgreSQL, scaling capacity to [insert QPS, e.g. 2,500 req/sec] with [insert uptime %, e.g. 99.9%] reliability.",
                    "framework_used": "Action-Context-Result",
                    "metric_placeholder": "[insert throughput QPS and uptime percentage]"
                }
            ],
            "supporting_evidence": ["Confirmed skills: Python, FastAPI, PostgreSQL."],
            "rag_citations": [
                {
                    "source_title": "Backend Engineering Competency Rubric",
                    "section": "Distributed Systems",
                    "key_principle": "Recruiters seek evidence of database indexing, latency tuning, and caching."
                }
            ],
            "prioritized_next_steps": [
                "1. Add Redis caching and Docker containerization.",
                "2. Rewrite experience bullets with ACR format.",
                "3. Detail database query indexing strategies."
            ],
            "limitations_and_uncertainty": "Evaluation restricted to provided text. Production reliability should be verified via technical interview.",
            "provider_used": "lora_supervised_tuning"
        }
    }
]

def prepare_dataset(split_ratio: float = 0.8) -> Dict[str, str]:
    """Generates train.jsonl and test.jsonl files for supervised instruction tuning."""
    train_file = os.path.join(DATA_DIR, "train.jsonl")
    test_file = os.path.join(DATA_DIR, "test.jsonl")

    train_data = RAW_FEEDBACK_EXAMPLES[:1]
    test_data = RAW_FEEDBACK_EXAMPLES[1:]

    with open(train_file, "w", encoding="utf-8") as f:
        for ex in train_data:
            f.write(json.dumps(ex) + "\n")

    with open(test_file, "w", encoding="utf-8") as f:
        for ex in test_data:
            f.write(json.dumps(ex) + "\n")

    logger.info(f"Generated SFT dataset: {len(train_data)} train samples, {len(test_data)} test samples.")
    return {"train_path": train_file, "test_path": test_file}

if __name__ == "__main__":
    paths = prepare_dataset()
    print(f"Dataset successfully prepared:\n  Train: {paths['train_path']}\n  Test:  {paths['test_path']}")

