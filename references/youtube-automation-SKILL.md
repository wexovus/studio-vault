# YouTube Automation — Faceless Channel Playbook
**Project:** `/opt/data/youtube-automation/`
**Compiled:** August 15, 2026
**Status:** Pipeline ready — needs API keys to run

---

## WHAT THIS IS

A local pipeline for building faceless YouTube channels — from niche research to produced video, fully automated. The goal: scale content production without showing your face.

---

## THE MONEY PLAY (From Scott Smith)

**Numbers:** $19,587 in 28 days, 27 videos uploaded, $75/video production cost, ~$650 profit/video.

**The model:** News/current events faceless channel. Trending topics + fast upload = viral compounding.

---

## THE FULL PIPELINE (From Scott Smith)

### Step 1: Find Trending Topics — Gemini + Manus AI
**Prompt (same for both):** [paste into Manus → send, on Gemini → select "deeper research" + check "sources" box]

Both generate a list of current trending topics relevant to your niche. Speed is the moat — faster upload after a trend emerges = higher viral probability.

### Step 2: Create Titles — Claude (Chrome Extension)
1. Find the 2 most popular channels in your niche
2. Use Claude Chrome extension with prompt:
   > Analyze how these two channels title their videos to go viral
3. Download the analysis sheet
4. Send Gemini/Manus research to Claude
5. Use this prompt to generate 3 title variations per topic:
   > [Generates 3 title variations per topic, click-worthy]

### Step 3: Outsource Production — Upwork ($75/video)
Hire 3 freelancers per video:
- **Script writer** — ~$20-30
- **Video editor** — ~$25-35
- **Thumbnail designer** — ~$10-15

### Step 4: Voiceover — 11labs.io
- AI text-to-speech via 11labs
- Editor creates the voiceover
- Keeps the channel faceless

### Step 5: Upload
- Editor delivers finished video
- Apply thumbnail + title
- Publish

---

## THE LOCAL PIPELINE (Already Built)

Located at `/opt/data/youtube-automation/`

### Step 0: Content Validation (NEW — SMTM Framework)
```bash
python3 scripts/content_validator.py --topic "desk exercises for diabetics" --niche "senior health"
```
Runs 5-stage validation BEFORE production:
1. **Topic Gate** — 4 forcing questions (demand, supply, edge, two-audience). Fails 80% of topics that would flop.
2. **Information Density** — score every sentence 0-80+. Cut filler, expand buried high-scorers.
3. **Authenticity Audit** — 12 AI-fingerprint signals. Rewrite if ≥6 detected.
4. **Hook Check** — 8 psychological mechanisms + 12 hook patterns. Minimum 2 mechanisms required.
5. **One-Core Resonance** — structural check for diluted/diffuse core.

**No script needed for Stage 1 (topic gate).** Provide a script to run all 5 stages.

### Step 1: Niche Research
```bash
python3 scripts/niche_researcher.py --channels "yt.com/channel/UCxxx"
```
Analyzes competitor channels for high-performing content.

### Step 2: Script Generation
```bash
# From YouTube video (needs TurboScribe key)
python3 scripts/script_writer.py --video-url "https://youtube.com/watch?v=xxx" --niche "ancient humans" --count 3

# Or from local transcript (free — uses whisper)
python3 scripts/script_writer.py --transcript path/to/transcript.txt --niche "ancient humans" --count 3
```

### Step 3: Video Production
```bash
python3 scripts/video_producer.py --script output/scripts/script_xxx.md --style ms_paint
```
Generates images (Higgsfield), voiceover, assembles video with FFmpeg.

### Run Everything
```bash
python3 run_pipeline.py --step all --niche "ancient humans" --style ms_paint
```

### Validate Topic First (recommended)
```bash
# Gate topics before spending time on scripts
python3 run_pipeline.py --step validate --topic "desk exercises for diabetics" --niche "senior health"
```

---

## TOOLS & COSTS

