# Defense v1 — Consent + Policy + Filtering

## Controls Implemented
1. **Trust-tiers in notes** — provenance headers reduce accidental mixing of untrusted content.
2. **Allowlist** — in `strict`, only approved recipients/invitees are permitted.
3. **Consent gate** — in `strict`, sensitive tool calls require human approval (`CONSENT_MODE`).
4. **Sanitization** — strip control phrases, zero-width chars, data: URIs; redact secrets.
5. **Output filter** — second scrub on final body/title.

## Effect on Risk
- **Integrity**: Wrong-recipient attacks are blocked by allowlist and consent.
- **Confidentiality**: Secret exfil reduced by redaction + output filter.
- **Residual Risk**: Obfuscations not matched; business logic errors; user mis-consents.

## Measured Outcome (example)
Baseline ASR (normal) vs Defense (strict) across {comment, css, zwc, reply, datauri, multipage}.
See `scripts/asr_compare.py` output and CSVs in `data/logs/`.

## Trade-offs
- **Friction**: Consent prompts add latency.
- **Recall vs Precision**: Overzealous filters may remove benign lines.
- **Coverage**: Allowlist requires maintenance.

## Next (Defense v2)
- Structured prompts + tool intent schema.
- Injection detector (regex → ML).
- Granular allowlists per workflow.

## Measured ASR (M2)
- Baseline (normal): see `data/logs/asr_normal_attack_*.csv`
- Defense  (strict): see `data/logs/asr_strict_attack_*.csv`
- Regex detector: blocks obvious cases; ML detector reduces residuals.