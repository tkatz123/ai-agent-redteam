# Streamlit Dashboard

## Overview

This interactive dashboard provides real-time monitoring and analysis for the AI Agent Red Team Framework. It allows you to run attacks, visualize defense effectiveness, and analyze Attack Success Rate (ASR) metrics through a web interface.

## Features

- **Attack Control Panel**: Run individual attacks with any variant and defense configuration
- **Live Execution**: Stream stdout/stderr from seed scripts and pipeline runs
- **Defense Timing Analysis**: Track execution time for each defense layer
- **ASR Metrics**: Aggregate and visualize attack success rates by variant and defense preset
- **Make Command Integration**: Execute batch evaluations and demos directly from the UI
- **Demo Readiness Checklist**: Verify environment setup before running attacks
- **Historical Analysis**: View metrics from all logged runs, not just current session

## Installation

### Install Dependencies

From the project root directory:

```bash
pip install -e .
```

This installs all dependencies including:
- `streamlit` - Web application framework
- `pandas` - Data manipulation and analysis
- `altair` - Declarative visualization library
- `python-dateutil` - ISO 8601 timestamp parsing
- Plus all existing project dependencies

## Running the Dashboard

From the project root directory:

```bash
streamlit run streamlit_app/app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`.

## Usage Guide

### Attack Controls (Left Sidebar)

1. **Attack Variant**: Select from 8 attack types:
   - `clean` - No attack (baseline benign content)
   - `comment` - HTML comment injection
   - `css` - CSS-hidden text injection
   - `zwc` - Zero-width character obfuscation
   - `multipage` - Multi-page attack
   - `reply` - Conditional trigger (reply-chain)
   - `evasion` - Evasion techniques
   - `collusion` - Agent collusion attack

2. **Mode**: Choose `attack` (default) or `clean`

3. **Defense Preset**:
   - `baseline` - Vulnerable (policy=normal, no defenses)
   - `strict` - Hardened (policy=strict, all defenses enabled)
   - `ablation` - Custom defense profile (D1, D2, D2+structured)

4. **Tool Selection**: `auto` (default), `email`, or `schedule`

5. Click **▶️ Run Attack** to execute

### Defense Timing Panel

After each run, view:
- **Per-layer timing**: How long each defense took (Output Filter, Regex Detector, Schema Validation, Allowlist, Consent Gate)
- **Total time**: End-to-end pipeline execution
- **Session averages**: Mean timing across all runs in current session
- **All runs table**: Complete history with timing breakdown

### ASR Metrics & Charts

Two tabs available:
- **Session Data**: ASR for runs in the current session
- **All Historical Data**: ASR from all logged runs in `data/dashboard/streamlit_runs.csv`

Features:
- Filter by attack variant and defense configuration
- Interactive bar charts (Altair)
- Aggregated ASR with total run counts and compromise counts
- Multi-config comparison

### Make Commands

Execute batch operations:
- **make demo** - Run quick demo with ASR comparison table
- **make dashboard** - Regenerate dashboard (if applicable)
- **make eval-5x300** - Large-scale evaluation (5 configs × 300 runs)

Each command:
- Shows live output in expandable log pane
- Displays elapsed time while running
- Shows ✅/❌ status when complete
- Prevents duplicate concurrent runs

### Demo Readiness Checklist

The sidebar shows status for:
- ✅ Python accessibility and version
- ✅ `scripts/seed_poison.sh` exists and is executable
- ✅ `data/` directory exists
- ℹ️ `poisoned_site/` exists (created on first seed)

## Data Storage

### Session State
- Runs are stored in `st.session_state.session_runs` (in-memory, clears on refresh)

### Persistent Storage
- **JSONL Logs**: `data/logs/run-<timestamp>.jsonl` (one per pipeline run)
- **Dashboard CSV**: `data/dashboard/streamlit_runs.csv` (appended after each attack)

### CSV Schema

```
ts,run_id,variant,policy,defense_profile,tool,compromised,
t_output_filter_ms,t_regex_ms,t_schema_ms,t_policy_ms,t_consent_ms,t_total_ms
```

- `ts`: ISO 8601 timestamp (UTC)
- `run_id`: Unique run identifier
- `variant`: Attack type (e.g., "comment", "css")
- `policy`: "normal" or "strict"
- `defense_profile`: Optional ablation profile (e.g., "D1", "D2")
- `tool`: "email" or "schedule"
- `compromised`: 1 = attack succeeded, 0 = blocked
- `t_*_ms`: Milliseconds from run start to each defense layer (or `None` if not triggered)
- `t_total_ms`: Total pipeline execution time

## Timing Methodology

The dashboard computes defense timings from JSONL event logs:

1. **t0**: Earliest timestamp in the run
2. **Event → Bucket Mapping**:
   - `output_filter` → `t_output_filter_ms`
   - `detector_regex` or `detector_block` → `t_regex_ms`
   - `schema_block` → `t_schema_ms`
   - `policy_block` → `t_policy_ms`
   - `consent_block` → `t_consent_ms`
3. **Total Time**: `(pipeline_result or finish timestamp) - t0`

Only the **first occurrence** of each event type is timed. If a defense didn't fire, its timing column is `None`.

## Security Notes

- All shell arguments are sanitized using `shlex.quote()`
- Only whitelisted commands are executable (no arbitrary shell input)
- Subprocess output is captured safely with `text=True` and `stdout=PIPE`
- No external APIs or network calls (fully local)

## Troubleshooting

### Dashboard won't start
- Ensure dependencies are installed: `pip install -e .`
- Check you're in the project root when running `streamlit run streamlit_app/app.py`

### Attacks not running
- Verify `scripts/seed_poison.sh` is executable: `chmod +x scripts/seed_poison.sh`
- Check Python is accessible: `python --version`
- Ensure project dependencies are installed: `pip install -e .`

### No historical data showing
- Run at least one attack to populate `data/dashboard/streamlit_runs.csv`
- Check file permissions on `data/` directory

### Timing columns are blank
- Ensure JSONL logs include `ts` fields (ISO 8601 timestamps)
- Verify events have correct `type` values (`output_filter`, `detector_regex`, etc.)

### Make commands fail
- Ensure `make` is installed: `make --version`
- Check your `Makefile` has the expected targets (`demo`, `dashboard`, `eval-5x300`)

## Development Notes

### File Structure
```
streamlit_app/
├── app.py     # Main Streamlit application
└── utils.py   # Helper functions (subprocess, JSONL parsing, timing)
```

### Key Functions (app.py)
- `run_seed_and_attack()` - Execute seed + pipeline run
- `parse_latest_run_jsonl()` - Extract metrics from latest JSONL
- `compute_defense_timings()` - Calculate per-layer timing from events
- `aggregate_asr()` - Compute ASR by variant and defense config
- `launch_make()` - Execute make targets with output capture

### Extending the Dashboard

To add new features:
1. **New attack variant**: Add to `ATTACK_VARIANTS` list in `app.py`
2. **New defense layer**: Add timing bucket to `compute_defense_timings()` and update `CSV_FIELDNAMES`
3. **New metric**: Extend `aggregate_asr()` or add new aggregation function
4. **New visualization**: Use Altair or Plotly to create charts from `pd.DataFrame`

## License

Same as main project (see root `LICENSE` file).

## Support

For issues or questions:
1. Check this README
2. Review main project documentation (`docs/overview.md`, `docs/product-requirements.md`)
3. Open an issue on the project repository
