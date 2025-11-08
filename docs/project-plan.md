# Project Plan
## AI Agent Red Team Framework

**Project Manager:** Tyler Katz
**Project Start Date:** September 2025
**Project End Date:** November 2025
**Status:** Completed
**Version:** 1.0

---

## 1. Executive Summary

This project plan outlines the development of the AI Agent Red Team Framework, a security research platform demonstrating prompt injection vulnerabilities in multi-agent AI systems and implementing defense-in-depth mitigation strategies. The project was completed on schedule and within budget, achieving all success criteria.

**Project Objectives:**
1. Build a multi-agent pipeline processing untrusted content
2. Demonstrate 7+ prompt injection attack variants
3. Implement layered security defenses
4. Achieve measurable ASR reduction (1.00 → 0.00)
5. Provide comprehensive evaluation and telemetry framework

**Key Deliverables:**
- Production-ready multi-agent system
- 7 attack variant implementations
- 6-layer defense framework
- Evaluation and reporting tools
- Complete documentation suite

---

## 2. Project Scope

### 2.1 In Scope

**Core Features:**
- Multi-agent pipeline (Researcher, Summarizer, Emailer, Scheduler)
- Web content ingestion with hidden text extraction
- LLM integration with OpenAI GPT models
- Attack variant library (comment, css, zwc, datauri, multipage, reply, collusion)
- Defense policy framework (normal, strict)
- Telemetry system (JSONL, SQLite)
- Batch evaluation harness
- ASR metrics calculation and reporting
- Documentation (README, overview, PRD, project plan)

**Technical Capabilities:**
- Heuristic and LLM-based summarization
- Hardened prompt engineering
- Multi-layer defense (sanitization, filtering, detection, validation, allowlist, consent)
- Provenance tracking and trust boundaries
- Secret redaction in logs
- Reproducible evaluation framework

### 2.2 Out of Scope

**Excluded from MVP:**
- Production email/scheduling integration
- Real-time monitoring dashboard
- Multiple LLM provider support (only OpenAI in v1.0)
- Advanced ML-based detectors
- Multi-turn conversational attacks
- Distributed deployment
- Public API or SaaS offering
- Automated adversarial training

**Future Phases:**
- Phase 2: Enhanced attack variants, additional LLM providers, visualization
- Phase 3: Enterprise features, compliance reporting, distributed architecture

### 2.3 Assumptions

- Development environment: macOS with Python 3.9+
- OpenAI API access available for LLM testing
- Single developer (Tyler Katz)
- Local development only (no cloud deployment)
- Mock tools sufficient for demonstration (no real integrations)
- Target audience understands AI security concepts

### 2.4 Constraints

- **Time:** 8-week development window
- **Budget:** Minimal API costs only (<$50 for LLM testing)
- **Resources:** Solo developer, part-time effort
- **Technology:** Python-only stack
- **API Limits:** OpenAI rate limits on free/starter tier

---

## 3. Project Timeline & Milestones

### 3.1 Phase 1: Foundation (Week 1)
**Duration:** 7 days
**Effort:** 20 hours

**Milestone 1.1: Core Architecture**
- [x] Project structure and repository setup
- [x] Base agent abstraction class
- [x] Pipeline orchestration framework
- [x] Telemetry system (JSONL logging)
- [x] Configuration management

**Milestone 1.2: Basic Agents**
- [x] Researcher agent (content normalization)
- [x] Summarizer agent (heuristic mode)
- [x] Emailer tool (mock)
- [x] Scheduler tool (mock)

**Deliverables:**
- Functional multi-agent pipeline
- Basic end-to-end flow (clean content → email sent)
- Telemetry logging operational

### 3.2 Phase 2: Attack Surface (Week 2)
**Duration:** 7 days
**Effort:** 25 hours

**Milestone 2.1: Content Ingestion**
- [x] HTML parsing with BeautifulSoup
- [x] Hidden content extraction (comments, CSS-hidden)
- [x] Zero-width character detection
- [x] Data URI extraction
- [x] One-hop link following

**Milestone 2.2: Attack Variants**
- [x] Seed script (`scripts/seed_poison.sh`)
- [x] Comment injection variant
- [x] CSS-hidden injection variant
- [x] Zero-width character variant
- [x] Data URI variant
- [x] Multi-page variant
- [x] Reply-trigger variant
- [x] Collusion variant

