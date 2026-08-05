---
name: report-to-infographic-toon
description: Draft, normalize, and validate a source-backed dry report from user research notes, then turn an approved report into either a single-page Korean editorial infographic-toon poster or a 2-8 page adult learning comic, including run initialization, claim-safe story design, prompt packs, verification, optional OpenAI image rendering, and visual QA. Use when the user says "조사 메모를 리포트로 정리해줘", "리포트 작성 가이드에 맞춰 작성해줘", "리포트 검증해줘", "위 리포트를 포스터 형태의 웹툰으로 만들어줘", "성인용 학습만화로 만들어줘", "리포트로 인포툰을 기획해줘", or asks to revise an existing report-based run.
---

# Report To Infographic Toon

Draft or validate the factual input, then convert approved research into a visual artifact without silently changing its claim status. Treat this skill as the single entry point; reuse the repository's existing guide, templates, verifier, renderer, and specialist skills.

## Choose The Task Mode

### Draft Or Normalize A Source Report

1. Read `references/source-report-guide.md` completely.
2. Convert the user's notes, excerpts, links, or rough report into the guide's full source-report format.
3. Preserve meaning, attribution, dates, names, numbers, uncertainty, and source connections. Do not strengthen a claim for readability.
4. Do not perform additional research by default. If the user explicitly asks for research, browse and cite appropriate current sources, record an information cutoff date, and keep conflicting evidence visible.
5. Mark unsupported or ambiguous claims `needs verification`; never invent a missing source, date, quotation, or corroboration.
6. Write to the user-specified path. If no path is given and this is a report-only request, use `reports/<slug>-source-report.md`; create `reports/` when needed.
7. Stop after the report and a short completeness summary unless the user also requests a poster or learning comic.

### Validate An Existing Source Report

1. Read `references/source-report-guide.md` completely and inspect the report without rewriting it first.
2. Check required sections, one-claim-per-row structure, status/source alignment, allowed wording, prohibited strengthening, cutoff date, exact names and numbers, and unresolved conflicts.
3. Report missing or unsafe items with claim IDs. Edit the report only when the user asks for correction or completion.

### Produce An Infographic-Toon

1. Require a source report that meets the minimum input contract below.
2. Choose the requested poster or adult-learning-comic deliverable and requested execution depth.
3. Build, verify, optionally render, and visually inspect the run using the remaining workflow.

## Input Contract

1. Read `references/source-report-guide.md` when validating, drafting, or explaining the source-report format.
2. For production, accept a pasted report or a report file and preserve a verbatim copy as `_workspace/<slug>/00_input/source-report.md`.
3. Require enough material to identify the topic, core summary, claim statuses, viewpoints, implications, uncertainties, prohibited wording, and sources.
4. Treat the report as the factual boundary. Do not browse, upgrade a claim's status, fill a missing fact, or invent a source unless the user explicitly asks for additional research.
5. Keep `reported`, `party-claim`, `analysis`, `speculation`, and `needs verification` visibly distinct. Never convert them into unattributed facts.
6. If a central claim lacks support, continue the prompt package when possible, record the gap, and keep the claim out of assertive baked text. Stop rendering only when the resulting artifact would be materially misleading.

## Choose The Deliverable

- Map `포스터`, `포스터 형태의 웹툰`, `한 장`, or `editorial poster` to `editorial-poster`.
- Map `성인용 학습만화`, `학습 웹툰`, `2-8페이지`, or a requested page range to `adult-learning-comic`.
- Require one of these two deliverables. If neither is explicit and the surrounding request does not resolve it, ask one short question.
- Respect an exact page count. For a range, choose the smallest count that supports the required knowledge-state changes; stay within 2-8 pages. Use 3-6 pages by default; use 2 pages only for deliberately narrow micro-lessons.

## Choose The Execution Depth

- `기획`, `설계`, `프롬프트만`: finish the run package and verifier; do not render.
- `만들어줘`, `제작해줘`, `그려줘`, `렌더링`: finish the run package, verify, dry-run, render, and inspect actual images.
- When intent is ambiguous, finish the prompt package and state that rendering has not run.

## Build The Run

1. Locate the repository root containing `AGENTS.md`, `templates/`, and `scripts/` and obey `AGENTS.md`.
2. Create a short kebab-case slug. If `_workspace/<slug>` exists, read it first and change only affected artifacts. Otherwise run:

   ```bash
   bash scripts/init_infographic_run.sh <slug>
   ```

3. Write `_workspace/<slug>/00_input/source-report.md` before derived artifacts.
4. Normalize the request into `00_input/brief.md`. Record deliverable, audience, scope, page budget, text policy, and requested execution depth.
5. Convert the report into `01_research/research-summary.md`. Preserve claim IDs, statuses, sources, allowed wording, uncertainties, and prohibited wording. Do not cite the user report as independent corroboration.

