# src/agents/researcher.py
from __future__ import annotations
import re
from typing import Dict, Optional
from .base import Agent

ZERO_WIDTH = "[\u200b\u200c\u200d\ufeff]"
CTRL = r"[\x00-\x08\x0b-\x1f\x7f]"

def _clean_text(s: str) -> str:
    if not s:
        return ""
    # remove zero-width and control chars
    s = re.sub(ZERO_WIDTH, "", s)
    s = re.sub(CTRL, " ", s)
    # collapse whitespace
    s = re.sub(r"\s+", " ", s).strip()
    return s

class Researcher(Agent):
    """
    Aggregates and normalizes raw inputs into concise 'notes'.
    v0: accepts strings directly (no web fetch yet).
    """
    name = "researcher"

    def ingest(
        self,
        visible: str,
        comments: Optional[str] = None,
        hidden: Optional[str] = None,
        trust: Optional[Dict[str, str]] = None,
        max_chars: int = 6000,
    ) -> str:
        # Normalize each channel
        v = _clean_text(visible)
        c = _clean_text(comments or "")
        h = _clean_text(hidden or "")

        # Compose notes with lightweight provenance headers 
        parts = []
        if v:
            parts.append("## VISIBLE\n" + v)
        if c:
            parts.append("## COMMENTS\n" + c)
        if h:
            parts.append("## HIDDEN\n" + h)

        notes = "\n\n".join(parts) if parts else ""
        notes, truncated = self.truncate(notes, max_chars=max_chars)

        # Telemetry for eval and sanity checks
        meta = {
            "visible_len": len(v),
            "comments_len": len(c),
            "hidden_len": len(h),
            "out_len": len(notes),
            "truncated_chars": truncated,
            "has_hidden": bool(h),
            "has_comments": bool(c),
            "trust": (trust or {}),
        }
        self._tlog("research_notes", meta)
        return notes
