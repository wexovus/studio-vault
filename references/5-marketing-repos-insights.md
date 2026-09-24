---
title: "5 Marketing Repos — Pipeline Insights (IG reel DdmOHahK2D8)"
created: 2026-09-24
type: research
tags: [repos, marketing, higgsfield, email-funnel, geo-seo, ads, video-prompts]
confidence: high
source: Instagram reel DdmOHahK2D8 (Coding for Marketers), OCR extraction
---

# 5 Repos from the Reel — What We Can Steal

## 1. AKCodez gist — Claude Code + Higgsfield UGC Pipeline ⭐ MOST RELEVANT
`gist.github.com/AKCodez/0d3f9874d0e147bd75a097ca0cc1dcc3`
Full copy: vault `references/higgsfield-ugc-guide.md`

**What it is:** End-to-end UGC ad pipeline — character image → video — driving Higgsfield via Playwright MCP browser automation + 21 custom skills.

**Steal for our pipeline:**
- **Prompt engineering standard:** 15-25 line production prompts with 2-second hook framework, beat-by-beat timeline segmentation (up to 15s), camera-movement encyclopedia (15-20 techniques), lighting/atmosphere setups, sound design guidance. → Use this shape for our Veo/Seedance prompts in the shot list.
- **Confirmation-before-Generate rule** ("costs credits") — same pattern as our APPROVAL_MODE. Validated.
- **CLAUDE.md workflow memory** — pipeline order + default settings + workflow rules in one file the agent reads every session. Same as house decision 0003.
- **SESSION-RESUME.md** crash recovery for batch generation — add to our produce runs.
- **Image→video asset chaining:** generate image, then reference it in the video form via the "Image Generations" tab — no download/re-upload. (Higgsfield internal asset system.)
- **Model URL map:** Soul 2.0 `/image/soul-v2` (portraits), Nano Banana Pro `/image/nano-banana-pro` (4K), Seedance 2.0 `/create/video?model=seedance_2_0`.
- **Default social settings:** 9:16, 720p, 8s clips.
- **Prompt-bar discipline** (browser automation): JS-clear Lexical editor, screenshot-verify empty, type slowly, re-clear after Generate.

**Our path is better than the gist's:** it drives the consumer web UI via Playwright; we have the official Higgsfield API + MCP server (`mcp.higgsfield.ai/mcp`). Same prompt craft, cleaner transport.

## 2. coreyhaines31/marketingskills — 51.4K stars
`github.com/coreyhaines31/marketingskills`
50+ Claude Code marketing skills. Relevant ones for us:
- `video` — AI video production workflows (avatars, programmatic video via Remotion, reverse-engineering reference edits: "copy this edit", "match this video style")
- `lead-magnets` + `offers` — for the WALK-keyword → protocol-PDF funnel
- `ad-creative`, `copywriting`, `content-strategy` — distribution phase
- Full video SKILL.md saved: vault `references/marketingskills-video.md`

## 3. zubair-trabzada/geo-seo-claude — 10.8K stars
GEO (Generative Engine Optimization): getting ChatGPT/Perplexity/Gemini to recommend you. Citability scoring, AI crawler analysis, schema markup, platform-specific optimization.
**Use when:** publishing — YouTube description/schema so AI search surfaces "Why Japanese Seniors Outlive Us"; later for the product site.

## 4. AgriciDaniel/claude-ads — 9.5K stars
Paid-media ops skill across 12 platforms (Google, Meta, YouTube, TikTok…). Source-grounded audits, deterministic scoring, capability-gated account changes.
**Use when:** we run paid against the senior-health products (Phase 5+). The capability-gating pattern = our approval gates for ad spend.

## 5. CosmoBlk/email-marketing-bible — 319 stars, 55K words, 908 sources
`github.com/CosmoBlk/email-marketing-bible`
Email flows, segmentation, deliverability, 19 industry playbooks. Hard gate: "no send to >1 recipient without explicit human approval" — same pattern as ours.
**Use when:** the WALK comment-keyword → email capture → one-page protocol PDF → paid product funnel (desk-exercise PDF $19-29 → masterclass per product-opportunities doc).

## Cross-Repo Patterns (all 5 agree with house rules)
1. Hard human gates before spend/send — universal.
2. SKILL.md as the unit of workflow memory.
3. Session-context files (CLAUDE.md / product-marketing.md) read every run.
4. Resume files for crash recovery on batch jobs.
