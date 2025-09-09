# src/app.py
import argparse, json, os
from datetime import datetime, timezone
from src.utils.config import load_settings
from src.telemetry import Telemetry

def _make_run_id(prefix: str = "run") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{prefix}-{ts}-{os.urandom(3).hex()}"  # small random suffix to avoid collisions

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["clean", "attack"], default="clean")
    parser.add_argument("--policy", choices=["normal", "strict"], default=None, help="override config policy")
    args = parser.parse_args()

    cfg = load_settings()

    # CLI `--policy` overrides YAML/.env if provided
    effective_policy = args.policy if args.policy else cfg.policy

    run_id = _make_run_id("run")
    tel = Telemetry(
        run_id=run_id,
        log_dir=cfg.log_path,
        sqlite_enabled=cfg.telemetry_sqlite,
        sqlite_path=cfg.sqlite_path,
    )

    tel.log_meta({"mode": args.mode, "policy": effective_policy})

    # Day-2 placeholder business logic
    record = {
        "run_id": run_id,
        "mode": args.mode,
        "policy": effective_policy,
        "message": "Day-2 sanity check with config + telemetry (jsonl + optional sqlite)."
    }
    tel.log_step("placeholder", record)

    tel.finish(success=True)
    print(f"[OK] {record}")

if __name__ == "__main__":
    main()