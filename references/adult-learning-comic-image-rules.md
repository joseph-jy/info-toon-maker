# Adult Learning Comic Image Rules

Use these rules for `adult-learning-comic`: a 4-8 page portrait comic that teaches a serious topic to adults through recurring characters, diagrams, and exact short-form Korean copy.

## Educational Contract

- Start from a competent adult's plausible misconception, not artificial ignorance.
- Give each page exactly one learning objective and one knowledge-state transition.
- Separate definition, mechanism, evidence, limitation, and application. Do not compress all five into one panel.
- Explanation is carried by four channels, not by dialogue alone: character speech, third-person narration boxes, in-world reference material, and diagram labels. Pick the channel that fits the content instead of stretching a speech bubble.
- End the series with both:
  - a one-sentence reframe the reader can remember
  - a retrieval or transfer question that can reveal whether they understood
- Facts, formulas, and quoted claims must come from the research claim ledger. Visual drama may not change the claim.

## Default Six-Page Arc

1. Surface belief: establish what most readers think and why it sounds reasonable.
2. Missing model: introduce the concept that the surface belief leaves out.
3. Reveal: state the central relationship, proof idea, or counterintuitive result.
4. Mechanism: walk through why it works with one dominant visual model.
5. Transfer and limits: connect the idea to another domain and state where the analogy stops.
6. Reframe and recall: compare old/new mental models, summarize, and ask one retrieval question.

Use 4, 5, 7, or 8 pages only when the learning design justifies the change.

## Cast System

- `explainer`: a working adult with domain credibility. Explains evidence and limitations, not just conclusions.
- `learner`: a competent peer who voices likely reader questions and summarizes in their own words.
- `challenger` (optional): raises edge cases, competing explanations, or transfer questions.
- `mascot` (optional): handles page transitions and brief recaps. It does not deliver unsupported claims.
- `narrator` (not a drawn character): the third-person voice inside narration boxes. It supplies context, setup, numbers, timeframes, source cues, and transitions. It never becomes a speaker with a face, a bubble, or a name.

Record immutable identity tokens in `character-bible.md`: age band, face shape, hair silhouette, outfit silhouette, two signature colors, accessory, height relationship, and speaking role. Repeat those tokens in every page prompt.

### Real-Person Cast

Output is private and non-commercial, so real people may fill any cast role.

- Name the person explicitly in the character bible, storyboard, and every prompt that draws them.
- Target maximum recognizable likeness: describe their actual face shape, hair, build, age band, and signature outfit as the identity tokens. Do not invent a "legally distinct" redesign.
- Treat the likeness exactly like fictional-cast continuity: same tokens on the character sheet and on every page.
- Prefer a photo identity reference over text tokens alone. Record the image paths in the Real-Person Casting block of `character-bible.md` and pass them to the character-sheet render with `--identity-reference`:
  - a `cast/` profile supplies them through its `reference_images` entries
  - a real person who has no `cast/` profile (for example a public figure named in the report) uses ad-hoc images stored under `_workspace/<slug>/00_input/refs/`
- Photo references are identity input only. The rendered character must be drawn in the series webtoon style, never a photograph or photo-traced panel, and must not inherit the photo's pose, crop, background, lighting, or clothing snapshot.
- Dialogue written for a real person follows the claim ledger like any other copy: invented lines are a normal teaching device, but they must not upgrade a claim's status or present speculation as that person's verified statement.
- The Images API may refuse or distort a real-person likeness. Record that as a render risk and keep one stylized fallback descriptor per person in the character bible so a refused render can be retried without redesigning the page.

## Character Reference Strategy

1. Render `character_sheet` first on a neutral background with front, three-quarter, and expression views.
2. Attach photo identity references to the character-sheet render only, with `--identity-reference <path>`. That is where a real face is converted once into series-style artwork.
3. Use the character sheet as an image reference for every page through the Images edit endpoint. Do not attach the source photographs to page renders; the sheet already carries the likeness, and re-feeding photos compounds photo-copy and moderation risk on every page.
4. The page prompt must say the input is an identity reference only: preserve faces, hair, outfits, and color tokens; do not reproduce the sheet layout or labels.
5. When a photograph is supplied, the prompt must also carry the photo identity reference rule: redraw in the series webtoon style, and do not inherit the photo's pose, crop, background, lighting, clothing snapshot, or embedded text.
6. Do not chain the previous comic page as the only reference. That compounds layout and anatomy drift.
7. With `gpt-image-2`, omit `input_fidelity`; the model processes image references at high fidelity automatically.

