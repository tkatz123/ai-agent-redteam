# src/policy/consent.py
from __future__ import annotations
import os, sys
from typing import Dict, Any, Tuple

def _env(name: str, default: str = "") -> str:
    return (os.getenv(name) or default).strip().lower()

def _is_tty() -> bool:
    try:
        return sys.stdin.isatty() and sys.stdout.isatty()
    except Exception:
        return False

def confirm_action(intent: Dict[str, Any], policy: str) -> Tuple[bool, str]:
    """
    Returns (allowed, reason). In strict, require consent depending on CONSENT_MODE.
    Modes:
      - always: approve automatically
      - never: deny automatically
      - prompt: ask user on TTY; else deny
      - auto  : deny (safe default for headless runs)
    """
    if (policy or "normal").lower() != "strict":
        return True, "policy=normal"

    mode = _env("CONSENT_MODE", "auto")  # always|never|prompt|auto
    tool = (intent.get("tool") or "email").lower()
    if tool not in ("email", "schedule"):
        return True, "non-sensitive"

    if mode == "always":
        return True, "consent=auto-approve"
    if mode == "never":
        return False, "consent=auto-deny"
    if mode == "prompt":
        if not _is_tty():
            return False, "consent=prompt-no-tty"
        to = intent.get("to") or intent.get("invitee") or "unknown"
        subj = intent.get("subject") or intent.get("title") or "(no subject)"
        print(f"\nCONSENT REQUIRED: send via {tool} to {to} — \"{subj}\" [y/N]? ", end="", flush=True)
        ans = sys.stdin.readline().strip().lower()
        return (ans in ("y","yes")), ("consent=prompt-yes" if ans in ("y","yes") else "consent=prompt-no")
    # default auto
    return False, "consent=auto-deny"
