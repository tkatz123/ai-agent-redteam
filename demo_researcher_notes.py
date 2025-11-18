#!/usr/bin/env python3
"""
Demo script to show Researcher agent output for presentations.
Loads the poisoned site and shows what the Researcher creates.
"""

from src.tools.webloader import load_page_follow_one
from src.agents.researcher import Researcher

def main():
    print("=" * 70)
    print("RESEARCHER AGENT DEMO - What the AI Actually Reads")
    print("=" * 70)
    print()

    # Load the poisoned content
    html, visible, comments, hidden = load_page_follow_one(
        "poisoned_site/index.html",
        include_hidden=True,
    )

    print("INPUT - What humans see in browser:")
    print("-" * 70)
    print(visible[:200])
    print()

    print("INPUT - Hidden in HTML comments (invisible in browser):")
    print("-" * 70)
    print(comments)
    print()

    # Create researcher and generate notes (no telemetry needed for demo)
    researcher = Researcher(telemetry=None)
    trust = {
        "visible": "untrusted-web",
        "comments": "untrusted-web",
        "hidden": "untrusted-web"
    }

    notes = researcher.ingest(visible, comments, hidden, trust=trust)

    print("OUTPUT - Researcher Agent's Structured Notes:")
    print("-" * 70)
    print(notes)
    print()
    print("=" * 70)
    print("Notice:")
    print("  ✓ Clear channel separation (VISIBLE vs COMMENTS)")
    print("  ✓ Provenance labels (<<<UNTRUSTED:...>>>)")
    print("  ✓ Malicious instruction is preserved and passed downstream")
    print("  ✓ AI agent will read ALL of this content")
    print("=" * 70)

if __name__ == "__main__":
    main()
