---
title: Video ingest
created: 2026-09-22
updated: 2026-09-22
type: concept
tags: [video, transcript, lesson]
sources: []
confidence: high
---

# Video ingest

A video enters as a URL or a file in `studio-inbox`. Hermes parses it, writes an immutable note in `raw/videos/`, and files reusable rules as [[lesson-format]] notes under `lessons/`.

The vault stores the reading of the video, not the video. Video binaries live on `/mnt/bulk/studio-media`.

Related: [[lesson-format]]
