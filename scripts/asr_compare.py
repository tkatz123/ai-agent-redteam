#!/usr/bin/env python3
import csv, glob, collections, sys
def summarize(pat):
    path = sorted(glob.glob(pat))[-1]
    tot=collections.Counter(); bad=collections.Counter()
    with open(path, newline='', encoding='utf-8') as f:
        r=csv.DictReader(f)
        for row in r:
            v=row["variant"]; c=int(row["compromised"])
            tot[v]+=1; bad[v]+=c
    return path, {v: bad[v]/tot[v] for v in tot}
if __name__ == "__main__":
    npath, nres = summarize("data/logs/asr_normal_attack_*.csv")
    spath, sres = summarize("data/logs/asr_strict_attack_*.csv")
    print("Baseline (normal):", npath)
    for v in sorted(nres): print(f"  {v:10s} {nres[v]:.2f}")
    print("Defense  (strict):", spath)
    for v in sorted(sres): print(f"  {v:10s} {sres[v]:.2f}")
