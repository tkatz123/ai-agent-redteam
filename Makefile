PY := ./.venv/bin/python

.PHONY: venv run-clean run-attack
venv:
	python3.11 -m venv .venv && $(PY) -V

run-clean:
	$(PY) -m src.app --mode clean --policy normal

run-attack:
	$(PY) -m src.app --mode attack --policy strict
