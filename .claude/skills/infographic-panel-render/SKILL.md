---
name: infographic-panel-render
description: "인포그래픽 포스터, PAGE형 세로 웹툰, 성인 학습만화 시리즈용 프롬프트 팩을 만드는 스킬. 학습만화에서는 공통 스타일/캐릭터 계약, 캐릭터 시트, 페이지별 exact-copy whitelist와 프롬프트를 만든다."
---

# Infographic Panel Render

이 스킬은 실제 렌더보다 앞선 단계인 **prompt engineering harness**다. 목표는 이미지 모델이 실패해도 작업이 무너지지 않게 하는 것이다.

## 사적 이용 및 실존 인물 정책

이 하네스의 산출물은 소유자의 사적·비상업 용도로만 쓰인다 (`AGENTS.md`의 Usage Context And Likeness Policy 참조).

- 프롬프트에서 기존 작품/작가/프랜차이즈의 스타일을 직접 지칭해도 된다. 저작권 회피용 문구나 "실존 대상과 닮지 않게" 류의 negative prompt를 넣지 않는다.
- 실존 인물이 등장하면 이름을 그대로 쓰고, 실제 얼굴형·헤어·체형·연령대·시그니처 의상을 identity token으로 서술해 **최대한 닮게** 그린다. 일부러 다르게 변형한 유사 캐릭터를 만들지 않는다.
- 실존 인물의 likeness token도 가상 캐릭터와 동일하게 캐릭터 시트와 모든 페이지 프롬프트에서 반복한다.
- 실존 인물은 텍스트 토큰만 쓰지 말고 사진 참조를 함께 쓴다. `cast/` 프로필이 있으면 그 프로필의 `reference_images`, 없으면 `_workspace/<slug>/00_input/refs/`에 둔 사진을 쓰고 경로를 `character-bible.md`의 Real-Person Casting 블록에 적는다.
- 사진 참조는 **캐릭터 시트 렌더에만** `--identity-reference`로 붙인다. 페이지는 완성된 `character-sheet.png`에서 likeness를 물려받는다. 원본 사진을 페이지마다 다시 넣지 않는다.
- 사진은 identity 참조 전용이다. `series-prompts.md`의 `PHOTO IDENTITY REFERENCE RULE`을 반드시 포함해, 사진을 그대로 옮기지 않고 시리즈 웹툰 스타일로 다시 그리도록 지시한다 (포즈·구도·배경·조명·의상 스냅샷·사진 내 텍스트 복제 금지).
- 단, 이미지 API 자체 모더레이션이 실존 인물 렌더를 거부하거나 왜곡할 수 있다. 이 경우를 render risk로 `imagegen-checklist.md`에 기록하고, 인물별 stylized fallback descriptor를 준비해 페이지 재설계 없이 재시도할 수 있게 한다.

## Required Outputs

- `_workspace/<slug>/03_prompts/master-image-prompt.md`
- `_workspace/<slug>/03_prompts/panel-prompts.md`
- `adult-learning-comic`에서는 `_workspace/<slug>/03_prompts/series-prompts.md`

## Prompt Strategy

### Mode C: Dialogue-Baked Learning Series
`adult-learning-comic` 기본값.

