import os
import re
import time
import logging
from collections import defaultdict
from typing import Tuple, Optional, List
from fastapi import HTTPException, status, Request

logger = logging.getLogger("security_validator")

# Maximum upload size: default 10 MB
MAX_FILE_SIZE = int(os.environ.get("MAX_FILE_SIZE_BYTES", 10 * 1024 * 1024))
RATE_LIMIT_PER_MINUTE = int(os.environ.get("RATE_LIMIT_PER_MINUTE", 60))

# In-memory sliding window request store for rate limiting: ip -> list of timestamps
_request_records = defaultdict(list)

# Supported magic bytes signatures
MAGIC_SIGNATURES = {
    "pdf": [b"%PDF-"],
    "docx": [b"PK\x03\x04"]
}

def sanitize_filename(filename: Optional[str]) -> str:
    """
    Sanitizes upload filenames to prevent directory traversal and injection attacks.
    """
    if not filename:
        return "uploaded_document.pdf"
    # Strip paths
    clean_name = os.path.basename(filename)
    # Remove null bytes and dangerous shell characters
    clean_name = re.sub(r'[\x00-\x1f\\/<>:"|?*]', '_', clean_name)
    # Ensure reasonable length
    if len(clean_name) > 100:
        base, ext = os.path.splitext(clean_name)
        clean_name = base[:90] + ext
    return clean_name or "uploaded_document.pdf"

def validate_uploaded_file(
    filename: Optional[str],
    contents: bytes,
    allowed_extensions: Tuple[str, ...] = (".pdf",)
) -> Tuple[bool, Optional[str]]:
    """
    Performs comprehensive validation on uploaded file:
    - Empty file check
    - File size check
    - Extension check
    - Magic-byte (file signature) verification to prevent MIME-type spoofing
    """
    if not contents or len(contents) == 0:
        return False, "Uploaded file is empty (0 bytes)."

    if len(contents) > MAX_FILE_SIZE:
        max_mb = MAX_FILE_SIZE // (1024 * 1024)
        return False, f"File size exceeds maximum limit of {max_mb} MB."

    safe_name = sanitize_filename(filename)
    ext = os.path.splitext(safe_name)[1].lower()

    if ext not in allowed_extensions:
        allowed_str = ", ".join(allowed_extensions)
        return False, f"Invalid file format '{ext}'. Supported formats: {allowed_str}."

    # Validate Magic Bytes
    if ext == ".pdf":
        if not contents.startswith(b"%PDF-"):
            return False, "File signature mismatch: File does not appear to be a valid PDF document."
    elif ext == ".docx":
        if not contents.startswith(b"PK\x03\x04"):
            return False, "File signature mismatch: File does not appear to be a valid DOCX document."

    return True, None

def check_rate_limit(client_ip: str, max_requests: int = RATE_LIMIT_PER_MINUTE) -> bool:
    """
    Simple in-memory sliding-window rate limiter per client IP.
    Returns True if request is allowed, False if rate-limited.
    """
    now = time.time()
    cutoff = now - 60.0

    # Purge old records
    timestamps = [t for t in _request_records[client_ip] if t > cutoff]
    if len(timestamps) >= max_requests:
        return False

    timestamps.append(now)
    _request_records[client_ip] = timestamps
    return True

def get_allowed_origins() -> List[str]:
    """
    Retrieves allowed CORS origins from environment variable or defaults to secure localhost.
    """
    origins_env = os.environ.get("ALLOWED_ORIGINS", "")
    if not origins_env:
        return [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000"
        ]
    if origins_env.strip() == "*":
        return ["*"]
    return [o.strip() for o in origins_env.split(",") if o.strip()]

def sanitize_error_message(err: Exception) -> str:
    """
    Generates user-safe error messages without leaking stack traces or credentials.
    """
    err_str = str(err)
    # Remove file paths
    err_str = re.sub(r'([A-Za-z]:\\[^:\s]+|/(?:[\w.-]+/)+[\w.-]+)', '[FILE_PATH]', err_str)
    # Remove potential tokens or keys
    err_str = re.sub(r'(?:sb_|sk-|Bearer\s+)[A-Za-z0-9_\-\.]{15,}', '[REDACTED_SECRET]', err_str)
    return err_str

