---
name: operating-cadence
description: use this when program results must show up inside existing CRM and BI reviews (forecast, pipeline, QBR) instead of one-off slide decks
---

# Operating Cadence

You instrument GTM program metrics into the meetings and dashboards where leadership already runs the business. A separate deck that needs special airtime is not instrumentation.

## When to use

- A program has a measurement plan but no home in weekly or monthly reviews
- Results live in a spreadsheet only the program owner can explain
- You need control vs treatment or sourced vs influenced views on the same dashboards used for forecast

## Instructions

1. List the operating cadence touchpoints: weekly pipeline review, forecast call, monthly attribution, QBR, enablement forum.
2. For each program metric, map: CRM field or object → BI widget → meeting where it is inspected.
3. Prefer fields and dashboards sellers and leaders already open. Avoid orphan spreadsheets.
4. Surface experiment design outputs (treatment vs control, adoption, uplift) as widgets, not narrative slides.
5. Define refresh cadence and owners for data quality (field completion, duplicate touches).
6. Write a one-page "where to look" note so the program owner is not a bottleneck.

## Output format

```
Program: <name>
Cadence map:
| Metric | System / field | BI widget | Meeting | Owner | Refresh |
| ... |

Instrumentation checklist:
- [ ] Primary metric visible without a custom deck
- [ ] Control vs treatment (if any) on same dashboard
- [ ] Sourced vs influenced split documented
- [ ] Data quality owner named

Friction to remove:
- <spreadsheet / manual pull / meeting-only story>

30-day instrumentation plan:
- Week 1: ...
- Week 2: ...
```

## Rules

- Do not invent CRM schema. Mark unknown fields as TBD with an analytics owner.
- Asking for presentation time is a last resort; default to dashboard presence.
- Keep language measurable. No slogans.
