#!/usr/bin/env bash

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: bash scripts/verify_infographic_run.sh <run_dir>" >&2
  exit 1
fi

RUN_DIR="$1"
FAIL=0

required_files=(
  "${RUN_DIR}/00_input/brief.md"
  "${RUN_DIR}/01_research/research-summary.md"
  "${RUN_DIR}/02_storyboard/storyboard.md"
  "${RUN_DIR}/02_storyboard/layout-bible.md"
  "${RUN_DIR}/03_prompts/master-image-prompt.md"
  "${RUN_DIR}/03_prompts/panel-prompts.md"
  "${RUN_DIR}/04_review/imagegen-checklist.md"
  "${RUN_DIR}/04_review/handoff.md"
)

for file in "${required_files[@]}"; do
  if [[ ! -f "${file}" ]]; then
    echo "missing file: ${file}" >&2
    FAIL=1
  fi
done

check_heading() {
  local file="$1"
  local pattern="$2"
  local label="$3"
  if ! rg -q "${pattern}" "${file}"; then
    echo "missing ${label}: ${file}" >&2
    FAIL=1
  fi
}

check_pattern() {
  local file="$1"
  local pattern="$2"
  local label="$3"
  if ! rg -q "${pattern}" "${file}"; then
    echo "missing ${label}: ${file}" >&2
    FAIL=1
  fi
}

is_learning_comic=0
if [[ -f "${RUN_DIR}/02_storyboard/storyboard.md" ]] && \
  rg -q '^- Selected: `adult-learning-comic`' "${RUN_DIR}/02_storyboard/storyboard.md"; then
  is_learning_comic=1
fi

if [[ -f "${RUN_DIR}/02_storyboard/storyboard.md" ]]; then
  check_heading "${RUN_DIR}/02_storyboard/storyboard.md" "^## Section Map" "Section Map heading"
  check_heading "${RUN_DIR}/02_storyboard/storyboard.md" "^## Blocks" "Blocks heading"
fi

if [[ -f "${RUN_DIR}/02_storyboard/layout-bible.md" ]]; then
  check_heading "${RUN_DIR}/02_storyboard/layout-bible.md" "^## Grid" "Grid heading"
  check_heading "${RUN_DIR}/02_storyboard/layout-bible.md" "^## Render Mode" "Render Mode heading"
  check_heading "${RUN_DIR}/02_storyboard/layout-bible.md" "^## Storyboard Mode" "Storyboard Mode heading"
  if ! rg -q "editorial-poster|vertical-webtoon-page|adult-learning-comic" "${RUN_DIR}/02_storyboard/layout-bible.md"; then
    echo "missing storyboard mode value: ${RUN_DIR}/02_storyboard/layout-bible.md" >&2
    FAIL=1
  fi
fi

if [[ -f "${RUN_DIR}/02_storyboard/storyboard.md" ]]; then
  if ! rg -q "editorial-poster|vertical-webtoon-page|adult-learning-comic" "${RUN_DIR}/02_storyboard/storyboard.md"; then
    echo "missing storyboard mode value: ${RUN_DIR}/02_storyboard/storyboard.md" >&2
    FAIL=1
  fi
fi

if [[ -f "${RUN_DIR}/03_prompts/master-image-prompt.md" ]]; then
  check_heading "${RUN_DIR}/03_prompts/master-image-prompt.md" "^## Master Prompt" "Master Prompt heading"
fi

if [[ -f "${RUN_DIR}/03_prompts/panel-prompts.md" ]]; then
  check_heading "${RUN_DIR}/03_prompts/panel-prompts.md" "^## Panel Prompt Pack" "Panel Prompt Pack heading"
fi

if [[ -f "${RUN_DIR}/04_review/imagegen-checklist.md" ]]; then
  check_heading "${RUN_DIR}/04_review/imagegen-checklist.md" "^## Render Mode" "Render Mode heading"
fi

if [[ -f "${RUN_DIR}/04_review/handoff.md" ]]; then
  check_heading "${RUN_DIR}/04_review/handoff.md" "^## First Render Pass" "First Render Pass heading"
fi

