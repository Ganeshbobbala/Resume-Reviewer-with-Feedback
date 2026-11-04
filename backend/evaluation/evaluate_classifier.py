import os
import sys
import json
import logging
from typing import Dict, Any

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from train_classifier import train_and_evaluate

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("evaluate_classifier")

def run_classifier_evaluation() -> Dict[str, Any]:
    """Runs classifier evaluation and returns results dict."""
    logger.info("Evaluating baseline and enhanced resume classifiers...")
    return train_and_evaluate(random_seed=42, save_artifacts=False)

if __name__ == "__main__":
    res = run_classifier_evaluation()
    print("\n--- CLASSIFIER EVALUATION METRICS ---")
    print(json.dumps(res, indent=2))

