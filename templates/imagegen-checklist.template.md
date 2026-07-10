# Imagegen Checklist

## Render Mode
- `text-conservative`
- `dialogue-baked`
- `all-baked`

## Baked Text Policy
- Short baked labels allowed:
- Long exact Korean text excluded:

## First-Pass Validation
- Hero block reads clearly:
- Scene card count matches storyboard:
- Comparison/table blocks are separated:
- No random English or gibberish:
- No duplicated characters or symbols:
- Dark hero vs light paper cards contrast reads clearly:

## Adult Learning Comic Validation
- Page count matches learning design:
- Every page has one learning objective:
- Knowledge state changes page by page:
- Page 1 misconception is resolved by the final page:
- Final retrieval and transfer checks are present:
- Character sheet exists before page renders:
- Faces, hair, outfits, accessories, and speaking roles remain stable:
- Every rendered string appears in the exact-copy whitelist:
- Formulas and diagrams match the claim ledger:
- Adult tone avoids school-life, chibi, and juvenile framing:

## Known Risks
- Example: dense Korean comparison chart should not be baked in one shot

## Recommended Fallback
- Which blocks should be rendered separately first?
- Which page should be regenerated first if continuity or text fails?
