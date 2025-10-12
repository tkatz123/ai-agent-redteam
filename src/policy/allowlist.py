# src/policy/allowlist.py
from __future__ import annotations

from typing import Dict, Any, Tuple

DEFAULT_ALLOWED_EMAILS = {"mentor@example.com"}
DEFAULT_ALLOWED_INVITEES = {"mentor@example.com"}

def enforce_tool_policy(intent: Dict[str, Any], policy: str) -> Tuple[bool, str]:
    """
    Returns (allowed, reason). In 'strict', gate sensitive tool parameters.
    """
    pol = (policy or "normal").lower()
    tool = (intent.get("tool") or "email").lower()
    if pol != "strict":
        return True, "policy=normal"

    if tool == "email":
        to = (intent.get("to") or "").lower()
        if to not in DEFAULT_ALLOWED_EMAILS:
            return False, f"email.to '{to}' not in allowlist"
    elif tool == "schedule":
        inv = (intent.get("invitee") or "").lower()
        if inv not in DEFAULT_ALLOWED_INVITEES:
            return False, f"schedule.invitee '{inv}' not in allowlist"

    return True, "ok"
