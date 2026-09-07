# Demos

CLI demos using the Anthropic Python SDK Messages API (01-02) plus an offline decision-log builder (03).

**Default model (API demos):** `claude-sonnet-4-20250514` (override with `--model`).

## Prerequisites

```bash
cd /path/to/claude-gtm-programs
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

Scripts 01 and 02 exit with code `2` if `ANTHROPIC_API_KEY` is missing. Script 03 needs no API key.

## 01 - Tool use sales brief

Loads fictional `sample_data/account.json` (Acme Energy), calls a tool to extract account facts, then drafts a one-page sales brief.

```bash
python demos/01_tool_use_sales_brief.py
python demos/01_tool_use_sales_brief.py --account demos/sample_data/account.json --model claude-sonnet-4-20250514
```

![Tool-use sales brief demo flow](../docs/images/demo_tool_use_flow.png)

*Tool-use flow: load Acme Energy JSON, call tool, draft brief.*

## 02 - Structured program plan

Loads fictional `sample_data/program_inputs.json` and returns a JSON program plan with name, baseline, metrics, owners, and milestones.

```bash
python demos/02_structured_program_plan.py --pretty
```

## 03 - Decision log builder (offline)

Renders a single version of truth from `sample_data/decision_log.json` (Sales vs Marketing hypotheses). No API key.

```bash
python demos/03_decision_log_builder.py
python demos/03_decision_log_builder.py --input demos/sample_data/decision_log.json
```

## Sample data

- `account.json` - Acme Energy (fictional)
- `program_inputs.json` - AMER mid-market AI discovery play inputs (fictional; TBD baselines on purpose)
- `decision_log.json` - competing Sales vs Marketing hypotheses (fictional)
- `experiment_design.json` - control vs treatment staged rollout template (fictional)

## Visual examples

![Sample structured program plan JSON](../docs/images/program_plan_json.png)

*Sample structured program plan JSON (matches demo 02 output shape).*

![Seller play one-pager for fictional Northwind Retail](../docs/images/seller_play_card.png)

*Related seller-play packaging example (skill output style).*

![Decision log aligning Sales vs Marketing](../docs/images/decision_log_truth.png)

*Decision log as one version of truth across functions.*
