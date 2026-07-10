# Master Image Prompt

## Prompt Intent
- Generate the whole poster in one shot only when the layout is simple enough and the text density is manageable.
- `adult-learning-comic` does not use a multi-page one-shot. Use `series-prompts.md`, one page image per request.

## Master Prompt
```text
Create a single tall editorial infographic-toon page. Use either an asymmetric poster structure with a dominant left-side hero scene, stacked right-side dossier cards, and a strong closing footer, or a vertical webtoon-page structure with a black PAGE title bar, 4-6 horizontal comic panels, numbered corner tags, caption boxes, sparse speech bubbles, and a narrow footer note. Use a dark navy/charcoal cinematic background, amber highlight accents, red warning stamps, and off-white paper data cards. The page should feel like a dramatic executive intelligence brief mixed with documentary webtoon storytelling, not a clean dashboard or slide deck.

Reading order must be obvious from top to bottom. Use 5-8 blocks for poster mode, or 4-6 panels for webtoon-page mode. Mix narrative illustration zones with structured information cards. Allow only short Korean baked labels such as section headers, page labels, panel numbers, badges, speech bubbles, and warning stamps. Keep long Korean body copy minimal or visually implied. Avoid random English, gibberish text, generic charts, duplicated faces, unstable character continuity, and flat corporate presentation aesthetics.

[Replace the block-specific narrative, subjects, and labels with the final poster prompt.]
```

## Negative Prompt
```text
no watermark, no gibberish, no broken anatomy, no duplicated faces, no random English, no unrelated charts, no cropped headlines, no clean modern dashboard, no startup landing page infographic, no minimal swiss poster, no cute manga panel page, no pastel app presentation, no generic presentation slide layout, no flat corporate dashboard look
```

## Notes
- Keep exact Korean body copy outside the baked image unless render mode is explicitly `all-baked`.
- If the page is modeled after a dense infographic-toon, prioritize:
  - cinematic hero block
  - clearly separated scene cards
  - PAGE header and numbered panels for webtoon-page mode
  - alternating dark scene cards and light paper cards
  - readable short baked labels only
