# Infographic And Learning Comic Harness

## Purpose
- This repo is a harness for producing either a **single-page infographic poster** or a **2-8 page adult learning comic series** with recurring characters.
- This repo is **not** responsible for HTML page assembly. It stops at image-generation guidance, prompt packs, and image QA handoff.
- One narrow exception: `scripts/render_openai.py` is allowed to call the OpenAI Images API (default model `gpt-image-2`) and write real files to `_workspace/<slug>/05_renders/`. The rest of the harness must still treat rendering as downstream — never claim renders exist unless the files actually exist on disk.
- Treat dense Korean copy as a reliability problem. Default to an **image-first but text-conservative workflow**:
  - Generate illustrations, scene boxes, badges, stamps, and atmosphere with image prompts.
  - Keep long exact Korean body copy out of the baked image unless the user explicitly asks for a risky all-baked render.
- Use full in-image Korean text only for short headlines, badges, labels, counters, and stamps unless the user explicitly wants a riskier all-baked render.

## Project Commands
- Initialize a new run: `bash scripts/init_infographic_run.sh <slug>`
- Verify a run package: `bash scripts/verify_infographic_run.sh _workspace/<slug>`
- Render via OpenAI Images API (optional):
  - poster/page: `python scripts/render_openai.py --slug <slug> --track <editorial-poster|vertical-webtoon-page|both> --mode <oneshot|fallback|all>`
  - learning series: `python scripts/render_openai.py --slug <slug> --track adult-learning-comic --mode series`
  - requires `.env` with `OPENAI_API_KEY`; add `--dry-run` to preview the render plan.

## Workspace Contract
- Every run lives under `_workspace/<slug>/`.
- Standalone source-report drafts that are not yet production runs live under `reports/<slug>-source-report.md` unless the user names another path.
- Required files:
  - `00_input/brief.md`
  - `01_research/research-summary.md`
  - `02_storyboard/storyboard.md`
  - `02_storyboard/layout-bible.md`
  - `03_prompts/master-image-prompt.md`
  - `03_prompts/panel-prompts.md`
  - `04_review/imagegen-checklist.md`
  - `04_review/handoff.md`
- Additional required files for `adult-learning-comic`:
  - `02_storyboard/learning-design.md`
  - `02_storyboard/character-bible.md`
  - `03_prompts/series-prompts.md`
- Optional generated assets:
  - `05_renders/block_*.png`
  - `05_renders/final-poster.png`
  - `05_renders/character-sheet.png`
  - `05_renders/thumbnail.png` (landscape catalog cover for the series list page)
  - `05_renders/page-01.png` through `page-08.png`

## Cross-Tool Skill Entry Point
- The canonical report drafting, validation, and infographic-toon production workflow lives at `.claude/skills/report-to-infographic-toon/SKILL.md`.
- Claude Code uses the canonical `.claude/skills/` path.
- Codex discovers the repo skill through `.agents/skills/report-to-infographic-toon/SKILL.md`; that entry point must delegate to the canonical workflow instead of duplicating it.
- Use the same skill for three task modes: source-report drafting/normalization, source-report validation, and approved-report-to-infographic production.
- Do not perform additional research during report normalization unless the user explicitly requests research. Mark unsupported material `needs verification`.

## Target Visual Grammar
- Default target is a **dark, editorial, cinematic infographic-toon poster**.
- Preferred page logic:
  - large left-side hero narrative block
  - stacked right-side information cards
  - alternating dark scene panels and light paper/table cards
  - strong closing footer or slogan block
- Preferred visual ingredients:
  - navy or charcoal background
  - amber/gold accent
  - red warning or denied stamps
  - off-white data cards for tables and checklists
  - beveled borders, sticker-like badges, emergency bulletin energy
- Preferred information shapes:
  - numbered scene headers
  - versus tables
  - three-step chains
  - checklist cards
  - quote or warning stamps
- Do not flatten everything into one uniform card system. The page should feel editorial and dramatic, not dashboard-like.

## Adult Learning Comic Grammar
- Use `adult-learning-comic` when the user asks for a character-led educational comic, an explainer series, or a sequence like the LLM learning-comic reference.
- Default to 3-6 pages, allow 2 pages for deliberately narrow micro-lessons, and cap at 8 pages. Each page is one portrait image with a title bar, 4-6 comic/diagram panels, and a short recap or forward hook.
- The series must change the reader's knowledge state, not merely decorate facts. Use this default arc unless the topic requires another:
  1. surface belief or plausible misconception
  2. contrasting model or missing concept
  3. core reveal or proof
  4. mechanism and visual intuition
  5. transfer to an adjacent real-world case
  6. recap, decision rule, or retrieval check
- Use 2-4 recurring adult characters with stable jobs and speaking roles:
  - explainer: introduces evidence, mechanism, and limits
  - learner: voices a competent adult's plausible questions
  - optional second learner: tests transfer or raises objections
  - optional mascot: carries transitions and summaries, never replaces the explanation
- Lock face shape, hair, outfit, age band, color tokens, and role before page prompts are written. Render `character-sheet` first and use it as a high-fidelity reference for all page renders.
- Avoid school uniforms, child-coded proportions, chibi rendering, juvenile slang, fan-service, and empty reaction panels. The tone may be friendly and anime/webtoon-inspired while remaining professional and technically serious.
- Every page must declare one learning objective, the reader's knowledge state before/after, one central visual model, and an exact-copy budget.

