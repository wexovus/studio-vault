---
title: "Second Wind Video 1 — produce-run debugging saga (6 failures, 6 fixes)"
created: 2026-09-24
type: lesson
tags: [gemini, providers, thinking-models, script-gate, evidence, debugging]
---

# Lesson: the first Second Wind produce run took 10 attempts — every failure is now a fix or a rule

Source: `studio produce --channel senior-health` runs, 2026-09-24. Decision record: C_Video_Studio `docs/decisions/0008-thinking-models.md`. Code: commits `5a85b09`, `3288190`, `8d9d919`, `8c6bf3b`, `ce5aa06` on `feature/shorts-clipper`.

## What happened

Six runs died before the script gate, each one deeper: missing keys → saturated default model → reasoning-model fallback → thought-part JSON corruption → thinking-budget truncation → reluctant-searcher Pro → duplicate JSON emission. Every fix was verified against the live API before re-firing.

## The durable rules

1. **Never trust a masked grep for key presence** — check value LENGTH.
2. **Flash searches, Pro writes** (`RESEARCH_GROUNDING_MODEL` vs `RESEARCH_MODEL`).
3. **Thinking models need**: thought-part skip + `thinkingBudget` caps + first-complete-object JSON parsing. All three are in the provider now.
4. **No reasoning/echo-prone models in the writing chain** — `LLM_PROVIDER=gemini` alone; resume beats garbage fallback.
5. **Evidence must be ingestible**: efetch for papers, World Bank API for life expectancy. Paywalls starve the ledger, and a starved ledger = a C+ script.
6. **The gate is literal about figures** — phrase notes so every number you state survives extraction.
7. **Gate review is ledger review first** (`brief.facts`), writer review second.
8. **Reject-with-note rewrites immediately** — DB-update to abandon.

## Payoff

The same fixes hardened every channel's Gemini path, not just Second Wind. Next produce run should go research → script gate in one pass.
