"""Utility functions for Streamlit dashboard."""
import os
import json
import csv
import shlex
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Generator, Dict, List, Any
from dateutil import parser as dateparser


def safe_quote(arg: str) -> str:
    """Safely quote shell arguments."""
    return shlex.quote(arg)


def get_project_root() -> Path:
    """Get project root directory (parent of streamlit_app)."""
    return Path(__file__).parent.parent


def ensure_dirs():
    """Ensure required directories exist."""
    root = get_project_root()
    (root / "data" / "dashboard").mkdir(parents=True, exist_ok=True)
    (root / "data" / "logs").mkdir(parents=True, exist_ok=True)


def parse_iso_timestamp(ts_str: str) -> Optional[datetime]:
    """Parse ISO 8601 timestamp string to datetime."""
    try:
        return dateparser.isoparse(ts_str)
    except (ValueError, TypeError):
        return None


def read_jsonl(file_path: Path) -> List[Dict[str, Any]]:
    """Read JSONL file and return list of dicts."""
    entries = []
    if not file_path.exists():
        return entries

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def get_latest_run_jsonl() -> Optional[Path]:
    """Get path to most recent run-*.jsonl file."""
    root = get_project_root()
    log_dir = root / "data" / "logs"

    if not log_dir.exists():
        return None

    run_files = sorted(log_dir.glob("run-*.jsonl"))
    return run_files[-1] if run_files else None


def get_all_run_jsonl() -> List[Path]:
    """Get all run-*.jsonl files."""
    root = get_project_root()
    log_dir = root / "data" / "logs"

    if not log_dir.exists():
        return []

    return sorted(log_dir.glob("run-*.jsonl"))


def stream_process_output(proc: subprocess.Popen) -> Generator[str, None, None]:
    """Stream stdout and stderr from process."""
    if proc.stdout:
        for line in iter(proc.stdout.readline, ''):
            if line:
                yield line.rstrip()

    # Wait for process to complete
    proc.wait()


def launch_subprocess(
    cmd: List[str],
    cwd: Optional[Path] = None
) -> subprocess.Popen:
    """Launch subprocess with output capture."""
    if cwd is None:
        cwd = get_project_root()

    return subprocess.Popen(
        cmd,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )


def get_python_command() -> str:
    """Get the correct Python command (prefer venv, then python3, then python)."""
    root = get_project_root()

    # Check for virtualenv python first
    venv_python = root / ".venv" / "bin" / "python"
    if venv_python.exists():
        return str(venv_python)

    # Fall back to system python
    for cmd in ["python3", "python"]:
        try:
            result = subprocess.run(
                [cmd, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return cmd
        except Exception:
            continue
    return "python"  # Fallback


def check_python() -> Dict[str, Any]:
    """Check if Python is accessible."""
    # Try python3 first (common on macOS/Linux), then python
    for cmd in ["python3", "python"]:
        try:
            result = subprocess.run(
                [cmd, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip() or result.stderr.strip()
                return {
                    "ok": True,
                    "version": version,
                    "command": cmd
                }
        except Exception:
            continue

    return {"ok": False, "error": "Python not found (tried python3 and python)"}


def check_seed_script() -> bool:
    """Check if seed_poison.sh exists and is executable."""
    root = get_project_root()
    script = root / "scripts" / "seed_poison.sh"
    return script.exists() and os.access(script, os.X_OK)


def check_poisoned_site() -> bool:
    """Check if poisoned_site directory exists."""
    root = get_project_root()
    return (root / "poisoned_site").exists()


def read_csv_safe(file_path: Path) -> List[Dict[str, Any]]:
    """Safely read CSV file."""
    if not file_path.exists():
        return []

    rows = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except Exception:
        pass

    return rows


def append_to_csv(file_path: Path, row: Dict[str, Any], fieldnames: List[str]):
    """Append row to CSV file (create if doesn't exist)."""
    file_exists = file_path.exists()

    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def get_run_metadata(entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Extract run metadata from JSONL entries."""
    metadata = {
        "run_id": None,
        "variant": None,
        "policy": None,
        "defense_profile": None,
        "tool": None
    }

    for entry in entries:
        if entry.get("type") == "meta":
            metadata["run_id"] = entry.get("run_id")
            metadata["variant"] = entry.get("variant")
            metadata["policy"] = entry.get("policy")
            metadata["defense_profile"] = entry.get("defense_profile")
        elif entry.get("type") == "pipeline_result":
            metadata["tool"] = entry.get("tool")

    return metadata
