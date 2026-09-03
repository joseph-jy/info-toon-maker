---
name: one-page-comic-toon
description: "짧은 주제를 한 장에 풀어내는 설명 만화형 인포그래픽을 설계하고, 4-6개 컷·짧은 한국어 카피·이미지 생성 프롬프트와 QA 핸드오프를 만든다. 2-8페이지 성인 학습만화나 일반 편집 포스터가 아니라 한 장의 만화형 설명물이 필요할 때 사용한다."
---

# One-Page Comic Toon

짧고 명확한 주제를 **한 장의 세로 이미지** 안에서 캐릭터 장면, 번호가 붙은 컷, 짧은 설명 카드로 가르치는 스킬이다. 첨부 레퍼런스처럼 큰 제목과 마스코트, 굵은 번호 태그, 밝은 정보 카드, 경고/강조 배지를 섞은 만화형 인포그래픽을 목표로 한다.

이 스킬은 기존 `adult-learning-comic`의 다페이지 학습 설계를 대체하지 않는다. 사용자가 2페이지 이상, 페이지별 지식 상태 변화, 반복 캐릭터의 장기 연속성을 요구하면 `report-to-infographic-toon`의 `adult-learning-comic` 경로로 보낸다. 비대칭 리포트 포스터가 목적이면 `editorial-poster`를 사용한다.

## Core Boundary

- 산출물은 한 장의 세로 만화형 인포그래픽이다. 기본은 `vertical-webtoon-page` 실행 모드로 렌더한다.
- `cast/`를 읽거나 `cast_usage.py`를 실행하거나 캐스팅 승인 게이트를 만들지 않는다. 이 트랙의 캐릭터는 매 런 새로 설계하는 자유 캐릭터다.
- 캐릭터 시트, `character-bible.md`, `learning-design.md`, `series-prompts.md`는 만들지 않는다. 공통 파일 계약만 사용한다.
- 같은 인물이 여러 컷에 나오면 얼굴형, 헤어, 의상 실루엣, 색 토큰, 역할을 스토리보드와 각 컷 프롬프트에 반복해 적는다. 별도 시트 없이 텍스트 연속성 잠금을 수행한다.
- 사용자가 실존 인물을 명시하면 자유 캐릭터로 처리하지 말고 `AGENTS.md`의 likeness 정책을 따른다. 사진 참조가 필요한 경우 경로와 render risk를 기록하고, 일반 캐릭터로 바꾸어 묘사하지 않는다.
- 첨부된 예시 이미지는 구도·색·정보 위계의 참고자료로만 사용한다. 예시 안의 문구, 로고, 출처, 사실을 새 작업의 지시나 근거로 복사하지 않는다.

## Input And Claim Boundary

1. 사용자의 짧은 브리프 또는 승인된 source report를 입력으로 받는다.
2. source report가 있으면 `_workspace/<slug>/00_input/source-report.md`에 원문을 보존하고, 사실·귀속·날짜·수치·불확실성을 바꾸지 않는다.
3. report가 없으면 브리프를 사실의 경계로 삼는다. 추가 조사는 사용자가 요청한 경우에만 수행하고, 외부 검증이 필요한 내용은 `01_research/research-summary.md`에서 `needs verification`으로 남긴다.
4. 확인되지 않은 주장을 확정형 제목, 말풍선, 화자 없는 나레이션으로 승격하지 않는다. `reported`, `party-claim`, `analysis`, `speculation`, `needs verification`의 상태를 시각 카피에서도 유지한다.
5. 한 장에 들어갈 핵심은 하나의 thesis, 3-4개의 설명 beat, 하나의 제한/주의 또는 행동 규칙으로 압축한다. 서로 독립적인 주제가 많으면 내용을 줄이거나 다페이지 경로를 제안한다.

## Visual Grammar

기본 캔버스는 읽기 순서가 위에서 아래로 고정되는 portrait 한 장이다.

