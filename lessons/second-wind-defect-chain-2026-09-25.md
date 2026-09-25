---
title: "Second Wind defect chain — eight root causes from the b5c51bf9 postmortem and reruns 14-18"
created: 2026-09-25
updated: 2026-09-25 (batches 1-3: 62bd144..f430c5c, 20 defects)
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

## Second batch (reruns 19-23, commits c700125..5c90d5f)

9. **A spelled decimal is ONE figure.** 'seventy-eight point four' scanned as the integers 78 and 4
   because 'point' is not a number word — the dialogue gate demanded a claim carrying 78 where the facts
   carry 78.4, so the writer's correct line was unpassable and it "fixed" it to a wrong digit three runs
   running. Fix: a shared `_figure_matches` iterator merges 'point'/'decimal' spans for both
   `numbers_in` and `claim_figures`. Known limitation: a decimal whose next match spans an 'and'
   compound will not merge (rare in narration).
10. **Never mutate a list you are iterating.** The first cut of that iterator set `matches[i+1] = None`
    and then read `.end()` on it — a claim with two chained spelled decimals crashed `verify_claims` with
    AttributeError, the gemini research pass died, the run fell through to nvidia (which returns prose,
    not JSON) and the whole run failed as "research unusable, 0 claims". A crash inside the number
    parser presents as a research-provider failure. Fix: consumed-index set.
11. **The fill gate fought the dedupe gate.** Forcing 75% fill made the writer pad with repeated lines,
    which the repeat gate then blocked — two gates in a standoff across four runs. Calibrated to the
    evidence: the writer's line is ~7 words, fill plateaus at 62-66% at every plan size. Threshold now
    0.62 (keeps the b5c51bf9 55%-unpadded disaster out; 62% + breath pads lands in the 3-5s cut window).
12. **Notes must never contain quotable lines.** The catchphrase 'the recovery minutes are part of the
    training' was in --notes for eight runs; the writer copied it into beats and the dedupe gate killed
    it every time. Notes steer the ARC; quote nothing you don't want to hear four times.
13. **Segment indices in notes are a hazard.** 'The hook equals segment 1's dialogue' produced a hook in
    BOTH segments[0] and segments[1] (segments are zero-indexed). Say 'the FIRST segment (segments[0])'.
14. **`studio reject` records the note but spawns no rewrite worker** — the project sits in
    script/running until `studio resume <id>`. Also: the reject CLI call itself can outlive a short
    foreground timeout after the note is already persisted; check the DB, don't re-reject.

## Third batch (the render + QC phase, commits 69017ff..f430c5c)

15. **A single-key pool must sleep through its cooldown, not die.** ElevenLabs 429
    (36s) killed an approved render at TTS: pool_exhausted marked any wait over 12s
    non-retryable — right for multi-key pools with a failover target, wrong for the
    single ElevenLabs key. Fix: one-credential pools stay retryable; retry ceiling
    raised to 120s.
16. **Wikimedia's public-domain shelf is a military/government firehose.** All 12
    archival slots shipped Navy briefing videos, a 52-min Obama address (1.19GB for
    a 2.8s slot), a NASA press conference. Three-part fix: off-domain title poison
    list (-2.0), zero-keyword-overlap rejection (a title sharing NO query word is a
    score accident, not a candidate), and a LIVE vision review of every candidate.
17. **The vision reviewer was dead for every prior run.** VISION_PROVIDER was
    gemini,nvidia and nvidia registers NO vision role — one gemini 429 and the chain
    fell through to "passing unreviewed, score 0.00". Chain: openrouter,gemini (paid
    first). The project's config SNAPSHOT pins providers at produce time — fixing
    .env does not fix a live project; patch the snapshot in the DB.
18. **Free-tier gemini + per-candidate vision review = a crawl.** Each archive
    candidate cost a vision call, each 429 benched the key 30-60s. When the archive
    has no real footage (Wikimedia has almost no senior-walking content), the
    correct move is to flip coverage to generated stills and stop asking.
19. **Every master shipped SILENT.** compose has full music+ducking support that
    was never once used because no channel set music_path. senior-health now has an
    in-house synthesized warm pad (assets/music/second_wind_bed.wav, A-major stack,
    -22dB under VO ducking) — zero licensing exposure. The project config snapshot
    needed the same music_path patch, and the shorts needed re-cutting (the clip
    source caches the master at clip_sources/; re-render after any re-compose).
20. **Dailies review now works end-to-end**: keyframes rejected for real reasons
    ("young woman strolls — FAIL forbidden" when the bible wants seniors) and
    approved at score 1.00 for on-brand shots. A master is only as trustworthy as
    its reviewer.

## Also fixed en route
- Grounded-research refusals ("reluctant searcher", 0 citations) are a known flash-model failure — the run
  correctly died at `ResearchUnusable`. Re-fire; do not `--force`.
- Coverage 20/45/35 → 50/25/25 (body-in-motion is what wins in this niche; the failed render was 80% stills).
- Warm-up durations: AARP says 10 minutes, the fed trial abstracts carry no warm-up figure — never state
  warm-up/cool-down durations as digits, describe them as easy walking on either end.

[[lesson-format]] · [[produce-run-debugging-2026-09-24]] · [[b5c51bf9-shipped-video]]
