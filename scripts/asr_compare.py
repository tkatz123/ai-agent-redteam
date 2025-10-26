#!/usr/bin/env python3
import csv, glob, collections, sys, os
from typing import Dict, Tuple

# Stable display order (now includes collusion)
DISPLAY_ORDER = ["comment", "css", "zwc", "datauri", "multipage", "reply", "evasion", "collusion"]
LABELS = {
    "comment":    "HTML Comment",
    "css":        "CSS-Hidden",
    "zwc":        "Zero-Width",
    "datauri":    "data: URI",
    "multipage":  "Multi-Page",
    "reply":      "Reply-Bait",
    "evasion":    "Evasion",
    "collusion":  "Collusion-Lite",
}

def _latest_csv(pattern: str) -> str:
    paths = sorted(glob.glob(pattern))
    return paths[-1] if paths else ""

def _summarize(path: str) -> Tuple[str, Dict[str, float]]:
    """
    Returns (path, asr_by_variant) where ASR = (#compromised / #total) per variant.
    If the path is empty or file missing, returns empty results.
    """
    if not path or not os.path.exists(path):
        return path, {}
    tot = collections.Counter()
    bad = collections.Counter()
    with open(path, newline='', encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            v = row.get("variant", "").strip()
            if not v:
                continue
            c = int(row.get("compromised", "0"))
            tot[v] += 1
            bad[v] += c
    asr = {v: (bad[v] / tot[v]) for v in tot if tot[v] > 0}
    return path, asr

def _fmt(x):
    return f"{x:.3f}" if x is not None else "—"

if __name__ == "__main__":
    npath = _latest_csv("data/logs/asr_normal_attack_*.csv")
    spath = _latest_csv("data/logs/asr_strict_attack_*.csv")

    npath, nres = _summarize(npath)
    spath, sres = _summarize(spath)

    if not nres and not sres:
        print("No ASR CSVs found. Run a batch first (e.g., `python -m src.eval.batch_runner ...`).")
        sys.exit(1)

    print("Compare latest ASR CSVs:")
    if npath: print(f"  Baseline (normal): {npath}")
    if spath: print(f"  Defense  (strict): {spath}")
    print()

    # Build ordered list: show known variants in DISPLAY_ORDER first, then any extras
    seen = set()
    ordered = []
    for v in DISPLAY_ORDER:
        if v in nres or v in sres:
            ordered.append(v); seen.add(v)
    # Any unexpected variants present in CSVs
    extras = [v for v in sorted(set(nres.keys()) | set(sres.keys())) if v not in seen]
    ordered.extend(extras)

    # Print a compact table
    print(f"{'Variant':<18} {'Normal':>8} {'Strict':>8}")
    print("-" * 36)
    for v in ordered:
        label = LABELS.get(v, v)
        normal = nres.get(v, None)
        strict = sres.get(v, None)
        print(f"{label:<18} {_fmt(normal):>8} {_fmt(strict):>8}")
