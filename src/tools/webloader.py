# src/tools/webloader.py
from __future__ import annotations
import os, re, requests
from bs4 import BeautifulSoup, Comment
from typing import Tuple, Optional

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
    Returns raw HTML as a string. Supports local files and http(s) URLs.
    Applies a simple size cap via max_bytes.
    """
    if _is_url(path_or_url):
        headers = {"User-Agent": user_agent, "Accept": ",".join(HTML_TYPES)}
        r = requests.get(path_or_url, headers=headers, timeout=timeout)
        ctype = (r.headers.get("content-type") or "").split(";")[0].strip().lower()
        if r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code} fetching {path_or_url}")
        if ctype and all(ht not in ctype for ht in HTML_TYPES):
            # We’ll still try to parse (many sites omit proper types), but note it.
            pass
        raw = _clamp_bytes(r.content, max_bytes)
        return raw.decode(r.apparent_encoding or "utf-8", errors="replace")
    else:
        # Local file
        with open(path_or_url, "rb") as f:
            raw = _clamp_bytes(f.read(), max_bytes)
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            return raw.decode("latin-1", errors="replace")

def extract_text(html: str, include_hidden: bool = False) -> Tuple[str, str, str]:
    """
    Given raw HTML, returns (visible_text, comments_text, hidden_text)
    - visible_text: what a normal reader sees
    - comments_text: HTML comments (<!-- like this -->)
    - hidden_text: display:none / [hidden] elements (only if include_hidden=True)
    """
    soup = BeautifulSoup(html, "html.parser")

    # Remove scripts/styles entirely from visible text
    for tag in soup(["script", "style", "noscript", "template"]):
        tag.decompose()

    # Visible text
    visible_chunks = [t.strip() for t in soup.stripped_strings]
    visible_text = " ".join(ch for ch in visible_chunks if ch)

    # Comments
    comments = [c.strip() for c in soup.find_all(string=lambda t: isinstance(t, Comment))]
    comments_text = "\n".join([c for c in comments if c])

    # Hidden text (guarded)
    hidden_text = ""
    if include_hidden:
        hidden_nodes = soup.select("[style*='display:none'], [hidden], [aria-hidden='true']")
        hidden_pieces = []
        for el in hidden_nodes:
            txt = el.get_text(" ", strip=True)
            if txt:
                hidden_pieces.append(txt)
        hidden_text = " ".join(hidden_pieces)

    # Normalize whitespace a bit
    def _norm(s: str) -> str:
        return re.sub(r"\s+", " ", s).strip()

    return _norm(visible_text), _norm(comments_text), _norm(hidden_text)

def load_page(path_or_url: str,
              include_hidden: bool = False,
              user_agent: str = "CraniumAgent/0.1 (+local)",
              timeout: int = 10,
              max_bytes: Optional[int] = 2_000_000):
    """
    Convenience wrapper: fetch → extract. Returns (html, visible, comments, hidden).
    """
    html = fetch(path_or_url, user_agent=user_agent, timeout=timeout, max_bytes=max_bytes)
    visible, comments, hidden = extract_text(html, include_hidden=include_hidden)
    return html, visible, comments, hidden
