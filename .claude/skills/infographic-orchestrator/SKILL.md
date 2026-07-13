---
name: infographic-orchestrator
description: "단일 페이지 인포그래픽, PAGE형 세로 웹툰, 또는 2-8페이지 성인 학습만화를 위한 이미지 생성 하네스 오케스트레이터. 학습만화에서는 학습 목표, 오개념 교정, 캐릭터 바이블, 페이지별 지식 상태 변화, 시리즈 프롬프트와 이미지 QA까지 만든다. 트리거: '인포그래픽 만들어', '웹툰 느낌 인포그래픽', '성인용 학습만화', '캐릭터가 설명하는 만화', '이 주제를 만화로 가르쳐줘'."
---

# Infographic Orchestrator

긴 서사를 **한 장의 세로 포스터**, **한 페이지짜리 세로 웹툰 인포그래픽**, 또는 **2-8페이지 성인 학습만화 시리즈**로 설계하는 하네스다.

## Core Principle

이 하네스는 **이미지 생성 규칙 전용**이다. HTML/CSS/뷰어 조립은 다루지 않는다.

기본값은 **text-conservative hybrid prompt mode**다.

- 짧은 제목, 배지, 스탬프, 경고 라벨은 이미지에 베이크할 수 있다.
- 긴 한국어 본문, 표, 체크리스트, 비교표는 baked text로 무리하게 밀어 넣지 않는다.
- 사용자가 명시적으로 원하면 `all-baked` 프롬프트도 함께 만든다. 다만 리스크를 기록한다.

기본 시각 문법은 다음을 따른다.
- 좌측 대형 hero 블록 + 우측 stacked info cards + 하단 closing/footer
- 또는 검은 PAGE title bar + 4-6개 가로 패널 + 주석/footer
- dark editorial poster + emergency bulletin + dossier card의 혼합
- 장면 카드와 데이터 카드를 섞되, 전부 같은 박스로 평탄화하지 않음

## Output Contract

Run root: `_workspace/<slug>/`

- `00_input/brief.md`
- `01_research/research-summary.md`
- `02_storyboard/storyboard.md`
- `02_storyboard/layout-bible.md`
- `03_prompts/master-image-prompt.md`
- `03_prompts/panel-prompts.md`
- `04_review/imagegen-checklist.md`
- `04_review/handoff.md`

`adult-learning-comic` 추가 산출:
- `02_storyboard/learning-design.md`
- `02_storyboard/character-bible.md`
- `03_prompts/series-prompts.md`

Optional:
- `05_renders/block_*.png`
- `05_renders/final-poster.png`
- `05_renders/character-sheet.png`
- `05_renders/page-*.png`

## Workflow

### Phase 0: Run Detection
1. If no run exists, initialize with `bash scripts/init_infographic_run.sh <slug>`.
2. If a run exists, read the current artifacts before changing anything.
3. If the user changes the story materially, revise `brief.md` first and cascade only the necessary downstream files.

### Phase 1: Brief Normalization
1. Convert the user prompt/report into `00_input/brief.md`.
2. Identify:
   - must-keep facts
   - inferred framing
   - places where exact wording matters
   - sections too text-dense for safe baked rendering

### Phase 2: Research Compression
1. Write `01_research/research-summary.md`.
2. Reduce the long report into:
   - core narrative
   - conflict map
   - visualizable blocks
   - risk notes
3. Mark uncertain claims as `needs verification`.

### Phase 3: Storyboard
1. Use `infographic-storyboard`.
2. Choose the storyboard mode:
   - `editorial-poster` for a one-page asymmetric poster
   - `vertical-webtoon-page` for `PAGE 1` / `PAGE 2` style comic-infographic pages
   - `adult-learning-comic` for a coherent 2-8 page character-led teaching series
3. Break the page into 5-8 blocks for poster mode, or 4-6 panels for webtoon page mode.
4. Each block or panel must specify:
   - purpose
   - story beat
   - visual motif
   - copy bucket
   - baked-text policy
   - image prompt intent
5. Prefer this block rhythm unless the brief strongly disagrees:
   - prologue hero
   - technical/comparison block
   - risk/dilemma block
   - geopolitical escalation block
   - strategic close or checklist
6. For `adult-learning-comic`, keep the whole series in one run. Fill `learning-design.md` and `character-bible.md` before page prompts.
7. The learning-series default arc is surface belief -> missing model -> reveal -> mechanism -> transfer/limits -> reframe/recall.

### Phase 4: Prompt Pack
1. Use `infographic-panel-render`.
2. Produce both:
   - a one-shot poster prompt
   - block-by-block prompts for fallback rendering
3. For `adult-learning-comic`, produce `series-prompts.md` instead: shared policy + character sheet + one `page_XX` prompt per page.
4. Keep the storyboard and prompt pack strictly aligned.

### Phase 5: Image QA
1. Run `bash scripts/verify_infographic_run.sh _workspace/<slug>`.
2. Fill `imagegen-checklist.md` with:
   - render mode
   - baked-text policy
   - known render risks
   - first-pass validation points
3. Fill `handoff.md` with the next render action and recommended order.
4. For `adult-learning-comic`, verify the character sheet first, then page 01, then the remaining pages using the same reference image.

## Decision Rules

- If the poster requires dense tables or long Korean body paragraphs, choose `hybrid`.
- If the user explicitly asks for a single raster image with all text baked in, still generate block prompts as fallback.
- Never claim rendering completed unless image files exist on disk.

## Minimal Team Topology

This harness works best with these roles:
- `brief-analyst`
- `research-synthesizer`
- `storyboard-architect`
- `art-director`
- `prompt-smith`
- `panel-validator`

Use only the smallest subset needed for the request.