## Baked Text Rules
- Safe baked text:
  - short Korean titles
  - numeric labels
  - warning stamps
  - 1-6 word badges
  - very short callouts
- Risky baked text:
  - long body paragraphs
  - dense comparison tables
  - exact legal or technical wording
  - multi-line checklist items
- If a block depends on exact Korean readability, mark it in `layout-bible.md` and keep the prompt visually suggestive instead of text-heavy.
- `adult-learning-comic` may use `dialogue-baked` mode:
  - exact page title, panel labels, diagram labels, formulas, and short/medium speech bubbles may be baked
  - prefer 1-2 bubbles per panel and one idea per bubble
  - keep paragraph prose, citations, and source notes out of illustrated panels; reserve a simple footer box
  - copy every exact string into the page prompt and prohibit extra text

## Workflow
### When Starting A New Infographic
- Run `bash scripts/init_infographic_run.sh <slug>`.
- Normalize the user brief into `00_input/brief.md`.
- Distill facts, framing, and risk notes into `01_research/research-summary.md`.
- Convert the brief into 5-8 numbered content blocks in `02_storyboard/storyboard.md`.
- Define layout, palette, typography, iconography, and text-density rules in `02_storyboard/layout-bible.md`.
- Produce both:
  - `03_prompts/master-image-prompt.md` for one-shot poster generation.
  - `03_prompts/panel-prompts.md` for block-by-block fallback generation.
- Write final checks and remaining risks in `04_review/imagegen-checklist.md`.
- Summarize what is ready, what is inferred, and what still needs rendering in `04_review/handoff.md`.

### When Starting An Adult Learning Comic
- Run `bash scripts/init_infographic_run.sh <slug>`.
- Normalize topic, adult audience, prior knowledge, desired depth, source material, and page budget in `00_input/brief.md`.
- Build a claim ledger in `01_research/research-summary.md`; mark unsupported or unstable claims `needs verification`.
- Fill `02_storyboard/learning-design.md` before drawing the page storyboard. It must define learning objectives, misconception ladder, explanation spine, page-level knowledge-state changes, and a final retrieval/transfer check.
- Fill `02_storyboard/character-bible.md` with stable visual identity tokens and speaking roles.
- Write a 2-8 page series map in `02_storyboard/storyboard.md` and the series-wide page grammar in `02_storyboard/layout-bible.md`.
- Produce `03_prompts/series-prompts.md` with:
  - one shared prompt policy
  - one `character_sheet` prompt
  - one `thumbnail` prompt (single landscape catalog cover: one short Korean topic phrase plus one simple motif, nothing more)
  - one complete `page_XX` prompt per page
- Render the character sheet first. Render the thumbnail and every page through the image edit endpoint using that sheet as a reference unless the user explicitly disables reference conditioning. The thumbnail renders once per series at landscape size (default `1536x1024`; the catalog page crops to 16:10).
- Record factual, pedagogical, Korean-text, and continuity checks in `04_review/imagegen-checklist.md` and exact render order in `04_review/handoff.md`.

### When Revising An Existing Run
- Read the existing run package first.
- Change the smallest necessary artifact.
- Do not rewrite accepted sections unless the brief changed.

## Definition Of Done
A task is complete only when all of the following are true:
1. `bash scripts/verify_infographic_run.sh _workspace/<slug>` exits `0`.
2. `storyboard.md` contains numbered sections, visual intent, and copy buckets.
3. `layout-bible.md` defines grid, palette, typography, and render mode.
4. `master-image-prompt.md` and `panel-prompts.md` both exist and reflect the same storyboard.
5. `imagegen-checklist.md` records baked-text policy, known render risks, and validation checks.
6. `handoff.md` tells the downstream renderer exactly what to render first.
7. The agent does not claim image rendering happened unless files actually exist under `05_renders/`.
8. For `adult-learning-comic`, `learning-design.md`, `character-bible.md`, and `series-prompts.md` pass the mode-specific verifier.
9. For `adult-learning-comic`, the series contains 2-8 page prompts, each with a learning objective, knowledge-state change, exact-copy contract, panel sequence, and character reminder.
10. A dry-run of `scripts/render_openai.py --track adult-learning-comic --mode series` resolves `character_sheet`, `thumbnail`, and every `page_XX` slot without parser warnings.

## When Blocked
- If factual claims are uncertain, mark them as `needs verification` in the research summary.
- If image tools are unavailable, still finish the **prompt pack + image QA handoff** and state the blocker clearly.
- If the brief is too text-dense for reliable baked Korean rendering, keep long copy out of the image prompts and record that decision in `layout-bible.md`.
- Never invent screenshots, final posters, or rendered panels that do not exist on disk. `scripts/render_openai.py` is the only path that may create files under `05_renders/`; if it fails, report the failure — do not fabricate outputs.

## Editing Rules
- Keep prompts and templates in ASCII where possible; Korean content is allowed in user-facing artifacts.
- Prefer updating templates and skills over burying workflow rules in prose.
- Keep repo-wide rules here; keep workflow detail in `.claude/skills/`.
