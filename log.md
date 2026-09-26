# Log

## 2026-09-22
- Created the studio vault. Domain is video ingest and reusable craft lessons. No sources ingested yet.
- Pointed media at `/mnt/bulk/studio-media`. Hermes now produces through `/home/ai/C_Video_Studio` and files lessons here after a run.

## 2026-09-24
- Second Wind channel installed in C_Video_Studio (brand `second-wind`, title locked "Why Japanese Seniors Outlive Us"). Deep-dive synthesis filed under `content-analysis/japanese-walking-deepdive/`.
- First produce run took 10 attempts. Six provider/pipeline fixes committed (thinking-model hardening, search/writer split, JSON extraction) — decision 0008 in C_Video_Studio. Lesson: `lessons/produce-run-debugging-2026-09-24.md`.
- 5-repo IG reel mined: `references/5-marketing-repos-insights.md` (Higgsfield UGC prompt craft, email funnel, GEO, ads — generation stays on OpenRouter).
## 2026-09-25
- b5c51bf9 postmortem: shipped video audited shot-by-shot (76 frames + narration). Eight root causes filed in `lessons/second-wind-defect-chain-2026-09-25.md` — TTS config, PCM-in-mp3 pad bug, script/segments divergence, fill gate, repeat gate, world-brief subjects, claim-verifier false contradictions, gemini token-cap/timeout pairing. Fixes: C_Video_Studio commits cbb8c8a, 62bd144, 32a7750, 3786bb7.
- Veo 3.1 official prompting research mapped to the compiler: `references/veo-3.1-prompting-research.md`.

## 2026-09-25 (later)
- Reference library built: 2 Instagram reels + 5 YouTube videos ingested (transcript, shot boundaries, one frame per shot, contact sheets, vision reads). Artefacts under `/mnt/bulk/studio-media/artifacts/ref_*`.
- Filed [[animated-narrative-explainer]] (pattern: the 2.58M-view winner on our own topic is 100% stick-figure animation; two winning registers; 8 load-bearing devices) and [[oversimplified-vector-style]] (art spec for the Louisiana Purchase reel Nicolas flagged).
- Key structural finding: animation, not stock or AI stills, is the constant across the niche's winners — and it removes the three defects that survived every generation-time guardrail (robot, clipping, age-swap).

## 2026-09-26
- Locked "stick figure" as the house default style (`studio/styles.py`, `style:` in all five bibles). New `StickFigure` Remotion composition + `studio/stickfigure.py` compiler draw the picture from geometry, with the `generated` path kept as an alternative.
- First video on the drawn path: **how Nikola Tesla started** ([[stick-figure-first-video-2026-09-26]]) — 89 scenes, 281s, 1080p, $0.18 total spend against an $11 bible budget. Script written by subagents on nvidia against the grounded Graz-1875/Gramme-dynamo ledger (9/9 claims usable); voice by ElevenLabs.
- Filed the run's defects: mixed mp3/WAV audio folder silently costing 15% of the voice in a concat, mp3 encoder delay desyncing captions, `mid`-as-ink black-void surfaces, the `place` overlay colliding with captions, and figure placement against set furniture.
- Provider finding: a chain hop must be able to do the ROLE it is asked (nvidia resolves to a vision model for research/writing), and single-credential pools still spend their retry budget on instant failures instead of sleeping through the cooldown.

