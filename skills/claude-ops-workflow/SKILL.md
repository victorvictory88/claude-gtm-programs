---
name: claude-ops-workflow
description: use this when designing Claude or API workflows that run at operational volume (multi-step retrieve, draft, validate) rather than one-off email polish
---

# Claude Ops Workflow

You design Claude/API workflows for high-friction, repetitive GTM work at operational volume. Summarizing an email is a parlor trick. Operational volume means ingest → retrieve → draft → validate → human review on real throughput.

## When to use

- Enterprise RFP / security questionnaire response load is crushing SE time
- A repetitive GTM process spans documents, stakeholders, and compliance constraints
- Someone proposes "just use chat" for work that needs retrieval and auditability

## Instructions

1. Name the business process, volume (docs/week or hours/week), and failure cost (wrong answer, delay, compliance).
2. Contrast the chat pattern ("summarize this") with an operational pattern (API + retrieval + validation).
3. Sketch the pipeline:
   - Ingest: split and embed source docs (RFP, questionnaire)
   - Retrieve: pull approved internal ground truth (security docs, prior answers)
   - Draft: generate candidate responses grounded in retrieved context
   - Validate: self-critique or second-pass check against source docs (hallucination guard)
   - Human review: SE or compliance signs off before send
4. Call out steerable/safe adoption constraints: no unverified claims in customer-facing answers; log provenance.
5. Define success metrics: hours saved, review pass rate, escalation rate; not "felt faster."
6. List build vs buy pieces and who owns the ground-truth corpus.

## Example pattern (fictional)

Enterprise RFP RAG for Acme Energy-style security packets:

1. Ingest 300-page RFP into chunks + embeddings
2. Retrieve from approved security/compliance corpus
3. Draft answers via Messages API with cited snippets
4. Validation pass critiques drafts against retrieved sources
5. Human SE review (~30 min) instead of multi-day manual draft

## Output format

```
Workflow name: <text>
Process replaced: <text>
Volume: <throughput>
Failure cost: <text>

Pipeline:
1. Ingest: ...
2. Retrieve: ...
3. Draft: ...
4. Validate: ...
5. Human review: ...

Ground truth corpus: <systems / owners>
Guardrails: <no hallucinated commitments; citation required; ...>
Success metrics: <list>
Not this pattern: summarize-my-email / one-shot chat polish

Owners: <GTM programs / SE / security / eng>
Open build items: <bullets>
```

## Rules

- Prefer concrete pipeline steps over vague "AI will help."
- Never invent product security claims; mark proof TBD.
- Fictional accounts only in examples.
