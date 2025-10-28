# src/eval/asr_harness.py
from __future__ import annotations
import os, subprocess, glob, json, time
from typing import Optional, Dict, Any

def _pybin() -> str:
    # Honor env override from Make/demo.sh; fall back to python/python3
    pb = os.environ.get("PYBIN")
    if pb:
        return pb
    for cand in ("./.venv/bin/python", "python", "python3"):
        if cand.startswith("./") and os.path.exists(cand):
            return cand
        try:
            subprocess.check_call([cand, "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return cand
        except Exception:
            continue
    return "python"

def _latest_run_jsonl() -> Optional[str]:
    paths = sorted(glob.glob("data/logs/run-*.jsonl"))
    return paths[-1] if paths else None

def _read_result_from_log(path: str) -> Dict[str, Any]:
    # Expect JSONL with types including "pipeline_result"
    with open(path, encoding="utf-8") as f:
        entries = [json.loads(line) for line in f]
    run_id = entries[0].get("run_id", "") if entries else ""
    tool = ""
    success = False
    for e in entries:
        if e.get("type") == "pipeline_result":
            tool = e.get("tool", tool)
            success = bool(e.get("success", False))
    # ASR = attack success rate; 'compromised' means the attack got through.
    compromised = not success
    return {"run_id": run_id, "tool": tool, "compromised": compromised}

def run_once(
    variant: str,
    policy: str = "normal",
    mode: str = "attack",
    force_tool: Optional[str] = None,
    defense_profile: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Seed the variant, run the app once, read the latest JSONL, and
    return {'tool','run_id','compromised'} for CSV logging.
    """
    # 1) Seed the poisoned content
    subprocess.check_call(["bash", "scripts/seed_poison.sh", variant])

    # 2) Build command to run the pipeline
    py = _pybin()
    cmd = [py, "-m", "src.app", "--mode", mode, "--policy", policy]
    if force_tool:
        cmd += ["--tool", force_tool]
    if defense_profile:
        cmd += ["--defense_profile", defense_profile]

    env = os.environ.copy()
    # Help strict behave consistently if you gate on consent
    if policy == "strict":
        env.setdefault("CONSENT_MODE", "always")
    else:
        env.setdefault("CONSENT_MODE", env.get("CONSENT_MODE", "never"))

    # 3) Run once
    subprocess.check_call(cmd, env=env)

    # 4) Read the newest run log and compute compromised=not success
    # small wait in case file system lags
    time.sleep(0.05)
    path = _latest_run_jsonl()
    if not path:
        return {"tool": force_tool or "", "run_id": "", "compromised": 0}
    return _read_result_from_log(path)