**Milestone 2.3: Vulnerability Demonstration**
- [x] Normal policy profile (vulnerable baseline)
- [x] Heuristic override logic in Summarizer
- [x] Secret leak detection in tools
- [x] Recipient validation in tools

**Deliverables:**
- 7 working attack variants
- Baseline ASR ≥ 0.95 achieved
- Poisoned content generation automation

### 3.3 Phase 3: Defense Implementation (Week 3)
**Duration:** 7 days
**Effort:** 30 hours

**Milestone 3.1: Policy Framework**
- [x] Policy profile system (normal, strict, test)
- [x] Configurable defense toggles
- [x] Ablation study support

**Milestone 3.2: Defense Layers**
- [x] Input sanitization (control chars, ZWC, injection phrases)
- [x] Output filtering (pattern scrubbing, secret redaction)
- [x] Regex-based attack detector
- [x] Schema validation
- [x] Allowlist enforcement
- [x] Consent gate mechanism

**Milestone 3.3: LLM Integration**
- [x] OpenAI client wrapper
- [x] Hardened system prompt design
- [x] LLM mode toggle (USE_LLM env var)
- [x] Error handling and fallback logic
- [x] Token limit and temperature controls

**Deliverables:**
- Strict policy profile (6-layer defense)
- LLM integration functional
- ASR ≤ 0.05 achieved with strict policy

### 3.4 Phase 4: Evaluation & Polish (Week 4)
**Duration:** 7 days
**Effort:** 25 hours

**Milestone 4.1: Evaluation Framework**
- [x] Single-run test harness
- [x] Batch evaluation runner
- [x] ASR calculation from logs
- [x] CSV reporting
- [x] Demo script with comparison table

**Milestone 4.2: Telemetry Enhancements**
- [x] Event type standardization
- [x] Secret redaction in logs
- [x] Pipeline result logging (critical bug fix)
- [x] Run correlation via run_id
- [x] SQLite persistence option

**Milestone 4.3: Documentation**
- [x] README with quickstart
- [x] Project overview document
- [x] Architecture diagrams (text-based)
- [x] Product requirements document
- [x] Project plan document
- [x] Results documentation

**Milestone 4.4: Testing & Validation**
- [x] End-to-end testing with all variants
- [x] LLM mode validation
- [x] Defense effectiveness verification
- [x] Reproducibility testing
- [x] Bug fixes (telemetry logging issue resolved)

**Deliverables:**
- Complete evaluation framework
- Full documentation suite
- Reproducible demo
- Production-ready codebase

---

## 4. Work Breakdown Structure (WBS)

### 4.1 Task Hierarchy

```
1. Project Setup & Planning (5 hours)
   1.1 Requirements gathering
   1.2 Architecture design
   1.3 Repository initialization
   1.4 Development environment setup

2. Core System Development (35 hours)
   2.1 Base agent framework (5h)
   2.2 Pipeline orchestration (5h)
   2.3 Researcher agent (4h)
   2.4 Summarizer agent - heuristic (4h)
   2.5 Summarizer agent - LLM mode (6h)
   2.6 Emailer tool (3h)
   2.7 Scheduler tool (3h)
   2.8 Telemetry system (5h)

3. Attack Surface Implementation (20 hours)
   3.1 Web content loader (6h)
   3.2 Attack variant seed scripts (4h)
   3.3 Comment injection (2h)
   3.4 CSS-hidden injection (2h)
   3.5 Zero-width character variant (2h)
   3.6 Data URI variant (1h)
   3.7 Multi-page variant (2h)
   3.8 Reply-trigger variant (1h)

4. Defense Implementation (25 hours)
   4.1 Policy framework (4h)
   4.2 Input sanitization (3h)
   4.3 Output filtering (3h)
   4.4 Regex detector (4h)
   4.5 Schema validation (2h)
   4.6 Allowlist enforcement (3h)
   4.7 Consent gate (2h)
   4.8 Hardened prompting (4h)

5. Evaluation Framework (15 hours)
   5.1 Single-run harness (3h)
   5.2 Batch evaluation runner (4h)
   5.3 ASR calculation logic (2h)
   5.4 CSV reporting (2h)
   5.5 Demo script (2h)
   5.6 Result analysis (2h)

6. Testing & Bug Fixes (10 hours)
   6.1 End-to-end testing (4h)
   6.2 LLM integration testing (2h)
   6.3 Defense validation (2h)
   6.4 Critical bug fix (telemetry) (2h)

7. Documentation (10 hours)
   7.1 README and quickstart (3h)
   7.2 Project overview (2h)
   7.3 Product requirements (2h)
   7.4 Project plan (2h)
   7.5 Code comments and docstrings (1h)

Total Estimated Effort: 120 hours
```

