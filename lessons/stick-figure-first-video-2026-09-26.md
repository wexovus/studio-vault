---
title: Stick-figure render path — first produced video
created: 2026-09-26
updated: 2026-09-26
type: lesson
tags: [lesson, visual, audio, pipeline, craft]
sources: ["[[animated-narrative-explainer]]", "[[oversimplified-vector-style]]", "[[lesson-format]]"]
confidence: high
---

# Stick-figure render path — first produced video

First video produced entirely by the drawn path (`studio/styles.py`, the
`StickFigure` Remotion composition, `studio/stickfigure.py`). Topic: how Nikola
Tesla started. 89 scenes, 281s, 1080p. **Total spend $0.18** ($0.06 research +
$0.121 ElevenLabs voice) against an $11 bible budget, because a drawn frame has
no video-model cost at all.

## Result

- `artifacts/f26e7638cdc44c03/masters/tesla_master_16x9.mp4` — 281.3s, 8438
  frames at 30fps, −14.5 LUFS, 33.3 MB.
- Script written by three parallel subagents on nvidia (see the provider note
  below), staged by hand, drawn by Remotion, voice by ElevenLabs.

## Rules

**Mixed mp3/WAV in one audio folder destroys a concat silently.** The
breath-padding path rewrites a segment as WAV (pcm_s16le, stereo) while keeping
its `.mp3` name, so a project's `audio/` holds a mix of real MP3s (mono) and
WAVs. The concat *demuxer* takes the first file's parameters and mis-reads the
rest — 28.4s came out of 32.9s for ten segments, a 15% loss with exit code 0.
Normalise every segment to one format first, then join. Verify by comparing the
joined duration against the locked timeline; anything but ~0 drift is a defect.

**Decoding an MP3 drops the encoder delay, and it accumulates.** ~39ms per mono
file, 1.05s across this film. The picture timeline is built from
`segments.duration_seconds`, so the voice runs ahead of the picture and the
captions lag by a second at the end. Pad each normalised segment back to its
locked duration (`apad` + `-t <duration>`). File and number must agree.

**`loudnorm` upsamples and the encoder inherits it.** Without an explicit `-ar`
the master's AAC came out at 96 kHz. Always pass `-ar 48000` on the mux.

**In the drawn renderer, `mid` must not BE the ink.** The tones object set
`mid: t.ink`, so every surface asked for in mid — windows, crates, hills, the
commutator — rendered as solid black. A shape painted in the same value as the
outlines reads as a hole, not a surface: the vision audit called the lecture-hall
window "a large floating black rectangle behind the person's head". Derive the
mid tone by blending paper toward ink.

**A "place" beat label at 0.78 height collides with the captions.** Captions sit
at the foot of the frame; a location card placed low is drawn on top of the line
being spoken. All beat labels go at the top.

**Stage the figure clear of the set furniture.** The figure's standing position
has to be chosen against the background's own shapes, or it overlaps them: at
x≈0.25 the student stood inside the window.
- Stand the figure clear of the window (ends 0.25w) and left of the desk (from
  0.50w) — x≈0.40.
- Do not place a second figure where the prop is drawn. The lecturer at 0.66
  stood inside the dynamo at 0.70; the establishing shot drops the prop instead.
- Keep desk legs clear of the caption band.

**A frame is empty only if it has neither figures NOR props.** The hook and the
inventory of the machine's parts are *supposed* to be shots of the machine
alone. But a drawn film where nobody appears repeats the "no consistent
character" failure that started this work: the recurring figure must carry about
two thirds of the shots (60 of 89 here), and the machine-only shots are reserved
for where a person would block the object.

**Discipline for subagent-written scripts.** A subagent can write a grounded
script into the studio's JSON contract, but the studio's own
`_segment_from` / `_split_oversized` must do the parsing and persistence.
- `ShotSpec` takes non-string fields verbatim, so `"diagram": null` is a
  validation error, not a default — omit the key when there is no diagram.
- Verify the parts independently: index coverage, per-line word budget, that
  every `claim_id` is in the ledger, and that no forbidden material appears.
  All three writers self-reported clean; the checks confirmed it, and one
  writer had already caught its own over-budget line.

## Provider note

Two blockers, both structural, both hit today:

- **A provider must be able to do the job it is asked.** The nvidia hop
  resolves to `meta/llama-3.2-11b-vision-instruct` — a small vision model — so
  the research and writer roles answered a structured JSON prompt in prose, and
  every run died as `ResearchUnusable` / no JSON. Check what model a chain hop
  actually resolves to for that ROLE before trusting the chain.
- **A single-credential pool still burns its retry budget on fast failures.**
  `NoKeysAvailable` is raised again the instant the key is benched, so attempts
  1 and 3 fail in ~1s and the budget is spent while the key is 30s from free.
  Hit both gemini (script stage) and ElevenLabs (audio stage, 85/89 segments).
  Re-running the idempotent stage finishes the remainder.

Nicolas's call: do not route around this with OpenRouter. Use a subagent on
another provider. The studio's writer is still gemini-only.

## Next

- Music: `company-history` sets no `music_path`, so the master is voice-only.
  `senior-health` has an in-house bed at `assets/music/second_wind_bed.wav`.
- The middle of the script restates its idea ("it fights itself") about six
  times; the opening is stronger than the stretch after it.
- 752 words against a 415s plan gives 281s of voice. Plan the word budget from
  the spoken rate, not from `words_per_second`.
