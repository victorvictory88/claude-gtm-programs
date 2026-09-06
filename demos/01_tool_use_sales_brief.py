#!/usr/bin/env python3
"""Demo 01: tool use to extract account facts, then write a one-page sales brief.

Uses the Anthropic Messages API with a tool for structured fact extraction.
Fictional account data only (Acme Energy).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

DEFAULT_MODEL = "claude-sonnet-4-20250514"
SAMPLE_PATH = Path(__file__).resolve().parent / "sample_data" / "account.json"

EXTRACT_TOOL = {
    "name": "extract_account_facts",
    "description": (
        "Extract structured account facts needed for a one-page sales brief. "
        "Call this before drafting narrative prose."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "account_name": {"type": "string"},
            "industry": {"type": "string"},
            "segment": {"type": "string"},
            "geo": {"type": "string"},
            "primary_contact": {"type": "string"},
            "primary_pain": {"type": "string"},
            "buying_stage": {"type": "string"},
            "stakeholders": {
                "type": "array",
                "items": {"type": "string"},
            },
            "next_milestones": {
                "type": "array",
                "items": {"type": "string"},
            },
            "risks_or_competitors": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": [
            "account_name",
            "industry",
            "primary_contact",
            "primary_pain",
            "buying_stage",
        ],
    },
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


def load_account(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def run_brief(account: dict, model: str) -> str:
    import anthropic

    client = anthropic.Anthropic()
    account_blob = json.dumps(account, indent=2)

    messages = [
        {
            "role": "user",
            "content": (
                "You are helping an AMER GTM Programs Manager prepare a one-page "
                "sales brief for an AE/SE team.\n\n"
                "Step 1: Call extract_account_facts with facts from the JSON.\n"
                "Step 2: After tool results return, write a one-page markdown sales "
                "brief with sections: Snapshot, Pain and impact, Stakeholders, "
                "Buying stage and next steps, Risks, Suggested discovery angles.\n"
                "Rules: do not invent metrics or ROI; use only provided facts; "
                "keep it concise and actionable.\n\n"
                f"Account JSON:\n{account_blob}"
            ),
        }
    ]

    first = client.messages.create(
        model=model,
        max_tokens=1024,
        tools=[EXTRACT_TOOL],
        messages=messages,
    )

    tool_results = []
    assistant_content = first.content
    for block in assistant_content:
        if block.type == "tool_use":
            # Echo validated subset of account facts; demo shows tool loop pattern.
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(block.input, indent=2),
                }
            )

    if not tool_results:
        # Model skipped tool; still ask for brief from raw account.
        messages.append({"role": "assistant", "content": assistant_content})
        messages.append(
            {
                "role": "user",
                "content": "Write the one-page sales brief now using only the account JSON.",
            }
        )
    else:
        messages.append({"role": "assistant", "content": assistant_content})
        messages.append({"role": "user", "content": tool_results})

    second = client.messages.create(
        model=model,
        max_tokens=2048,
        tools=[EXTRACT_TOOL],
        messages=messages,
    )

    parts = []
    for block in second.content:
        if hasattr(block, "text"):
            parts.append(block.text)
    return "\n".join(parts).strip() or json.dumps(
        {"error": "No text content in model response", "stop_reason": second.stop_reason},
        indent=2,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract account facts via tool use, then write a sales brief."
    )
    parser.add_argument(
        "--account",
        type=Path,
        default=SAMPLE_PATH,
        help="Path to account JSON (default: sample_data/account.json)",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Anthropic model id (default: {DEFAULT_MODEL})",
    )
    args = parser.parse_args()

    require_api_key()
    account = load_account(args.account)
    brief = run_brief(account, args.model)
    print(brief)


if __name__ == "__main__":
    main()
