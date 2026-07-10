#!/usr/bin/env bash

set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "usage: bash scripts/init_infographic_run.sh <slug> [target_dir]" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SLUG="$1"
TARGET_DIR="${2:-${REPO_ROOT}/_workspace/${SLUG}}"

if [[ -e "${TARGET_DIR}" ]]; then
  echo "target already exists: ${TARGET_DIR}" >&2
  exit 1
fi

mkdir -p \
  "${TARGET_DIR}/00_input" \
  "${TARGET_DIR}/01_research" \
  "${TARGET_DIR}/02_storyboard" \
  "${TARGET_DIR}/03_prompts" \
  "${TARGET_DIR}/04_review" \
  "${TARGET_DIR}/05_renders"

cp "${REPO_ROOT}/templates/brief.template.md" "${TARGET_DIR}/00_input/brief.md"
cp "${REPO_ROOT}/templates/research-summary.template.md" "${TARGET_DIR}/01_research/research-summary.md"
cp "${REPO_ROOT}/templates/storyboard.template.md" "${TARGET_DIR}/02_storyboard/storyboard.md"
cp "${REPO_ROOT}/templates/layout-bible.template.md" "${TARGET_DIR}/02_storyboard/layout-bible.md"
cp "${REPO_ROOT}/templates/learning-design.template.md" "${TARGET_DIR}/02_storyboard/learning-design.md"
cp "${REPO_ROOT}/templates/character-bible.template.md" "${TARGET_DIR}/02_storyboard/character-bible.md"
cp "${REPO_ROOT}/templates/master-image-prompt.template.md" "${TARGET_DIR}/03_prompts/master-image-prompt.md"
cp "${REPO_ROOT}/templates/panel-prompts.template.md" "${TARGET_DIR}/03_prompts/panel-prompts.md"
cp "${REPO_ROOT}/templates/series-prompts.template.md" "${TARGET_DIR}/03_prompts/series-prompts.md"
cp "${REPO_ROOT}/templates/imagegen-checklist.template.md" "${TARGET_DIR}/04_review/imagegen-checklist.md"
cp "${REPO_ROOT}/templates/handoff.template.md" "${TARGET_DIR}/04_review/handoff.md"

echo "initialized: ${TARGET_DIR}"
