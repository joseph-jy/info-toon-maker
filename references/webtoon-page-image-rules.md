# Webtoon Page Image Rules

This file captures the image-generation bias for `vertical-webtoon-page` mode — the `PAGE 1` / `PAGE 2` style infographic-toon page with 4-6 horizontal panels.

## Core Mood
- documentary webtoon meets executive briefing
- dense but readable, not a cute comic page
- alternates bright UI / whiteboard clarity with dark cinematic system shots

## Page Structure Bias
- top black title bar
  - page label (`PAGE 1`, `PAGE 2`, ...)
  - large main title in Korean
  - short 1-line thesis under the title
- 4-6 horizontal panels stacked vertically
- narrow footer strip
  - one footnote, warning, or next-page hook only

## Panel Rhythm
- Panel 1: baseline, past state, or `before` frame
- Panel 2: escalation, change, or new pressure
- Panel 3: concept reveal, hidden system, or core mechanic
- Panel 4: consequence, policy shift, or next-page hook
- Panels 5-6 (optional): only when the beat count truly needs them

## Panel Types
- `bright-ui-panel`: whiteboard, UI insert, diagram, comparison shell
- `dark-cinematic-panel`: server room, government scene, city noir, control room
- `system-diagram-panel`: 1-2-3 chain, cause/effect strip, layered stack
- `reference-material-panel`: an in-world document, screen, memo, log, or mini table that a character reads or points at
- `reaction-panel`: close-up of a recurring character reacting to reveal
- `epilogue-panel`: closing consequence, hierarchy diagram, class-tier map

Alternate bright and dark panels to keep hierarchy readable.

## Panel Composition Bias
- black numbered tag in the upper-left of each panel
- narration caption box in the left or lower-left, not floating in the middle: a rectangular tail-less box with a flat fill and a thin border
- at most one narration box per panel; never place one over a face, a hand, or a diagram label
- speech bubble only when a character is on-camera and speaking
- reference material is drawn as an object inside the panel: a paper document with visible edges, a screen inside a device bezel, a pinned memo, a whiteboard, or a small bordered table
- system diagrams sit inside the panel frame, not overlapping gutters
- consistent gutter width between panels

## Cast Continuity Bias
- pick 1-2 recurring characters (analyst, official, engineer) and repeat them
- keep face shape, hairstyle, outfit, and role stable across panels
- do not swap in random extras just because the scene changes
- if a character speaks, keep their bubble style consistent

## Baked Text Guidance

Explanation runs on four channels, not on dialogue alone: speech bubbles, third-person narration boxes, in-world reference material, and short labels. Pick the channel that fits the content instead of stretching a speech bubble.

### Explanation Density

- `standard`: about 300 Korean characters of baked copy per page. Use for simple pages or when a render keeps failing legibility.
- `extended` (default): about 450 Korean characters per page, hard cap 500. Spend the extra budget on narration boxes and reference material, not on longer speech bubbles.

Record the selected density in `layout-bible.md` and count the page total before writing prompts. A page over the hard cap loses a narration box or moves material text to the footer.

### Per-Channel Budget (`extended`)

- `PAGE N`, main title, 1-line thesis: one line each
- panel numbers and labels: 1-6 words
- speech bubbles: 1-2 per panel, one idea per bubble, preferably 10-40 Korean characters
- narration boxes: 2-4 per page, at most 1 per panel, 25-60 Korean characters each, 1-2 lines
- reference material inserts: 1-2 per page, each either one title line plus 3-5 items of up to 20 Korean characters, or a mini table of 2 columns by up to 3 rows
- stamps or warning badges: 1-4 words
- footer note: up to two sentences, about 80 Korean characters

Under `standard`, drop to a single short bubble per panel, 0-2 narration boxes per page, and at most one reference material insert.

### Channel Rules

- Narration is a third-person voice with no speaker. It carries context, setup, numbers, timeframes, transitions, and source cues.
- Narration never carries the page's core reveal. That belongs to the panel art and its dominant diagram. A page whose argument still works with the art removed is a captioned illustration, not an infographic-toon.
- Narration inherits claim status. Attributed claims, analysis, and speculation keep their attribution inside the narration box; an unverified claim never appears in narration at all, because a faceless voice reads as settled fact.
- Reference material must look like an object in the scene, with a frame, a device bezel, or paper edges. Floating body text is not a material insert.
- Keep material text short and list-shaped.

### Copy Voice

Every baked string passes the voice rules in `references/korean-copy-voice-rules.md` before the whitelist is frozen.

- Drop the AI signature phrases: summation labels, significance inflation, enumeration intros, hype adjectives, closing formulas, formal-noun endings, sentence-initial connectives in narration, double passives, `~에 의해`, `~에 대해`, third-person pronouns, emoji, emphasis quotes inside bubbles.
- The page title and the closing line are where these cluster. Colon-subtitle titles are never used; `A가 아니라 B` parallelism and `X에서 Y로` appear at most once per page.
- Narration is the channel where a stylistic tell shows most, because there is no speaker to absorb it. Hold it to zero.
- The claim ledger outranks the voice rules: remove stylistic hedges, keep the ones that carry attribution or uncertainty.
- With a recurring cast, keep each speaker's speech level and ending set stable across panels.

### Still Unsafe

- full body paragraphs in narration boxes
- exact policy or legal quotes
- multi-line tables baked into a panel beyond the 2x3 material insert
- long system prompts baked as text
- footnote paragraphs

## Prompt Phrases That Usually Help
- `vertical webtoon-page infographic`
- `black PAGE title bar with large Korean title and 1-line thesis`
- `four horizontal comic panels with numbered corner tags`
- `alternating bright UI panel and dark cinematic system panel`
- `rectangular tail-less narration caption box in the lower-left of the panel`
- `in-world document or screen insert that a character reads`
- `documentary webtoon rendering`
- `consistent cast across panels`
- `narrow footer note strip`

## Prompt Phrases To Avoid
- `cute manga panel page`
- `chibi character sheet`
- `shonen action spread`
- `flat webtoon slice-of-life`
- `pastel app presentation`
- `clean modern dashboard`
- `startup landing page infographic`
- `minimal swiss poster`
