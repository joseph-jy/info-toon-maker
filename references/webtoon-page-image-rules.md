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
- `reaction-panel`: close-up of a recurring character reacting to reveal
- `epilogue-panel`: closing consequence, hierarchy diagram, class-tier map

Alternate bright and dark panels to keep hierarchy readable.

## Panel Composition Bias
- black numbered tag in the upper-left of each panel
- caption box in the left or lower-left, not floating in the middle
- speech bubble only when a character is on-camera and speaking
- system diagrams sit inside the panel frame, not overlapping gutters
- consistent gutter width between panels

## Cast Continuity Bias
- pick 1-2 recurring characters (analyst, official, engineer) and repeat them
- keep face shape, hairstyle, outfit, and role stable across panels
- do not swap in random extras just because the scene changes
- if a character speaks, keep their bubble style consistent

## Baked Text Guidance
- Safe:
  - `PAGE N`
  - main title
  - 1-line thesis
  - panel numbers
  - 1-6 word labels
  - short stamps or warning badges
  - a single short speech bubble per panel
- Unsafe:
  - full body paragraphs in caption boxes
  - exact policy or legal quotes
  - multi-line tables baked into a panel
  - long system prompts baked as text
  - footnote paragraphs

## Prompt Phrases That Usually Help
- `vertical webtoon-page infographic`
- `black PAGE title bar with large Korean title and 1-line thesis`
- `four horizontal comic panels with numbered corner tags`
- `alternating bright UI panel and dark cinematic system panel`
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
