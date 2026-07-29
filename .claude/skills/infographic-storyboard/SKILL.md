---
name: infographic-storyboard
description: "긴 문서나 설명 주제를 인포그래픽 포스터, 세로 웹툰 페이지, 또는 2-8페이지 성인 학습만화로 설계하는 스토리보드 스킬. 학습 목표, 오개념 교정, 페이지별 지식 상태 변화, 캐릭터 역할, 컷 전환, 카피 버킷과 시각 모델을 정의한다."
---

# Infographic Storyboard

이 스킬은 리포트나 에세이를 **한 장의 읽히는 포스터** 또는 **세로 웹툰형 인포그래픽 페이지**로 바꾸는 단계다. 좋은 스토리보드는 내용을 줄이는 것이 아니라, **읽기 순서, 컷 전환, 시각적 위계**를 만든다.

## Required Outputs

- `_workspace/<slug>/02_storyboard/storyboard.md`
- `_workspace/<slug>/02_storyboard/layout-bible.md`
- `adult-learning-comic`에서는 `_workspace/<slug>/02_storyboard/learning-design.md`
- `adult-learning-comic`에서는 `_workspace/<slug>/02_storyboard/character-bible.md`

## Choose A Storyboard Mode

### Mode A: Editorial Poster
사용자가 한 장짜리 포스터, 비대칭 인포그래픽, 리포트 압축 이미지를 원할 때 사용한다.

기본 리듬:
- 좌측 1개 대형 narrative hero
- 우측 2-4개 stacked analysis cards
- 마지막에 전체 폭 closing strip 또는 footer slogan

### Mode B: Vertical Webtoon Page
사용자가 `PAGE 1`, `PAGE 2`처럼 이어지는 세로 웹툰 인포그래픽, 첨부 레퍼런스 같은 4컷 설명 만화, 컷별 대화/캡션 전개를 원할 때 사용한다.

기본 리듬:
- 상단 검은 title bar: `PAGE N`, 큰 제목, 1문장 thesis
- 4-6개 가로 컷: 각 컷 왼쪽 위에 검은 번호 박스
- 컷마다 하나의 논리 beat만 담당
- 밝은 UI/화이트보드 컷과 어두운 시네마틱 시스템 컷을 교차
- footer에는 주석, 경고, 다음 페이지 훅 중 하나만 배치
- 설명은 네 채널로 나눈다: 말풍선, 제3자 나레이션 캡션 박스, 작품 내 자료 인서트(문서/화면/메모/미니 표), 짧은 라벨. 페이지당 나레이션 박스 2-4개(패널당 최대 1개, 개당 25-60자), 자료 인서트 1-2개가 기준이다.
- explanation density를 `standard`(페이지당 약 300자)와 `extended`(약 450자, 하드캡 500자) 중에서 고르고 `layout-bible.md`에 적는다. 기본은 `extended`이며, 늘어난 분량은 나레이션과 자료 인서트에 배정한다.
- 나레이션은 맥락, 수치, 시점, 전환, 출처 단서를 담고 핵심 reveal은 담지 않는다. 그림을 지워도 나레이션만으로 논지가 성립하면 인포툰이 아니라 캡션 붙은 삽화다. 출처 표시가 필요한 주장은 나레이션 안에서도 attribution을 유지하고, 미검증 주장은 나레이션에 넣지 않는다.

### Mode C: Adult Learning Comic
사용자가 특정 주제를 성인용 캐릭터 학습만화로 가르쳐 달라고 할 때 사용한다.

