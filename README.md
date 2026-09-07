# claude-gtm-programs

Public toolkit and reference for **Claude skills** applied to **GTM Programs** work.

This repo shows how Claude skills, small demos, offline evals, and a short workshop fit real GTM Programs themes: baselines before launch, packaging wins into seller plays, attribution reviews, AI SaaS discovery coaching, and measured enablement.

Author: **Albert Chan**  
LinkedIn: [linkedin.com/in/albe88](https://www.linkedin.com/in/albe88)

Fictional accounts only: **Acme Energy**, **Northwind Retail**. No real customer secrets.

## What's inside

| Folder | Maps to GTM Programs work |
|--------|---------------------------|
| `skills/` | Reusable agent instructions for baseline, play packaging, attribution, discovery, enablement |
| `demos/` | Messages API demos: tool-use sales brief; structured JSON program plan |
| `evals/` | Offline rubric scoring for program plans (no API) |
| `teaching/` | 45-minute workshop for business leaders + baseline exercise |

**Default demo model:** `claude-sonnet-4-20250514` (override with `--model`).


## Visual examples

Screenshots for a quick look without running code. Regenerate with `python scripts/generate_visuals.py` (needs `pillow`).

![Repo architecture: skills, demos, evals, teaching](docs/images/architecture.png)

*Repo map: skills, demos, evals, and teaching folders.*

![Five Claude skills as cards](docs/images/skills_grid.png)

*Skills grid: program-baseline, seller-play-packager, attribution-review, discovery-coach, enablement-outline.*

![Program baseline card for fictional Acme Energy](docs/images/program_baseline_card.png)

*Sample program baseline card (Acme Energy, fictional).*

![Seller play one-pager for fictional Northwind Retail](docs/images/seller_play_card.png)

*One-page seller play mock (Northwind Retail, fictional).*

![Discovery coach flow](docs/images/discovery_coach_flow.png)

*Discovery coach flow: context through post-call capture.*

![Attribution review dashboard mock](docs/images/attribution_review_dashboard.png)

*Mock monthly attribution review with influence vs credit.*

![Eval harness terminal JSON summary](docs/images/eval_harness_terminal.png)

*Offline eval summary from `python evals/harness.py`.*

![Pretty sample structured program plan JSON](docs/images/program_plan_json.png)

*Sample structured program plan JSON (from fixtures).*

![Workshop agenda timeline](docs/images/workshop_agenda.png)

*45-minute workshop agenda timeline.*

![Tool-use sales brief demo flow](docs/images/demo_tool_use_flow.png)

*Demo 01 tool-use flow: load account, call tool, draft brief.*


## Quickstart

```bash
cd claude-gtm-programs
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # then set ANTHROPIC_API_KEY
export ANTHROPIC_API_KEY=sk-ant-...

# Demos (exit code 2 if key missing)
python demos/01_tool_use_sales_brief.py
python demos/02_structured_program_plan.py --pretty

# Offline evals (no API key)
python evals/harness.py
```

## Install skills (Claude / Cursor)

Copy each skill folder into your skills directory so the agent can load `SKILL.md`:

```bash
# Example: Claude Code / Cursor skills location may vary by setup
cp -R skills/program-baseline <YOUR_SKILLS_DIR>/program-baseline
cp -R skills/seller-play-packager <YOUR_SKILLS_DIR>/seller-play-packager
cp -R skills/attribution-review <YOUR_SKILLS_DIR>/attribution-review
cp -R skills/discovery-coach <YOUR_SKILLS_DIR>/discovery-coach
cp -R skills/enablement-outline <YOUR_SKILLS_DIR>/enablement-outline
```

Each `SKILL.md` has YAML frontmatter (`name`, `description` starting with "use this when…") plus actionable instructions.

### Skills at a glance

- **program-baseline** - lock metrics, owners, and scope before launch
- **seller-play-packager** - turn a win pattern into a one-page seller play
- **attribution-review** - monthly/quarterly readout with influence vs credit
- **discovery-coach** - AI SaaS discovery questions and post-call capture
- **enablement-outline** - session design with leading and lagging adoption metrics

## Demos

See `demos/README.md`. Both CLIs use `argparse` and the Anthropic Python SDK Messages API.

## Evals

See `evals/README.md`. `harness.py` loads fixtures, scores baseline clarity / measurable metrics / named owners / no fluff, and prints a JSON summary.

## Teaching

See `teaching/README.md`. Workshop length: 45 minutes. Exercise: set a program baseline without inventing numbers.

## License

MIT License. Copyright (c) 2026 Albert Chan.
