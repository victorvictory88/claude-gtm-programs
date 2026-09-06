#!/usr/bin/env python3
"""Offline eval harness for GTM program plans. No API calls.

Loads fixtures listed in cases/program_plan_cases.jsonl, scores against
rubric dimensions, prints a JSON summary.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "fixtures"
CASES = ROOT / "cases" / "program_plan_cases.jsonl"

DIMENSIONS = (
    "baseline_clarity",
    "measurable_metrics",
    "named_owners",
    "no_fluff",
)


def load_cases(path: Path) -> list[dict]:
    cases = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            cases.append(json.loads(line))
    return cases


def load_plan(rel: str) -> dict:
    path = ROOT / rel
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def score_baseline_clarity(plan: dict) -> int:
    baseline = plan.get("baseline") or {}
    if not isinstance(baseline, dict) or not baseline:
        return 0
    notes = str(baseline.get("current_state_notes") or "").strip()
    has_scope = all(
        str(baseline.get(k) or "").strip()
        for k in ("audience", "geo", "segment", "launch_date")
    )
    if not has_scope:
        return 0
    vague = notes.lower() in {"", "n/a"} or "transform" in notes.lower()
    if notes and not vague and ("TBD" in notes or "baseline" in notes.lower() or "CRM" in notes):
        return 2
    if notes and not vague:
        return 1
    return 1 if has_scope else 0


def score_measurable_metrics(plan: dict) -> int:
    metrics = plan.get("metrics") or []
    if not metrics:
        return 0
    primary = [m for m in metrics if str(m.get("role", "")).lower() == "primary"]
    if not primary:
        primary = metrics[:1]
    def ok(m: dict) -> bool:
        name = str(m.get("name") or "").strip()
        unit = str(m.get("unit") or "").strip()
        source = str(m.get("source") or "").strip()
        owner = str(m.get("owner") or "").strip()
        if not name or name.lower() in {"more pipeline", "success", "growth"}:
            return False
        return bool(unit or source) and bool(owner or "TBD" in str(m.get("baseline_value")))

    good = sum(1 for m in metrics if ok(m))
    if good >= 2 and primary and ok(primary[0]):
        return 2
    if good >= 1:
        return 1
    return 0


def score_named_owners(plan: dict) -> int:
    owners = plan.get("owners") or {}
    if not isinstance(owners, dict):
        return 0
    keys = ("program", "sales_sponsor", "enablement", "analytics")
    filled = sum(1 for k in keys if str(owners.get(k) or "").strip())
    if filled == 4:
        return 2
    if filled >= 2:
        return 1
    return 0


FLUFF_MARKERS = (
    "transform",
    "excellence",
    "synergy",
    "unlock",
    "cutting-edge",
    "delve",
    "leverage",
    "harness",
    "tapestry",
)


def score_no_fluff(plan: dict) -> int:
    blob = json.dumps(plan).lower()
    hits = sum(1 for w in FLUFF_MARKERS if w in blob)
    metrics = plan.get("metrics") or []
    invented = False
    for m in metrics:
        bv = str(m.get("baseline_value") or "").lower()
        if bv in {"a lot", "huge", "massive"}:
            invented = True
    milestones = plan.get("milestones") or []
    if hits >= 2 or invented:
        return 0
    if hits == 1 or not milestones:
        return 1
    return 2


SCORERS = {
    "baseline_clarity": score_baseline_clarity,
    "measurable_metrics": score_measurable_metrics,
    "named_owners": score_named_owners,
    "no_fluff": score_no_fluff,
}


def evaluate(plan: dict) -> dict:
    scores = {dim: SCORERS[dim](plan) for dim in DIMENSIONS}
    total = sum(scores.values())
    passed = total >= 6 and all(v > 0 for v in scores.values())
    return {"scores": scores, "total": total, "max": 8, "pass": passed}


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline GTM program plan eval harness")
    parser.add_argument(
        "--cases",
        type=Path,
        default=CASES,
        help="JSONL cases file",
    )
    args = parser.parse_args()

    cases = load_cases(args.cases)
    results = []
    for case in cases:
        plan = load_plan(case["fixture"])
        ev = evaluate(plan)
        results.append(
            {
                "id": case["id"],
                "fixture": case["fixture"],
                "expect_pass": case.get("expect_pass"),
                "expect_match": case.get("expect_pass") == ev["pass"],
                **ev,
            }
        )

    summary = {
        "harness": "evals/harness.py",
        "rubric": "evals/rubrics/gtm_program.md",
        "case_count": len(results),
        "passed_cases": sum(1 for r in results if r["pass"]),
        "expect_matches": sum(1 for r in results if r.get("expect_match")),
        "results": results,
    }
    print(json.dumps(summary, indent=2))

    # Non-zero exit if expectation mismatch (useful in CI)
    if any(not r.get("expect_match") for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
