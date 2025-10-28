# src/policy/ablations.py
from dataclasses import dataclass

@dataclass(frozen=True)
class DefenseProfile:
    name: str
    use_structured_notes: bool
    sanitize_output: bool
    regex_detector: bool
    schema_validate: bool
    allowlist_tools: bool
    consent_gate: bool

# Baselines / Defenses:
BASELINE = DefenseProfile("baseline",  False, False, False, False, False, False)   # ~ your "normal"
D1       = DefenseProfile("D1", use_structured_notes=True, sanitize_output=True,
                    regex_detector=False, schema_validate=False,
                    allowlist_tools=False, consent_gate=False)
D2       = DefenseProfile("D2",        True,  True,  True,  True,  False, False)   # + regex + schema
D2S      = DefenseProfile("D2+structured", True, True, True, True, True, True)     # + allowlist + consent (strict-ish)

PROFILES = {
    "baseline": BASELINE,
    "D1": D1,
    "D2": D2,
    "D2+structured": D2S,
}
