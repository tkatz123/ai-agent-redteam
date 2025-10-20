# scripts/build_dashboard.py
import csv, glob, os, json
from datetime import datetime

OUT = "data/dashboard/index.html"
os.makedirs("data/dashboard", exist_ok=True)

def load_asr_rows(pattern):
    paths = sorted(glob.glob(pattern))
    rows = []
    for p in paths[-3:]:
        with open(p, newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r: rows.append(row)
    return rows

def summarize(rows):
    # expect columns: variant, compromised (0/1)
    agg = {}
    for r in rows:
        v = r.get("variant","?")
        c = int(r.get("compromised",0))
        agg.setdefault(v, {"tot":0,"bad":0})
        agg[v]["tot"] += 1
        agg[v]["bad"] += c
    return [{"variant":v,"total":d["tot"],"comp":d["bad"],"asr": (d["bad"]/d["tot"] if d["tot"] else 0.0)} for v,d in agg.items()]

def latest_runs(n=10):
    logs = sorted(glob.glob("data/logs/run-*.jsonl"))[-n:]
    out=[]
    for p in logs:
        js=[json.loads(x) for x in open(p,encoding="utf-8")]
        rid = js[0].get("run_id")
        when = js[0].get("ts")
        mode = next((e.get("mode") for e in js if e.get("type")=="meta" and "mode" in e), "?")
        pol  = next((e.get("policy") for e in js if e.get("type")=="meta" and "policy" in e), "?")
        outcome = next((e for e in js if e.get("type")=="pipeline_result"), {})
        out.append({"run_id":rid,"ts":when,"mode":mode,"policy":pol,"success":outcome.get("success")})
    return out[::-1]

if __name__ == "__main__":
    norm = summarize(load_asr_rows("data/logs/asr_normal_attack_*.csv"))
    strict = summarize(load_asr_rows("data/logs/asr_strict_attack_*.csv"))
    runs = latest_runs(12)

    def table(rows):
        head = "<tr><th>Variant</th><th>Total</th><th>Comp</th><th>ASR</th></tr>"
        body = "".join(f"<tr><td>{r['variant']}</td><td>{r['total']}</td><td>{r['comp']}</td><td>{r['asr']:.2f}</td></tr>" for r in rows)
        return f"<table>{head}{body}</table>"

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    run_rows = "".join(f"<tr><td>{r['ts']}</td><td>{r['run_id']}</td><td>{r['mode']}</td><td>{r['policy']}</td><td>{r['success']}</td></tr>" for r in runs)

    html = f"""<!doctype html><html><head>
<meta charset="utf-8"/><title>Red Team Dashboard</title>
<style>
body{{font-family:system-ui,Segoe UI,Roboto,Arial,sans-serif;margin:20px}}
h2{{margin-top:1.4rem}} table{{border-collapse:collapse}} td,th{{border:1px solid #ccc;padding:6px 10px}}
small{{color:#666}}
</style></head><body>
<h1>AI Agent Red Team — ASR Dashboard</h1>
<small>Generated {now}</small>

<h2>Baseline (normal)</h2>
{table(norm)}

<h2>Defense (strict)</h2>
{table(strict)}

<h2>Recent Runs</h2>
<table><tr><th>TS</th><th>Run</th><th>Mode</th><th>Policy</th><th>Success</th></tr>{run_rows}</table>

</body></html>"""
    open(OUT,"w",encoding="utf-8").write(html)
    print("[OK] wrote", OUT)
