import os
import json
import sqlite3
import uuid
from datetime import datetime, timezone
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger("local_db")

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DB_PATH = os.path.join(DB_DIR, "reviews_history.db")

def init_db():
    """Initializes local SQLite database for resume review persistence."""
    os.makedirs(DB_DIR, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resume_reviews (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                filename TEXT NOT NULL,
                target_role TEXT,
                predicted_category TEXT,
                overall_score INTEGER,
                detected_skills TEXT,
                missing_skills TEXT,
                strengths TEXT,
                weaknesses TEXT,
                recommendations TEXT,
                bullet_rewrites TEXT,
                format_analysis TEXT,
                raw_text TEXT,
                user_id TEXT
            )
        """)
        conn.commit()

init_db()

def save_local_review(review_data: Dict[str, Any]) -> Dict[str, Any]:
    """Saves review into local SQLite fallback database."""
    init_db()
    record_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO resume_reviews (
                id, created_at, filename, target_role, predicted_category,
                overall_score, detected_skills, missing_skills, strengths,
                weaknesses, recommendations, bullet_rewrites, format_analysis,
                raw_text, user_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record_id,
            now_iso,
            review_data.get("filename", "resume.pdf"),
            review_data.get("target_role"),
            review_data.get("predicted_category"),
            review_data.get("overall_score", 0),
            json.dumps(review_data.get("detected_skills", [])),
            json.dumps(review_data.get("missing_skills", [])),
            json.dumps(review_data.get("strengths", [])),
            json.dumps(review_data.get("weaknesses", [])),
            json.dumps(review_data.get("recommendations", [])),
            json.dumps(review_data.get("bullet_rewrites", [])),
            json.dumps(review_data.get("format_analysis", {})),
            review_data.get("raw_text", "")[:4000],
            review_data.get("user_id")
        ))
        conn.commit()

    return {
        "id": record_id,
        "created_at": now_iso,
        **review_data
    }

def get_local_reviews(limit: int = 15, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves recent reviews from local SQLite database."""
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if user_id:
            cursor.execute("""
                SELECT * FROM resume_reviews
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (user_id, limit))
        else:
            cursor.execute("""
                SELECT * FROM resume_reviews
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
        
        rows = cursor.fetchall()
        results = []
        for r in rows:
            d = dict(r)
            for k in ["detected_skills", "missing_skills", "strengths", "weaknesses", "recommendations", "bullet_rewrites"]:
                try:
                    d[k] = json.loads(d[k]) if d.get(k) else []
                except Exception:
                    d[k] = []
            try:
                d["format_analysis"] = json.loads(d["format_analysis"]) if d.get("format_analysis") else {}
            except Exception:
                d["format_analysis"] = {}
            results.append(d)
        return results

def get_local_review_by_id(review_id: str, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Retrieves a single review by id from local SQLite database."""
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if user_id:
            cursor.execute("SELECT * FROM resume_reviews WHERE id = ? AND user_id = ?", (review_id, user_id))
        else:
            cursor.execute("SELECT * FROM resume_reviews WHERE id = ?", (review_id,))
        row = cursor.fetchone()
        if not row:
            return None
        d = dict(row)
        for k in ["detected_skills", "missing_skills", "strengths", "weaknesses", "recommendations", "bullet_rewrites"]:
            try:
                d[k] = json.loads(d[k]) if d.get(k) else []
            except Exception:
                d[k] = []
        try:
            d["format_analysis"] = json.loads(d["format_analysis"]) if d.get("format_analysis") else {}
        except Exception:
            d["format_analysis"] = {}
        return d

def delete_local_review(review_id: str, user_id: Optional[str] = None) -> bool:
    """Deletes a review by id from local SQLite database."""
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        if user_id:
            cursor.execute("DELETE FROM resume_reviews WHERE id = ? AND user_id = ?", (review_id, user_id))
        else:
            cursor.execute("DELETE FROM resume_reviews WHERE id = ?", (review_id,))
        conn.commit()
        return cursor.rowcount > 0

