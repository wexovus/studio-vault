---
title: "Local TTS chain: Voicebox + Kokoro replaces ElevenLabs"
created: 2026-09-29
updated: 2026-09-29
type: lesson
tags: [tts, voicebox, kokoro, audio, cost]
sources: []
confidence: high
---

# Local TTS chain: Voicebox + Kokoro replaces ElevenLabs

What was tried, what happened, what to do next time.

## What was tried
Produce the Sparta helots reel ([[sparta-helots-reel-2026-09-29]]) with a fully local TTS chain: Voicebox
(https://github.com/jamiepine/voicebox) backend running uvicorn on 127.0.0.1:17600, Kokoro 82M as the
TTS engine, replacing the exhausted ElevenLabs free tier (10k chars/month, already spent).

## What happened
- **pedalboard SIGILL is uncatchable**: Voicebox imports `pedalboard` (Spotify audio DSP) during
  `database.init_db()` → `seed_builtin_presets()` → `backend/utils/effects.py`. Its prebuilt C extension
  executes an AVX-512 instruction this CPU does not have, so the interpreter dies with SIGILL at import.
  A `try/except` in `seed.py` does nothing — SIGILL is a signal, not an exception; the process is dead
  before Python can raise. Symptom: "the monitored command dumped core" with no traceback, right after
  "Data directory set to:".
- **Fix that works**: replace the binary package with a pure-Python stub. `mv pedalboard pedalboard_sigill_backup`,
  then write a `pedalboard/__init__.py` exposing `Pedalboard, Chorus, Reverb, Compressor, Gain,
  HighpassFilter, LowpassFilter, Delay, PitchShift` as no-op classes. TTS does not use pedalboard;
  effects processing becomes pass-through. Server then boots clean.
- **API shape** (98 routes, openapi.json is the source of truth): `POST /generate {profile_id, text,
  engine:"kokoro", language}` → returns generation id immediately (async). Poll
  `GET /generate/{id}/status` — the body is SSE-prefixed (`data: {...}`), strip it before json.loads.
  Fetch audio at `GET /audio/{id}`. Voice selection is NOT per-request: each voice needs its own
  profile (`POST /profiles {name, engine:"kokoro", voice_id:"am_michael", voice_type:"preset",
  preset_engine:"kokoro", preset_voice_id:"am_michael", default_engine:"kokoro"}`).
  Default engine is qwen — a kokoro preset profile rejects requests without `engine:"kokoro"` (400).
- **Performance**: 367-word script (2151 chars) synthesized in ~85s wall clock, 162.3s audio output,
  ~136 wpm narration pace. CPU only (no GPU in the container). Am_michael voice picked by ear by
  Nicolas from a 3-voice A/B (am_michael / am_onyx / bm_george).
- **Cost**: $0. The whole reel (VO + drawn render + mux) cost nothing against the $9/video bible budget.
- **Run detached**: start with `start_new_session=True` (setsid). A plain Popen child dies with the
  kernel when a gateway interruption recycles the session — that killed the first server instance.
- **Startup patience**: first boot runs DB migrations + HF model download; `Ready` appears in the log
  after ~60-90s. `/api/health` 404s — the real health route is `/health`.

## What to do next time
1. Treat Voicebox as the studio TTS default; don't re-derive the API shape, it's in this lesson.
2. If a python process "dumps core" with no traceback on this machine, suspect a binary wheel built
   for a newer instruction set (pedalboard, potentially others) before suspecting the code.
3. Time narration from the REAL synthesized duration (ffprobe), never from word counts — Kokoro
   paced 367 words at 136 wpm, 1.9x the naive 150-wpm estimate. Same rule the drawn skill already
   taught for ElevenLabs applies to every TTS engine.
4. Keep the pedalboard stub in place; `pip list` shows pedalboard as installed but it is a stub.
   Re-installing requirements would re-break the server.

Links: [[sparta-helots-reel-2026-09-29]], [[stick-figure-first-video-2026-09-26]], [[lesson-format]]
