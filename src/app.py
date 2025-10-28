# src/app.py
import argparse, json, os
from datetime import datetime, timezone
from typing import Optional

from src.utils.config import load_settings
from src.telemetry import Telemetry
from src.pipeline import run_pipeline

# Try to import ablation profiles if available
try:
    from src.policy.ablations import PROFILES  # dict: name -> DefenseProfile
except Exception:
    PROFILES = {}  # keeps CLI working even if ablations file not added yet


def _make_run_id(prefix: str = "run") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{prefix}-{ts}-{os.urandom(3).hex()}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["clean", "attack"], default="clean")
    parser.add_argument("--policy", choices=["normal", "strict"], default=None)
    parser.add_argument(
        "--tool",
        choices=["auto", "email", "schedule"],
        default="auto",
        help="Force specific tool for testing; 'auto' uses Summarizer's intent",
    )

    # Add --defense_profile if we have profiles; otherwise accept the flag without choices
    if PROFILES:
        parser.add_argument(
            "--defense_profile",
            choices=list(PROFILES.keys()),
            default=None,
            help="Override layer toggles via ablation profile (baseline, D1, D2, D2+structured).",
        )
    else:
        parser.add_argument(
            "--defense_profile",
            default=None,
            help="Optional ablation profile (enable after adding src/policy/ablations.py).",
        )

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

    # Resolve the ablation profile object (if any)
    profile = PROFILES.get(args.defense_profile) if args.defense_profile else None

    # Log meta (include profile + toggles if present)
    meta = {"mode": args.mode, "policy": effective_policy}
    if profile is not None:
        # dataclass -> dict of toggles for transparent telemetry
        try:
            toggles = {
                "use_structured_notes": profile.use_structured_notes,
                "sanitize_output": profile.sanitize_output,
                "regex_detector": profile.regex_detector,
                "schema_validate": profile.schema_validate,
                "allowlist_tools": profile.allowlist_tools,
                "consent_gate": profile.consent_gate,
            }
        except Exception:
            toggles = {}
        meta.update({"defense_profile": getattr(profile, "name", args.defense_profile), "defense_toggles": toggles})
    else:
        if args.defense_profile:
            # Provided name not found (e.g., PROFILES empty) — still record it for traceability
            meta.update({"defense_profile": args.defense_profile})

    tel.log_meta(meta)

    force = None if args.tool == "auto" else args.tool

    # Pass profile through to the pipeline (ensure pipeline.run_pipeline accepts profile=...)
    result = run_pipeline(args.mode, effective_policy, cfg, tel, force_tool=force, profile=profile)

    tel.finish(success=result.get("success", False))
    print("[PIPELINE RESULT]", result)


if __name__ == "__main__":
    main()
