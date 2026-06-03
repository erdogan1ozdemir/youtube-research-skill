# Video Selection

How to pick the `video_count` most useful videos from the search results for a topic. Relevance to the topic and niche beats raw popularity (see quality-rules.md Section 6).

## Hard filters (drop these outright)

- Shorts (result type `shorts`, or duration under ~60s). They rarely carry enough substance.
- Pure clips, montages, reaction videos, and "funny moments" compilations - they react to content rather than explain a topic.
- Videos whose title/channel is clearly off-topic or a different language than requested (unless no in-language video exists).
- Obvious clickbait with no descriptive substance ("YOU WON'T BELIEVE...") when better options exist.
- Duplicate re-uploads of the same content.

## Relevance scoring (rank the survivors)

Score each remaining video and take the top `video_count`. Weight in this order:

1. Topic match (highest weight): does the title/description directly address the topic, not just mention it in passing? An explainer, guide, review, or comparison about the exact topic scores highest.
2. Niche/channel fit: is the channel credible in this niche (gaming channel for a gaming topic, beauty channel for a cosmetics tutorial)? Authority and topical focus matter.
3. Substance signals: longer-form (a real explainer, typically 5+ minutes), chapter markers in the description, a detailed description - all signal depth worth transcribing.
4. Recency: more recent is better, heavily so in fast-moving niches (gaming, tech, pricing, software). An old video can still rank if it is foundational/evergreen.
5. View count / engagement: a tiebreaker, not a primary driver. High views confirm resonance but do not rescue an off-topic video.

## Selection output

For each selected video, record a one-line reason, e.g.:
- "Konuyu birebir işleyen güncel rehber, bölüm başlıkları mevcut"
- "Nicheinde otorite kanal, detaylı karşılaştırma"

Record rejected-but-close calls only if useful; otherwise keep it lean.

## Edge cases

- Fewer good videos than `video_count`: take what passes the filters and note "yalnızca N uygun video bulundu". Do not pad with weak results.
- All results are Shorts or clips (common for very broad or very new topics): widen by trying a more specific or a more general phrasing of the keyword ONCE, then proceed with the best available, flagging low confidence.
- Mixed-language niche (e.g. a global gaming topic): prefer the requested language, but a high-value foreign-language video with a usable transcript can be included if marked, since the synthesis is rewritten anyway.
- Topic is a brand/product the portfolio owns (VitrA, Game+, Flormar, etc.): include the brand's own channel videos if present, but also competitor/creator coverage for the gap analysis - do not let the brand's own framing dominate.
