# Output Formats

Templates for the three deliverables: the per-topic BRIEF, the full DRAFT, and the batch CONTENT PLAN (Excel). Every deliverable follows the output style rules in SKILL.md (hyphen not em dash, no cover page, no "Hazırlayan", correct Turkish characters, advisory tone, tables where they help).

All templates are written here in Turkish because TR is the default market; translate the section headings to the topic's language when it is not Turkish.

## A) Research BRIEF (always produced)

Use this structure exactly. Start directly with the title - no cover section.

```markdown
# İçerik Brief'i: [topic]

## Özet
[2-3 cümle: bu konuda YouTube'da ne işleniyor, ana eğilim ne, fırsat nerede.]

## Önerilen Başlık ve Meta
- Başlık önerisi: [<=60 karakter, çekici, anahtar kelimeli]
- Meta açıklama: [<=155 karakter, fayda + CTA]

## Önerilen İçerik İskeleti (Outline)
- H2: ...
  - H3: ...
- H2: ...
[Videoların ortak işlediği alt başlıkların konsensüsü + kendi editoryal eklemen.]

## İçerik Açıkları (Fırsat Alanı)
[Hiçbir videonun değinmediği veya zayıf bıraktığı konular. Farklılaşmanın yeri burası.]

## Somut Bilgiler / Veriler
[Videolarda gerçekten geçen, kullanılabilir veri/örnek/istatistik. Uydurma yok.]

## FAQ Adayları
[Yorumlardan ve tekrarlayan sorulardan. include_comments kapalıysa transkriptlerdeki sorular.]

## İncelenen Kaynaklar
| Video | Kanal | Görüntülenme | Tarih | URL | Not |
|-------|-------|--------------|-------|-----|-----|
| ...   | ...   | ...          | ...   | ... | (transkript yok / güncel / vb.) |
```

## B) Full DRAFT (only when mode=draft)

Produced in addition to the brief, following the brief's outline.

- Written in the topic's language, original prose, advisory tone.
- Length: target what the topic warrants (typically 1200-1800 words); do not pad.
- Weave the somut veriler in naturally; attribute in spirit ("bazı kanallar X'i öne çıkarıyor"), never copy phrasing.
- Include the H2/H3 structure from the brief.
- End with a short FAQ section built from the FAQ candidates (good for GEO and PAA).
- No transcript reproduction. If the draft starts mirroring one video too closely, stop and re-synthesize across sources.

Output the draft as its own section after the brief (single mode) or its own `.md` file (batch mode).

## C) Batch CONTENT PLAN (Excel)

One workbook for the whole batch run. One sheet, one row per topic.

Columns:
| Topic | Dil | Video Sayısı | Önerilen Başlık | Outline Özeti | İçerik Açığı | Mod | Durum |
|-------|-----|--------------|-----------------|---------------|--------------|-----|-------|

- `Outline Özeti`: the H2s joined compactly (e.g. "Kurulum > Fiyat > Alternatifler > SSS").
- `İçerik Açığı`: the single biggest differentiation opportunity for that topic.
- `Mod`: brief or draft (from the row config).
- `Durum`: `Tamamlandı` once processed (idempotency marker).

Alongside the Excel, write one brief `.md` file per topic, and one draft `.md` file only for rows whose `Mod` is `draft`. Name files predictably: `brief_[slug].md`, `draft_[slug].md`.

Use openpyxl for the workbook (matches the user's established Excel workflow). Apply light, readable formatting - bold header row, autosized-ish columns - but no decorative styling.

## File placement

Save all deliverables under the outputs directory and present them. In single mode a short brief can stay inline in chat; anything longer than a screen goes to a file.
