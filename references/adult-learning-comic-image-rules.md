# Adult Learning Comic Image Rules

Use these rules for `adult-learning-comic`: a 4-8 page portrait comic that teaches a serious topic to adults through recurring characters, diagrams, and exact short-form Korean copy.

## Educational Contract

- Start from a competent adult's plausible misconception, not artificial ignorance.
- Give each page exactly one learning objective and one knowledge-state transition.
- Separate definition, mechanism, evidence, limitation, and application. Do not compress all five into one panel.
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

## Page Grammar

- portrait 3:4 page, normally `1536x2048`
- top title strip with `N 페이지` and one literal Korean headline
- 4-6 panels with clean black borders and stable white gutters
- mix three panel types:
  - character dialogue or reaction
  - large visual explanation or comparison
  - diagram, formula, or decision rule
- use one dominant teaching diagram per page
- use eye lines and pointing gestures to connect characters to diagrams
- reserve the bottom strip for a recap, limitation, source cue, or next-page hook

Avoid a uniform dashboard grid. Panel sizes should follow the explanation: a mechanism reveal can be large, while a reaction or transition can be small.

## Adult Visual Tone

- polished Korean educational webtoon or anime-inspired editorial illustration
- adult faces and body proportions; expressive but not child-coded
- professional studio, lab, workshop, office, or domain-relevant setting
- bright warm-white base, black ink borders, blue/teal structure colors, and one warm emphasis color
- diagrams are clean and textbook-legible; scenes remain atmospheric enough to feel like a comic
- friendly and inviting, but not chibi, school-life, fan-service, or children's workbook art

## Dialogue-Baked Text Contract

`dialogue-baked` is the default for this track.

- exact page title: one line
- panel labels: 1-8 words
- speech bubbles: usually 1-2 per panel, one idea per bubble, preferably 10-32 Korean characters
- diagram labels: short noun phrases
- equations: one central equation or transformation per panel
- footer recap: one or two short sentences
- source note: short citation key only; keep full bibliographic text outside the illustrated panels when possible

The page prompt must list every allowed string verbatim and state: `Render only these strings. Do not add, paraphrase, translate, or duplicate text.`

## Prompt Stack

Every page render combines these layers in this order:

1. topic and page learning objective
2. reader knowledge state before and after
3. character identity lock and role lock
4. shared adult educational comic style system
5. page layout and panel-by-panel teaching beats
6. exact baked-copy whitelist
7. continuity reminder
8. output requirements and negative constraints

## QA Gates

- factual: claims and formulas match the claim ledger
- pedagogical: each panel advances the page objective
- continuity: character identity and roles match the character sheet
- copy: every rendered string is on the whitelist and readable
- layout: title, panels, gutters, and footer are not cropped or overlapping
- audience: tone respects adult readers and avoids juvenile framing
- series: the last page actually resolves the misconception introduced on page 1