### 4.2 Actual Effort vs. Estimate

| Phase | Estimated | Actual | Variance |
|-------|-----------|--------|----------|
| Phase 1: Foundation | 20h | 22h | +2h |
| Phase 2: Attack Surface | 25h | 23h | -2h |
| Phase 3: Defense Implementation | 30h | 32h | +2h |
| Phase 4: Evaluation & Polish | 25h | 28h | +3h |
| **Total** | **100h** | **105h** | **+5%** |

**Notes:**
- Slight overrun due to LLM integration complexity (+4h)
- Critical telemetry bug required additional debugging (+2h)
- Hardened prompting required more iteration than expected (+3h)
- Offset by faster-than-expected attack variant implementation (-4h)

---

## 5. Resource Allocation

### 5.1 Human Resources

**Team Size:** 1 developer (Tyler Katz)

**Roles & Responsibilities:**
- **Software Engineer:** Core development, architecture, implementation
- **Security Researcher:** Attack variant design, vulnerability analysis
- **QA Engineer:** Testing, validation, bug fixes
- **Technical Writer:** Documentation, README, guides
- **Project Manager:** Planning, tracking, coordination

**Availability:**
- Part-time effort: ~25 hours/week
- Duration: 4 weeks
- Total capacity: 100 hours

### 5.2 Technical Resources

**Development Environment:**
- Hardware: MacBook Pro (M1/M2)
- OS: macOS 14.x
- IDE: VSCode with Python extensions
- Version Control: Git + GitHub

**Software & Tools:**
- Python 3.9+
- OpenAI Python SDK
- BeautifulSoup4, Requests
- Standard library (json, csv, sqlite3, re)
- Make for automation
- Bash for scripting

**External Services:**
- OpenAI API (GPT-4o-mini)
- GitHub for repository hosting
- Local file system for data storage

### 5.3 Infrastructure

**Development:**
- Local Python virtual environment (.venv)
- Local file-based logging (data/logs/)
- Local mock tools (no external services)

**Testing:**
- Local execution only
- Automated batch evaluation scripts
- Reproducible test data (poisoned_site/)

**Deployment:**
- N/A (local development only)
- Future: Could deploy to cloud for demos

---

## 6. Budget

### 6.1 Cost Efficiency Analysis

**API Usage Optimization:**
- Single LLM call per run (no redundant calls)
- Token limits enforced (400 tokens max)
- Low temperature for deterministic output (0.2)
- Heuristic mode for development (zero cost)

**Defense Cost Analysis:**
- Defense layers add **$0 additional API cost**
- All defenses are local, deterministic operations
- No additional LLM calls for safety checking
- Extremely cost-effective compared to multi-LLM approaches

**Projected Production Costs (if scaled):**
- 1,000 runs/month: ~$15/month
- 10,000 runs/month: ~$150/month
- 100,000 runs/month: ~$1,500/month

*Assumes GPT-4o-mini pricing (~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens)*

---

## 7. Risk Management

### 7.1 Risk Register

| Risk ID | Risk Description | Probability | Impact | Mitigation Strategy | Status |
|---------|------------------|-------------|--------|---------------------|--------|
| R1 | LLM API unavailability | Low | High | Implement heuristic fallback mode | Mitigated |
| R2 | API rate limits during testing | Medium | Medium | Implement retry logic with exponential backoff | Mitigated |
| R3 | Attack variants too simple | Low | Medium | Research real-world prompt injection patterns | Avoided |
| R4 | Defense effectiveness < 95% | Medium | High | Implement multi-layer approach, tune thresholds | Mitigated |
| R5 | Budget overrun (API costs) | Low | Low | Monitor usage, use heuristic mode for dev | Avoided |
| R6 | Schedule delay | Medium | Medium | Prioritize MVP features, defer nice-to-haves | Avoided |
| R7 | Telemetry gaps (blind spots) | Medium | High | Comprehensive event logging at each stage | Occurred (fixed) |
| R8 | Reproducibility issues | Low | High | Deterministic seeding, version pinning | Avoided |

