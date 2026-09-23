---
title: "Tudor Morari — AI Animation Production Reference"
created: 2026-09-23
updated: 2026-09-23
type: pattern
tags: [ai-animation, production-reference, midjourney, seedance, runway, freepik, style-reference, character-reference, workflow, faceless, higgsfield, gpt-image, soul-character]
confidence: high
source: tudormorari.ai, YouTube @tudormariai, transcripts (aVfawxDj6uw, tudor_workflow, Is4wgEpPMJQ), Day 20 reel
---

# AI Animation Production Reference — Complete

## Source
- **Account:** @tudormorari.ai (427K IG followers)
- **YouTube:** @tudormariai — 1.37M views on best AI animation tutorial
- **Challenge:** 30-day AI animation challenge on Instagram (Day 19, Day 20 analyzed)

---

## PRODUCTION FORMATS IDENTIFIED

### Format 1: AI Animation (Tudor — High Production)
Full AI-generated animated short films. 30-day challenge format.
**Tools:** Reference images + GPT Image + Seedance 2.5 inside Higgsfield.ai

### Format 2: Text-Graphic Faceless (Nate Herk, Austin Georgas — Low Production)
Text overlays + voiceover. No animation. Fast turnaround.
**Tools:** Simple text graphics + AI voiceover

**For our studio:** Format 1 for premium content, Format 2 for rapid testing/scaling.

---

## FORMAT 1: TUDOR'S COMPLETE PIPELINE

### The Evolution (Day 19 → Day 20)

**Day 19 stack (from transcript analysis):**
1. ChatGPT → script/story
2. Freepik Nano Banana → character reference sheet
3. Midjourney → key frame images
4. Seedance 2.5 → animate key frames
5. Runway → lip sync
6. Video editor → assemble

**Day 20 (reel caption):**
> *"created this mexican drama animation using a combination of reference images + GPT Image and Seedance 2.5 inside @higgsfield.ai"*

**Conclusion:** Tudor consolidated the FULL pipeline into Higgsfield.ai:
- Replaced Midjourney → GPT Image (image gen)
- Replaced Runway lip sync → embedded in Seedance/Higgsfield workflow
- All generation now happens inside Higgsfield

### 8-Step Pipeline

```
Step 1: STORY
├── ChatGPT for ideation
└── Inject your own creativity

Step 2: CHARACTER REFERENCE (consistency)
├── Freepik Nano Banana or Higgsfield Soul Character
├── Upload 3-8 reference images of your character
└── Generate character sheet — locks look across all frames

Step 3: STYLE REFERENCE
├── Midjourney --sref parameter OR style image upload
├── Tudor's winner: Spider-Verse cel-shading + storybook illustration
└── Pick ONE style, commit to it — never mix aesthetics mid-production

Step 4: KEY FRAME GENERATION
├── One image per scene
├── Simple prompting first: "establishing shot of this restaurant"
├── Upscale the best, discard the rest
└── 19 shots per short film typical

Step 5: SHOT PLANNING
├── Plan all shots in advance
└── Each shot = one generation with style + character refs

Step 6: ANIMATION
├── Seedance 2.5 animates between key frames
├── Creates "2000s animation" aesthetic
└── 5-30 seconds per clip

Step 7: LIP SYNC (if dialogue)
├── Runway Gen-3 for lip sync (Day 19)
└── May be embedded in Higgsfield workflow (Day 20)

Step 8: VIDEO EDITOR
└── Final assembly — cut video to audio track
```

### Key Principles

**"Don't look AI"** — cel-shaded style (black outlines + flat fills) hides AI artifacts. Spider-Verse aesthetic = professional, non-generic.

**Character consistency** — Upload refs to Nano Banana/Freepik or use Higgsfield Soul Character. Never show the same character with different faces.

**Simple prompting first** — "There's no reason to make it super complex on the front end."

**Inject your own creativity** — ChatGPT gives scaffold, you make it interesting.

---

## THE HIGGSFIELD DISCOVERY (Critical)

**Higgsfield.ai** is a unified API platform aggregating top AI image/video models.

### Available Models via API

**Video (all behind one API key):**
- **Seedance 2.0 / 2.5** — ByteDance flagship, Tudor's primary, up to 30s/clip
- **Kling 3.0** — cinema-grade, 4K
- **Sora 2** — OpenAI video (brokered through Higgsfield)
- **Veo 3.1** — Google's long-form video
- **WAN 2.6** — fast, cheap
- **Minimax Hailuo 02** — character-driven animation

