# Handoff

## Storyboard Mode
- `editorial-poster`, `vertical-webtoon-page`, or `adult-learning-comic`

## First Render Pass
- 1.
- 2.
- 3.

## Recommended Order
- editorial-poster:
  - Hero first
  - High-risk text-light blocks second
  - Dense information blocks last or keep out of image
- vertical-webtoon-page:
  - PAGE title bar + panel_01 first
  - Middle panels (escalation, reveal) next
  - Closing panel and footer/next-page hook last
- adult-learning-comic:
  - Character sheet first
  - Page 01 as the style/copy smoke test
  - Remaining pages in numeric order using the same character sheet reference
  - Final-page retrieval/transfer check last

## Asset Expectations
- `05_renders/final-poster.png`
- `05_renders/block_*.png` for editorial-poster
- `05_renders/panel_*.png` for vertical-webtoon-page
- `05_renders/character-sheet.png` and `05_renders/page-*.png` for adult-learning-comic

## Visual Intent To Preserve

### editorial-poster
- dominant hero on the left
- stacked dossier cards on the right
- warning stamps / badges used as hierarchy, not decoration
- dark scene cards contrasted with light paper data cards

### vertical-webtoon-page
- black PAGE title bar with page label, main title, 1-line thesis
- 4-6 horizontal panels with numbered corner tags
- alternating bright UI / whiteboard panels and dark cinematic system panels
- consistent cast (faces, outfits, roles) across panels
- clear panel gutter and border style
- caption/speech placement obeys the storyboard, not decoration

### adult-learning-comic
- recurring adult cast preserves immutable identity and speaking roles
- each page has one objective and a visible knowledge-state transition
- one dominant teaching diagram per page
- exact Korean strings come only from each page's whitelist
- final page resolves the opening misconception and includes a retrieval or transfer check

## Notes For Downstream Assembly
- This harness does not build HTML.
- Exact Korean long-form copy may need separate composition downstream.
- If the run is `vertical-webtoon-page`, downstream should preserve panel order and cast continuity when compositing captions.
- If the run is `adult-learning-comic`, render pages through the Images edit endpoint with `character-sheet.png` as the identity reference.
