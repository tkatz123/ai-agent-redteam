# src/utils/sanitize.py
from __future__ import annotations
import re

# Remove zero-width (ZW) chars used to obfuscate payloads
_ZW = re.compile(r"[\u200B-\u200D\uFEFF]")

# Drop lines that contain control phrases like "INSTRUCTION:"
_CTRL_LINE = re.compile(r"(?im)^.*\bINSTRUCTION\b.*$", re.M)

# Redact obvious secret patterns
_SECRET = re.compile(
    r"(\$\{?API_KEY\}?|Bearer\s+[A-Za-z0-9\-\._~\+\/]+=*|\btoken=[A-Za-z0-9\-_]+)",
    re.I,
)

# De-emphasize data: URIs (remove or neutralize)
_DATAURI = re.compile(r"data:[^ \t\n\r]+", re.I)

def sanitize_text(s: str) -> str:
    if not isinstance(s, str):
        return s
    s = _ZW.sub("", s)
    s = _CTRL_LINE.sub("", s)
    s = _SECRET.sub("[REDACTED]", s)
    s = _DATAURI.sub("[DATA-URI]", s)
    # Collapse extra whitespace
    s = re.sub(r"\s+\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()
