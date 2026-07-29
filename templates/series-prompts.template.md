# Adult Learning Comic Prompt Pack

## Shared Prompt Policy
```text
Create a coherent multi-page Korean educational webtoon series for adult readers. Each output is one portrait 3:4 comic page belonging to the same series.

SERIES INVARIANTS
- preserve the exact recurring cast identity, adult age band, face shapes, hair silhouettes, outfits, accessories, signature colors, relative heights, and speaking roles from the character bible
- use polished Korean educational webtoon rendering with adult proportions, clean black ink borders, bright professional environments, restrained cel shading, and expressive but credible acting
- each page has one learning objective and changes one clearly stated reader knowledge state
- each panel performs one teaching action: question, contrast, reveal, mechanism, evidence, limitation, application, recap, or retrieval
- use one dominant explanatory visual model per page; diagrams must support the dialogue rather than decorate it
- use a top title strip, 4-6 varied comic/diagram panels, stable white gutters, and a narrow recap or forward-hook footer
- keep the series friendly and visually inviting without becoming childish, chibi, school-life, fan-service, or a cute productivity infographic

CHARACTER SHEET REFERENCE RULE
- when a character sheet is supplied, use it only as a high-fidelity identity reference
- preserve faces, hair, outfits, accessories, and color tokens
- do not reproduce the character-sheet grid, poses, labels, or neutral background inside the comic page

PHOTO IDENTITY REFERENCE RULE
- when a photograph of a person is supplied, treat it strictly as an identity reference for facial structure, hair, build, age band, and signature outfit
- redraw that person fully in this series' webtoon illustration style; the output must be drawn artwork, never a photograph, photo cutout, photo collage, or photo-traced panel
- do not copy the photograph's pose, framing, crop, camera angle, lighting, background, or clothing snapshot; pose and stage the character according to the panel description only
- if the photograph shows a different outfit than the character bible specifies, the character bible wins
- ignore any text, logo, badge, or watermark present in the photograph

TEXT CONTRACT
- render only the exact Korean/Latin strings explicitly whitelisted in the slot-specific prompt
- do not add, paraphrase, translate, misspell, duplicate, or invent text
- keep all text horizontal, high contrast, and inside generous bubbles or diagram labels
- prioritize page title, speech bubbles, formula symbols, and diagram labels in that order
- never fill empty space with pseudo-text

OUTPUT
- one complete portrait comic page, no mockup frame, no device frame, no watermark
- obvious top-to-bottom and left-to-right reading order
- no cropped title, speech bubble, face, hand, diagram, footer, or panel border
```

## Shared Negative Prompt
```text
no watermark, no random text, no gibberish Korean, no misspelled technical terms, no duplicated speech bubbles, no duplicated characters, no identity drift, no age drift, no wardrobe drift, no role swap, no school uniforms, no child-coded body proportions, no chibi, no fan-service, no photorealistic portrait, no uniform dashboard grid, no slide deck, no startup infographic, no unreadable formula, no cropped title, no overlapping text, no extra fingers, no broken hands
```

## Page Slot Policy
- Keep only the actual `page_XX` sections for this run.
- Minimum: `page_01` and `page_02`.
- Default: add `page_03` through `page_06` as needed.
- Maximum: `page_08`.
- Keep exactly one `thumbnail` slot. It renders once as a landscape catalog cover
  (default 1536x1024; the list page crops to 16:10 with `object-fit: cover`, so keep
  the phrase and motif inside a centered 16:10 safe area).
- Remove unused placeholder page sections before verification.

### character_sheet
- purpose: lock the recurring adult cast before page rendering
- prompt:
```text
Replace this block with the final character-sheet prompt. Include every immutable identity token from character-bible.md, front and three-quarter views, relative heights, expression row, fixed outfits, fixed accessories, and a neutral background. Use no speech bubbles and only short name/role labels if needed.
```
- negative:
```text
no comic panels, no scene background, no alternate costumes, no age variants, no school uniforms, no chibi proportions, no duplicated views, no long text
```

### thumbnail
- purpose: one landscape catalog cover that reveals the series topic at a glance
- exact baked copy:
- character reminder:
- prompt:
```text
Replace this block with the final thumbnail prompt. One simple landscape cover image, not a comic page: one short Korean topic phrase (2-6 words) as the ONLY baked text, one central visual motif taken from the series, and at most 1-2 recurring characters from the character sheet. Keep the composition bold and readable at small card size. Keep the phrase and motif inside a centered 16:10 safe area because the catalog crops the image.
```
- negative:
```text
no comic panels, no panel borders, no speech bubbles, no long sentences, no paragraph text, no dense diagram, no page title bar, no footer, no watermark, no identity drift
```

### page_01
- learning objective:
- knowledge state before:
- knowledge state after:
- central visual model:
- exact baked copy:
- character reminder:
- prompt:
```text
Replace this block with the complete page 01 prompt. Specify title, 4-6 panel geometry, panel-by-panel teaching action, speakers, expressions, diagrams, every exact string, footer, and transition to page 02.
```
- negative:
```text
no extra text, no identity drift, no panel that does not advance the learning objective
```

### page_02
- learning objective:
- knowledge state before:
- knowledge state after:
- central visual model:
- exact baked copy:
- character reminder:
- prompt:
```text
Replace this block with the complete page 02 prompt.
```
- negative:
```text
no extra text, no identity drift, no panel that does not advance the learning objective
```
