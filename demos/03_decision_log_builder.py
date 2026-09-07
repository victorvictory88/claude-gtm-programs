#!/usr/bin/env python3
"""Build a printable decision log from sample JSON (no API required).

Usage:
  python demos/03_decision_log_builder.py
  python demos/03_decision_log_builder.py --input demos/sample_data/decision_log.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def render(data: dict) -> str:
    lines: list[str] = []
    lines.append(f"Decision: {data.get('decision', '')}")
    lines.append(f"Date: {data.get('date', '')}")
    lines.append(f"Context: {data.get('context', '')}")
    lines.append("")
    lines.append("Competing hypotheses:")
    for i, h in enumerate(data.get("competing_hypotheses", []), 1):
        lines.append(
            f"{i}. {h.get('team')}: {h.get('claim')} | metric: {h.get('metric')} | "
            f"owner: {h.get('owner')} | source: {h.get('source_system')}"
        )
    lines.append("")
    lines.append(f"Chosen path: {data.get('chosen_path', '')}")
    lines.append(f"Rationale: {data.get('rationale', '')}")
    lines.append("Falsifiers:")
    for f in data.get("falsifiers", []):
        lines.append(f"- {f}")
    owners = data.get("owners", {})
    lines.append(
        "Owners: "
        + ", ".join(f"{k}={v}" for k, v in owners.items())
    )
    follow = data.get("follow_ups", {})
    lines.append(
        "Follow-ups: "
        + ", ".join(f"{k}={v}" for k, v in follow.items())
    )
    lines.append("Open questions:")
    for q in data.get("open_questions", []):
        lines.append(f"- {q}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a GTM decision log from JSON")
    default = Path(__file__).resolve().parent / "sample_data" / "decision_log.json"
    parser.add_argument("--input", type=Path, default=default, help="Path to decision_log JSON")
    args = parser.parse_args()
    if not args.input.exists():
        print(f"Missing input: {args.input}", file=sys.stderr)
        return 1
    print(render(load(args.input)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
