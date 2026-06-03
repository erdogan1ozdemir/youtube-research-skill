---
name: youtube-content-research
description: >
  Research YouTube videos on a topic with DataForSEO and turn them into blog content briefs and full drafts.
  Use this skill whenever the user wants to mine YouTube for content research, gather what top videos cover
  on a topic, build a blog brief or draft from video research, find content gaps against YouTube, or analyze
  the YouTube content landscape for a keyword. Trigger on phrases like "youtube araştırması", "video araştırması yap",
  "şu konuda youtube'dan içerik topla", "bu kelime için video araştır", "youtube videolarından blog çıkar",
  "video to blog", "içerik açığı için youtube", "transkriptlerden brief", "youtube content research",
  "research this topic on youtube", or when the user gives a target keyword/topic (or a list/Excel/CSV of topics)
  and asks what to write about based on video content. Also trigger when the user uploads a spreadsheet of
  topics and asks for YouTube-based content research. Uses DataForSEO YouTube endpoints (search, video info,
  subtitles, comments) - no browser automation needed. Turkish-first, multilingual (auto-detects or asks).
---

# YouTube Content Research

Take a topic (or many), find the most relevant YouTube videos, pull their transcripts and metadata via DataForSEO, and synthesize that into original blog content briefs and full drafts. The skill never reproduces video content verbatim - it extracts angles, structure, facts, and gaps, then writes something new.

## Execution Mode: AUTONOMOUS

Once the user provides a topic (or a list/file of topics), run the full workflow end-to-end without asking permission at intermediate steps. Deliver the finished output in one response.

Do NOT ask for confirmation before:
- Making DataForSEO YouTube calls (search, video info, subtitles, comments)
- Selecting which videos are niche-relevant
- Cleaning transcripts or extracting key points
- Reading reference files or running bash commands
- Parsing an uploaded Excel/CSV of topics
- Creating output files (markdown briefs, Excel content plan)
- Installing packages needed for file generation

Only pause and ask the user if:
- No topic/keyword can be found anywhere in the request or uploaded file
- The language or target market is genuinely ambiguous and cannot be inferred
- A DataForSEO call keeps failing after all retry/alternative attempts
- The user explicitly asks for a review before output

## Before you start

Read reference files based on what the run needs:

- Always read: `references/quality-rules.md` - originality, no-hallucination, transcript cleanup, credit limits. These are non-negotiable.
- Always read: `references/dataforseo-youtube.md` - which endpoints to call, parameters, location rules, response parsing.
- Read when selecting videos: `references/video-selection.md` - niche relevance filtering and scoring.
- Read when producing output: `references/output-formats.md` - brief template, draft template, batch content-plan table, Excel structure.

## Workflow Overview

```
Step 1: Build the topic queue (auto-detect input shape)
        ├─ Single topic in chat            -> 1 item, deep
        ├─ Pasted list of topics           -> N items, defaults
        └─ Uploaded Excel/CSV              -> N items, per-row params (scripts/parse_input.py)
Step 2: Per topic -> YouTube search (serp_youtube_organic)
Step 3: Score & select niche-relevant videos (video-selection.md)
Step 4: Per selected video -> video_info + subtitles [+ comments if enabled]
Step 5: Clean transcript, extract points / subtopics / facts / gaps
Step 6: Synthesize per-topic BRIEF (always) [+ full DRAFT if mode=draft]
Step 7: Output
        ├─ Single  -> brief (+draft) as markdown
        └─ Batch   -> content-plan Excel + per-topic brief files; mark processed
```

## Step 1 - Build the topic queue

The skill supports three input shapes and auto-detects which one it is. Do NOT ask the user which mode they want - infer it.

- One topic/keyword written in chat -> single mode (deep: full video count, draft allowed).
- A pasted list (newline / comma separated topics) -> batch mode with defaults.
- An uploaded `.xlsx` / `.csv` -> batch mode with per-row parameters. Run `scripts/parse_input.py <path>` to normalize it.

Normalize every item to this config (fill missing fields with defaults):

