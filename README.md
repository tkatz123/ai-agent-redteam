# ai-agent-redteam

# Multi-Agent Indirect Prompt Injection — Red-Team Demo

## Problem Statement
Modern AI assistants ingest untrusted content (web, docs, calendar). A single poisoned note can hijack downstream tool use (email, scheduling), creating a **supply-chain style** risk. This project demonstrates an **indirect prompt injection** compromise in a multi-agent workflow, then shows how layered defenses reduce the Attack Success Rate (ASR).

**Goal:** clean run → compromised run → defenses ON (blocked) with reproducible metrics.

## Scope (What’s in)
- Agents: Researcher → Summarizer → (Email/Scheduler tools, mocked)
- Attacks: Hidden HTML comments, CSS-hidden text, zero-width/data-URI
- Defenses: Trust tiers, Tool allowlist + consent gates, Injection detector (regex/ML), Structured prompts
- Metrics: ASR, time-to-compromise, detector precision/recall

## Out of Scope (for now)
- Real email/calendar integrations (we mock them)
- Production auth/provenance (future work)
- Complex agent frameworks (plain Python first, swappable later)

## Roadmap (Milestones)
- **M1 (Sep 24):** First compromise, 3 attack variants, ASR harness v0
- **M2 (Oct 8):** Defense v1 blocks (trust tiers, allowlist/consent, regex detector)
- **M3 (Oct 22):** Defense v2 + metrics (structured prompts, 300-run eval)
- **M4 (Oct 29):** Polished demo, brief draft
- **M5 (Nov 13):** Final results & 5-min exec pitch

## Quickstart
```bash
make run-clean     # baseline: writes a log file
make run-attack    # strict policy: placeholder run (defenses wired later)
```

## Architecture

```mermaid
flowchart LR
  U[Untrusted content (web/docs)]
  L[Web loader v0 (fetch + strip HTML)]
  R[Researcher — normalize notes]
  S[Summarizer — intent JSON]
  TT[Trust tiers]
  TG[Tool allowlist]
  DC[Detector]
  CG[Consent gate]
  E[(Email — mock)]
  C[(Calendar — mock)]
  T[(Telemetry: JSONL / SQLite)]

  U --> L --> R --> S
  S --> TG --> CG --> E
  S -.-> DC
  R --> T
  S --> T
  TG --> T
  CG --> T
  DC --> T
  E --> T
```