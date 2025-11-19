PY := ./.venv/bin/python

.PHONY: install venv run-clean run-attack \
        poison-clean poison-comment poison-css poison-zwc poison-datauri poison-multipage \
        serve-poison attack-clean attack-comment attack-css attack-zwc attack-datauri attack-multipage

# Install dependencies and setup environment
install:
	python3.11 -m venv .venv
	./.venv/bin/pip install --upgrade pip
	./.venv/bin/pip install -e .
	mkdir -p data/logs data/dashboard
	@echo "✅ Installation complete! Virtual environment created at .venv/"
	@echo "📁 Created data/logs and data/dashboard directories"
	@echo "Next steps:"
	@echo "  1. (Optional) Copy .env.example to .env and add your OpenAI API key"
	@echo "  2. Run 'make demo' to see a quick demonstration"

.PHONY: eval-batch
runs ?= 20
variants ?= comment css zwc datauri
eval-batch:
	$(PY) -m src.eval.batch_runner --runs $(runs) --policy $(policy) --mode $(mode) --tool $(tool) --variants $(variants)
# usage:
# make eval-batch policy=normal mode=attack runs=50

.PHONY: doctor
doctor: ; bash scripts/doctor.sh

.PHONY: poison-reply attack-reply eval-reply release-m1 report-m1

poison-reply: ; bash scripts/seed_poison.sh reply
attack-reply: poison-reply ; $(PY) -m src.app --mode attack --policy normal

eval-reply: ; $(PY) -m src.eval.asr_harness --variant reply --policy normal --mode attack

release-m1: ; bash scripts/release_m1.sh

report-m1:
	@echo "See docs/m1_report.md; run eval-batch and paste table."

venv:
	python3.11 -m venv .venv && $(PY) -V

run-clean:
	$(PY) -m src.app --mode clean --policy normal

run-attack:
	$(PY) -m src.app --mode attack --policy strict

# --- Poison site generators ---
poison-clean:       ; scripts/seed_poison.sh clean
poison-comment:     ; bash scripts/seed_poison.sh comment
poison-css:         ; scripts/seed_poison.sh css
poison-zwc:         ; scripts/seed_poison.sh zwc
poison-datauri:     ; scripts/seed_poison.sh datauri
poison-multipage:   ; scripts/seed_poison.sh multipage

# Static server for local viewing
serve-poison:       ; scripts/serve_poison.sh

# Convenience: seed a variant, then run attack
attack-clean:       poison-clean     run-attack
attack-comment:     poison-comment   run-attack
attack-css:         poison-css       run-attack
attack-zwc:         poison-zwc       run-attack
attack-datauri:     poison-datauri   run-attack
attack-multipage:   poison-multipage run-attack

# --- ASR harness (single-run) ---
# Defaults (can be overridden on the CLI)
variant ?= comment
policy  ?= normal
mode    ?= attack
tool    ?= auto

.PHONY: eval-once eval-clean eval-comment eval-css eval-zwc eval-datauri

# Generic, param-driven run:
eval-once:
	$(PY) -m src.eval.asr_harness --variant=$(variant) --policy=$(policy) --mode=$(mode) --tool=$(tool)

# Convenience shortcuts:
eval-clean:     ; $(PY) -m src.eval.asr_harness --variant clean    --policy $(policy) --mode $(mode) --tool $(tool)
eval-comment:   ; $(PY) -m src.eval.asr_harness --variant comment  --policy $(policy) --mode $(mode) --tool $(tool)
eval-css:       ; $(PY) -m src.eval.asr_harness --variant css      --policy $(policy) --mode $(mode) --tool $(tool)
eval-zwc:       ; $(PY) -m src.eval.asr_harness --variant zwc      --policy $(policy) --mode $(mode) --tool $(tool)
eval-datauri:   ; $(PY) -m src.eval.asr_harness --variant datauri  --policy $(policy) --mode $(mode) --tool $(tool)

.PHONY: demo
demo: ; bash scripts/demo.sh

eval-roc:
	$(PY) -m src.eval.eval_detector

plot-asr:
	$(PY) -m src.eval.plot_asr

.PHONY: eval-5x300
eval-5x300:
	$(PY) -m src.eval.batch_runner --runs 60 --policy normal --mode attack --tool auto --variants comment css zwc reply multipage
	CONSENT_MODE=always $(PY) -m src.eval.batch_runner --runs 60 --policy strict --mode attack --tool auto --variants comment css zwc reply multipage
	$(PY) scripts/asr_compare.py

.PHONY: results-draft
results-draft:
	@echo "Draft at docs/results.md — update tables from dashboard."

.PHONY: demo dashboard docker-build docker-demo docker-repro

# demo.sh already respects $PYBIN; export PY as PYBIN for consistency
demo: export PYBIN=$(PY)
demo:
	bash scripts/demo.sh

dashboard:
	$(PY) scripts/build_dashboard.py
	@echo "Open file://$$(pwd)/data/dashboard/index.html"

IMAGE ?= agent-redteam-demo:latest

.PHONY: docker-build docker-demo

docker-build:
	docker build -t $(IMAGE) .

# Run both demo and dashboard INSIDE the container, using system python.
# We override the image CMD and do not invoke the host `dashboard` rule.
docker-demo:
	mkdir -p "$(CURDIR)/data"
	docker run --rm -t \
	  -v "$(CURDIR)/data:/app/data" \
	  $(IMAGE) \
	  bash -lc 'make demo PY=python && make dashboard PY=python && ls -la data/dashboard && echo "Dashboard ready at data/dashboard/index.html"'
docker-repro: docker-build docker-demo
	@echo "Open ./data/dashboard/index.html"

.PHONY: leaderboard
leaderboard:
	$(PY) scripts/leaderboard.py