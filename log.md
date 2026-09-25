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
