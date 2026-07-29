# Imagegen Checklist

## Render Mode
- `text-conservative`
- `dialogue-baked`
- `all-baked`

## Baked Text Policy
- Short baked labels allowed:
- Long exact Korean text excluded:
- Explanation density (`standard` / `extended`):
- Page character total vs budget:

## Korean Copy Voice Pass
<!-- Run once before the exact-copy whitelist is frozen. Rules and pattern IDs: references/korean-copy-voice-rules.md -->
- Pass performed at (before whitelist freeze / after render):
- S1 banned patterns remaining (must be 0; list ID + string if any):
- Character count recheck after voice fixes:
- Stylistic hedges removed:
- Epistemic hedges kept for `party-claim` / `analysis` / `speculation`:
- No claim status was upgraded by a voice fix:
- No new figure, metaphor, or cliche was introduced that the report does not support:
- Per-character ending sets stay separated and register is fixed across the series:
- Same ending repeated 4+ times in a row on any page:
- Series-level counts (English gloss first-use only / parallelism <=1 / "X에서 Y로" <=1 / colon subtitle 0 / closing formula 0):
- Voice defects accepted without re-render (and recorded in handoff):

## First-Pass Validation
- Hero block reads clearly:
- Scene card count matches storyboard:
- Comparison/table blocks are separated:
- No random English or gibberish:
- No duplicated characters or symbols:
- Dark hero vs light paper cards contrast reads clearly:

## Vertical Webtoon Page Validation
- PAGE header, main title, and 1-line thesis are present and uncropped:
- Panel count and numbered corner tags match the storyboard:
- Page baked-copy total stays inside the density budget and no panel is text-choked:
- Narration boxes are tail-less, speaker-less, and placed left or lower-left rather than floating mid-panel:
- Narration carries only context, numbers, timeframe, transition, or source cue, never the core reveal:
- Narration preserves attribution for reported claims, analysis, and speculation, and contains no unverified claim:
- Reference-material inserts read as objects in the scene and their text is legible at full page size:
- Recurring cast face, hair, outfit, and role stay stable across panels:

## Adult Learning Comic Validation
- Page count matches learning design:
- Every page has one learning objective:
- Knowledge state changes page by page:
- Page 1 misconception is resolved by the final page:
- Final retrieval and transfer checks are present:
- Character sheet exists before page renders:
- Faces, hair, outfits, accessories, and speaking roles remain stable:
- Every rendered string appears in the exact-copy whitelist:
- Page baked-copy total stays inside the density budget and no panel is text-choked:
- Narration boxes are tail-less, speaker-less, and not placed over faces or diagram labels:
- Narration carries only context, numbers, timeframe, transition, or source cue, never the core reveal or mechanism:
- Narration preserves attribution for `party-claim`, `analysis`, and `speculation`, and contains no `needs verification` claim:
- Reference-material inserts read as objects in the scene and their text is legible at full page size:
- Formulas and diagrams match the claim ledger:
- Adult tone avoids school-life, chibi, and juvenile framing:

## Known Risks
- Example: dense Korean comparison chart should not be baked in one shot

## Recommended Fallback
- Which blocks should be rendered separately first?
- Which page should be regenerated first if continuity or text fails?