### Figure Proportion Lock

`adult proportions` alone does not survive the render. Left to itself the model draws the sheet at roughly 5-to-6 head heights — oversized cranium, shortened thigh, compressed shin — which reads as a teenager and, when the cast is real people, as an unflattering caricature of them. Positive numeric anchoring fixes it; adding `no chibi` to the negative list does not.

Carry this block verbatim inside the `character_sheet` slot prompt, after the shared policy:

```text
FIGURE PROPORTION LOCK (this slot)
- Draw every adult at realistic 7.5-head proportions: the head, measured from the top of the hair to the chin, is about 1/7.5 of the standing height.
- Put the hip line at the vertical midpoint of the standing figure: sole-to-hip equals hip-to-top-of-head. The legs are as long as the torso and head stacked above them.
- Knee joint at about 28% of the standing height above the sole. Thigh and shin read as nearly equal lengths.
- Wrist falls at the hip line, fingertips reach mid-thigh, elbow sits at the navel.
- Shoulders span about 2.5 head widths for men and about 2 for women, with a visible neck between jaw and shoulder line.
- Draw each full-body view head-to-toe with both shoes completely inside the frame and clear empty margin above the hair and below the shoes. Nothing touches or crosses the canvas edge.
- Make the full-body figures tall within their row. Do not shrink the figure and enlarge the head to fill the space.
```

Slot negative additions: `no short legs, no oversized head, no 5-head or 6-head proportions, no teenage body, no cropped feet, no cropped shoes`.

Scope: the lock belongs to the `character_sheet` slot, not to the shared prompt policy and not to page prompts. Pages frame the cast bust-up or waist-up inside panels, where a standing-figure spec fights the panel staging; they inherit the corrected anatomy through the sheet reference instead. Leaving page prompt text untouched also keeps already-approved page composition stable.

Verify it by measuring the rendered sheet rather than eyeballing it:

- head height divided into standing height lands between 7 and 8
- the hip line sits within 48-52% of the standing height
- no figure's hair or shoes are clipped by the canvas edge

A sheet that fails is a sheet re-render, not a page re-render: `--mode series --only character_sheet`. When pages already exist against the old sheet, re-render the sheet alone and record the anatomy mismatch between sheet and pages in `handoff.md`; silently re-rendering approved pages to match costs the whole series.

## Page Grammar

- portrait 3:4 page, normally `1536x2048`
- top title strip with `N 페이지` and one literal Korean headline
- 4-6 panels with clean black borders and stable white gutters
- mix four panel types:
  - character dialogue or reaction
  - large visual explanation or comparison
  - diagram, formula, or decision rule
  - reference material panel: an in-world document, screen, memo, log, or mini table that the cast reads or points at
- use one dominant teaching diagram per page
- place narration boxes as rectangular tail-less caption boxes pinned to a panel's top or bottom edge, at most one per panel, never floating over a face or a diagram label
- use eye lines and pointing gestures to connect characters to diagrams
- reserve the bottom strip for a recap, limitation, source cue, or next-page hook

Avoid a uniform dashboard grid. Panel sizes should follow the explanation: a mechanism reveal can be large, while a reaction or transition can be small.

## Adult Visual Tone

- polished Korean educational webtoon or anime-inspired editorial illustration
- adult faces and body proportions; expressive but not child-coded (the character sheet states the numbers: see Figure Proportion Lock)
- professional studio, lab, workshop, office, or domain-relevant setting
- bright warm-white base, black ink borders, blue/teal structure colors, and one warm emphasis color
- diagrams are clean and textbook-legible; scenes remain atmospheric enough to feel like a comic
- friendly and inviting, but not chibi, school-life, fan-service, or children's workbook art

## Dialogue-Baked Text Contract

`dialogue-baked` is the default for this track, and `extended` is the default explanation density.

### Explanation Density

