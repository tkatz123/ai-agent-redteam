# src/eval/plot_asr.py
from __future__ import annotations
import csv, glob, collections, os
import numpy as np
import matplotlib.pyplot as plt

OUT = "docs/fig/asr_compare.png"
os.makedirs(os.path.dirname(OUT), exist_ok=True)

def summarize(pat):
    path = sorted(glob.glob(pat))[-1]
    tot=collections.Counter(); bad=collections.Counter()
    with open(path, newline="", encoding="utf-8") as f:
        r=csv.DictReader(f)
        for row in r:
            v=row["variant"]; c=int(row["compromised"])
            tot[v]+=1; bad[v]+=c
    return path, {v: bad[v]/tot[v] for v in tot}

if __name__ == "__main__":
    npath, nres = summarize("data/logs/asr_normal_attack_*.csv")
    spath, sres = summarize("data/logs/asr_strict_attack_*.csv")
    variants = sorted(set(nres.keys()) | set(sres.keys()))
    n = np.array([nres.get(v,0.0) for v in variants])
    s = np.array([sres.get(v,0.0) for v in variants])

    x = np.arange(len(variants))
    w = 0.35
    plt.figure()
    plt.bar(x - w/2, n, width=w, label="Baseline (normal)")
    plt.bar(x + w/2, s, width=w, label="Defense (strict)")
    plt.xticks(x, variants, rotation=15)
    plt.ylim(0,1); plt.ylabel("ASR"); plt.title("Attack Success Rate by Variant")
    plt.legend(); plt.tight_layout()
    plt.savefig(OUT)
    print("[OK] wrote", OUT)
