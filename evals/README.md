# Evals

Offline evaluation for structured GTM program plans. No API key required.

## What it checks

Rubric dimensions (see `rubrics/gtm_program.md`):

- baseline clarity
- measurable metrics
- named owners
- no fluff

Fixtures:

- `fixtures/good_plan.json` - should pass
- `fixtures/weak_plan.json` - should fail

## Run

```bash
python evals/harness.py
```

Prints a JSON summary with per-case scores. Exit code `1` if a case does not match its `expect_pass` flag.

## Visual examples

![Eval harness terminal JSON summary](../docs/images/eval_harness_terminal.png)

*Terminal-style view of the JSON summary from `python evals/harness.py`.*

![Sample structured program plan JSON](../docs/images/program_plan_json.png)

*Fixture-shaped program plan used by the offline evals.*

![Attribution review dashboard mock](../docs/images/attribution_review_dashboard.png)

*Related monthly readout shape (skill theme; not scored by the harness).*
