# Quality Rules

These rules are non-negotiable. They protect content originality, prevent fabricated data, and keep DataForSEO credit usage sane. Read this before every run.

## 1. Originality - never reproduce, always synthesize

The whole point is to produce something NEW informed by the videos, not a repackaging of them.

- Never paste transcript text into the brief or draft. Extract the idea, then write it from scratch in the skill's own words.
- Never reconstruct a single video's structure section-by-section. The outline must be a consensus across multiple videos plus your own judgment, not a clone of the top video.
- No verbatim quotes from transcripts. If a phrasing is genuinely important, paraphrase it.
- The output must read as original editorial content, not a summary of "what video 1 said, then video 2, then video 3".

Why it matters: verbatim reuse is both a copyright problem and a duplicate-content / thin-content SEO problem. Google rewards original synthesis, not transcription.

## 2. No hallucinated facts

- Only use figures, dates, names, and claims that actually appear in the transcript, video metadata, or comments.
- If you want to state a statistic, it must trace back to a real video. If no video stated it, do not invent one.
- When a video has no transcript, mark it `transkript yok` and rely only on its title, description, and chapter titles - and say so in the source notes. Do not fill the gap with guesses.
- Distinguish fact from opinion: if a creator asserts something contested, frame it as a claim ("bazı kanallar ... olduğunu öne sürüyor"), not as established fact.

## 3. Transcript cleanup

Auto-generated captions (the common case) arrive as a wall of lowercase text with no punctuation, run-on lines, filler words, and recognition errors.

Before extracting, clean each transcript:
- Re-segment into sentences and restore basic punctuation.
- Strip filler ("ee", "yani", "işte", "um", "uh") and timestamps.
- Fix obvious recognition errors using context (especially brand and product names - e.g. a gaming transcript mishearing "GeForce NOW").
- For Turkish, verify special characters survived (ş, ç, ğ, ı, ö, ü, İ); auto-captions often drop or mangle them.

Do the cleanup in working memory or a temp file - the cleaned text is an intermediate, not a deliverable.

## 4. Recency

- Always capture each video's publish date and show it in the source list.
- Flag information from older videos as potentially dated, especially in fast-moving niches (gaming, tech, software, pricing). A "best games 2023" video should not drive a 2026 article's facts unpraised.
- In the content-gap analysis, note when the gap is simply "no recent video covers X" - that itself is an opportunity.

## 5. Credit discipline

Each DataForSEO call costs credits. Be deliberate:
- Respect `video_count` - do not pull more videos than configured.
- One search call per topic; do not re-search the same keyword.
- Only call comments when `include_comments=true`.
- In batch mode, process topics sequentially and stop at the queue end - never loop.
- If a topic returns no usable videos after search, record it as "yeterli video bulunamadı" and move on rather than burning calls on weak results.

## 6. Niche fit over popularity

A 2M-view video that is tangential to the topic is worth less than a 40k-view video that nails it. Relevance to the user's actual topic and niche always outranks raw view count. See `video-selection.md` for the scoring.
