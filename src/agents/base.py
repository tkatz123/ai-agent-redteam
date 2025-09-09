# src/agents/base.py
from __future__ import annotations
import time
from typing import Any, Dict, Optional, Tuple

class Agent:
    """
    Minimal base class for all agents.
    - Provides telemetry hooks
    - Provides a swappable model call
    """
    name: str = "agent"

    def __init__(self, telemetry=None, llm=None):
        self.tel = telemetry
        self.llm = llm # Placeholder for an LLM instance

    # --- telemetry helpers ---
    def _tlog(self, kind: str, payload: Dict[str, Any]) -> None:
        if self.tel:
            self.tel.log_step(kind, {"agent": self.name, **payload})

    # --- model call ---
    def call_model(self, prompt: str, meta: Optional[Dict[str, Any]] = None) -> str:
        """
        Single place to call an LLM (or stub). Keeps retries/telemetry consistent.
        """
        self._tlog("model_call_start", {"chars": len(prompt), **(meta or {})})
        t0 = time.time()
        if self.llm is not None:
            # real LLM path 
            out = self.llm.ask(prompt)
        else:
            # stub fallback
            out = f"[STUB RESPONSE]\n{prompt[:256]}..."
        self._tlog("model_call_end", {"duration_ms": int(1000 * (time.time() - t0)),
                                      "out_chars": len(out)})
        return out

    # --- utility ---
    @staticmethod
    def truncate(text: str, max_chars: int = 8000) -> Tuple[str, int]:
        if len(text) <= max_chars:
            return text, 0
        return text[:max_chars], len(text) - max_chars
