# src/utils/schema.py
from __future__ import annotations
from typing import Dict, Tuple

REQUIRED_BY_TOOL = {
    "email":    ("to", "subject", "body"),
    "schedule": ("invitee", "title", "when"),
}

def validate_intent(intent: Dict) -> Tuple[bool, str]:
    tool = (intent.get("tool") or "").lower()
    if tool not in REQUIRED_BY_TOOL:
        return False, f"unknown-tool:{tool}"
    for k in REQUIRED_BY_TOOL[tool]:
        v = intent.get(k)
        if not isinstance(v, str) or not v.strip():
            return False, f"missing:{k}"
    return True, "ok"