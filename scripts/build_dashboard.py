# scripts/build_dashboard.py
import csv, glob, os, json
from datetime import datetime
from typing import List, Dict, Any

OUT = "data/dashboard/index.html"
os.makedirs("data/dashboard", exist_ok=True)

# Stable display order (includes collusion)
ORDER = ["comment", "css", "zwc", "datauri", "multipage", "reply", "evasion", "collusion"]
LABELS = {
    "comment":    "HTML Comment",
    "css":        "CSS-Hidden",
    "zwc":        "Zero-Width",
    "datauri":    "data:URI",
    "multipage":  "Multi-Page",
    "reply":      "Reply-Bait",
    "evasion":    "Evasion",
    "collusion":  "Collusion-Lite",
}

def load_asr_rows(pattern: str) -> List[Dict[str, Any]]:
    """Load rows from the last up-to-3 matching CSVs."""
    paths = sorted(glob.glob(pattern))
    rows: List[Dict[str, Any]] = []
    for p in paths[-3:]:
        try:
            with open(p, newline="", encoding="utf-8") as f:
                r = csv.DictReader(f)
                for row in r:
                    rows.append(row)
        except FileNotFoundError:
            continue
    return rows

def summarize(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Expect columns: variant, compromised (0/1).
    Returns list of dicts with variant, total, comp, asr.
    Ordered by ORDER (known variants first), then any extras.
    """
    tot: Dict[str, int] = {}
    bad: Dict[str, int] = {}

    for r in rows:
        v = (r.get("variant") or "?").strip()
        try:
            c = int(r.get("compromised", 0))
        except ValueError:
            c = 0
        tot[v] = tot.get(v, 0) + 1
        bad[v] = bad.get(v, 0) + c

    variants_present = list(tot.keys())
    seen = set()
    ordered: List[str] = []
    for v in ORDER:
        if v in tot:
            ordered.append(v); seen.add(v)
    # include any unexpected variants at the end (sorted)
    extras = [v for v in sorted(variants_present) if v not in seen]
    ordered.extend(extras)

    out: List[Dict[str, Any]] = []
    for v in ordered:
        t = tot.get(v, 0)
        b = bad.get(v, 0)
        asr = (b / t) if t else 0.0
        out.append({
            "variant": v,
            "label": LABELS.get(v, v),
            "total": t,
            "comp": b,
            "asr": asr,
        })
    return out

def latest_runs(n: int = 10) -> List[Dict[str, Any]]:
    logs = sorted(glob.glob("data/logs/run-*.jsonl"))[-n:]
    out: List[Dict[str, Any]] = []
    for p in logs:
        try:
            with open(p, encoding="utf-8") as fh:
                js = [json.loads(x) for x in fh]
        except FileNotFoundError:
            continue
        if not js:
            continue
        rid = js[0].get("run_id")
        when = js[0].get("ts")
        mode = next((e.get("mode") for e in js if e.get("type") == "meta" and "mode" in e), "?")
        pol  = next((e.get("policy") for e in js if e.get("type") == "meta" and "policy" in e), "?")
        outcome = next((e for e in js if e.get("type") == "pipeline_result"), {})
        out.append({"run_id": rid, "ts": when, "mode": mode, "policy": pol, "success": outcome.get("success")})
    return out[::-1]

def table(rows: List[Dict[str, Any]]) -> str:
    head = "<tr><th>Variant</th><th>Total</th><th>Comp</th><th>ASR</th></tr>"
    body = "".join(
        f"<tr><td>{r['label']}</td><td>{r['total']}</td><td>{r['comp']}</td><td>{r['asr']:.3f}</td></tr>"
        for r in rows
    )
    return f"<table>{head}{body}</table>"

def mean_asr(rows: List[Dict[str, Any]]) -> float:
    """Mean ASR across the known ORDER variants present in rows."""
    vals = [r["asr"] for r in rows if r["variant"] in ORDER]
    return sum(vals) / len(vals) if vals else 0.0

if __name__ == "__main__":
    norm_rows = summarize(load_asr_rows("data/logs/asr_normal_attack_*.csv"))
    strict_rows = summarize(load_asr_rows("data/logs/asr_strict_attack_*.csv"))
    runs = latest_runs(12)

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    run_rows = "".join(
        f"<tr><td>{r['ts']}</td><td>{r['run_id']}</td><td>{r['mode']}</td><td>{r['policy']}</td><td>{r['success']}</td></tr>"
        for r in runs
    )

    normal_mean = mean_asr(norm_rows)
    strict_mean = mean_asr(strict_rows)

    html = f"""<!doctype html><html><head>
<meta charset="utf-8"/><title>Red Team Dashboard</title>
<style>
body{{font-family:system-ui,Segoe UI,Roboto,Arial,sans-serif;margin:20px}}
h2{{margin-top:1.4rem}}
table{{border-collapse:collapse;margin-top:0.5rem}}
td,th{{border:1px solid #ccc;padding:6px 10px}}
small{{color:#666}}
.cards{{display:flex;gap:12px;margin:12px 0}}
.card{{border:1px solid #ddd;border-radius:8px;padding:10px 14px}}
.card h3{{margin:0 0 4px 0;font-size:1rem}}
.card p{{margin:0;color:#333}}
</style></head><body>
<h1>AI Agent Red Team — ASR Dashboard</h1>
<small>Generated {now}</small>

<div class="cards">
  <div class="card"><h3>Normal</h3><p>Mean ASR: {normal_mean:.3f}</p></div>
  <div class="card"><h3>Strict</h3><p>Mean ASR: {strict_mean:.3f}</p></div>
</div>

<h2>Baseline (normal)</h2>
{table(norm_rows)}

<h2>Defense (strict)</h2>
{table(strict_rows)}

<h2>Recent Runs</h2>
<table><tr><th>TS</th><th>Run</th><th>Mode</th><th>Policy</th><th>Success</th></tr>{run_rows}</table>

</body></html>"""
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("[OK] wrote", OUT)
