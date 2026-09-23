---
title: "Tudor Morari Day 20 Update — Higgsfield AI Pipeline"
created: 2026-09-23
updated: 2026-09-23
type: update
tags: [ai-animation, tudormorari, day-20, higgsfield, seedance, gpt-image, workflow-update]
confidence: high
---

# Day 20 Update — Tudormorari.ai

## New Pipeline
**Day 20:** "Mexican drama animation using reference images + **GPT Image** + **Seedance 2.5** inside @higgsfield.ai"

**Tools confirmed in use:**
1. **Reference images** — uploaded to Higgsfield
2. **GPT Image** — image generation (replacing/displacing Midjourney in some workflows)
3. **Seedance 2.5** — animates reference images into video clips (up to 30 seconds per clip)
4. **Higgsfield.ai** — the unified platform hosting all of this

## Higgsfield.ai — The Key Discovery

Higgsfield is an API platform that aggregates top AI image/video models behind one unified API. Key facts:

### Models Available via API
- **Seedance 2.0 / 2.5** — ByteDance's flagship video model (Tudor's primary tool)
- **Kling 3.0** — cinema-grade, 4K
- **Sora 2** — OpenAI's video model (brokered through Higgsfield)
- **Veo 3.1** — Google's long-form video
- **WAN 2.6** — fast, cheap video
- **GPT Image 2** — OpenAI's latest image model (4K, near-perfect text rendering)
- **Nano Banana Pro** — billed as "best 4K image model ever"
- **Soul 2.0** — ultra-realistic fashion/portraits
- **Flux 2** — fast general-purpose stills

### Soul Character — The Cast Consistency Feature
This is what makes multi-shot productions work. Train a character once from a small set of reference photos, then invoke that character ID across subsequent image and video generations. **This directly replaces Tudor's Nano Banana character consistency workflow.**

### Pricing (per generation)
- Image generation: ~0.5–2 cents per image at 1K–2K
- Video: ~$0.02–0.32 per second depending on model
- 6-second Seedance clip: ~$0.32 after discount
- No subscription — pay-as-you-go wallet

### The MCP Server — Critical for Our Studio
Higgsfield ships an MCP server at `https://mcp.higgsfield.ai/mcp` that exposes ALL of these models as tools any MCP-compatible AI agent can call. This means:

**Our Hermes agent can directly call Seedance 2.5, GPT Image, Kling, etc. through Higgsfield — no custom code needed, no GPU setup, just OAuth authentication.**

## What This Means for Our Production Pipeline

### Instead of running ComfyUI locally, we can:
1. Connect to Higgsfield MCP from our agent
2. Generate images (GPT Image 2, Flux) for key frames
3. Animate them into video (Seedance 2.5)
4. Maintain character consistency (Soul Character)
5. All driven from scripts, no GPU needed

### The Workflow for Health Content
1. **Generate key frame illustrations** using GPT Image 2 or Flux (consistent character style)
2. **Animate with Seedance 2.5** — upload illustration, get 5-30 second clip
3. **Assemble in ffmpeg** with voiceover

### Practical Questions
- Do we have a Higgsfield account?
- Is there an existing MCP connector in our system, or do we set one up?

## Comment Gate Update
Day 20 uses keyword **"BAG"** (previous was "MEDUSA"). These change per video — lead capture mechanism.