기본 리듬:
- 전체 시리즈를 run 1개로 유지한다.
- 3-6페이지를 기본으로 하고, 좁은 micro lesson은 2페이지까지 허용하며, 최대 8페이지까지 확장한다. 페이지당 4-6개 panel.
- 각 페이지는 learning objective와 knowledge state before/after를 하나씩 가진다.
- 캐릭터 역할은 설명자, 학습자, 선택형 반론자/마스코트로 고정한다.
- 캐릭터를 새로 만들기 전에 `cast/`의 재사용 프로필(`*.character.yaml`, `*.ensemble.yaml`)을 먼저 확인한다. 주제 대비 `usage.good_topics`, `expertise`, `blind_spots`, 역할로 캐스팅을 고르고, 고른 이유를 한 줄로 밝힌 뒤 `identity_tokens`와 `voice`를 그대로 `character-bible.md`로 옮기고 출처 프로필 id를 적는다. 포맷은 `references/cast-library-format.md`.
- 폴백: `cast/`가 없거나 비어 있거나 맞는 인물이 없으면 평소대로 새로 설계한다. 일부만 맞으면 맞는 인물만 재사용하고 빈 역할만 새로 만든다. 프로필 작성을 요구하며 런을 멈추지 않는다.
- 기본 6페이지 arc: 통념 -> 빠진 모델 -> 핵심 reveal -> 작동 원리 -> 적용과 한계 -> 재정의와 회상 질문.
- `dialogue-baked`를 기본으로 하되 exact-copy whitelist를 페이지별로, 채널별로 묶어 작성한다.
- 설명은 캐릭터 대사만으로 싣지 않는다. 말풍선, 제3자 나레이션 박스, 작품 내 자료 인서트(문서/화면/메모/미니 표), 다이어그램 라벨 네 채널로 나눈다. 페이지당 나레이션 박스 2-3개(패널당 최대 1개, 개당 25-60자), 자료 인서트 1-2개가 기준이다.
- explanation density를 `standard`(페이지당 약 300자)와 `extended`(약 450자, 하드캡 500자) 중에서 고르고 `layout-bible.md`에 적는다. 기본은 `extended`이며, 늘어난 분량은 나레이션과 자료 인서트에 배정한다.
- 나레이션은 맥락, 수치, 시점, 전환, 출처 단서를 담고 핵심 reveal과 메커니즘은 담지 않는다. 출처 표시가 필요한 클레임은 나레이션 안에서도 attribution을 유지하고, `needs verification` 클레임은 나레이션에 넣지 않는다.

## Storyboard Rules

### 1. Build Around A Clear Beat Count

Editorial Poster는 5-8개 block을 사용한다.

권장 구조:
- Prologue / Hero
- Block 1: 핵심 기술 또는 핵심 사실
- Block 2: 리스크 또는 딜레마
- Block 3: 사건 전개 또는 지정학 축
- Block 4: 경쟁 구도 또는 구조 비교
- Epilogue / Checklist / Closing line

Vertical Webtoon Page는 보통 4개 panel을 사용하고, 정보가 많을 때만 5-6개로 늘린다.

Adult Learning Comic은 페이지 수부터 정하지 않는다. `learning-design.md`의 explanation spine에 필요한 개념 전환 수를 세고 2-8페이지로 배분한다. 기본은 3-6페이지이며, 2페이지는 좁은 micro lesson에만 사용한다. 각 페이지에는 반드시 다음이 있어야 한다.
- learning objective
- knowledge state before / after
- central visual model
- one misconception, distinction, mechanism, evidence, limitation, application, recap, or retrieval function per panel
- exact baked-copy whitelist
- forward hook or resolution

권장 4컷 전개:
- Panel 1: 기준점 또는 과거 상태
- Panel 2: 변화가 커지는 장면
- Panel 3: 핵심 개념 reveal
- Panel 4: 결과, 부작용, 정책 변화, 다음 페이지 훅

### 2. Separate Copy Types
본문을 섞지 말고 다음 타입으로 분해한다.
- headline
- deck
- short label
- badge or stamp
- narration box (제3자 서술, 화자 없음)
- reference material text (문서/화면/메모/미니 표 안의 텍스트)
- sidebar bullets
- table
- checklist
- closing line

각 조각마다 "누가 말하는가"를 먼저 정한다. 캐릭터가 말할 이유가 없는 정보(배경, 수치, 시점, 출처, 전환)는 말풍선에 억지로 넣지 말고 나레이션 박스나 자료 인서트로 보낸다.

긴 문단은 그대로 두지 말고, 어디까지 이미지에 베이크할지와 어디부터 **이미지 밖에서 별도 처리할 텍스트**인지 구분한다.

