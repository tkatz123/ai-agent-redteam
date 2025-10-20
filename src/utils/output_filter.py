from __future__ import annotations
import re
from typing import Tuple, Dict, Any

_ZW = re.compile(r"[\u200B-\u200D\uFEFF]")
_CTRL_LINES = re.compile(r"(?im)^\s*.*\b(INSTRUCTION|ON[_\s-]?THANKS)\b.*$", re.M)
_DATAURI = re.compile(r"data:[^ \t\n\r]+", re.I)
_SECRET = re.compile(r"(\$\{?API_KEY\}?|Bearer\s+[A-Za-z0-9\-\._~\+\/]+=*|\btoken=[A-Za-z0-9\-_]+)", re.I)

def filter_intent(intent: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, bool]]:
    """
    Returns (filtered_intent, flags). Only processes 'body'/'title' fields.
    Flags: removed_ctrl, removed_zw, redacted_secret, neutralized_datauri
    """
    flags = {"removed_ctrl": False, "removed_zw": False, "redacted_secret": False, "neutralized_datauri": False}
    out = dict(intent)

    def _clean(s: str) -> str:
        if not isinstance(s, str): return s
        orig = s
        s2 = _ZW.sub("", s); flags["removed_zw"] |= (s2 != s); s = s2
        s2 = _CTRL_LINES.sub("", s); flags["removed_ctrl"] |= (s2 != s); s = s2
        s2 = _SECRET.sub("[REDACTED]", s); flags["redacted_secret"] |= (s2 != s); s = s2
        s2 = _DATAURI.sub("[DATA-URI]", s); flags["neutralized_datauri"] |= (s2 != s); s = s2
        return s

    if "body" in out: out["body"] = _clean(out["body"])
    if "title" in out: out["title"] = _clean(out["title"])
    return out, flags
