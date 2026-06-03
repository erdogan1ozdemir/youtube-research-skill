# youtube-content-research

A Claude Code Agent Skill that researches YouTube videos on a topic via DataForSEO and turns them into original blog content briefs and full drafts. No browser automation - it uses DataForSEO's YouTube endpoints (search, video info, subtitles, comments).

## What it does

Given a topic (or many), it:
1. Searches YouTube for the topic in the right market/language.
2. Selects the most niche-relevant videos (drops Shorts, clips, off-topic results).
3. Pulls each video's transcript and metadata (and comments, optionally).
4. Synthesizes an original content brief - consensus outline, content gaps, FAQ candidates, suggested title/meta, source list.
5. Optionally writes a full blog draft from that brief.

## Input modes (auto-detected)

- A single topic typed in chat -> deep research, draft allowed.
- A pasted list of topics -> batch with defaults.
- An uploaded `.xlsx` / `.csv` -> batch with per-row parameters via `scripts/parse_input.py`.

Per-topic config: `topic`, `language` (default tr), `location_code` (default 2792), `video_count` (default 5), `mode` (`brief`/`draft`), `include_comments` (default false).

## Requirements

- DataForSEO MCP connected (YouTube endpoints).
- Python with `pandas` + `openpyxl` for Excel input/output.

## Structure

```
youtube-content-research/
├── SKILL.md
├── references/
│   ├── quality-rules.md       # originality, no-hallucination, transcript cleanup, credits
│   ├── dataforseo-youtube.md  # endpoints, params, location rules, parsing
│   ├── video-selection.md     # niche filtering & scoring
│   └── output-formats.md       # brief / draft / batch Excel templates
└── scripts/
    └── parse_input.py          # normalize Excel/CSV topic lists -> JSON configs
```

## Output conventions

Hyphen not em dash; no cover page or "Hazırlayan" sections; correct Turkish characters; advisory tone; tables where they aid scanning.
