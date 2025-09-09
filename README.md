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
  subgraph Ingestion
    U[Untrusted Content<br/>(Web/Docs)]
    L[Web Loader v0<br/>(fetch + strip HTML)]
  end

  subgraph Agents
    R[Researcher<br/>normalize notes]
    S[Summarizer<br/>intent JSON]
  end

  subgraph Defenses
    TT[Trust tiers]
    TG[Tool allowlist]
    DC[Detector/Regex<br/>(+optional ML)]
    CG[Consent gate]
  end

  subgraph Tools
    E{{Email (mock)}}
    C{{Calendar (mock)}}
  end

  subgraph Telemetry
    T[JSONL / SQLite]
  end

  U --> L --> R --> S
  S -->|intent| TG --> CG --> E
  S -.-> DC
  R --> T
  S --> T
  TG --> T
  CG --> T
  DC --> T
  E --> T
  ```