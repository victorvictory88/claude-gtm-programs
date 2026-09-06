#!/usr/bin/env python3
"""Demo 02: produce a structured JSON GTM program plan via the Messages API.

Outputs name, baseline, metrics, owners, and milestones.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

DEFAULT_MODEL = "claude-sonnet-4-20250514"
SAMPLE_PATH = Path(__file__).resolve().parent / "sample_data" / "program_inputs.json"

PLAN_SCHEMA_HINT = {
    "name": "string",
    "baseline": {
        "audience": "string",
        "geo": "string",
        "segment": "string",
        "launch_date": "string",
        "current_state_notes": "string",
    },
    "metrics": [
        {
            "name": "string",
            "role": "primary|supporting",
            "unit": "string",
            "baseline_value": "string or number or TBD",
            "source": "string",
            "owner": "string",
        }
    ],
    "owners": {
        "program": "string",
        "sales_sponsor": "string",
        "enablement": "string",
        "analytics": "string",
    },
    "milestones": [
        {
            "name": "string",
            "due": "string",
            "owner": "string",
            "done_when": "string",
        }
    ],
}


def require_api_key() -> str:
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        print(
            "ANTHROPIC_API_KEY is missing. Export it or copy .env.example to .env.",
            file=sys.stderr,
        )
        sys.exit(2)
    return key


def load_inputs(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def run_plan(inputs: dict, model: str) -> dict:
    import anthropic

    client = anthropic.Anthropic()
    payload = json.dumps(inputs, indent=2)
    schema = json.dumps(PLAN_SCHEMA_HINT, indent=2)

    message = client.messages.create(
        model=model,
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": (
                    "Build a structured GTM program plan as a single JSON object.\n"
                    "Follow this shape exactly (values filled from inputs):\n"
                    f"{schema}\n\n"
                    "Rules:\n"
                    "- Do not invent win rates, pipeline dollars, or customer secrets.\n"
                    "- Use TBD with an owner when a baseline number is missing.\n"
                    "- Include at least one primary metric and one supporting metric.\n"
                    "- Include at least three milestones covering baseline lock, "
                    "enablement launch, and first attribution review.\n"
                    "- Return JSON only, no markdown fences.\n\n"
                    f"Program inputs:\n{payload}"
                ),
            }
        ],
    )

    text_parts = []
    for block in message.content:
        if hasattr(block, "text"):
            text_parts.append(block.text)
    raw = "\n".join(text_parts).strip()

    # Tolerate accidental markdown fences
    if raw.startswith("```"):
        lines = raw.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        raw = "\n".join(lines).strip()

    return json.loads(raw)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Produce a structured JSON GTM program plan."
    )
    parser.add_argument(
        "--inputs",
        type=Path,
        default=SAMPLE_PATH,
        help="Path to program inputs JSON (default: sample_data/program_inputs.json)",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Anthropic model id (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output",
    )
    args = parser.parse_args()

    require_api_key()
    inputs = load_inputs(args.inputs)
    plan = run_plan(inputs, args.model)
    if args.pretty:
        print(json.dumps(plan, indent=2))
    else:
        print(json.dumps(plan))


if __name__ == "__main__":
    main()
