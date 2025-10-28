#!/usr/bin/env python3
import csv, glob, os, collections
from typing import Dict, List

PROFILES = ["baseline","D1","D2","D2+structured"]

def latest(pattern: str) -> str:
    paths = sorted(glob.glob(pattern))
    return paths[-1] if paths else ""

def load(path: str) -> List[dict]:
    if not path or not os.path.exists(path): return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def summarize(rows: List[dict]) -> Dict[str, float]:
    tot = collections.Counter(); bad = collections.Counter()
    for r in rows:
        v = r.get("variant","?"); c = int(r.get("compromised",0))
        tot[v]+=1; bad[v]+=c
    return {v: bad[v]/tot[v] for v in tot if tot[v]}

def print_table(results: Dict[str, Dict[str,float]]):
    variants = sorted({v for prof in results.values() for v in prof.keys()})
    hdr = "Variant".ljust(16) + "".join(p.rjust(16) for p in PROFILES)
    print(hdr); print("-"*len(hdr))
    for v in variants:
        row = v.ljust(16)
        for p in PROFILES:
            val = results.get(p,{}).get(v,None)
            row += (f"{val:.3f}" if val is not None else "—").rjust(16)
        print(row)

if __name__ == "__main__":
    results = {}
    # Expect you ran batch files with --defense_profile set; filenames still asr_normal_attack_*.csv
    # We rely on the fact each run uses a single profile and you run profiles sequentially.
    # If your harness embeds profile in CSV rows, adjust filter here accordingly.
    npath = latest("data/logs/asr_normal_attack_*.csv")
    rows = load(npath)
    # Group by a marker if present; else assume last four runs correspond to the four profiles, newest last.
    # Easiest: run profiles in order baseline, D1, D2, D2+structured and keep 4 latest files.
    files = sorted(glob.glob("data/logs/asr_normal_attack_*.csv"))[-4:]
    for p, fp in zip(PROFILES, files):
        results[p] = summarize(load(fp))
    print(f"Using CSVs:\n" + "\n".join(f"  {p}: {f}" for p,f in zip(PROFILES,files)))
    print()
    print_table(results)