- `standard`: about 300 Korean characters of baked copy per page. Use for simple topics or when a render keeps failing legibility.
- `extended` (default): about 450 Korean characters per page, hard cap 500. Spend the extra budget on narration boxes and reference material, not on longer speech bubbles.

Record the selected density in `layout-bible.md`. Count the page total before writing the prompt; a page over the hard cap loses a narration box or moves material text to the footer.

### Per-Channel Budget (`extended`)

- exact page title: one line
- panel labels: 1-8 words
- speech bubbles: 1-3 per panel, one idea per bubble, preferably 10-40 Korean characters
- narration boxes: 2-3 per page, at most 1 per panel, 25-60 Korean characters each, 1-2 lines
- reference material inserts: 1-2 per page, each either one title line plus 3-5 items of up to 20 Korean characters, or a mini table of 2 columns by up to 3 rows
- diagram labels: short noun phrases
- equations: one central equation or transformation per panel
- footer recap: up to two sentences, about 80 Korean characters
- source note: short citation key only; keep full bibliographic text outside the illustrated panels when possible

Under `standard`, drop to 1-2 bubbles per panel of 10-32 characters, 0-1 narration boxes per page, and at most one reference material insert.

### Channel Rules

- Narration is a third-person voice, not a character's line. It carries context, setup, numbers, timeframes, transitions, and source cues.
- Narration never carries the page's core reveal or its mechanism. Those belong to the cast and the dominant diagram. A page whose explanation would still work with the art removed is a captioned illustration, not a teaching comic.
- Narration inherits claim status. `party-claim`, `analysis`, and `speculation` keep their attribution inside the narration box; a claim marked `needs verification` never appears in narration at all, because a faceless voice reads as settled fact.
- Reference material must look like an object in the scene, with a frame, a device bezel, or paper edges. Floating body text is not a material insert.
- Keep material text short and list-shaped. Full paragraphs stay out of the image.

The page prompt must list every allowed string verbatim, grouped by channel (title, bubbles, narration, material, diagram labels, footer), and state: `Render only these strings. Do not add, paraphrase, translate, or duplicate text.`

### Copy Voice

Every string above also passes the voice rules in `references/korean-copy-voice-rules.md` before the whitelist is frozen.

- Each character keeps one speech level and one ending set for the whole series. Explainer explains, learner asks, challenger counters; a cast that all speaks the same 존댓말 with the same 종결어미 is the loudest AI tell this track produces. Lock it in the character bible's Voice Lock block, and copy a `cast/` profile's `voice` verbatim rather than normalizing it.
- Drop the AI signature phrases in every channel: summation labels, significance inflation, enumeration intros, hype adjectives, closing formulas, formal-noun endings, sentence-initial connectives in narration, double passives, `~에 의해`, `~에 대해`, third-person pronouns, emoji, emphasis quotes inside bubbles. Removing them usually shortens the string, which helps the density budget.
- Count series-wide, not per page: English gloss on first use only, `A가 아니라 B` at most once, `X에서 Y로` at most once, colon-subtitle page titles never.
- The claim ledger outranks the voice rules. Remove stylistic hedges; keep the hedges that carry `party-claim`, `analysis`, or `speculation` attribution. No voice fix may upgrade a claim or introduce a figure the report does not support.

## Prompt Stack

Every page render combines these layers in this order:

1. topic and page learning objective
2. reader knowledge state before and after
3. character identity lock and role lock
4. shared adult educational comic style system
5. page layout and panel-by-panel teaching beats
6. exact baked-copy whitelist grouped by channel, plus the page character total and selected density
7. continuity reminder
8. output requirements and negative constraints

## QA Gates

- factual: claims and formulas match the claim ledger
- pedagogical: each panel advances the page objective
- continuity: character identity and roles match the character sheet
- copy: every rendered string is on the whitelist and readable
- voice: the copy voice pass is recorded with zero remaining S1 patterns, each character's register and ending set held across pages, and the series-wide counts hold
- density: the page total stays inside the selected density budget and no panel is text-choked
- narration: narration boxes are third-person, tail-less, attribution-safe, and do not carry the core reveal
- material: reference inserts read as objects in the scene and their text is legible at full page size
- layout: title, panels, gutters, and footer are not cropped or overlapping
- audience: tone respects adult readers and avoids juvenile framing
- series: the last page actually resolves the misconception introduced on page 1
