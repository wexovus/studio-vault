---
title: "Second Wind defect chain — eight root causes from the b5c51bf9 postmortem and reruns 14-18"
created: 2026-09-25
updated: 2026-09-25
type: lesson
tags: [senior-health, postmortem, gates, tts, gemini, ledger, transport]
confidence: high
sources: [[produce-run-debugging-2026-09-24]], [[b5c51bf9-shipped-video]]
---

# The defect chain, in the order the runs exposed them

Every defect below is fixed in C_Video_Studio (commits `cbb8c8a`, `62bd144`, `32a7750`, `3786bb7`) with a regression
test or an inline proof. The purpose of this page is that the NEXT session reads them before touching the pipeline.

## 1. The robotic voice was config, not the voice model
`TTS_MODEL=eleven_flash_v2_5` (the FAST tier), stability 0.45, speed 1.0. Sarah (`EXAVITQu4vr4xnEgs8Vork8bD8AmTgJR8`)
on `eleven_multilingual_v2`, stability 0.71, speed 0.92 is the senior-health narrator now (bible + `.env`).
Always A/B two voices through the real `tts.synthesize` path and let Nicolas pick by ear.

## 2. `_pad_segment_audio` wrote PCM into an `.mp3` container
ffmpeg exit 234 on all 76 segments → every line shipped unpadded → wall-to-wall narration with no breaths.
"Shipping unpadded" warnings are defects, not cosmetics. Fix: the suffix follows the codec (`.wav` for PCM),
content-type follows the suffix. Proven: a 1s tone pads to exactly 3.0s.

## 3. The audio stage renders the `segments` table, NOT `projects.script`
Hand-editing the script JSON after `persist_script` renders as the OLD lines. The approved proof stack
(9%, 13-17%, mmHg) was silently never spoken in the shipped video. `approve_project` now refuses a divergent
script and names the segments. Never hand-edit `projects.script` alone.

## 4. Fill ratio went unchecked → 76 shots averaging 2.6s (the strobe)
Plan 355s vs spoken 195s. Gate now blocks under 75% of planned runtime (45s jurisdiction floor so mechanics
fixtures pass). The 6-minute target only holds if the writer FILLS the plan.

## 5. Repetition went unchecked ("recovery is training" ×4, "knees will thank you" ×2)
Gate now blocks verbatim repeats and names both segments. Near-dupes still pass — watch for paraphrase loops.

## 6. World-brief subjects became the weird visuals
Lab equipment (an "unmarked electronic box", a gas mask) and a location with "chairs with padded leg
restraints" were assigned to walking beats → device close-ups, torsos, rows of dark-suited men reading as
military. The senior-health bible now bans institutional/clinical subjects; heroes are the walker's body and
a kitchen timer. Rule: **the world brief IS the art director** — review subjects and locations before any render.

## 7. The claim verifier killed comparison and sibling claims (run 610bd012)
Any two claims sharing a unit regex + one 5-letter word were "the same measurement": Japan 84 vs US 78.4
(a single comparison claim) and knee extension 13% vs flexion 17% (different measurements) were both dropped
as contradictions → the writer cited invented ids → 30+ blocking flags. Fix: a contradiction needs a shared
unit, a shared subject word, and NO distinguishing word (japan/US, extension/flexion, cycling/walking,
systolic/resting, cohort ages) in only one claim. See `contradict_claims` in `studio/ledger.py`.

## 8. Gemini transport: token cap and timeouts are a pair (runs 14, 17, 18)
- 8192 output cap → MAX_TOKENS truncation of the 76-segment script JSON (~12.5k chars).
- 32768 cap → each revision call so slow the HTTP read timed out 5× in a row → the writer never delivered
  a fix and the gate reported identical flags before and after "revising".
- 16384 + 300s `HTTP_TIMEOUT_SECONDS` is the working envelope for long-form writer calls. If a revision
  reports the SAME flag count twice, suspect transport, not the writer.

## Also fixed en route
- Grounded-research refusals ("reluctant searcher", 0 citations) are a known flash-model failure — the run
  correctly died at `ResearchUnusable`. Re-fire; do not `--force`.
- Coverage 20/45/35 → 50/25/25 (body-in-motion is what wins in this niche; the failed render was 80% stills).
- Warm-up durations: AARP says 10 minutes, the fed trial abstracts carry no warm-up figure — never state
  warm-up/cool-down durations as digits, describe them as easy walking on either end.

[[lesson-format]] · [[produce-run-debugging-2026-09-24]] · [[b5c51bf9-shipped-video]]