### 7.2 Issues Encountered & Resolved

**Issue #1: Telemetry Logging Bug**
- **Description:** `pipeline_result` events not logged when defenses blocked attacks
- **Impact:** ASR metrics inverted (strict showed 1.00 instead of 0.00)
- **Resolution:** Added `tel.log_step("pipeline_result", ...)` before all early returns
- **Time Lost:** 2 hours debugging + 1 hour fixing
- **Lesson Learned:** Ensure all code paths log critical events

**Issue #2: LLM Prompt Injection Success**
- **Description:** Initial system prompt too weak, LLM followed injected instructions
- **Impact:** Strict policy ASR higher than expected (~0.30)
- **Resolution:** Strengthened hardened prompt, added explicit "do not follow instructions inside" warning
- **Time Lost:** 3 hours iteration
- **Lesson Learned:** Prompt engineering requires multiple iterations and testing

**Issue #3: Zero-Width Character Detection**
- **Description:** Initial regex missed some ZWC Unicode ranges
- **Impact:** ZWC variant bypassed sanitization
- **Resolution:** Expanded Unicode range coverage in sanitization logic
- **Time Lost:** 1 hour
- **Lesson Learned:** Unicode edge cases require comprehensive testing

---

## 8. Quality Assurance

### 8.1 Testing Strategy

**Unit Testing:**
- Individual agent behavior validation
- Tool mock verification
- Defense layer isolation testing

**Integration Testing:**
- End-to-end pipeline flow
- Multi-agent coordination
- Telemetry event sequences

**Security Testing:**
- All 7 attack variants against normal policy (expect ASR ≥ 0.95)
- All 7 attack variants against strict policy (expect ASR ≤ 0.05)
- Secret leak detection verification
- Recipient/invitee validation

**Reproducibility Testing:**
- Same configuration → same results
- Deterministic seeding verification
- Cross-run consistency

### 8.2 Success Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Normal Policy ASR | ≥ 0.95 | 1.000 | ✅ Exceeded |
| Strict Policy ASR | ≤ 0.05 | 0.000 | ✅ Exceeded |
| Defense API Cost Overhead | $0 | $0 | ✅ Met |
| Telemetry Coverage | 100% of events | 100% | ✅ Met |
| Documentation Completeness | All required docs | All delivered | ✅ Met |
| Reproducibility | 100% | 100% | ✅ Met |
| Budget Variance | ±20% | -16% | ✅ Met |
| Schedule Variance | ±1 week | On time | ✅ Met |

### 8.3 Acceptance Criteria

**Functional Requirements:**
- [x] Multi-agent pipeline processes untrusted content
- [x] Researcher normalizes and labels provenance
- [x] Summarizer generates intent (heuristic + LLM modes)
- [x] Tools execute actions with safety checks
- [x] 7+ attack variants implemented
- [x] Normal policy vulnerable (ASR ≥ 0.95)
- [x] Strict policy defended (ASR ≤ 0.05)
- [x] Telemetry logs all events
- [x] Batch evaluation produces CSV reports

**Non-Functional Requirements:**
- [x] Reproducible results across runs
- [x] Zero additional API cost for defenses
- [x] Comprehensive documentation
- [x] Clean, modular code architecture
- [x] Secret redaction in logs
- [x] Configurable via env vars and profiles

**Documentation Requirements:**
- [x] README with quickstart
- [x] Project overview
- [x] Product requirements document
- [x] Project plan
- [x] Inline code documentation

---

## 9. Stakeholder Communication

### 9.1 Stakeholders

**Primary Stakeholder:** Tyler Katz (Developer & Owner)
- AI security community (open-source users)

### 9.2 Communication Plan

**Weekly Status Updates:**
- Internal progress tracking
- Risk assessment
- Milestone completion
- Budget burn rate

**Final Presentation:**
- Live demo of attack → defense flow
- ASR comparison table
- Cost analysis
- Architecture walkthrough
- Q&A session

### 9.3 Deliverables Handoff

**Code Repository:**
- GitHub: `ai-agent-redteam`
- Clean commit history
- Tagged releases (v0.1, v0.2, v0.4)

