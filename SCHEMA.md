# Wiki Schema

## Domain
Local optimization layer for a 24/7 video studio. Hermes ingests a video, parses it, and files durable lessons here. The vault is markdown so Obsidian can open it. Source videos are not stored in the vault.

## Paths
- Host vault: `/home/ai/.hermes/studio-vault`
- Container vault: `/opt/data/studio-vault`
- Host media staging: `/mnt/bulk/studio-media/inbox` (also linked from `/home/ai/.hermes/studio-inbox`)
- Container media staging: `/opt/data/studio-inbox`
- Bulk media disk: `/mnt/bulk/studio-media` (1TB, already mounted). Renders live in `artifacts/`. Source files dropped for ingest live in `inbox/`.
- Future offload: Google Drive folder `Hermes Studio`, via the google-workspace skill. The vault stays on this machine. Drive holds the video files.

## Conventions
- File names: lowercase, hyphens, no spaces.
- Every page starts with YAML frontmatter.
- Use `[[wikilinks]]`. A lesson or pattern page needs at least two outbound links.
- When updating a page, bump `updated`.
- Add every new page to `index.md`.
- Append every ingest or lesson to `log.md`.
- Raw files under `raw/` are immutable after the ingest that created them. Corrections go in a new raw note or in a lesson, not by rewriting history.
- Do not put video or audio binaries in this vault. Binaries go to `studio-inbox`, then to the 1TB disk or Google Drive.

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: source | lesson | pattern | concept | entity | query
tags: []
sources: []
confidence: high | medium | low
---
```

Raw video notes use:
```yaml
---
title: Source title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: source
source_url:
local_path:
duration_sec:
ingested: YYYY-MM-DD
parse: captions | whisper | metadata-only
---
```

## Tag taxonomy
Add a tag here before using it.
- video, transcript, lesson, pattern, hook, retention, pacing, edit, audio, visual
- youtube, short-form, long-form, local-file
- craft, distribution, cta, thumbnail, title

## What becomes a page
- One source note per video, under `raw/videos/`.
- One lesson note when a source states a reusable rule. File it under `lessons/`.
- One pattern note when the same lesson shows up in two or more sources. File it under `patterns/`.
- Do not make a page for a passing remark.
- Split a page that grows past about 200 lines.

## Ingest
1. Read `SCHEMA.md`, `index.md`, and the last 30 lines of `log.md`.
2. Search the vault for the video title or URL before creating a source note.
3. Parse the video. YouTube and other captioned URLs use `youtube_transcript_api` or `yt-dlp`. Local files use `ffprobe` and `ffmpeg`. If there are no captions and Whisper is not installed, write the source note with `parse: metadata-only` and say the transcript is still missing.
4. Write the immutable source note. Keep the transcript, or a faithful condensation with timestamps, in `raw/transcripts/` when it is long.
5. Extract lessons. Each lesson links to the source and to at least one pattern or concept.
6. Update `index.md` and append `log.md`.

## Update policy
Newer sources supersede older ones. If two lessons conflict, keep both, set `contradictions`, and lower `confidence`.
