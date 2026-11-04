import os
import io
import re
import logging
from typing import Tuple, Optional, Dict, Any
import pymupdf  # PyMuPDF

logger = logging.getLogger("resume_parser")

MAX_PAGES = 25
MAX_EXTRACTED_CHARS = 50000

def extract_text_from_pdf(file_bytes: bytes) -> Tuple[str, Optional[str]]:
    """
    Extracts raw text from PDF bytes using PyMuPDF safely.
    Defends against zero-byte files, corrupt headers, oversized page bombs, and malformed streams.
    Returns (extracted_text, error_message).
    """
    if not file_bytes:
        return "", "Uploaded PDF file is empty (0 bytes)."

    if not file_bytes.startswith(b"%PDF-"):
        return "", "Invalid file format: Document does not have a valid PDF header signature."

    doc = None
    try:
        doc = pymupdf.open(stream=file_bytes, filetype="pdf")

        if doc.page_count == 0:
            return "", "PDF file contains no readable pages."

        if doc.page_count > MAX_PAGES:
            return "", f"Document exceeds maximum resume page limit of {MAX_PAGES} pages (found {doc.page_count})."

        text_content = []
        total_chars = 0

        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            if text:
                text_content.append(text)
                total_chars += len(text)
                if total_chars > MAX_EXTRACTED_CHARS:
                    logger.warning("Resume text truncated due to maximum character limit.")
                    break

        full_text = "\n".join(text_content).strip()

        if not full_text or len(full_text.strip()) < 15:
            return "", "Could not extract readable text from this PDF. It may be a scanned image or empty. Please upload a text-based PDF or DOCX."

        return full_text, None

    except Exception as e:
        logger.error(f"Failed to parse PDF document safely: {e}")
        return "", f"Failed to parse PDF document: {str(e)}"
    finally:
        if doc is not None:
            try:
                doc.close()
            except Exception:
                pass


def extract_text_from_docx(file_bytes: bytes) -> Tuple[str, Optional[str]]:
    """
    Extracts text from DOCX (Word) bytes safely.
    Defends against zip bombs, corrupt headers, and empty files.
    """
    if not file_bytes:
        return "", "Uploaded DOCX file is empty (0 bytes)."

    if not file_bytes.startswith(b"PK\x03\x04"):
        return "", "Invalid file format: Document does not have a valid DOCX zip signature."

    try:
        import docx
        doc = docx.Document(io.BytesIO(file_bytes))
        paragraphs = []
        total_chars = 0

        # Extract regular paragraphs
        for p in doc.paragraphs:
            txt = p.text.strip()
            if txt:
                paragraphs.append(txt)
                total_chars += len(txt)
                if total_chars > MAX_EXTRACTED_CHARS:
                    break

        # Extract table cells (resumes often use layout tables)
        for table in doc.tables:
            for row in table.rows:
                row_texts = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_texts:
                    paragraphs.append(" | ".join(row_texts))

        full_text = "\n".join(paragraphs).strip()

        if not full_text or len(full_text) < 15:
            return "", "Could not extract readable text from this DOCX document. It may be empty or contain only images."

        return full_text, None

    except Exception as e:
        logger.error(f"Failed to parse DOCX document: {e}")
        return "", f"Failed to parse DOCX document: {str(e)}"


def extract_text_from_document(file_bytes: bytes, filename: str) -> Tuple[str, Optional[str]]:
    """
    Unified entry point for document text extraction based on filename extension and file signature.
    Supports both .pdf and .docx.
    """
    ext = os.path.splitext(filename.lower())[1]
    if ext == ".docx":
        return extract_text_from_docx(file_bytes)
    return extract_text_from_pdf(file_bytes)


def extract_contact_info(text: str) -> Dict[str, Any]:
    """
    Extracts key candidate contact metadata and evaluates ATS parsing hygiene.
    Identifies Email, Phone, LinkedIn, GitHub, and Portfolio URLs.
    """
    email_match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    phone_match = re.search(r'(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?', text)
    linkedin_match = re.search(r'(?:https?://)?(?:www\.)?linkedin\.com/(?:in|profile)/[A-Za-z0-9_-]+', text, re.IGNORECASE)
    github_match = re.search(r'(?:https?://)?(?:www\.)?github\.com/[A-Za-z0-9_-]+', text, re.IGNORECASE)
    portfolio_match = re.search(r'(?:https?://)?(?:www\.)?(?:[a-zA-Z0-9-]+\.(?:dev|me|io|tech|app|vercel\.app|netlify\.app))', text, re.IGNORECASE)

    extracted_email = email_match.group(0) if email_match else None
    extracted_phone = phone_match.group(0).strip() if (phone_match and len(phone_match.group(0).strip()) >= 7) else None
    extracted_linkedin = linkedin_match.group(0) if linkedin_match else None
    extracted_github = github_match.group(0) if github_match else None
    extracted_portfolio = portfolio_match.group(0) if portfolio_match else None

    # ATS Hygiene Checks
    hygiene_alerts = []
    if not extracted_email:
        hygiene_alerts.append("No standard email address detected. Ensure your email is plain text, not in a header/footer image.")
    if not extracted_phone:
        hygiene_alerts.append("No standard phone number found. Verify formatting (e.g., +1 555-0199).")
    if not extracted_linkedin:
        hygiene_alerts.append("No LinkedIn profile URL found. Including a LinkedIn URL significantly increases recruiter callbacks.")
    if len(text.splitlines()) < 10:
        hygiene_alerts.append("Text formatting appears unusually condensed. Ensure multi-column layouts do not merge lines.")

    return {
        "email": extracted_email,
        "phone": extracted_phone,
        "linkedin": extracted_linkedin,
        "github": extracted_github,
        "portfolio": extracted_portfolio,
        "hygiene_alerts": hygiene_alerts,
        "total_words": len(text.split()),
        "total_characters": len(text)
    }
