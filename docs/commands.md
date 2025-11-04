# ai-agent-redteam — Command Runbook

A quick, copy‑paste friendly cheat‑sheet for every way to run the project.

---

## 0) One‑time setup

```bash
# Fresh venv (Python 3.11)
rm -rf .venv
python3.11 -m venv .venv
./.venv/bin/python -V
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install -e .
```

**.env example** (put in repo root):

```dotenv
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
USE_LLM=0              # set to 1 when you want to call the LLM
CONSENT_MODE=auto      # auto|always|never
POLICY=strict          # default if your entrypoint reads it
USER_AGENT=CraniumAgent/0.1 (+local)
HTTP_TIMEOUT=10
MAX_FETCH_BYTES=2000000
READ_HIDDEN_CONTENT=0
```

*Load .env into shell (optional):*

```bash
set -a; source .env; set +a
```

---

## 1) Poison site generators (attack payloads)

Seed the local test page (`poisoned_site/index.html`) with a variant:

```bash
make poison-clean
make poison-comment
make poison-css
make poison-zwc
make poison-datauri
make poison-multipage
```

Serve locally for eyeballing:

```bash
make serve-poison     # http://127.0.0.1:8000
```

**Variant + run (one shot):**

```bash
make attack-clean
make attack-comment
make attack-css
make attack-zwc
make attack-datauri
make attack-multipage
```

---

## 2) Single run (manual)

**Normal (baseline, vulnerable):**

```bash
./.venv/bin/python -m src.app --mode attack --policy normal
```

**Strict (defended):**

```bash
CONSENT_MODE=always ./.venv/bin/python -m src.app --mode attack --policy strict
```

**Force a specific tool path:**

```bash
./.venv/bin/python -m src.app --mode attack --policy strict --tool email
./.venv/bin/python -m src.app --mode attack --policy strict --tool schedule
```

**Clean (no hidden content):**

```bash
./.venv/bin/python -m src.app --mode clean --policy strict
```

---

## 3) Using the real LLM

Enable and verify:

```bash
# turn on for this shell
set -a; source .env; set +a
export USE_LLM=1

# run a single attack
bash scripts/seed_poison.sh comment
./.venv/bin/python -m src.app --mode attack --policy normal

# confirm the run hit the LLM
last=$(ls -1t data/logs/run-*.jsonl | head -n1)
egrep -n '"type":\s*"(llm_init|intent_llm_raw|intent_llm_error|llm_init_error)"' "$last"
```

Turn off LLM for cheap runs:

```bash
USE_LLM=0 ./.venv/bin/python -m src.app --mode attack --policy strict
```

---

## 4) Batch evaluation (ASR tables)

**Generic:**

```bash
./.venv/bin/python -m src.eval.batch_runner \
  --runs 30 --policy normal --mode attack --tool auto \
  --variants comment css zwc

CONSENT_MODE=always ./.venv/bin/python -m src.eval.batch_runner \
  --runs 30 --policy strict --mode attack --tool auto \
  --variants comment css zwc
```

**Make targets (shortcuts):**

```bash
make eval-batch policy=normal mode=attack runs=30 variants="comment css zwc"
CONSENT_MODE=always make eval-batch policy=strict mode=attack runs=30 variants="comment css zwc"
```

Show per‑variant ASR from the latest CSVs:

```bash
./.venv/bin/python - <<'PY'
import glob,csv,os
for path in sorted(glob.glob('data/logs/asr_*_attack_*.csv'))[-2:]:
    print(os.path.basename(path))
    by={}
    for r in csv.DictReader(open(path,encoding='utf-8')):
        v=r['variant']; c=int(r['compromised']);
        bad,tot=by.get(v,(0,0)); by[v]=(bad+c, tot+1)
    for v,(bad,tot) in sorted(by.items()):
        print(f"  {v:12s} {bad}/{tot} = {bad/tot:.2f}")
PY
```

**5×300 experiment:**

```bash
make eval-5x300 policy=normal
CONSENT_MODE=always make eval-5x300 policy=strict
```

---

## 5) Demo

One‑command demo (baseline vs strict):

```bash
# LLM OFF demo (fast)
make demo

# LLM ON demo
USE_LLM=1 make demo
```

---

## 6) Logging & forensics

Tail the latest run:

