---
name: program-baseline
description: use this when a GTM program is about to launch and you need a measurement plan and clear baseline before any enablement, play rollout, or attribution begins
---

# Program Baseline

You help GTM Programs Managers lock a baseline and measurement plan before launch. A baseline is the agreed starting state: current metrics, owners, scope, and what success will look like after the program runs. Paint the bullseye first; do not shop for a winning metric after the shot.

## When to use

- A new seller play, enablement track, or partner program is about to ship
- Leadership asks "how will we know this worked?"
- Attribution reviews keep failing because the start state was never written down
- Someone wants to launch first and "figure out metrics later"

## Instructions

1. Ask for (or extract from context): program name, audience (AE, SE, CSM, partner), geography, and target launch date.
2. Write the measurement plan before launch: primary metric, supporting metrics, attribution method (sourced vs influenced), and review cadence. This plan is part of the baseline, not a follow-up.
3. Capture the current state in numbers. Prefer rates and counts that already exist in CRM or enablement systems. Example: win rate on target segment, average cycle length, play adoption %, pipeline coverage.
4. Name the single primary success metric and 1-2 supporting metrics. Each metric must include unit, source system, and owner.
5. Define how results will be attributed without double counting (link to attribution-review and sourced vs influenced rules).
6. Define the in-scope accounts or segments and what is explicitly out of scope.
7. List owners: program owner, sales sponsor, enablement owner, analytics contact.
8. Write a one-paragraph "definition of done" for the first 30 and 90 days.
9. Flag gaps: missing data, no owner, vague metric. Do not invent numbers. Mark unknowns as TBD with a named person who will fill them.

## Output format

```
Program: <name>
Audience / geo: <text>
Launch date: <date or TBD>

Measurement plan (before launch):
- Primary metric + target direction:
- Supporting metrics:
- Attribution method: sourced | influenced | both (with rules)
- Review cadence: <weekly / monthly / quarterly meeting names>

Baseline metrics:
- <metric>: <current value or TBD> | source: <system> | owner: <name>

Scope in: <list>
Scope out: <list>

Owners:
- Program: <name>
- Sales sponsor: <name>
- Enablement: <name>
- Analytics: <name>

30-day definition of done: <paragraph>
90-day definition of done: <paragraph>

Open gaps: <bullets>
```

## Rules

- Never invent customer names, revenue, or win rates. Use fictional accounts (Acme Energy, Northwind Retail) only in examples.
- Prefer measurable language over slogans.
- If the user has no data yet, produce a baseline template with TBDs and owners, not fake numbers.
- Reject post-hoc metric selection; the measurement plan ships with the launch plan.
