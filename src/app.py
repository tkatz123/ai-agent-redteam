# src/app.py
import argparse, json, os
from datetime import datetime, timezone
from src.utils.config import load_settings
from src.telemetry import Telemetry
from src.pipeline import run_pipeline

def _make_run_id(prefix: str = "run") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{prefix}-{ts}-{os.urandom(3).hex()}"  # small random suffix to avoid collisions

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["clean", "attack"], default="clean")
    parser.add_argument("--policy", choices=["normal", "strict"], default=None)
    parser.add_argument("--tool", choices=["auto", "email", "schedule"], default="auto",
                        help="Force specific tool for testing; 'auto' uses Summarizer's intent")
    args = parser.parse_args()

    cfg = load_settings()
    effective_policy = args.policy if args.policy else cfg.policy

    run_id = datetime.now(timezone.utc).strftime("run-%Y%m%dT%H%M%SZ")
    tel = Telemetry(
        run_id=run_id,
        log_dir=cfg.log_path,
        sqlite_enabled=getattr(cfg, "telemetry_sqlite", False),
        sqlite_path=getattr(cfg, "sqlite_path", None),
    )
    tel.log_meta({"mode": args.mode, "policy": effective_policy})

    force = None if args.tool == "auto" else args.tool
    result = run_pipeline(args.mode, effective_policy, cfg, tel, force_tool=force)
    tel.finish(success=result["success"])
    print("[PIPELINE RESULT]", result)

if __name__ == "__main__":
    main()