| Tool | Purpose | Cost |
|------|---------|------|
| **Manus AI** | Research — trending topics | Subscription |
| **Gemini** | Research — trending topics | Free tier available |
| **Claude** | Title optimization, script writing, content validation | Free tier / $20/mo |
| **11labs.io** | AI voiceover | ~$10-20/mo |
| **Upwork** | Freelance production | ~$75/video |
| **Higgsfield** | Image + video generation (Seedance, GPT Image, Flux) | Pay-as-you-go |
| **TurboScribe** | Transcription | Paid (use whisper free instead) |
| **whisper** | Local transcription | Free |
| **Show Me The Money** | Content validation framework (topic gate, density, authenticity) | Free (CC BY-NC 4.0) |

**Free total:** All AI research + transcription + content validation is free. Only costs are voiceover (~$15/mo) and video generation if you don't do it yourself.

---

## CASE STUDIES

### Scott Smith — News Channel ($19,587 in 28 days)
- 27 videos in 28 days
- $75/video production (Upwork)
- $725/video revenue average
- Trending current events topics
- Gemini + Manus for research, Claude for titles, 11labs voice

### WOP Channel — Shorts Growth Model
- Anchor to known viral channels/accounts
- Ideas first, then content
- Consistent posting schedule

### 20-Year-Old — $50-60K/Month Shorts Pipeline
**The 4-step process:**
1. ChatGPT → generate script/outline
2. Viblo.ai → create video (AI video generation)
3. TikTok clips → post and test
4. YouTube Shorts → repurpose

This is the simplest version: **AI generates script → AI creates video → post everywhere**.

---

## THE SHORTEST PATH TO $1K/DAY

If you want the simplest version of this playbook:

1. Pick a niche (news, facts, history, top 10s, etc.)
2. Set up Claude + 11labs + Upwork
3. Use Gemini/Manus for research
4. Hire script writer + video editor on Upwork ($75/video)
5. Publish daily
6. Let YouTube algorithm compound

**The key insight:** Faceless channels can be 100% outsourced. You manage the system, not create the content.

---

## SETUP CHECKLIST

- [ ] Claude account (claude.ai)
- [ ] 11labs account (11labs.io)
- [ ] Upwork account
- [ ] Manus AI (manus.ai) or Gemini
- [ ] API keys in `config/config.yaml`
- [ ] FFmpeg installed
- [ ] whisper (via `/opt/data/timesfm_check/.venv/bin/python3`)

---

## FILE STRUCTURE

```
youtube-automation/
├── SKILL.md                              ← you are here
├── README.md                             ← original readme
├── config/config.yaml                    ← API keys
├── scripts/
│   ├── niche_researcher.py              ← competitor analysis
│   ├── script_writer.py                 ← transcript → script
│   └── video_producer.py                 ← script → video
├── prompts/                              ← prompt templates
├── output/
│   ├── niche_report.md
│   ├── scripts/                          ← generated scripts
│   └── videos/                           ← produced videos
├── run_pipeline.py                       ← master orchestrator
└── references/
    ├── digital-product-prompts.md         ← @bylanger prompts
    └── scott-smith-faceless-channel-workflow.md  ← detailed workflow
```

---

## CREDITS / SOURCES

- Scott Smith (@scott.smith) — Instagram Reels DaxuTbFxOpn, $19,587/month case study
- @bylanger — digital product 3-prompt system
- WOP channel growth methodology
- 20-year-old $50-60K/month Shorts pipeline (Viblo.ai method)
- **@jamesai / Orris.ai** — Show Me The Money (show-me-the-money repo), content validation framework: topic gate, information density scoring, 12-signal authenticity audit, 8-mechanism hook matrix, one-core resonance check
- **@tudormorari.ai** — AI animation production format, Higgsfield pipeline
- **@nateherk** — Text-graphic faceless format
- **@austingeorgas** — YouTube education content format

---

*Last updated: August 15, 2026*