- 공통 정책은 `series-prompts.md`의 `Shared Prompt Policy`에 한 번 정의한다.
- `character_sheet`를 첫 슬롯으로 둔다.
- `thumbnail` 슬롯을 정확히 하나 둔다. 시리즈 목록 카드용 가로형 커버 1장이며, 짧은 한국어 주제 문구(2-6단어) 하나와 간단한 중심 모티프, 최대 1-2명의 등장인물만 담는다. 만화 패널, 말풍선, 본문 텍스트는 금지. 렌더 기본 크기는 1536x1024이고 목록 페이지가 16:10으로 크롭하므로 문구와 모티프를 중앙 16:10 안전 영역에 둔다.
- 각 `page_XX`는 learning objective, knowledge state before/after, central visual model, explanation density, exact baked copy, narration copy, material copy, page character total, character reminder, prompt를 가진다.
- 설명은 네 개 채널로 나눠 싣는다: 캐릭터 말풍선, 제3자 나레이션 박스, 작품 내 자료 인서트(문서/화면/메모/미니 표), 다이어그램 라벨. 말풍선에 안 들어가는 내용은 말풍선을 늘리지 말고 나레이션이나 자료 인서트로 옮긴다.
- 기본 explanation density는 `extended`(페이지당 한국어 약 450자, 하드캡 500자)다. 늘어난 분량은 나레이션 박스와 자료 인서트에 쓰고 말풍선 길이로 쓰지 않는다. 가독성 실패가 반복되면 `standard`(약 300자)로 내린다. 채널별 상한은 `references/adult-learning-comic-image-rules.md`.
- 나레이션 박스는 꼬리 없는 사각 캡션 박스이며 화자가 없다. 페이지당 2-3개, 패널당 최대 1개, 개당 25-60자. 얼굴이나 다이어그램 라벨 위에 얹지 않는다.
- 나레이션은 맥락, 수치, 시점, 전환, 출처 단서만 담는다. 핵심 reveal과 메커니즘은 캐릭터와 다이어그램이 담당한다. 나레이션은 화자가 없어서 모든 문장을 확정 사실처럼 들리게 하므로, `party-claim`/`analysis`/`speculation`은 출처 표시를 유지하고 `needs verification` 클레임은 나레이션에 넣지 않는다.
- 자료 인서트는 페이지당 1-2개이며 장면 안의 사물(종이 문서, 기기 베젤 안 화면, 붙임 메모, 화이트보드, 테두리 있는 미니 표)로 그린다. 제목 1줄 + 20자 이내 항목 3-5개, 또는 2열 x 3행 미니 표 형태로 짧게 유지하고 문단을 넣지 않는다.
- 페이지 렌더 시 shared policy와 slot prompt를 합성한다.
- 캐릭터 시트는 identity reference로만 사용하고 페이지 레이아웃 참고로 사용하지 않는다.
- 페이지별 허용 문자열을 채널별로 묶어 정확히 열거하고 그 외 문자를 금지한다.
- whitelist를 확정하기 **직전에** 어투 패스를 한 번 돌린다. 전체 규칙과 패턴 ID는 `references/korean-copy-voice-rules.md`.
  - S1 금지 목록(결산 라벨, 의의 과장, 열거 도입, hype, 결말 공식, 형식명사 종결, 문두 접속사, 이중 피동, "~에 의해", "~에 대해", 대명사, 이모지, 말풍선 안 강조 따옴표)이 0건인지 확인하고, 고친 뒤 글자수를 다시 센다. 어투 수정은 대개 문자열을 줄이므로 density 예산에 유리하다.
  - 나레이션 박스는 화자가 없어 문체 티가 가장 크게 드러난다. S1 0건 기준을 여기에 가장 엄하게 적용한다.
  - 시리즈 단위로 센다: 영어 병기 첫 등장 1회, 대구 최대 1회, "X에서 Y로" 최대 1회, 콜론 부제 제목 0회, 결말 공식 0회.
  - 인물별 종결어미 세트가 섞이지 않았는지, register가 시리즈 전체에서 고정인지 본다. `cast/` 프로필의 `voice`와 `catchphrases`는 그대로 두고 일반 규칙으로 고치지 않는다.
  - claim ledger가 어투보다 세다. 습관적 완곡만 빼고 출처·불확실성 표시는 남긴다.
  - `series-prompts.md`의 `## Copy Voice Contract`와 `imagegen-checklist.md`의 `## Korean Copy Voice Pass`에 결과를 적는다. 기록이 없으면 수행하지 않은 것으로 본다.
  - 렌더 후 문자열 수정은 그 페이지 재렌더를 뜻한다. 패스는 렌더 전에 끝낸다.
- 1차 렌더는 character sheet + page 01. 두 결과가 통과한 뒤 나머지 페이지를 진행한다.

### Mode A: Hybrid
추천 기본값.

- hero art, stamps, icon blocks, scene cards, cinematic panels: 이미지 생성
- 긴 한국어 본문, 정확 표, 비교표, 체크리스트: baked text로 무리하게 넣지 않음

이 모드의 기본 산출은:
- one-shot poster prompt 1개
- high-confidence block prompts 4-8개
- 어떤 블록이 text-light / text-heavy인지 명시한 handoff

### Mode B: All-Baked
사용자가 강하게 원할 때만.

- 전체 포스터를 한 번에 그리는 `Master Prompt` 작성
- 그래도 block prompts는 반드시 같이 만든다
- QA에 "dense Korean text may break"를 기록한다

이 모드에서도 긴 한국어 문단은 요약형 baked label로 축약하는 것이 기본이다.

## Master Prompt Rules

원샷 포스터 프롬프트에는 다음이 들어가야 한다.
- poster format and aspect
- reading order
- palette and atmosphere
- hero illustration concept
- block or panel structure count
- where short Korean labels are allowed
- what long text should be simplified
- explicit instruction to avoid random English or gibberish

