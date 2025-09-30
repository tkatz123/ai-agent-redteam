from __future__ import annotations
import csv, os, time
from typing import List, Dict, Any
from datetime import datetime, timezone
from src.eval.asr_harness import run_once
from src.attacks.variants import VARIANTS

def run_batch(variants: List[str], runs: int = 20, policy: str = "normal", mode: str = "attack", tool: str = "auto") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = "data/logs"
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, f"asr_{policy}_{mode}_{ts}.csv")

    fields = ["ts","variant","policy","mode","tool","run_id","compromised"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for v in variants:
            for i in range(runs):
                res = run_once(v, policy=policy, mode=mode, force_tool=None if tool=="auto" else tool)
                w.writerow({
                    "ts": ts,
                    "variant": v,
                    "policy": policy,
                    "mode": mode,
                    "tool": res["tool"],
                    "run_id": res["run_id"],
                    "compromised": int(bool(res["compromised"])),
                })
                time.sleep(0.05)  # tiny spacing for readability
    return csv_path

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--runs", type=int, default=20)
    p.add_argument("--policy", choices=["normal","strict"], default="normal")
    p.add_argument("--mode", choices=["attack","clean"], default="attack")
    p.add_argument("--tool", choices=["auto","email","schedule"], default="auto")
    p.add_argument("--variants", nargs="*", default=["comment","css","zwc","datauri"])
    args = p.parse_args()
    path = run_batch(args.variants, runs=args.runs, policy=args.policy, mode=args.mode, tool=args.tool)
    print(f"[OK] Wrote {path}")