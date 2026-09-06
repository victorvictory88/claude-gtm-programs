---
name: attribution-review
description: use this when you need a monthly or quarterly GTM attribution review that separates program influence from coincidence
---

# Attribution Review

You run structured attribution reviews for GTM programs. The goal is an honest read of what the program moved, what stayed flat, and what cannot be claimed yet.

## When to use

- End of month or quarter program readout
- Leadership asks whether enablement or a play "drove" pipeline
- You need a shared template before analytics deep-dives

## Instructions

1. Restate the program baseline (primary metric, supporting metrics, owners).
2. Pull or request the period's observed values for those metrics only. Do not add vanity metrics.
3. Classify each metric as: improved, flat, declined, or insufficient data.
4. For each improved metric, list plausible drivers (program activity, seasonality, territory change, pricing). Rank confidence: high / medium / low.
5. Separate influence from credit:
   - Influence: program activity touched the account or seller before the outcome
   - Credit: causal claim you are willing to defend
6. Produce decisions: keep, iterate, pause, or kill. Tie each decision to a metric and an owner.
7. End with 3 questions for the next review cycle.

## Output format

```
Program: <name>
Period: <month/quarter>
Baseline reminder: <primary metric + start value>

Results:
| Metric | Baseline | Period | Direction | Confidence |
| ... |

Influence vs credit notes:
- ...

Decisions:
- Keep/iterate/pause/kill: <reason> | owner: <name> | due: <date>

Next review questions:
1. ...
2. ...
3. ...
```

## Rules

- Never invent pipeline or win-rate numbers.
- Prefer "insufficient data" over a confident wrong story.
- Keep the review short enough for a 30-minute meeting.
