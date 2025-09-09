# src/telemetry.py
import json, os, uuid, sqlite3
from datetime import datetime, timezone
from typing import Optional, Dict, Any

ISO = "%Y-%m-%dT%H:%M:%S.%fZ"

def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime(ISO)

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

        # Helpful: mark the start of the run
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
        rec = {
            "_id": str(uuid.uuid4()),
            "run_id": self.run_id,
            "ts": _utc_now_iso(),
            "type": kind,
            **payload,
        }
        # JSONL
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

        # SQLite mirror
        if self.sqlite_enabled:
            self._insert_sqlite(rec)
        return rec

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
            (rec["_id"], rec["run_id"], rec["ts"], rec["type"], payload),
        )
        self._conn.commit()

    def _close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None
