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
  "${TARGET_DIR}/00_input/refs" \
  "${TARGET_DIR}/01_research" \
  "${TARGET_DIR}/02_storyboard" \
  "${TARGET_DIR}/03_prompts" \
  "${TARGET_DIR}/04_review" \
  "${TARGET_DIR}/05_renders"

cp "${REPO_ROOT}/templates/brief.template.md" "${TARGET_DIR}/00_input/brief.md"
cat > "${TARGET_DIR}/00_input/refs/README.md" <<'EOF'
# Identity Reference Images

실존 인물 캐스팅용 참조 이미지를 여기에 둔다.

- `cast/` 프로필이 있는 인물은 프로필의 `reference_images` 경로를 쓴다. 여기 복사하지 않는다.
- `cast/` 프로필이 없는 실존 인물(리포트에 등장하는 공인 등)의 사진만 여기 둔다.
- 파일명: `<person-slug>-01.jpg`
- `02_storyboard/character-bible.md`의 Real-Person Casting 블록에 경로를 적는다.
- 렌더는 캐릭터 시트에만 붙인다:
  `python scripts/render_openai.py --slug <slug> --track adult-learning-comic --mode series --identity-reference _workspace/<slug>/00_input/refs/<file>`
- 사진은 identity 참조 전용이다. 포즈, 구도, 배경, 조명, 의상 스냅샷을 그대로 옮기지 않고 시리즈 웹툰 스타일로 다시 그린다.
EOF
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