## Design A Poster

1. Read `../infographic-orchestrator/SKILL.md`, `../infographic-storyboard/SKILL.md`, and `../infographic-panel-render/SKILL.md`.
2. Build 5-8 numbered blocks with a dominant narrative hero, supporting evidence or contrast cards, and a strong closing strip.
3. Use `hybrid` by default. Bake only short Korean titles, badges, labels, counters, and stamps. Keep dense explanations, exact policy language, and source notes outside the illustration.
4. Fill `storyboard.md`, `layout-bible.md`, `master-image-prompt.md`, `panel-prompts.md`, `imagegen-checklist.md`, and `handoff.md` from one shared block map.
5. Run the Korean copy voice pass over every baked headline, badge, stamp, label, and closing line before the prompts are frozen, following `references/korean-copy-voice-rules.md` in the repository root. Headlines and closing strips are where the AI tells concentrate: colon subtitles, `A가 아니라 B` parallelism, `X에서 Y로`, hype adjectives, and summation labels. Record the result under `## Korean Copy Voice Pass` in `imagegen-checklist.md`. In the same pass, apply `references/korean-baked-text-spelling-rules.md`: the smallest strings (badges, stamps, axis numbers, arrow labels) fail rasterization most, and display-size titles must avoid compound final consonants.

## Design An Adult Learning Comic

1. Read `../infographic-orchestrator/SKILL.md`, `../infographic-storyboard/SKILL.md`, and `../infographic-panel-render/SKILL.md`.
2. Define the audience's plausible surface belief, missing distinction, corrected model, limits, and transfer decision in `learning-design.md` before writing pages.
3. Assign one learning objective, one before/after knowledge state, and one central visual model to every page.
4. Use 2-4 stable adult characters. Check `cast/` for reusable profiles before inventing anyone; if one fits, copy its `identity_tokens` and `voice` verbatim and note the profile id (format: `references/cast-library-format.md`). Run `python scripts/cast_usage.py --eligibility` first and obey the rotation rule in `AGENTS.md`; then **stop and get the user's approval of the proposed cast** before writing `character-bible.md` and before any `character_sheet` render. If they reject it or ask for different people, re-propose from the remaining pool and do not re-offer a rejected profile in the same run. Skip the approval step only when `cast/` is empty or nobody fits and the cast is designed from scratch. Lock identity and speaking roles in `character-bible.md` before page prompts. Before locking, check that every pair of cast members is visually distinguishable at page scale; when two would be confusable (same age band, same hair length and color, same outfit silhouette), apply a **run-scoped appearance override** — change a non-identity-critical attribute for this run only, record it in `character-bible.md` with its trigger and scope, and leave `cast/<id>.character.yaml` untouched. See the Confusable cast rule in `AGENTS.md` and step 5 of "How A Run Consumes This" in `references/cast-library-format.md`. Real people from the report may be cast directly at maximum recognizable likeness per the repository's Usage Context And Likeness Policy; fill the Real-Person Casting block in `character-bible.md` including identity reference image paths and a stylized fallback descriptor. A `cast/` profile supplies photo references through its `reference_images`; a real person with no profile uses ad-hoc images under `00_input/refs/` (ask the user for them if none exist and continue with text tokens only if they are unavailable).
5. Use `dialogue-baked` by default. Whitelist every exact title, panel label, diagram label, formula, speech bubble, narration box, and reference-material string, grouped by channel; prohibit all extra text.
6. Use `extended` explanation density by default: about 450 Korean characters of baked copy per page, hard cap 500. Spend the added budget on third-person narration boxes (2-3 per page, at most 1 per panel, 25-60 characters each) and in-world reference-material inserts (1-2 per page, drawn as a document, screen, memo, whiteboard, or mini table), not on longer speech bubbles. Narration carries context, numbers, timeframes, transitions, and source cues only; the core reveal and mechanism stay with the cast and the dominant diagram. Narration keeps a claim's attribution and never carries a `needs verification` claim. Drop to `standard` density (about 300 characters) when legibility keeps failing.
7. Lock voice before writing page copy, then run one voice pass before freezing the whitelist. Follow `references/korean-copy-voice-rules.md` in the repository root. Run the spelling-robustness pass at the same time, per `references/korean-baked-text-spelling-rules.md` — fragile strings get replaced while the copy is still soft, because after a page renders a string fix costs that render.
   - Fill the Voice Lock block in `character-bible.md` together with the identity tokens: relationship map, each character's speech level, and each character's ending set. A `cast/` profile's `voice` is copied verbatim and outranks the generic rules; do not normalize a real person's catchphrases.
   - Give each character a distinct ending set (explainer explains, learner asks, challenger counters) and hold the register for the whole series. A cast that all speaks the same 존댓말 with the same 종결어미 is the loudest AI tell this track produces.
   - Before freezing each page's exact-copy whitelist, check every string against the S1 banned list: summation labels, significance inflation, enumeration intros, hype adjectives, closing formulas, formal-noun endings, sentence-initial connectives in narration, double passives, `~에 의해`, `~에 대해`, third-person pronouns, emoji, emphasis quotes. Recount characters after the fixes; they usually shorten the string.
   - Count series-wide, not per page: English gloss on first use only, parallelism at most once, `X에서 Y로` at most once, colon-subtitle titles never.
   - The claim ledger wins. Remove stylistic hedges only; a hedge carrying `party-claim`, `analysis`, or `speculation` attribution stays, and no voice fix may upgrade a claim or introduce a figure the report does not support.
   - Record the pass under `## Korean Copy Voice Pass` in `imagegen-checklist.md`. Run it before rendering: fixing a string afterwards costs that page's render.