copy bucket을 채우는 순간부터 어투 규칙이 적용된다. 전체 규칙과 패턴 ID는 `references/korean-copy-voice-rules.md`.
- 결산 라벨("결론적으로", "요약하면", "이를 통해"), 의의 과장("시사하는 바가 큽니다", "주목할 만합니다"), 열거 도입("다음과 같습니다"), hype 어휘, 결말 공식("~할 때입니다"), 형식명사 종결("~한 것입니다"), 문두 접속사, 이중 피동, "~에 의해", "~에 대해", 대명사 그/그녀/그것, 이모지를 쓰지 않는다.
- 제목과 closing line이 AI 티가 가장 잘 드러나는 자리다. 콜론 부제 "X: Y"는 0회, 대구 "A가 아니라 B"와 변환 공식 "X에서 Y로"는 **시리즈 전체 최대 1회**로 센다. 페이지 제목 6개가 같은 수사 구조면 즉시 실패다.
- 캐릭터 관계(사수-후배, 강사-수강생, 동료)를 먼저 정하고 인물별 종결어미 세트를 나눈다. 전원이 같은 존댓말·같은 종결어미면 그림과 무관하게 대사가 AI 초안처럼 읽힌다. `cast/` 프로필의 `voice`는 그대로 옮기고 일반 규칙으로 "고치지" 않는다.
- claim ledger가 어투보다 세다. 습관적 완곡("~로 보입니다")은 빼고, `party-claim`/`analysis`/`speculation`의 출처·불확실성 표시는 남긴다. 어투를 다듬어 클레임을 올리거나 리포트에 없는 수치·비유를 새로 심지 않는다.

### 3. Every Block Needs Visual Intent
각 block 또는 panel에는 반드시 다음이 있어야 한다.
- purpose
- story beat
- visual motif
- copy bucket
- baked-text policy
- image prompt intent

visual motif는 추상어로 끝내지 말고 다음 수준까지 내려가야 한다.
- "긴급 속보 카드가 걸린 정부 연설 장면"
- "밝은 종이 카드 위 2열 비교표"
- "붉은 경고 배지와 검은 스탬프가 겹친 보안 딜레마 박스"
- "검은 상단 PAGE 바 아래, 흰 UI 카드 3개가 나란히 놓인 첫 컷"
- "어두운 서버룸에서 중앙 AI 코어 주변에 메일/코드/거래 UI가 떠 있는 두 번째 컷"

### 4. Design Panel Transitions
Vertical Webtoon Page에서는 각 panel이 독립 카드처럼 보이면 안 된다. 다음 중 하나의 전환 관계를 명시한다.
- before -> after
- cause -> effect
- attempt -> unintended consequence
- surface behavior -> hidden system
- concept definition -> operational consequence

각 panel에는 필요한 경우 다음 항목을 둔다.
- cast continuity: 반복 등장 인물, 표정, 의상, 위치
- camera/framing: wide lab shot, close-up reaction, UI insert, system diagram
- copy channel: 말풍선 / 나레이션 캡션 박스 / 자료 인서트 / 라벨 중 무엇으로 실을지
- caption placement: 좌측 또는 좌하단 나레이션 박스(꼬리 없음), 말풍선, 우하단 결론 박스
- material insert: 어떤 사물(문서, 기기 화면, 메모, 화이트보드, 미니 표)이 텍스트를 담는지와 누가 그것을 보는지
- transition note: 다음 panel로 넘어가는 이유

### 5. Use Comparative Shapes
정보량이 많은 포스터는 비교 구조가 읽히기 쉬워야 한다.
- versus table
- three-step incident chain
- checklist
- cause/effect strip
- quote card

권장 조합:
- dark scene card next to light paper comparison card
- procedural 1-2-3 chain card
- checklist epilogue card with icon bullets

### 6. Text Density Is A Layout Variable
다음 중 하나를 `layout-bible.md`에 명시한다.
- `text-conservative`: 긴 본문/표는 baked text로 밀어 넣지 않음
- `all-baked`: 전부 이미지 베이크 시도

기본값은 `text-conservative`.

Vertical Webtoon Page에서 안전한 baked text (`extended` 기준, 페이지 총량 약 450자·하드캡 500자):
- `PAGE 1`
- 큰 제목과 1문장 thesis
- panel 번호
- 1-6단어 라벨
- 말풍선: 패널당 1-2개, 개당 10-40자
- 나레이션 캡션 박스: 페이지당 2-4개, 패널당 최대 1개, 개당 25-60자
- 자료 인서트: 페이지당 1-2개, 제목 1줄 + 20자 이내 항목 3-5개 또는 2열 x 3행 미니 표
- 스탬프 또는 경고 배지
- footer note: 2문장·약 80자까지

