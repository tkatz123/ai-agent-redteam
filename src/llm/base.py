from __future__ import annotations
from typing import List, Dict, Any, Optional

class LLMClient:
    def generate(self, system: str, messages: List[Dict[str, str]],
                 temperature: float = 0.2, max_tokens: int = 400) -> str:
        raise NotImplementedError
