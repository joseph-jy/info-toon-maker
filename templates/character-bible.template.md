# Character Bible

## Cast Source
<!-- Reused from the private cast library? Record the profile ids. Format: references/cast-library-format.md -->
- Cast library profiles used (`cast/<id>.character.yaml`): none
- Ensemble used (`cast/<id>.ensemble.yaml`): none
- New characters designed in this run:
- Reference images to pass via `--reference`:

## Cast Lock

### Explainer
- Name and role:
- Adult age band:
- Face and body silhouette:
- Hair silhouette:
- Outfit silhouette:
- Signature colors:
- Fixed accessory:
- Speaking function:

### Learner
- Name and role:
- Adult age band:
- Face and body silhouette:
- Hair silhouette:
- Outfit silhouette:
- Signature colors:
- Fixed accessory:
- Speaking function:

### Challenger (Optional)
- Name and role:
- Identity tokens:
- Speaking function:

### Mascot (Optional)
- Name and concept:
- Shape and color tokens:
- Speaking function:

## Real-Person Casting (Optional)
<!-- Private, non-commercial use: real people may be cast at maximum recognizable likeness. Fill one block per real person; leave empty for a fully fictional cast. -->

### <Real Person Name>
- Cast role (explainer/learner/challenger/mascot):
- Likeness target: maximum recognizable likeness
- Actual face and build tokens:
- Actual hair tokens:
- Signature outfit and accessories:
- Age band as of today:
- Identity reference images:
  <!-- cast/ profile -> its reference_images paths. No cast/ profile (e.g. a public figure named in the report) -> store ad-hoc images under 00_input/refs/ and list them here. Leave "none (text tokens only)" if no photo is available. -->
- Reference usage: identity only; redraw fully in the series webtoon style. Do not inherit the photo's pose, crop, background, lighting, clothing snapshot, or embedded text.
- Reference attach point: character-sheet render only, via `--identity-reference`. Pages inherit the likeness from `character-sheet.png`.
- Stylized fallback descriptor (used only if the render API refuses the likeness):

## Identity Tokens
- Explainer immutable tokens:
- Learner immutable tokens:
- Challenger immutable tokens:
- Mascot immutable tokens:
- Relative heights:

## Voice Lock
<!-- Register is a character property and is fixed for the whole series. A cast/ profile's `voice` is the
     source of truth: copy speech_level, tone, catchphrases, and avoid verbatim and do not "fix" them.
     Rules and pattern IDs: references/korean-copy-voice-rules.md -->

- Relationship map (who outranks whom; what sets each speech level):
- Explainer register (`존댓말` / `반말` / `혼합`) and ending set:
- Learner register and ending set:
- Challenger register and ending set:
- Mascot register and ending set:
- Catchphrases copied verbatim from a `cast/` profile (do not normalize):
- Endings each character never uses:
- Narration voice (third-person, no speaker, no sentence-initial connective):
- Series-wide register drift check (no character mixes 해요체 / 합쇼체 / 한다체):

## Role Continuity
- Who introduces claims:
- Who voices misconceptions:
- Who tests edge cases:
- Who summarizes:

## Visual Continuity
- Rendering style:
- Line and shading style:
- Home environment:
- Repeating props:
- Expression range:
- Bubble style by speaker:

## Reference Render
- Required output: `05_renders/character-sheet.png`
- Views: front, three-quarter, side, and three expressions per main character
- Figure proportions: 7.5 head heights, hip line at the vertical midpoint, full body uncropped (Figure Proportion Lock in `references/adult-learning-comic-image-rules.md`; the numbers live in the `character_sheet` slot prompt)
- Background:
- Labels allowed:
- Identity reference instruction: preserve faces, hair, outfits, accessories, and color tokens; ignore the sheet layout in page renders.

## Prohibited Drift
- no age changes
- no hairstyle or outfit swaps
- no school uniforms or child-coded proportions
- no role swaps between explainer and learner
- no duplicated characters within one panel unless explicitly storyboarded
