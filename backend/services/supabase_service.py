import os
import logging
from typing import Optional, Dict, Any, List
import httpx

logger = logging.getLogger("supabase_service")

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

def get_headers(auth_token: Optional[str] = None) -> Dict[str, str]:
    token = auth_token or SUPABASE_KEY
    headers = {
        "apikey": SUPABASE_KEY,
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

import re

def redact_pii(text: str) -> str:
    """Redacts emails, phone numbers, and potential sensitive identifiers from text."""
    if not text:
        return ""
    # Redact email addresses
    redacted = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '[REDACTED_EMAIL]', text)
    # Redact phone numbers
    redacted = re.sub(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', '[REDACTED_PHONE]', redacted)
    return redacted

def save_resume_review(review_data: Dict[str, Any], auth_token: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Saves resume analysis details and feedback into Supabase 'resume_reviews' table.
    Redacts PII from stored raw text and associates user_id if provided.
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.warning("Supabase URL or Key not set. Skipping database store.")
        return None

    endpoint = f"{SUPABASE_URL}/rest/v1/resume_reviews"
    raw_text_clean = redact_pii(review_data.get("raw_text", ""))[:4000]

    payload = {
        "filename": review_data.get("filename", "resume.pdf"),
        "target_role": review_data.get("target_role"),
        "predicted_category": review_data.get("predicted_category"),
        "overall_score": review_data.get("overall_score"),
        "detected_skills": review_data.get("detected_skills", []),
        "missing_skills": review_data.get("missing_skills", []),
        "strengths": review_data.get("strengths", []),
        "weaknesses": review_data.get("weaknesses", []),
        "recommendations": review_data.get("recommendations", []),
        "bullet_rewrites": review_data.get("bullet_rewrites", []),
        "format_analysis": review_data.get("format_analysis", {}),
        "raw_text": raw_text_clean
    }
    if review_data.get("user_id"):
        payload["user_id"] = review_data["user_id"]

    try:
        with httpx.Client(timeout=10.0) as client:
            headers = get_headers(auth_token)
            response = client.post(endpoint, json=payload, headers=headers)
            if response.status_code in (200, 201):
                records = response.json()
                if records and isinstance(records, list):
                    return records[0]
                return {"status": "saved"}
            elif response.status_code == 404:
                logger.warning("Supabase table 'resume_reviews' does not exist yet. Please run the SQL schema migration in Supabase SQL Editor.")
                return None
            else:
                logger.error(f"Failed to store in Supabase: {response.status_code} - {response.text}")
                return None
    except Exception as e:
        logger.error(f"Error connecting to Supabase: {e}")
        return None

def get_recent_reviews(limit: int = 20, user_id: Optional[str] = None, auth_token: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Fetches the latest stored reviews from Supabase.
    Filters by user_id if provided.
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        return []

    endpoint = f"{SUPABASE_URL}/rest/v1/resume_reviews?select=id,created_at,filename,target_role,predicted_category,overall_score,detected_skills&order=created_at.desc&limit={limit}"
    if user_id:
        endpoint += f"&user_id=eq.{user_id}"

    try:
        with httpx.Client(timeout=10.0) as client:
            headers = get_headers(auth_token)
            response = client.get(endpoint, headers=headers)
            if response.status_code == 200:
                return response.json()
            return []
    except Exception as e:
        logger.error(f"Error fetching reviews from Supabase: {e}")
        return []

def get_review_by_id(review_id: str, user_id: Optional[str] = None, auth_token: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Fetches full review details by ID from Supabase.
    Ensures user ownership check if user_id is provided.
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None

    endpoint = f"{SUPABASE_URL}/rest/v1/resume_reviews?id=eq.{review_id}&select=*"
    if user_id:
        endpoint += f"&user_id=eq.{user_id}"

    try:
        with httpx.Client(timeout=10.0) as client:
            headers = get_headers(auth_token)
            response = client.get(endpoint, headers=headers)
            if response.status_code == 200:
                results = response.json()
                return results[0] if results else None
            return None
    except Exception as e:
        logger.error(f"Error fetching review {review_id} from Supabase: {e}")
        return None

def delete_review_by_id(review_id: str, user_id: Optional[str] = None, auth_token: Optional[str] = None) -> bool:
    """
    Deletes a review record by ID from Supabase with user ownership enforcement.
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        return False

    endpoint = f"{SUPABASE_URL}/rest/v1/resume_reviews?id=eq.{review_id}"
    if user_id:
        endpoint += f"&user_id=eq.{user_id}"

    try:
        with httpx.Client(timeout=10.0) as client:
            headers = get_headers(auth_token)
            response = client.delete(endpoint, headers=headers)
            return response.status_code in (200, 204)
    except Exception as e:
        logger.error(f"Error deleting review {review_id} from Supabase: {e}")
        return False