| Field            | Default            | Notes                                          |
|------------------|--------------------|------------------------------------------------|
| `topic`          | (required)         | The keyword / subject to research              |
| `language`       | auto-detect / `tr` | From topic language or market; TR-first        |
| `location_code`  | `2792` (integer)   | Turkey. See dataforseo-youtube.md for others   |
| `video_count`    | `5`                | How many videos to analyze for this topic      |
| `mode`           | `brief`            | `brief` or `draft`. Row value wins in batch    |
| `include_comments`| `false`           | Turn on for FAQ / GEO question mining          |

In batch mode the default depth is `brief`; a row only produces a full draft if its `mode` column says `draft`. This keeps credits and context sane across long lists.

Idempotency: when output is an Excel content plan, add a `Durum` (status) column and mark each processed topic `Tamamlandı`. If the user re-runs the same list, skip rows already marked done unless they ask for a refresh.

## Step 2-3 - Search and select

For each topic, search YouTube via DataForSEO with the correct location, then score and select the most niche-relevant videos. The selection logic (what to keep, what to drop, how to rank) lives in `references/video-selection.md` - read it before filtering. Briefly: keep videos whose title and channel clearly match the topic and niche; drop Shorts, clips, reactions, and off-topic results; prefer higher view counts and more recent uploads; record a one-line reason for each pick.

## Step 4 - Collect video data

For each selected video, gather:
- `video_info` - description, tags, exact view count, channel, duration
- `subtitles` - the transcript (raw)
- `comments` - only if `include_comments=true` (top comments for question/FAQ mining)

If a video has no subtitles, mark it `transkript yok` and fall back to title + description + chapter titles for that video. Never invent transcript content.

## Step 5 - Extract

Clean the raw transcript first (auto-captions arrive without punctuation and with errors - see quality-rules.md). Then extract, per video:
- Ana noktalar (key points the video actually makes)
- Alt başlıklar / bölümler (subtopics covered)
- Somut veri/istatistik (only figures actually stated)
- Eksik kalan konular (what this video does NOT cover)

## Step 6 - Synthesize

Always produce a per-topic BRIEF. If `mode=draft`, also produce a full blog DRAFT. Both must be original synthesis - structure and facts may be informed by the videos, but wording is the skill's own. Templates are in `references/output-formats.md`.

The brief aggregates across all analyzed videos for the topic:
- Ortak işlenen alt başlıklar (the consensus outline)
- İçerik açıkları (subtopics no video covered - the differentiation opportunity)
- FAQ adayları (from comments, if enabled, plus recurring questions)
- Önerilen H2/H3 iskeleti + başlık + meta açıklama önerisi
- Kaynak listesi (video başlık + kanal + URL + tarih)

The draft follows the proposed outline, written in the topic's language, original prose, with the somut veriler woven in and attributed in spirit (e.g. "bazı kanallar X'i öne çıkarıyor") rather than copied.

## Step 7 - Output

- Single mode: deliver the brief (and draft if requested) as markdown. Short enough for chat is fine; longer goes to a `.md` file in the outputs folder.
- Batch mode: build one Excel content plan (one row per topic: topic, seçilen video sayısı, önerilen başlık, outline özeti, içerik açığı, durum) plus a per-topic brief file for each row, and a draft file only for `draft` rows.

## Output style rules (apply to every deliverable)

These mirror the user's standing document preferences:
- Use "-" (hyphen), never the em dash character.
- No cover page, no decorative divider lines, no "Hazırlayan / Prepared by" sections. Start directly with the first section.
- Turkish characters must be complete and correct: ş, ç, ğ, ı, ö, ü, İ.
- Advisory tone, no imperative ("emir kipi") in the content delivered to clients.
- Prefer clean tables over dense paragraphs where it aids scanning.

## DataForSEO failure handling

If a call fails, do not silently skip. Diagnose, then retry with alternatives (verify param names via tool_search, try `location_name: "Turkiye"` instead of code, etc.). Only report to the user if all alternatives are exhausted. Details and the exact location-parameter rules are in `references/dataforseo-youtube.md`.
