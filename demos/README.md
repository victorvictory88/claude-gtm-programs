# Demos

Two CLI demos using the Anthropic Python SDK Messages API.

**Default model:** `claude-sonnet-4-20250514` (documented Messages API model id; override with `--model`).

## Prerequisites

```bash
cd /path/to/claude-gtm-programs
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

Both scripts exit with code `2` if `ANTHROPIC_API_KEY` is missing.

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

## Sample data

- `account.json` - Acme Energy (fictional)
- `program_inputs.json` - AMER mid-market AI discovery play inputs (fictional; TBD baselines on purpose)

## Visual examples

![Sample structured program plan JSON](../docs/images/program_plan_json.png)

*Sample structured program plan JSON (matches demo 02 output shape).*

![Seller play one-pager for fictional Northwind Retail](../docs/images/seller_play_card.png)

*Related seller-play packaging example (skill output style).*
