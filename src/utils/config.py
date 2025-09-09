# src/utils/config.py
import os
from dataclasses import dataclass
from typing import Any, Dict
import yaml
from dotenv import load_dotenv

TRUE_SET = {"1", "true", "yes", "y", "on"}

@dataclass
class Settings:
    policy: str
    log_path: str
    poisoned_site_path: str
    telemetry_sqlite: bool
    sqlite_path: str

def _bool_env(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in TRUE_SET

def load_settings(path: str = "configs/settings.yaml") -> Settings:
    # Load .env first so os.getenv sees values
    load_dotenv(override=True)

    data: Dict[str, Any] = {}
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

    policy = os.getenv("POLICY", data.get("policy", "normal"))
    log_path = os.getenv("LOG_PATH", data.get("log_path", "data/logs"))
    poisoned_site_path = os.getenv("POISONED_SITE_PATH", data.get("poisoned_site_path", "poisoned_site/index.html"))

    telemetry_sqlite = _bool_env("TELEMETRY_SQLITE", bool(data.get("telemetry_sqlite", False)))
    sqlite_path = os.getenv("SQLITE_PATH", data.get("sqlite_path", f"{log_path}/telemetry.sqlite3"))

    return Settings(
        policy=policy,
        log_path=log_path,
        poisoned_site_path=poisoned_site_path,
        telemetry_sqlite=telemetry_sqlite,
        sqlite_path=sqlite_path,
    )
