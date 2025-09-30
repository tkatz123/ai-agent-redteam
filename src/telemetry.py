# src/telemetry.py
from __future__ import annotations

import json, os, uuid, sqlite3, re
from datetime import datetime, timezone
from typing import Optional, Dict, Any

ISO = "%Y-%m-%dT%H:%M:%S.%fZ"

def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime(ISO)

# -------------------------
# Redaction (Step 5, hardened logs)
#   - Masks common secret/token patterns in ANY logged string
#   - Recurses into dicts/lists so nested payloads are scrubbed
# -------------------------
_RE_SECRET = re.compile(
    r"("                       # begin group
    r"\$\{?API_KEY\}?|"        # ${API_KEY} or $API_KEY
    r"Bearer\s+[A-Za-z0-9\-\._~\+\/]+=*|"  # Bearer <token>
    r"\btoken=[A-Za-z0-9\-_]+" # token=xxxx
    r")",
    re.IGNORECASE,
)

def _redact(x: Any) -> Any:
    if isinstance(x, str):
        return _RE_SECRET.sub("[REDACTED]", x)
    if isinstance(x, dict):
        return {k: _redact(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_redact(v) for v in x]
    return x


class Telemetry:
    """
    Writes events to JSONL and (optionally) mirrors them to a SQLite DB.
    Each event has: _id, run_id, ts (UTC), type, and JSON payload.
    """
    def __init__(
        self,
        run_id: str,
        log_dir: str = "data/logs",
        sqlite_enabled: bool = False,
        sqlite_path: Optional[str] = None,
    ):
        self.run_id = run_id
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.path = os.path.join(log_dir, f"{run_id}.jsonl")

        self.sqlite_enabled = sqlite_enabled
        self.sqlite_path = sqlite_path or os.path.join(log_dir, "telemetry.sqlite3")
        self._conn = None
        if self.sqlite_enabled:
            self._ensure_sqlite()

        # Mark the start of the run
        self.log_meta({"event": "run_start"})

    # -------- public API --------
    def log_meta(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._log("meta", payload)

    def log_step(self, name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._log(name, payload)

    def finish(self, success: bool) -> Dict[str, Any]:
        rec = self._log("finish", {"success": success})
        self._close()
        return rec

    # -------- internals --------
    def _log(self, kind: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        # Build raw record
        rec = {
            "_id": str(uuid.uuid4()),
            "run_id": self.run_id,
            "ts": _utc_now_iso(),
            "type": kind,
            **(payload or {}),
        }
        # Redact before persisting anywhere
        safe = _redact(rec)

        # JSONL
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(safe, ensure_ascii=False) + "\n")

        # SQLite mirror (store the redacted payload)
        if self.sqlite_enabled:
            self._insert_sqlite(safe)

        return safe

    def _ensure_sqlite(self) -> None:
        os.makedirs(os.path.dirname(self.sqlite_path), exist_ok=True)
        self._conn = sqlite3.connect(self.sqlite_path)
        self._conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            run_id TEXT,
            ts TEXT,
            type TEXT,
            payload TEXT
        )
        """)
        self._conn.commit()

    def _insert_sqlite(self, rec: Dict[str, Any]) -> None:
        if not self._conn:
            return
        payload = json.dumps(rec, ensure_ascii=False)
        self._conn.execute(
            "INSERT OR REPLACE INTO events (id, run_id, ts, type, payload) VALUES (?, ?, ?, ?, ?)",
            (rec.get("_id"), rec.get("run_id"), rec.get("ts"), rec.get("type"), payload),
        )
        self._conn.commit()

    def _close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None
