# src/tools/webloader.py
from __future__ import annotations
import os, re
from typing import Tuple, Optional

import requests
from bs4 import BeautifulSoup, Comment

HTML_TYPES = ("text/html", "application/xhtml+xml")

def _is_url(path_or_url: str) -> bool:
    return path_or_url.startswith("http://") or path_or_url.startswith("https://")

def _clamp_bytes(b: bytes, max_bytes: Optional[int]) -> bytes:
    if max_bytes and len(b) > max_bytes:
        return b[:max_bytes]
    return b

def fetch(path_or_url: str,
          user_agent: str = "CraniumAgent/0.1 (+local)",
          timeout: int = 10,
          max_bytes: Optional[int] = 2_000_000) -> str:
    """
    Return raw HTML as a string (never None).
    Supports local files and http(s) URLs. Size-caps large responses.
    """
    if _is_url(path_or_url):
        headers = {"User-Agent": user_agent, "Accept": ",".join(HTML_TYPES)}
        r = requests.get(path_or_url, headers=headers, timeout=timeout)
        r.raise_for_status()
        raw = _clamp_bytes(r.content, max_bytes)
        # decode with best-guess, never return None
        txt = raw.decode(r.apparent_encoding or "utf-8", errors="replace")
        return txt

    # Local file path
    if not os.path.exists(path_or_url):
        raise FileNotFoundError(f"No such file: {path_or_url}")
    with open(path_or_url, "rb") as f:
        raw = _clamp_bytes(f.read(), max_bytes)
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin-1", errors="replace")

def extract_text(html: str, include_hidden: bool = False) -> Tuple[str, str, str]:
    """
    Given raw HTML (str), return (visible_text, comments_text, hidden_text).
    """
    if not isinstance(html, str):
        raise TypeError(f"extract_text expected str HTML, got {type(html)}")

    soup = BeautifulSoup(html, "html.parser")

    # Drop non-visible sources for visible_text
    for tag in soup(["script", "style", "noscript", "template"]):
        tag.decompose()

    visible_chunks = [t.strip() for t in soup.stripped_strings]
    visible_text = " ".join(ch for ch in visible_chunks if ch)

    comments = [c.strip() for c in soup.find_all(string=lambda t: isinstance(t, Comment))]
    comments_text = "\n".join([c for c in comments if c])

    hidden_text = ""
    if include_hidden:
        # include display:none, hidden attributes, aria-hidden, and off-screen abs-pos
        hidden_nodes = soup.select(
            "[style*='display:none'], [hidden], [aria-hidden='true'], "
            "[style*='left:-'], [style*='position:absolute']"
        )
        hidden_pieces = []
        for el in hidden_nodes:
            txt = el.get_text(" ", strip=True)
            if txt:
                hidden_pieces.append(txt)
        hidden_text = " ".join(hidden_pieces)

    def _norm(s: str) -> str:
        return re.sub(r"\s+", " ", s).strip()

    return _norm(visible_text), _norm(comments_text), _norm(hidden_text)

def load_page(path_or_url: str,
              include_hidden: bool = False,
              user_agent: str = "CraniumAgent/0.1 (+local)",
              timeout: int = 10,
              max_bytes: Optional[int] = 2_000_000):
    """
    Convenience: fetch → extract. Returns (html, visible, comments, hidden).
    Always returns a non-empty string for html (or raises).
    """
    html = fetch(path_or_url, user_agent=user_agent, timeout=timeout, max_bytes=max_bytes)
    if not isinstance(html, str):
        raise TypeError(f"fetch() returned non-str: {type(html)} for {path_or_url}")
    visible, comments, hidden = extract_text(html, include_hidden=include_hidden)
    return html, visible, comments, hidden
