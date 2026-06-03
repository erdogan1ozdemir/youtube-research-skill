# DataForSEO YouTube Integration

How to use the DataForSEO YouTube endpoints for this skill. If a parameter name does not match at runtime, call `tool_search` to load the exact MCP tool schema before retrying - DataForSEO occasionally adjusts field names.

## Endpoints used

| Purpose                | MCP tool                                      | Key input        |
|------------------------|-----------------------------------------------|------------------|
| Search a keyword       | `serp_youtube_organic_live_advanced`          | keyword          |
| Video metadata         | `serp_youtube_video_info_live_advanced`       | video_id         |
| Video transcript       | `serp_youtube_video_subtitles_live_advanced`  | video_id         |
| Video comments (opt.)  | `serp_youtube_video_comments_live_advanced`   | video_id         |
| Available locations    | `serp_youtube_locations`                      | (none)           |

## Location and language rules

This is the most common source of errors. Apply the same convention used across the user's other DataForSEO work:

- Turkey: `location_code: 2792` (INTEGER, not string). If an endpoint wants a name instead, use `location_name: "Turkiye"` - never "Turkey".
- Language: pass `language_code` (e.g. `tr`, `en`, `de`) and/or `language_name` (`Turkish`, `English`, `German`) matching the topic's language.
- If a location-based call fails, switch between `location_code` and `location_name` before giving up.
- Other common markets used in this portfolio: UK `2826`, Germany `2276`, France `2250`, Italy `2380`, India `2356`, Russia `2643`, USA `2840`. Confirm via `serp_youtube_locations` if unsure.

## Step A - Search

Call `serp_youtube_organic_live_advanced` with:
- `keyword`: the topic
- `location_code`: e.g. 2792
- `language_code`: e.g. `tr`
- depth / block parameters: keep default; the endpoint returns roughly the top 20 result blocks.

From the response, collect for each video result:
- `video_id` (needed for all later calls)
- `title`
- `channel` name
- `views_count`
- `publication_date` (or `timestamp`)
- `url`
- `duration`
- result `type` (distinguish `video` vs `shorts` vs `playlist` vs `channel`)

Parse by result type, not by position. Ignore non-video blocks (channel cards, playlists) for selection, though a playlist title can hint at niche depth.

## Step B - Video info

For each selected `video_id`, call `serp_youtube_video_info_live_advanced` to enrich:
- full `description` (often contains chapter timestamps and key claims)
- `tags`
- exact `views_count`, `likes`
- `channel` details

The description's chapter list is a cheap, reliable outline signal even before reading the transcript.

## Step C - Subtitles (transcript)

Call `serp_youtube_video_subtitles_live_advanced` with the `video_id`.
- The result contains subtitle segments (text + timing). Concatenate the text in order.
- If the call returns empty or "no subtitles", mark the video `transkript yok` and rely on info + description only (per quality-rules.md).
- Prefer the topic-language track; if only an auto-translated or foreign track exists, note it.

## Step D - Comments (only if include_comments=true)

Call `serp_youtube_video_comments_live_advanced` with the `video_id`.
- Pull top comments (by relevance/likes).
- Mine them for recurring QUESTIONS and complaints - these become FAQ candidates and reveal real user intent for GEO. ("Bu oyun X cihazda çalışıyor mu?" style questions are gold.)
- Ignore spam, emoji-only, and off-topic comments.

## Response handling notes

- Live "advanced" endpoints return results directly (no separate task-get needed).
- Responses can be large. If a transcript or comment set is too big for context, save it to a temp file under the working directory and process from there - do not ask permission.
- Always check the `status_code` / `status_message` of the task in the response; a 200-level task status with an empty result usually means "no data for this video", not a hard error.

## Cost-aware call budget per topic

For `video_count = 5` with comments off, expect roughly: 1 search + 5 info + 5 subtitles = ~11 calls. With comments on, add ~5. Multiply by the number of topics in batch mode and warn the user if the queue is very large (e.g. 30+ topics) before running.