Vertical Webtoon Page에서 위험한 baked text:
- 나레이션 박스에 넣은 긴 한국어 문단
- 정확한 정책 문구
- 긴 시스템 프롬프트
- 2열 x 3행을 넘는 비교표
- footnote 문단

## Layout Bible Rules

`layout-bible.md`에는 최소 다음 섹션이 있어야 한다.
- `## Render Mode`
- `## Storyboard Mode`
- `## Grid`
- `## Color System`
- `## Typography`
- `## Visual Language`
- `## Text Density Policy`
- `## Render Notes`

추가 권장 섹션:
- `## Poster Rhythm`
- `## Safe Baked Text`
- `## High-Risk Blocks`

`adult-learning-comic`에서는 추가로 다음을 기록한다.
- `## Baked Copy Budget` (explanation density, 페이지 총량, 채널별 상한)
- `## Narration And Material Channel` (나레이션 박스 스타일과 허용/금지 내용, 자료 인서트를 담는 사물)

Vertical Webtoon Page에서는 추가로 다음을 기록한다.
- page aspect ratio and panel count
- title bar treatment
- panel gutter and border style
- numbered corner tag style
- narration box, caption, and speech bubble placement
- reference-material insert style and which object carries it
- explanation density와 페이지 총 글자 예산 (`## Baked Copy Budget`)
- narration 허용/금지 내용과 attribution 처리 (`## Narration And Material Channel`)
- character continuity rules
- light UI panel vs dark cinematic panel ratio

## Anti-Patterns

- 리포트의 문단 순서를 그대로 옮기지 말 것
- 긴 한국어 문장을 전부 이미지에 넣는 전제를 default로 두지 말 것
- 표와 체크리스트를 일러스트 블록과 섞어 읽기 순서를 무너뜨리지 말 것
- 블록 수가 너무 많아 한눈에 위계가 안 보이게 만들지 말 것
- 첨부 레퍼런스 같은 웹툰형 페이지를 전부 같은 크기의 대시보드 카드로 평탄화하지 말 것
- 한 panel 안에 setup, reveal, conclusion을 모두 넣지 말 것
- 등장 인물의 얼굴/의상/역할이 panel마다 바뀌게 두지 말 것
- 성인 학습자를 무지하거나 유치한 인물로 만들지 말 것
- 캐릭터 반응만 있고 개념 전환이 없는 페이지를 만들지 말 것
- 설명자가 결론만 선언하고 근거, 메커니즘, 한계를 생략하지 말 것
- 설명 부담을 나레이션 박스로 떠넘기지 말 것. 그림을 지워도 나레이션만으로 내용이 성립하면 만화가 아니라 캡션 붙은 삽화다
- 나레이션 박스를 캐릭터 대사처럼 쓰거나 말풍선 꼬리를 붙이지 말 것
- 출처가 필요한 주장을 화자 없는 나레이션으로 확정 사실처럼 서술하지 말 것
- 자료 인서트를 화면 위에 떠 있는 본문 텍스트 덩어리로 만들지 말 것. 장면 안의 사물로 그릴 것
- 마지막 페이지가 첫 페이지의 오개념을 명시적으로 해결하지 않은 채 끝나지 말 것

## Quality Check

- 블록 수는 5-8개인가
- 웹툰 페이지라면 panel 수는 4-6개이고 각 panel에 하나의 beat만 있는가
- Hero, comparison, risk, closing이 페이지에서 식별되는가
- PAGE 헤더, panel 번호, 컷 전환, footer/hook이 식별되는가
- baked-text 허용 영역과 비허용 영역이 구분되었는가
- 학습만화나 세로 웹툰이라면 explanation density가 선언되고 페이지 총량이 예산 안에 있는가
- 각 카피 조각의 채널(말풍선 / 나레이션 / 자료 인서트 / 라벨)이 정해졌는가
- 카피에 S1 금지 패턴이 남아 있지 않은가 (결산 라벨, 의의 과장, 열거 도입, hype, 결말 공식, 형식명사 종결, 문두 접속사, 이중 피동, 콜론 부제 제목)
- 학습만화라면 인물별 speech level과 종결어미 세트가 정해졌고 시리즈 전체에서 고정인가
- prompt writer가 바로 사용할 수 있을 만큼 visual intent가 구체적인가
- dark card / light paper card / warning stamp의 대비가 구조적으로 배치되었는가
