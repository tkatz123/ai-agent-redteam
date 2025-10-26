# src/eval/batch_runner.py
from __future__ import annotations
import csv, os, time, random, re
from typing import List
from datetime import datetime, timezone

from src.eval.asr_harness import run_once
from src.attacks.variants import VARIANTS

# ---- helpers ---------------------------------------------------------------

def _normalize_variants(args_variants: List[str]) -> List[str]:
    """Accepts: ["comment", "css"] or ["comment css,zwc"] and normalizes."""
    out: List[str] = []
    for item in args_variants:
        out.extend([t for t in re.split(r"[,\s]+", item) if t])
    # keep only known variants (order preserved)
    known = []
    seen = set()
    for v in out:
        if v in VARIANTS and v not in seen:
            known.append(v); seen.add(v)
    # If nothing valid was provided, fall back to a sensible default set (now includes collusion)
    return known or ["comment", "css", "zwc", "datauri", "collusion"]

def _with_retries(fn, tries: int = 3, base_delay: float = 0.25, backoff: float = 1.5):
    """Retry wrapper for transient failures."""
    t = 0
    while True:
        try:
            return fn()
        except Exception:
            t += 1
            if t >= tries:
                raise
            time.sleep(base_delay * (backoff ** (t-1)))

# ---- main ------------------------------------------------------------------

def run_batch(variants: List[str], runs: int = 20, policy: str = "normal",
              mode: str = "attack", tool: str = "auto") -> str:
    """
    Runs N trials per variant and writes a CSV:
      ts, variant, policy, mode, tool, run_id, compromised, note
    Notes: adds jitter, retries on transient failures, never crashes the batch.
    """
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = "data/logs"
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, f"asr_{policy}_{mode}_{ts}.csv")

    fields = ["ts","variant","policy","mode","tool","run_id","compromised","note"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for v in variants:
            if v not in VARIANTS:
                # Skip unknown variant gracefully
                w.writerow({
                    "ts": ts, "variant": v, "policy": policy, "mode": mode,
                    "tool": "", "run_id": "", "compromised": 0,
                    "note": f"unknown-variant:{v}"
                })
                continue

            for i in range(runs):
                # small jitter so concurrent file ops don’t collide
                time.sleep(random.uniform(0.02, 0.12))
                try:
                    # Retry the whole run_once (it includes seeding + pipeline)
                    res = _with_retries(
                        lambda: run_once(v, policy=policy, mode=mode,
                                         force_tool=None if tool == "auto" else tool),
                        tries=3, base_delay=0.25, backoff=1.6
                    )
                    w.writerow({
                        "ts": ts,
                        "variant": v,
                        "policy": policy,
                        "mode": mode,
                        "tool": res.get("tool",""),
                        "run_id": res.get("run_id",""),
                        "compromised": int(bool(res.get("compromised", False))),
                        "note": ""
                    })
                except Exception as e:
                    # Don’t kill the batch; record as non-compromised with reason
                    w.writerow({
                        "ts": ts,
                        "variant": v,
                        "policy": policy,
                        "mode": mode,
                        "tool": "",
                        "run_id": "",
                        "compromised": 0,
                        "note": f"error:{type(e).__name__}"
                    })
    return csv_path

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(
        description="Batch ASR runner. Variants include: comment css zwc datauri multipage reply evasion collusion"
    )
    p.add_argument("--runs", type=int, default=20)
    p.add_argument("--policy", choices=["normal","strict"], default="normal")
    p.add_argument("--mode", choices=["attack","clean"], default="attack")
    # Keep your existing choices; pipeline maps 'schedule' internally as needed
    p.add_argument("--tool", choices=["auto","email","schedule"], default="auto")
    # tolerant: space- or comma-separated; now default includes collusion
    p.add_argument("--variants", nargs="+", default=["comment","css","zwc","datauri","collusion"])
    args = p.parse_args()
    args.variants = _normalize_variants(args.variants)

    path = run_batch(args.variants, runs=args.runs, policy=args.policy, mode=args.mode, tool=args.tool)
    print(f"[OK] Wrote {path}")
