# Master Image Prompt

## Prompt Intent
- Generate the whole page in one shot only when the layout is simple enough and the text density is manageable.
- Keep only the track section this run actually uses; leave the heading text exactly as written so `scripts/render_openai.py` can find it.
- `adult-learning-comic` does not use a multi-page one-shot. Use `series-prompts.md`, one page image per request.

## Master Prompt (editorial-poster)
```text
Create a single tall editorial infographic poster. Use an asymmetric structure with a dominant left-side hero scene, stacked right-side dossier cards, and a strong closing footer. Use a dark navy/charcoal cinematic background, amber highlight accents, red warning stamps, and off-white paper data cards. The page should feel like a dramatic executive intelligence brief, not a clean dashboard or slide deck.

Reading order must be obvious from top to bottom. Use 5-8 blocks. Mix narrative illustration zones with structured information cards. Allow only short Korean baked labels such as section headers, badges, counters, and warning stamps. Keep long Korean body copy minimal or visually implied. Avoid random English, gibberish text, generic charts, duplicated faces, and flat corporate presentation aesthetics.

[Replace the block-specific narrative, subjects, and labels with the final poster prompt.]
```

## Negative Prompt
```text
no watermark, no gibberish, no broken anatomy, no duplicated faces, no random English, no unrelated charts, no cropped headlines, no clean modern dashboard, no startup landing page infographic, no minimal swiss poster, no cute manga panel page, no pastel app presentation, no generic presentation slide layout, no flat corporate dashboard look
```

## Master Prompt (vertical-webtoon-page)
```text
Create a single tall vertical webtoon-page infographic. Use a black PAGE title bar with a page label, a large Korean title, and a 1-line thesis, then 4-6 horizontal comic panels with black numbered corner tags, and a narrow footer note strip. Alternate bright UI/whiteboard panels with dark cinematic system panels. Use a dark navy/charcoal cinematic base, amber highlight accents, red warning stamps, and off-white paper cards. The page should feel like a documentary webtoon crossed with an executive briefing, not a cute comic page or a clean dashboard.

Reading order must be obvious from top to bottom. Carry the copy on four channels: sparse speech bubbles, rectangular tail-less third-person narration caption boxes placed left or lower-left, at most one or two in-world document or screen inserts drawn as objects in the scene, and short labels. Keep the page inside the declared explanation density (`extended` default: about 450 Korean characters, hard cap 500). Narration carries context, numbers, timeframes, transitions, and source cues only; the core reveal belongs to the panel art and its diagram. Avoid random English, gibberish text, paragraph text inside a narration box, duplicated faces, and unstable character continuity across panels.

[Replace the panel-specific narrative, subjects, and exact strings with the final page prompt.]
```

## Negative Prompt (vertical-webtoon-page)
```text
no watermark, no gibberish, no broken anatomy, no duplicated faces, no random English, no unrelated charts, no cropped headlines, no cute manga panel page, no chibi character, no flat webtoon slice-of-life, no clean modern dashboard, no startup landing page infographic, no minimal swiss poster, no narration box with a bubble tail, no narration box over a face or diagram label, no floating body text without a container, no paragraph inside a document or screen insert, no text-choked panel, no identity drift across panels
```

## Notes
- Keep exact Korean body copy outside the baked image unless render mode is explicitly `all-baked`.
- For `vertical-webtoon-page`, record explanation density and the page character total in `layout-bible.md` under `## Baked Copy Budget`. Per-channel numbers: `references/webtoon-page-image-rules.md`.
- If the page is modeled after a dense infographic-toon, prioritize:
  - cinematic hero block
  - clearly separated scene cards
  - PAGE header and numbered panels for webtoon-page mode
  - alternating dark scene cards and light paper cards
  - readable short baked labels, narration boxes, and one material insert only
