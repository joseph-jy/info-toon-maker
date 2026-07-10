---
name: report-to-infographic-toon
description: Draft, normalize, and validate a source-backed dry report from user research notes, then turn an approved report into either a single-page Korean editorial infographic-toon poster or a 4-8 page adult learning comic, including run initialization, claim-safe story design, prompt packs, verification, optional OpenAI image rendering, and visual QA. Use when the user says "조사 메모를 리포트로 정리해줘", "리포트 작성 가이드에 맞춰 작성해줘", "리포트 검증해줘", "위 리포트를 포스터 형태의 웹툰으로 만들어줘", "성인용 학습만화로 만들어줘", "리포트로 인포툰을 기획해줘", or asks to revise an existing report-based run.
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
- Map `성인용 학습만화`, `학습 웹툰`, `4-8페이지`, or a requested page range to `adult-learning-comic`.
- Require one of these two deliverables. If neither is explicit and the surrounding request does not resolve it, ask one short question.
- Respect an exact page count. For a range, choose the smallest count that supports the required knowledge-state changes; stay within 4-8 pages.

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

## Design An Adult Learning Comic

1. Read `../infographic-orchestrator/SKILL.md`, `../infographic-storyboard/SKILL.md`, and `../infographic-panel-render/SKILL.md`.
2. Define the audience's plausible surface belief, missing distinction, corrected model, limits, and transfer decision in `learning-design.md` before writing pages.
3. Assign one learning objective, one before/after knowledge state, and one central visual model to every page.
4. Use 2-4 stable adult characters. Lock identity and speaking roles in `character-bible.md` before page prompts.
5. Use `dialogue-baked` by default. Whitelist every exact title, diagram label, formula, and speech bubble; prohibit all extra text.
6. Enumerate the exact panel count and every panel in each page prompt. Put a closing group scene inside a named panel; do not append a free-floating closing-scene instruction that can create an extra panel.
7. Fill a complete 4-8 page series in `storyboard.md`, `layout-bible.md`, and `series-prompts.md`. Keep `master-image-prompt.md` and `panel-prompts.md` present and explicitly route rendering to `series-prompts.md`.
8. Resolve the opening misconception on the final page with a reframe, retrieval question, and transfer question.

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
4. For a learning comic, render `character_sheet` and `page_01` first. Inspect both before rendering the remaining pages with the same character sheet reference.
5. For a poster, render the one-shot first. Use block fallback only when the one-shot fails composition, legibility, or claim-safety checks.
6. If credentials or the Images API are unavailable, finish the verified prompt package, record the blocker, and do not fabricate renders.

## Visual QA

Inspect every rendered image and record the result in `imagegen-checklist.md` and `handoff.md`.

- Confirm the requested page count and reading order.
- Confirm character face, age, outfit, color, and role continuity.
- Confirm that every panel teaches or advances one intended beat.
- Check Korean text for corruption, invention, duplication, cropping, and overflow.
- Check that attributed claims remain attributed and speculation is not staged as verified fact.
- Check diagrams, formulas, timelines, and exact names against the report.
- Report actual filenames. Never treat a dry-run, placeholder, or prompt as a rendered image.

## Completion Contract

Finish only when the verifier passes, the learning-series dry-run has no parser warnings when applicable, handoff names the exact next or completed render action, and any claimed PNG exists on disk. Summarize what came directly from the report, what was inferred for pedagogy or art direction, and what remains unverified.