8. Enumerate the exact panel count and every panel in each page prompt. Put a closing group scene inside a named panel; do not append a free-floating closing-scene instruction that can create an extra panel.
9. Fill a complete 2-8 page series in `storyboard.md`, `layout-bible.md`, and `series-prompts.md`, including exactly one `thumbnail` slot: a single landscape catalog cover with one short Korean topic phrase (2-6 words) and one simple motif, no comic panels or body text. Keep `master-image-prompt.md` and `panel-prompts.md` present and explicitly route rendering to `series-prompts.md`.
10. Resolve the opening misconception on the final page with a reframe, retrieval question, and transfer question. Write the reframe and the decision rule as concrete assertions, not as `결론적으로`, `~할 때입니다`, or `~해야 합니다` — the closing page is where those formulas cluster.

## Verify And Render

1. Run the package verifier until it exits 0:

   ```bash
   bash scripts/verify_infographic_run.sh _workspace/<slug>
   ```

2. For a learning comic, run the full parser dry-run and require every slot to resolve without warnings:

   ```bash
   python scripts/render_openai.py --slug <slug> --track adult-learning-comic --mode series --dry-run
   ```

3. Render only through `scripts/render_openai.py`. Never create or claim files under `05_renders/` by another path.
4. After an actual render, read `_workspace/<slug>/04_review/render-cost-report.md` and include the reported token usage and estimated cost in the handoff or final summary. Treat rows marked with estimated output tokens as estimates, not exact billing data.
5. For a learning comic with real-person cast, attach photo identity references to the character-sheet render only, with `--identity-reference <path>` (repeatable). Page renders inherit the likeness from `character-sheet.png`; do not re-feed the source photos per page.
6. For a learning comic, render `character_sheet` and `page_01` first. Measure the sheet's proportions before going further: head fits 7-8 times into the standing height, hip line at 48-52%, no hair or shoes clipped. A failure is a sheet-only re-render (`--mode series --only character_sheet`), which leaves already-approved pages alone; record any sheet/page anatomy mismatch in `handoff.md`. Inspect both before rendering the remaining pages and the landscape `thumbnail` with the same character sheet reference. The thumbnail renders automatically in `--mode series` (default size `1536x1024`; override with `--thumbnail-size` or `OPENAI_THUMBNAIL_SIZE`).
7. For a poster, render the one-shot first. Use block fallback only when the one-shot fails composition, legibility, or claim-safety checks.
8. If credentials or the Images API are unavailable, finish the verified prompt package, record the blocker, and do not fabricate renders.

## Visual QA

Inspect every rendered image and record the result in `imagegen-checklist.md` and `handoff.md`.

- Confirm the requested page count and reading order.
- Confirm character face, age, outfit, color, and role continuity.
- Confirm that every panel teaches or advances one intended beat.
- Check Korean text for corruption, invention, duplication, cropping, and overflow.
- Check the rendered copy against the voice pass: no S1 pattern survived into the image, each character's register and ending set held across pages, and the series-wide counts still hold. A defect found here means re-rendering that page or recording the accepted defect in `handoff.md`.
- Check the page baked-copy total against the density budget and confirm no panel is text-choked.
- Check that narration boxes are tail-less and speaker-less, carry only context/numbers/transitions/source cues, and do not replace the cast and diagram as the source of the reveal.
- Check that reference-material inserts read as objects in the scene and stay legible at full page size.
- Check that attributed claims remain attributed and speculation is not staged as verified fact, including inside narration boxes.
- Check diagrams, formulas, timelines, and exact names against the report.
- Report actual filenames. Never treat a dry-run, placeholder, or prompt as a rendered image.

## Completion Contract

Finish only when the verifier passes, the learning-series dry-run has no parser warnings when applicable, handoff names the exact next or completed render action, and any claimed PNG exists on disk. Summarize what came directly from the report, what was inferred for pedagogy or art direction, and what remains unverified.
