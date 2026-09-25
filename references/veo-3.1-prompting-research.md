---
title: "Veo 3.1 prompting research — official Google guidance mapped to the compiler"
created: 2026-09-25
type: reference
tags: [video-studio, veo, prompting, senior-health, render-quality]
sources: [cloud.google.com Veo 3.1 ultimate prompting guide, docs.cloud.google.com Veo best practices, deepmind.google Veo prompt guide]
---

# Veo 3.1 prompting research → compiler mapping

Channel video model: `google/veo-3.1-lite` (envelope: 4/6/8s, 720p/1080p, 16:9/9:16, first/last frame, supports audio + seed, passthrough negativePrompt).

## The official five-part formula

**[Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]** — from Google Cloud's own Veo 3.1 guide. Lead with camera; end with style/light/mood.

## Rule-by-rule status (verified in code 2026-09-25)

1. **Lead with cinematography.** `compile_t2v` emits `register → size/lens → placement → camera_sentence → subject → frame → motion → setting → ambient → composition → look → imperfections → mood`. Camera precedes subject and action. ✅
2. **Subject with concrete traits.** Writer's `subject_state` + world subjects carry appearance; `realism.py` adds imperfections so nothing reads CGI. ✅
3. **Action over scene description.** Mandatory motion field per shot; the `describes more than one shot` gate rejects static collages. ✅
4. **Context = environment.** `_setting_parts` adds the location description only when the frame is thin (under 25 words) — matches the guidance to keep one scene, one main action. ✅
5. **Style & ambiance last.** `_look_sentence` + mood sentence are priority 3/5 — trimmed last, never first. ✅

## Image-to-video (our keyframe → clip path) — Google's explicit rule

> "Your source image already provides the subject, scene, and style. **Focus your prompt on the motion.** Re-describing the character, background, or lighting confuses the model and leads to poor results."

`compile_i2v` is camera + subject motion + stillness + imperfections + "keep the lighting, colours and composition of the first frame throughout" — nothing else. The docstring records the same lesson learned independently (the sliced-bread incident). ✅

Also per Google: **use general terms for the character in the i2v prompt** ("the senior", "she") — our `_subject_sentence` uses `subject_state` phrases, not re-descriptions. ✅

## Three types of movement (direct them separately)

- **Camera motion** — `camera_sentence(shot.camera)` (locked off / pushes in / tracks low)
- **Subject animation** — `sentence(shot.motion)` (the primary verb)
- **Environmental animation** — banned in i2v (the "second motion" rule), allowed in t2v via `_ambient_sentence`. ✅

## Audio

Veo generates native, synchronized audio. Guidance says prompt audio only when it supports the story. Our compose path strips clip audio (`-an` in normalize) and mixes the TTS narration + optional music bed — Veo's audio can never collide with the voiceover. ✅

## What the research CHANGES in our stack

1. **Timestamped multi-shot prompting is NOT adopted.** Google shows `[00:00-00:02] … [00:02-00:04]` sequences, but our house rule is one shot per segment — that gate exists precisely because multi-shot descriptions produced the b5c51bf9 torso/diagram confusion. The formula stays: one shot, one verb, one camera move.
2. **First-and-last-frame transitions**: Veo supports them and our envelope loads `frame_images: first_frame, last_frame`. Future enhancement — could give hero beats a matched transition instead of hard cuts. Not wired into the visuals stage yet.
3. **Ingredients/reference images for character consistency**: the model can take reference images; our visuals stage passes only the first frame. A future lever for keeping the same senior across shots.
4. **1080p**: envelope allows it; we render 1080p masters already.

## Verified capability facts

- Durations 4/6/8s; 16:9 and 9:16; 720p/1080p (lite tier).
- Dialogue: use a colon after the speaker, avoid quotation marks (prevents rendered text). Our prompts never contain spoken lines. ✅
- No "4K/masterpiece/best quality" words — already stripped by `_QUALITY_WORDS`.