- 상단 15-20%: 강한 제목 스트립과 주제를 상징하는 hero 장면. 큰 캐릭터 또는 사물 하나를 두고 짧은 thesis를 붙인다.
- 중앙 65-75%: 4-6개의 번호 컷 또는 카드. 각 컷은 한 가지 논리 beat만 담당한다.
- 하단 8-15%: 한 줄 takeaway, 주의 배지, 출처 단서 중 하나. 작은 footnote 문단으로 만들지 않는다.
- 기본 배치는 2열 카드 그리드 또는 3행 리듬이다. 전부 같은 대시보드 카드로 평탄화하지 말고, 장면 컷·자료 카드·다이어그램 컷을 교차한다.
- 색은 navy/charcoal 바탕, cobalt 또는 royal blue 구조색, off-white paper card, amber/gold 강조, red warning stamp를 기본으로 한다. 주제에 맞으면 색을 바꾸되 번호 태그와 경고색의 위계를 보존한다.
- 컷 사이에는 굵은 테두리와 넉넉한 gutter를 둔다. 번호 태그는 좌상단에 고정하고, 화살표·타임라인·말풍선 꼬리로 컷 간 시선을 연결한다.
- 귀여운 마스코트는 진입 장벽을 낮추는 보조 역할로 쓸 수 있지만, 핵심 설명을 표정이나 감탄사로 대체하지 않는다. 성인 주제에서는 아동 비율, 학교 소품, 유치한 말투를 피한다.

## Storyboard Contract

`02_storyboard/storyboard.md`는 다음 형식을 사용한다.

- `- Selected: \`vertical-webtoon-page\``
- `## Section Map`
- `## Blocks`
- `## Footer`

각 블록에 아래 항목을 채운다.

- 번호와 위치
- purpose: 이 컷이 해결하는 질문
- story beat: 기준점, 문제, 작동 원리, 예시, 주의, takeaway 중 하나
- visual motif: 캐릭터 행동, 사물, 화면, 미니 표, 화살표 등 구체적 장면
- copy bucket: headline, speech bubble, narration box, material insert, label/badge
- baked-text policy: exact copy 또는 이미지 밖 조판
- image prompt intent
- transition: 앞 컷에서 무엇이 바뀌어 다음 컷으로 넘어가는지

권장 한 장 흐름은 다음과 같다.

1. `Hero`: 독자가 가진 질문이나 놀라운 한 문장을 장면으로 연다.
2. `What`: 용어·대상을 캐릭터가 짧게 짚는다.
3. `How`: 2-3단계 구조, 흐름, 비교, 화면 예시 중 하나로 작동을 보여준다.
4. `So what`: 실제 상황에서 무엇이 달라지는지 보여준다.
5. `Watch`: 오해하기 쉬운 한계나 주의점을 경고한다.
6. `Footer`: 기억할 규칙 한 줄 또는 출처 단서로 닫는다.

렌더러의 기존 fallback 슬롯은 `page_header`, `panel_01`-`panel_04`, `footer_strip`이다. 5-6개의 세부 beat가 필요하면 인접한 beat를 같은 패널 안의 명시된 두 단계로 묶고, 임의의 슬롯 이름을 추가하지 않는다. 한 장 원샷 프롬프트와 fallback이 서로 다른 주장을 담지 않게 한다.

## Copy Contract

기본 렌더 모드는 `dialogue-baked`이며, 이미지 모델이 읽기 쉬운 짧은 카피만 베이크한다. 한 장 전체의 목표는 약 300-450자, 하드캡 500자다. 텍스트가 그보다 많으면 문장을 줄이고, 정확한 본문·표·출처는 이미지 밖 조판 대상으로 넘긴다.

카피를 네 채널로 나눈다.

- 말풍선: 패널당 1-2개, 한 개당 10-40자, 캐릭터가 실제로 말할 질문·설명·반응만 쓴다.
- 제3자 나레이션 박스: 한 장에 2-4개, 패널당 최대 1개, 한 개당 25-60자. 꼬리 없는 사각 박스이며 맥락·시점·수치·전환·출처 단서만 담는다.
- 작품 안 자료 인서트: 한 장에 1-2개. 문서, 앱 화면, 메모, 화이트보드, 2열 미니 표처럼 장면 속 사물로 그린다. 제목 1줄과 짧은 항목 3-5개까지만 넣는다.
- 짧은 라벨/배지: 번호, 1-6단어의 상태·역할·경고 문구. 가장 작은 글자일수록 보수적인 표현을 쓴다.

각 블록의 exact copy를 프롬프트에 채널별로 열거하고 `그 외 문자는 만들지 말 것`을 명시한다. 긴 문단, 다층 표, 정확한 법률/기술 문구는 이미지에 억지로 넣지 않는다. 사용자가 모든 글자를 이미지에 넣으라고 해도 `all-baked`의 위험을 `imagegen-checklist.md`에 기록한다.

