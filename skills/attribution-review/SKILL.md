---
name: attribution-review
description: use this when you need a monthly or quarterly GTM attribution review that separates sourced from influenced pipeline and program influence from coincidence without double counting
---

# Attribution Review

You run structured attribution reviews for GTM programs. The goal is an honest read of what the program moved, what stayed flat, and what cannot be claimed yet. Sourced and influenced credits must not sum past reality.

## When to use

- End of month or quarter program readout
- Leadership asks whether enablement or a play "drove" pipeline
- You need a shared template before analytics deep-dives
- Marketing, partnerships, and programs each claim the same dollars

## Instructions

1. Restate the program baseline and pre-launch measurement plan (primary metric, supporting metrics, owners, attribution method).
2. Pull or request the period's observed values for those metrics only. Do not add vanity metrics.
3. Classify each metric as: improved, flat, declined, or insufficient data.
4. Split pipeline claims into:
   - Sourced: program (or channel) was the genesis of the opportunity
   - Influenced: opportunity existed; program touch accelerated velocity, raised ACV, or unblocked a stage
5. Guard against double counting: sourced + influenced stories across teams must reconcile to closed-won and open pipeline totals.
6. For each improved metric, list plausible drivers (program activity, seasonality, territory change, pricing). Rank confidence: high / medium / low.
7. Separate influence from credit:
   - Influence: program activity touched the account or seller before the outcome
   - Credit: causal claim you are willing to defend (prefer claims backed by control vs treatment)
8. Produce decisions: keep, iterate, pause, or kill. Tie each decision to a metric and an owner.
9. End with 3 questions for the next review cycle.

## Output format

```
Program: <name>
Period: <month/quarter>
Baseline reminder: <primary metric + start value>
Measurement plan reminder: <attribution method>

Results:
| Metric | Baseline | Period | Direction | Confidence |
| ... |

Sourced vs influenced:
| Bucket | Amount / count | Rules used | Owner |
| Sourced | ... | ... | ... |
| Influenced | ... | ... | ... |
Double-count check: <reconciles to / gap TBD>

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
- Reject attribution that double-counts the same closed-won dollars.
