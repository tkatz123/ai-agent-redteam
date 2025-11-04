from __future__ import annotations
import os, json, time
from typing import List, Dict
import httpx
from .base import LLMClient

class OpenAIClient(LLMClient):
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.base = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY not set")

    def generate(self, system: str, messages: List[Dict[str, str]],
                 temperature: float = 0.2, max_tokens: int = 400) -> str:
        url = f"{self.base}/chat/completions"
        payload = {
            "model": self.model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [{"role": "system", "content": system}] + messages
        }
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        # tiny retry loop
        for i in range(3):
            try:
                with httpx.Client(timeout=30) as client:
                    r = client.post(url, headers=headers, json=payload)
                r.raise_for_status()
                data = r.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                if i == 2:
                    raise
                time.sleep(0.6 * (i + 1))
        return ""
