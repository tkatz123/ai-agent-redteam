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