**Images:**
- **GPT Image 2** — OpenAI's latest, 4K, near-perfect text rendering
- **Nano Banana Pro** — "best 4K image model ever"
- **Soul 2.0** — ultra-realistic fashion/portraits
- **Flux 2** — fast general-purpose stills
- **Seedream 5.0 Lite** — visual-reasoning tier

### Soul Character — Cast Consistency (The Key Feature)
Train a character once from reference photos → invoke character ID across all subsequent generations. **Replaces Freepik Nano Banana workflow.** Makes multi-shot productions work in an agent loop.

### The MCP Server — Agentic Access
`https://mcp.higgsfield.ai/mcp` exposes ALL models as tools any MCP-compatible AI agent can call. OAuth auth, no API keys needed in config.

**Our Hermes agent can call Seedance 2.5, GPT Image, Kling, etc. through Higgsfield MCP — no GPU needed.**

### Pricing
- Images: ~$0.005–0.02 per image
- Video: ~$0.02–0.32 per second
- 6-sec Seedance clip: ~$0.32 after discount
- No subscription — pay-as-you-go wallet

---

## FORMAT 2: TEXT-GRAPHIC FACELESS

Source: @nateherk (Nate Herk), @austingeorgas (Austin Georgas)

### Production Style
- Large bold text overlays
- AI voiceover
- Solid color or gradient background
- Topics compressed to 60-90 seconds

### Examples
- "Youtube 101 ✏️" (Austin Georgas)
- "NATIVE AI SHURE" series (Nate Herk)

### Comment Gates
| Creator | Keyword | Offer |
|---------|---------|-------|
| Tudor | MEDUSA → BAG (changes per video) | Full prompts + join challenge |
| Nate Herk | CHANNEL | "I'll send it over" |

### Production Advantage
Format 2 is 10x faster to produce than Format 1. Good for: testing topics, evergreen content, rapid scaling.

---

## OUR PIPELINE AT /opt/data/youtube-automation/

```
research → script → image generation → voiceover → assemble → publish
```

**Already wired:**
- `video_producer.py` → Higgsfield API (images + voice)
- `script_writer.py` → Claude API (scripts)
- `niche_researcher.py` → competitor analysis

**Tools available but NOT yet wired:**
- Higgsfield MCP (Seedance video generation)
- Soul Character (character consistency)
- GPT Image 2 (image generation)

**Config:** `/opt/data/youtube-automation/config/config.yaml` — needs Higgsfield + Anthropic API keys.

---

## RECOMMENDED WORKFLOW

### AI Animation Path (Format 1):
1. Pick health topic (e.g., "5 desk exercises for diabetics")
2. Soul Character → generate consistent character reference
3. GPT Image 2 or Flux → generate key frame illustrations
4. Seedance 2.5 → animate into 5-10s clips
5. Higgsfield TTS or 11labs → voiceover
6. ffmpeg → assemble

### Text-Graphic Path (Format 2):
1. Pick health fact/tip
2. Write 60s script
3. Generate voiceover
4. Create text-graphic visuals (code or Canva)
5. ffmpeg → assemble

---

## COMPETITOR MAP

| Creator | Format | Niche | Tools | Volume |
|---------|--------|-------|-------|--------|
| @tudormorari.ai | AI Animation | AI filmmaking | Higgsfield, GPT Image, Seedance | Daily IG |
| @nateherk | Text-graphic | AI content | Unknown | Daily |
| @austingeorgas | Text-graphic | YouTube education | Unknown | Frequent |

---

## KEY TRANSCRIPT QUOTES

> "It all starts with story." — Tudor

> "The problem is a lot of people rely too heavily on those AI tools, and so it's very important for you to inject your own creativity into the process." — Tudor

> "There's no reason to make it super complex on the front end." — Tudor

> "I liked that it had almost that kind of Spider-Verse tune-shaded look on top of what looks like classic storybook illustration." — Tudor

> "Sora is really weird, it's really inconsistent, and when you're working on a professional project, the application is really not the best." — Tudor

---

*Updated: 2026-09-23 — Higgsfield MCP, Day 20 pipeline, Soul Character, Format 2 competitors*
