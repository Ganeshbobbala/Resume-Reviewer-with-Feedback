import logging
from typing import Tuple, Optional
import pymupdf  # Modern PyMuPDF import

logger = logging.getLogger("resume_parser")

MAX_PAGES = 25
MAX_EXTRACTED_CHARS = 50000

def extract_text_from_pdf(file_bytes: bytes) -> Tuple[str, Optional[str]]:
    """
    Extracts raw text from PDF bytes using PyMuPDF (fitz) safely.
    Defends against zero-byte files, corrupt headers, oversized page bombs, and malformed streams.
    Returns (extracted_text, error_message).
    If extraction succeeds, error_message is None.
    """
    if not file_bytes:
        return "", "Uploaded PDF file is empty (0 bytes)."

    # Verify basic PDF magic bytes
    if not file_bytes.startswith(b"%PDF-"):
        return "", "Invalid file format: Document does not have a valid PDF header signature."

    doc = None
    try:
        # Open PDF document from memory stream
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
            return "", "Could not extract readable text from this PDF. It may be a scanned image or empty. Please upload a text-based PDF."

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