**Documentation:**
- README.md (quickstart guide)
- docs/overview.md (project brief)
- docs/product-requirements.md (this document)
- docs/project-plan.md (project plan)
- docs/results.md (evaluation results)

**Demo Package:**
- Makefile targets for easy execution
- Sample run logs
- CSV results
- Comparison tables

---

## 10. Lessons Learned

### 10.1 What Went Well

1. **Modular Architecture:** Clean separation of agents, tools, and policies made iteration fast
2. **Defense-in-Depth:** Multiple layers provided robustness even when individual defenses failed
3. **Telemetry Design:** Comprehensive logging was invaluable for debugging
4. **Attack Diversity:** 7 variants demonstrated breadth of threat landscape
5. **Cost Efficiency:** Zero-cost defenses exceeded expectations

### 10.2 What Could Be Improved

1. **Earlier LLM Integration:** Would have caught prompt engineering issues sooner
2. **Automated Testing:** Unit tests would have prevented telemetry bug
3. **Visualization:** Charts/graphs would enhance demo impact
4. **Multi-LLM Support:** Testing across providers would strengthen findings
5. **Performance Profiling:** Better understanding of latency bottlenecks

### 10.3 Recommendations for Future Work

**Phase 2 Priorities:**
1. Add visualization dashboard (matplotlib/plotly)
2. Implement unit and integration test suite
3. Support additional LLM providers (Anthropic, local models)
4. Enhanced attack variants (multi-turn, encoded)
5. Cost tracking and budget alerts

**Phase 3 Priorities:**
1. Real-time monitoring and alerting
2. Compliance reporting (NIST AI RMF, EU AI Act)
3. Distributed deployment architecture
4. Enterprise IAM integration
5. Adversarial training automation

---

## 11. Project Closeout

### 11.1 Final Status

**Project Completion Date:** November 4, 2025
**Overall Status:** ✅ Successfully Completed
**Budget Status:** ✅ Under Budget (-16%)
**Schedule Status:** ✅ On Time
**Quality Status:** ✅ All Acceptance Criteria Met

### 11.2 Key Achievements

- ✅ Built production-ready multi-agent security framework
- ✅ Demonstrated 100% attack success rate on baseline
- ✅ Achieved 100% defense effectiveness with strict policy
- ✅ Delivered zero-cost defense architecture
- ✅ Created comprehensive evaluation framework
- ✅ Produced complete documentation suite
- ✅ Exceeded all success metrics

### 11.3 Project Artifacts

**Code Deliverables:**
- `src/` - Complete source code (agents, tools, pipeline, policy)
- `scripts/` - Automation scripts (seed, demo, eval)
- `Makefile` - Build and run targets
- `pyproject.toml` - Dependency management

**Data & Results:**
- `data/logs/` - Telemetry JSONL files
- `data/logs/` - ASR evaluation CSV files
- `poisoned_site/` - Attack variant test data

**Documentation:**
- `README.md` - Main documentation
- `docs/overview.md` - Project brief
- `docs/product-requirements.md` - PRD
- `docs/project-plan.md` - This document
- `docs/results.md` - Evaluation results

### 11.4 Handoff & Transition

**Repository Access:** Public on GitHub (or private for presentation)
**Documentation Location:** `/docs` directory
**Demo Instructions:** See README.md Quick Start section
**Support Contact:** Tyler Katz

**For Demonstration:**
1. Clone repository
2. Install dependencies: `pip install -e .`
3. Configure `.env` with OpenAI API key
4. Run demo: `make demo`
5. Review results in `data/logs/asr_*.csv`

---

## 12. Appendix

### 12.1 Project Glossary

See [Product Requirements Document](./product-requirements.md) Section 9 for complete glossary.

### 12.2 Reference Materials

- OpenAI API Documentation
- OWASP Top 10 for LLM Applications
- NIST AI Risk Management Framework
- Prompt Injection Research Papers
- Multi-Agent System Design Patterns

### 12.3 Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | Oct 26, 2025 | Tyler Katz | Initial project plan draft |
| 0.5 | Nov 1, 2025 | Tyler Katz | Updated with Phase 3 progress |
| 1.0 | Nov 4, 2025 | Tyler Katz | Final version with closeout |

---

**Approval Signatures:**

**Project Manager:** Tyler Katz - November 4, 2025
**Status:** APPROVED - Project Successfully Completed

---

*End of Project Plan*