if [[ "${is_learning_comic}" -eq 1 ]]; then
  learning_files=(
    "${RUN_DIR}/02_storyboard/learning-design.md"
    "${RUN_DIR}/02_storyboard/character-bible.md"
    "${RUN_DIR}/03_prompts/series-prompts.md"
  )
  for file in "${learning_files[@]}"; do
    if [[ ! -f "${file}" ]]; then
      echo "missing adult-learning-comic file: ${file}" >&2
      FAIL=1
    fi
  done

  learning_design="${RUN_DIR}/02_storyboard/learning-design.md"
  if [[ -f "${learning_design}" ]]; then
    check_heading "${learning_design}" "^## Audience And Prerequisites" "Audience And Prerequisites heading"
    check_heading "${learning_design}" "^## Learning Contract" "Learning Contract heading"
    check_heading "${learning_design}" "^## Claim Ledger" "Claim Ledger heading"
    check_heading "${learning_design}" "^## Misconception Ladder" "Misconception Ladder heading"
    check_heading "${learning_design}" "^## Explanation Spine" "Explanation Spine heading"
    check_heading "${learning_design}" "^## Page Arc" "Page Arc heading"
    check_heading "${learning_design}" "^## Assessment" "Assessment heading"
    check_heading "${learning_design}" "^## Accuracy Gates" "Accuracy Gates heading"
    check_pattern "${learning_design}" "^- Final one-sentence reframe: .+" "final reframe"
    check_pattern "${learning_design}" "^- Retrieval question: .+" "retrieval question"
    check_pattern "${learning_design}" "^- Transfer question: .+" "transfer question"
  fi

  character_bible="${RUN_DIR}/02_storyboard/character-bible.md"
  if [[ -f "${character_bible}" ]]; then
    check_heading "${character_bible}" "^## Cast Lock" "Cast Lock heading"
    check_heading "${character_bible}" "^## Identity Tokens" "Identity Tokens heading"
    check_heading "${character_bible}" "^## Role Continuity" "Role Continuity heading"
    check_heading "${character_bible}" "^## Visual Continuity" "Visual Continuity heading"
    check_heading "${character_bible}" "^## Reference Render" "Reference Render heading"
    check_heading "${character_bible}" "^## Prohibited Drift" "Prohibited Drift heading"
    check_pattern "${character_bible}" "character-sheet\.png" "character sheet output contract"
    check_pattern "${character_bible}" "^- Explainer immutable tokens: .+" "explainer identity tokens"
    check_pattern "${character_bible}" "^- Learner immutable tokens: .+" "learner identity tokens"
  fi

  series_prompts="${RUN_DIR}/03_prompts/series-prompts.md"
  if [[ -f "${series_prompts}" ]]; then
    check_heading "${series_prompts}" "^## Shared Prompt Policy" "Shared Prompt Policy heading"
    check_heading "${series_prompts}" "^## Shared Negative Prompt" "Shared Negative Prompt heading"
    check_heading "${series_prompts}" "^### character_sheet" "character_sheet slot"

    page_count="$(rg -c '^### page_[0-9][0-9]\b' "${series_prompts}" || true)"
    if [[ "${page_count}" -lt 2 || "${page_count}" -gt 8 ]]; then
      echo "adult-learning-comic requires 2-8 page prompts; found ${page_count}: ${series_prompts}" >&2
      FAIL=1
    fi

    objective_count="$(rg -c '^- learning objective: .+' "${series_prompts}" || true)"
    before_count="$(rg -c '^- knowledge state before: .+' "${series_prompts}" || true)"
    after_count="$(rg -c '^- knowledge state after: .+' "${series_prompts}" || true)"
    visual_count="$(rg -c '^- central visual model: .+' "${series_prompts}" || true)"
    copy_count="$(rg -c '^- exact baked copy: .+' "${series_prompts}" || true)"
    reminder_count="$(rg -c '^- character reminder: .+' "${series_prompts}" || true)"

    if [[ "${objective_count}" -lt "${page_count}" || \
          "${before_count}" -lt "${page_count}" || \
          "${after_count}" -lt "${page_count}" || \
          "${visual_count}" -lt "${page_count}" || \
          "${copy_count}" -lt "${page_count}" || \
          "${reminder_count}" -lt "${page_count}" ]]; then
      echo "one or more page prompts lack required learning metadata: ${series_prompts}" >&2
      FAIL=1
    fi

    if rg -q "Replace this block|TODO|TBD|<fill" "${series_prompts}"; then
      echo "unfinished placeholder remains in series prompts: ${series_prompts}" >&2
      FAIL=1
    fi
  fi

  if [[ -f "${RUN_DIR}/04_review/imagegen-checklist.md" ]]; then
    check_heading "${RUN_DIR}/04_review/imagegen-checklist.md" "^## Adult Learning Comic Validation" "Adult Learning Comic Validation heading"
  fi

  if [[ -f "${RUN_DIR}/04_review/handoff.md" ]]; then
    check_pattern "${RUN_DIR}/04_review/handoff.md" "character-sheet\.png" "character sheet handoff"
    check_pattern "${RUN_DIR}/04_review/handoff.md" "page-01\.png" "page 01 handoff"
  fi
fi

if [[ "${FAIL}" -ne 0 ]]; then
  exit 1
fi

echo "verified: ${RUN_DIR}"
