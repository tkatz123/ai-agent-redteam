from __future__ import annotations
import json, re
from typing import Any, Dict, Tuple

def extract_json_block(text: str) -> Tuple[Dict[str, Any], str]:
    """
    Try to find and parse the first JSON object in text.
    Returns (obj, reason). If fails, obj={}
    """
    if not text:
        return {}, "empty"
    # quick path: direct parse
    try:
        return json.loads(text), "exact"
    except Exception:
        pass
    # fenced code blocks?
    m = re.search(r"\{.*\}", text, re.S)
    if m:
        try:
            return json.loads(m.group(0)), "snippet"
        except Exception:
            return {}, "malformed"
    return {}, "no-json"