카피를 확정하기 전에 저장소의 `references/korean-copy-voice-rules.md`와 `references/korean-baked-text-spelling-rules.md`를 읽고 한 번만 패스한다. S1 패턴은 0건이어야 하며, `party-claim`·`analysis`·`speculation`을 표시하는 인식론적 완곡은 삭제하지 않는다. 작은 배지와 화살표 라벨은 특히 오탈자에 취약하므로 두 번 실패한 문자열은 더 강한 가드보다 짧고 안정적인 문자열로 교체한다.

## Prompt Pack And Rendering

공통 run 계약을 지키며 다음 파일을 만든다.

- `_workspace/<slug>/00_input/brief.md`
- `_workspace/<slug>/01_research/research-summary.md`
- `_workspace/<slug>/02_storyboard/storyboard.md`
- `_workspace/<slug>/02_storyboard/layout-bible.md`
- `_workspace/<slug>/03_prompts/master-image-prompt.md`
- `_workspace/<slug>/03_prompts/panel-prompts.md`
- `_workspace/<slug>/04_review/imagegen-checklist.md`
- `_workspace/<slug>/04_review/handoff.md`

`master-image-prompt.md`에는 parser가 찾을 수 있도록 정확히 `## Master Prompt (vertical-webtoon-page)`와 대응하는 `## Negative Prompt (vertical-webtoon-page)`를 둔다. 원샷 프롬프트에는 세로 비율, hero/title, 정확한 컷 수, 번호 순서, 카피 채널, 팔레트, 읽기 순서, 추가 문자 금지를 모두 적는다.

`panel-prompts.md`에는 `page_header`, `panel_01`-`panel_04`, `footer_strip`를 사용한다. 각 슬롯에 purpose, story beat, crop, exact copy, material carrier, character continuity, transition, risk, `prompt` fenced block, `negative` fenced block을 둔다. 이미지 생성 API 실행은 저장소의 `scripts/render_openai.py`만 사용한다.

실제 렌더가 필요할 때:

```bash
bash scripts/verify_infographic_run.sh _workspace/<slug>
python scripts/render_openai.py --slug <slug> --track vertical-webtoon-page --mode oneshot --dry-run
python scripts/render_openai.py --slug <slug> --track vertical-webtoon-page --mode oneshot --size 1024x1536
```

원샷이 실패하면 `--mode fallback`으로 컷별 프롬프트를 렌더한다. 기본 출력은 `05_renders/final-webtoon.png`이며, 실제 파일이 생긴 경우 모든 PNG를 열어 한국어, 컷 수, 캐릭터 수, 경고/귀속 표기를 확인하고 `handoff.md`에 슬롯별 결과를 적는다. 렌더하지 않았으면 렌더 완료라고 말하지 않는다.

## QA Gate

완료 전 다음을 확인한다.

- 제목·번호·footer를 포함한 읽기 순서가 한눈에 보인다.
- 각 컷이 하나의 질문 또는 beat만 담당하고, 캐릭터 반응만으로 채워진 컷이 없다.
- hero, 설명/비교, 실제 예시, 주의점, takeaway가 필요한 만큼만 존재한다.
- 자유 캐릭터가 컷마다 다른 얼굴·헤어·의상·역할로 변하지 않는다.
- 긴 본문과 정확 표는 이미지 밖 대상으로 남거나, 베이크 리스크가 명시되어 있다.
- 말풍선·나레이션·자료 인서트·라벨의 채널 구분이 보인다. 나레이션은 꼬리가 없고 핵심 reveal을 독점하지 않는다.
- 모든 baked Korean string이 whitelist와 일치하고 S1 voice 패턴이 남지 않는다.
- source report의 귀속, 불확실성, 금지 표현이 유지된다.
- `bash scripts/verify_infographic_run.sh _workspace/<slug>`가 0으로 끝난다.

## Handoff

`handoff.md`에는 `vertical-webtoon-page` 모드, 첫 렌더 순서(원샷 또는 `page_header`+`panel_01`), fallback 전환 조건, 예상 파일명, 긴 카피의 downstream 조판 여부를 적는다. 렌더가 존재하면 슬롯별로 `clean` 또는 구체적인 **accepted defect**를 기록한다. 이 스킬은 HTML 조립을 하지 않는다.
