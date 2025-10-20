# src/detect/regex_detector.py
from __future__ import annotations
import re
from typing import Dict, Any

_PATTERNS = {
    "instruction": re.compile(r"\bINSTRUCTION\b", re.I),
    "on_thanks":   re.compile(r"\bON[_\s-]?THANKS\b", re.I),
    "send_email":  re.compile(r"\bsend\s+email\b", re.I),
    "ignore_prev": re.compile(r"ignore (all|previous) instructions", re.I),
    "secret_refs": re.compile(r"\$\{?API_KEY\}?|Bearer\s+\S+|\btoken=[A-Za-z0-9\-_]+", re.I),
    "data_uri":    re.compile(r"\bdata:[^ \t\n\r]+", re.I),
    "zero_width":  re.compile(r"[\u200B-\u200D\uFEFF]"),
}

def score(text: str) -> Dict[str, Any]:
    text = text or ""
    hits = {name: bool(p.search(text)) for name, p in _PATTERNS.items()}
    # simple additive score
    s = sum(hits.values())
    # weight secrets & instruction a bit higher
    if hits["secret_refs"]: s += 1
    if hits["instruction"]: s += 1
    return {"score": s, "hits": hits}

def is_injection(text: str, threshold: int = 2) -> bool:
    return score(text)["score"] >= threshold
