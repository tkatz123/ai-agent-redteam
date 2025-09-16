PY := ./.venv/bin/python

.PHONY: venv run-clean run-attack \
        poison-clean poison-comment poison-css poison-zwc poison-datauri poison-multipage \
        serve-poison attack-clean attack-comment attack-css attack-zwc attack-datauri attack-multipage

venv:
	python3.11 -m venv .venv && $(PY) -V

run-clean:
	$(PY) -m src.app --mode clean --policy normal

run-attack:
	$(PY) -m src.app --mode attack --policy strict

# --- Poison site generators ---
poison-clean:       ; scripts/seed_poison.sh clean
poison-comment:     ; scripts/seed_poison.sh comment
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