그리고 다음 구성 지시를 우선 고려한다.
- asymmetrical editorial poster, one dominant hero block on the left, stacked dossier-style information cards on the right
- for webtoon-page mode: black PAGE title bar, 4-6 horizontal comic panels, numbered corner tags, tail-less narration caption boxes, sparse speech bubbles, and at most 1-2 in-world document/screen inserts
- alternating dark cinematic illustration zones and light paper data zones
- bold numbered scene tags, warning stickers, denied stamps, executive-briefing atmosphere
- dense but legible composition, not a clean SaaS dashboard, not a cute comic page

## Block Prompt Rules

각 block prompt는 다음을 포함한다.
- purpose
- story beat
- crop or framing
- baked text limited to headlines/badges/short labels
- mood and iconography
- what poster region it maps to
- caption, narration-box, or speech bubble placement when using webtoon-page mode
- 채널별 카피: 말풍선 / 나레이션 박스 / 자료 인서트(어떤 사물이 담고 누가 보는지) / 라벨
- character or object continuity notes when panels repeat the same cast
- risk note for Korean baked text

권장 형식:

```md
### block_02
- purpose: data retention dilemma
- crop: medium information card
- baked text: "30일 보관", "ZDR 철회"
- poster region: right-middle paper card
- prompt: ...
- negative: ...
```

## Korean Text Policy

- 긴 문단은 baked text로 넣지 않는다
- baked text는 짧고 의미 있는 단위만 허용:
  - 섹션 제목
  - 숫자 라벨
  - 스탬프
  - 경고 배지
  - 매우 짧은 말풍선
- 그 외 텍스트는 downstream composition 대상으로 남긴다

권장 상한:
- headline: 4-12 words
- badge: 1-6 words
- warning stamp: 1-4 words
- short caption: 1 short line

`adult-learning-comic`과 `vertical-webtoon-page`는 이 상한 대신 채널별 예산을 따른다. 두 트랙 모두 나레이션 박스와 자료 인서트가 허용 채널이고, 기본 explanation density는 `extended`(페이지 총량 약 450자, 하드캡 500자)이며 페이지당 총량으로 관리한다. 상세 수치는 각각 `references/adult-learning-comic-image-rules.md`와 `references/webtoon-page-image-rules.md`.

`vertical-webtoon-page` 채널 상한: 말풍선 패널당 1-2개(10-40자), 나레이션 캡션 박스 페이지당 2-4개(패널당 최대 1개, 25-60자), 자료 인서트 페이지당 1-2개(제목 1줄 + 20자 이내 항목 3-5개 또는 2열 x 3행 미니 표), footer note 2문장·약 80자.

## Negative Prompt Baseline

다음을 기본 부정 프롬프트에 포함한다.
- no watermark
- no random English
- no gibberish
- no duplicated faces
- no extra charts
- no cropped text
- no unrelated UI
- no flat corporate dashboard look
- no pastel productivity app aesthetic
- no generic presentation slide layout

나레이션 박스와 자료 인서트를 쓰는 트랙(`vertical-webtoon-page`, `adult-learning-comic`)에서는 다음을 추가한다.
- no narration box with a bubble tail
- no narration box over a face or diagram label
- no floating body text without a container
- no paragraph inside a document or screen insert
- no text-choked panel
- no shrunken unreadable caption text

`adult-learning-comic`에서는 `no cute manga panel page`를 사용하지 않는다. 대신 다음을 쓴다.
- no school uniforms
- no child-coded proportions
- no chibi
- no juvenile slang
- no identity or wardrobe drift
- no panel without a teaching function

## Poster-Specific Render Rules

### Hero Block
- 가장 강한 상징 이미지 1개를 중심에 둔다.
- 주변에 1-2개의 secondary inset card 또는 warning stamp를 붙일 수 있다.
- hero는 정보 카드보다 서사적이어야 한다.

### Data Cards
- 비교표/체크리스트 성격 블록은 밝은 종이 카드 느낌으로 분리한다.
- 너무 많은 실제 문장을 baked text로 넣지 않는다.
- 표가 핵심이면 "table-ready visual shell"을 그리게 하고 텍스트는 후속 단계로 넘길 수 있게 한다.

### Warning And Badge Layer
- 붉은 경고 스탬프, 검은 거부 배지, 금색 하이라이트는 1페이지당 여러 번 쓸 수 있지만 남발하지 않는다.
- 장식이 아니라 읽기 위계를 만드는 용도로 사용한다.

## Render Reality Rule

이 스킬은 프롬프트 팩을 만든다. 실제 PNG가 없다면 렌더 완료라고 말하지 않는다.