```bash
last=$(ls -1t data/logs/run-*.jsonl | head -n1)
cat "$last"
```

Filter important events:

```bash
egrep -n '"type":\s*"(load_page|research_notes|intent|intent_llm_raw|policy_block|consent_block|detector_block|email_sent|pipeline_result|finish)"' "$last"
```

Check LLM parity across recent runs:

```bash
for f in $(ls -1t data/logs/run-*.jsonl | head -n 20); do
  i=$(grep -c '"type":\s*"intent"' "$f" || true)
  l=$(grep -c '"type":\s*"intent_llm_raw"' "$f" || true)
  e=$(grep -c '"type":\s*"\(intent_llm_error\|llm_init_error\)"' "$f" || true)
  printf "%-30s intent=%-2s llm=%-2s errors=%-2s  %s\n" "$(basename "$f")" "$i" "$l" "$e" "$( [ "$i" = "$l" ] && echo OK || echo MISMATCH )"
done
```

SQLite mirror (if enabled in telemetry):

```bash
./.venv/bin/sqlite3 data/logs/telemetry.sqlite3 'select type,count(*) from events group by type order by 2 desc limit 20;'
```

---

## 7) Policies, consent, ablations

Run strict with explicit consent:

```bash
CONSENT_MODE=always ./.venv/bin/python -m src.app --mode attack --policy strict
```

Try “baseline” ablation (turns defenses off even in strict):

```bash
PROFILE_ABLATION=baseline ./.venv/bin/python -m src.app --mode attack --policy strict
```

Strongest profile (example):

```bash
PROFILE_ABLATION=D2_structured CONSENT_MODE=always \
  ./.venv/bin/python -m src.app --mode attack --policy strict
```

---

## 8) Dataset export & (optional) ML detector

Export notes/labels from past runs:

```bash
./.venv/bin/python -m src.eval.export_notes
head -n 5 data/datasets/notes_dataset.csv
```

Train simple BoW+LogReg (optional):

```bash
make train-detector
```

> If you removed ML: skip this; `make demo` and defense logic still work.

---

## 9) Dashboard (static HTML)

Generate a quick HTML from latest CSVs:

```bash
./.venv/bin/python -m src.eval.dashboard --out data/logs/asr_report.html
open data/logs/asr_report.html  # on macOS
```

---

## 10) Collusion & reply‑chain variants

Seed collusion‑lite variant, run, and inspect:

```bash
bash scripts/seed_poison.sh collusion
./.venv/bin/python -m src.app --mode attack --policy normal
```

Reply trigger variant:

```bash
bash scripts/seed_poison.sh reply
./.venv/bin/python -m src.app --mode attack --policy normal
```

Batch including collusion:

```bash
make eval-batch policy=normal mode=attack runs=30 variants="comment css zwc reply collusion"
CONSENT_MODE=always make eval-batch policy=strict mode=attack runs=30 variants="comment css zwc reply collusion"
```

---

## 11) Docker (repro runs)

Build & run (example):

```bash
docker build -t redteam .
docker run --rm -it -e OPENAI_API_KEY -e USE_LLM=1 -v "$PWD":/app redteam \
  ./.venv/bin/python -m src.app --mode attack --policy strict
```

---

## 12) Troubleshooting quickies

```bash
# Recreate venv
rm -rf .venv && python3.11 -m venv .venv && ./.venv/bin/pip install -e .

# Ensure .env is loaded into process
set -a; source .env; set +a

# Verify LLM envs are seen by Python
./.venv/bin/python - <<'PY'
import os
print('USE_LLM=', os.getenv('USE_LLM'))
print('OPENAI_MODEL=', os.getenv('OPENAI_MODEL'))
print('API set? ', bool(os.getenv('OPENAI_API_KEY')))
PY

# Confirm strict profile toggles
./.venv/bin/python - <<'PY'
from src.policy.profiles import get_profile
for p in ('normal','strict'):
    prof=get_profile(p)
    print(p, {k:getattr(prof,k,None) for k in (
        'allow_untrusted_override','regex_detector','regex_threshold',
        'allowlist','consent','sanitize_notes','sanitize_body','output_filter','schema_validate')})
PY
```

---

**That’s it.** Drop this file as `docs/COMMANDS.md`. Adjust variant lists or thresholds as you evolve the project.
