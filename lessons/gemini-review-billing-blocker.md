---
title: Verify review access before buying historical visuals
created: 2026-09-29
updated: 2026-09-29
type: lesson
tags: [lesson, visual]
sources: ["/opt/data/cache/scratch/bulge-director/revised/production-blocker.json"]
confidence: high
---

# Verify review access before buying historical visuals

For the War Machines Battle of the Bulge production, run a genuine image review through the authorized review provider before purchasing keyframes or clips. An OpenRouter generation balance does not imply Gemini review access. Keep the exact historical source, source-date disclaimer, equipment-preserving restoration and final whole-master sweep as separate acceptance criteria. See [[lesson-format]] and [[video-ingest]].

## Observed failure

Project `440b57593aa44110` had a fresh OpenRouter balance of $17.82. The first full-resolution archive-source Gemini review failed across the studio's five transport attempts, reported as rate limiting. A direct diagnostic against the same configured model, `gemini-3.8-flash`, returned **HTTP 402**, `RESOURCE_EXHAUSTED`, with the explicit message that prepaid credits were depleted. Model listing still returned HTTP 200.

This is a demonstrated billing blocker, not a demonstrated daily quota exhaustion. No paid visual generation was attempted; the project remained `awaiting_plan`, recorded cost $0, timeline unlocked. No master, export, source-review verdict or audiovisual QC pass was produced. Existing narration and source assets were preserved.

## Reusable rules

- Read the HTTP status and original body when repeated `RESOURCE_EXHAUSTED` errors contradict the reported cooldown. Do not turn billing failure into endless rate-limit waits.
- A successful model list is not evidence that review generation works; require an actual image-review result.
- Respect a Gemini-only review policy. Do not substitute paid OpenRouter vision or purchase assets that cannot receive the required review.
- After review access is restored, reuse pinned narration and existing assets, refresh the generation balance, and resume the approved exact plan. Final audit must cover the entire master at one frame per second in 9–12-tile sheets, with full-size confirmation of flags.

Evidence and diagnostic scripts: `/opt/data/cache/scratch/bulge-director/revised/production-blocker.json`, `source-review.py`, `gemini-diagnostic.py`.
