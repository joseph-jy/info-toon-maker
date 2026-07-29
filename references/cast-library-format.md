# Cast Library Format

재사용 가능한 개인 캐릭터 라이브러리의 데이터 포맷 정의.

- 저장 위치: `cast/` (gitignore 대상, 레포에 올라가지 않음)
- 파일 포맷: YAML (`.yaml`)
- 파일 단위: 캐릭터 1명 = 파일 1개
- 파일명: `cast/<id>.character.yaml`
- 앙상블(캐스팅 조합): `cast/<id>.ensemble.yaml`
- 레퍼런스 이미지: `cast/images/<id>-NN.png`
- 빈 템플릿: `templates/cast-profile.template.yaml`
- 예시: `cast/EXAMPLE.character.yaml`

키 이름은 영문 snake_case로 고정하고, 값은 한국어로 써도 된다. 키를 임의로
바꾸면 학습만화 런에서 자동으로 읽어 쓰기 어려워진다.

## Why This Exists

`_workspace/<slug>/02_storyboard/character-bible.md`는 **런 1개짜리** 캐스팅
문서다. `cast/`는 그보다 상위에 있는 **여러 런에서 재사용하는 인물 원장**이다.
학습만화를 새로 만들 때 `cast/`에서 인물을 골라 오면 캐릭터 시트, 말투, 시각
토큰이 시리즈 간에 유지된다.

흐름:

```
cast/<id>.character.yaml   (영구, 비공개)
        |
        v  캐스팅 선택 + 이번 주제에 맞게 각색
02_storyboard/character-bible.md   (런 전용)
        |
        v  identity token 문자열로 전개
03_prompts/series-prompts.md       (character_sheet / page_XX)
```

## Field Reference

### 1. Header (필수)

| key | 필수 | 타입 | 설명 |
| --- | --- | --- | --- |
| `schema_version` | 필수 | int | 현재 `1` |
| `id` | 필수 | string | 파일명과 동일한 kebab-case 식별자. 앙상블/런에서 이 값으로 참조 |
| `name` | 필수 | string | 만화에 실제로 표기될 이름 (예: `드웨인`) |
| `name_en` | 선택 | string | 영문 표기. 이미지 프롬프트에서 라틴 문자가 필요할 때 사용 |
| `one_liner` | 필수 | string | 한 줄 정의 (예: `15년차 시니어 백엔드 개발자`) |
| `real_person` | 필수 | bool | 실존 인물이면 `true` |
| `default_role` | 필수 | enum | `explainer` / `learner` / `challenger` / `mascot` |
| `alt_roles` | 선택 | enum[] | 이 인물이 소화 가능한 다른 역할 |
| `status` | 선택 | enum | `active` / `draft` / `retired` |

### 2. `profile` (필수)

| key | 필수 | 설명 |
| --- | --- | --- |
| `age_band` | 필수 | 성인 연령대 (예: `30대 후반`). 아동 코드 금지 |
| `occupation` | 필수 | 직업/직함 |
| `expertise` | 필수 | 강점 도메인 목록. 캐스팅 적합도 판단에 사용 |
| `blind_spots` | 선택 | 모르는 영역. learner/challenger 배치에 사용 |
| `personality` | 선택 | 성격 키워드 3-5개 |
| `background` | 선택 | 2-3문장 배경. 대사 톤의 근거 |

### 3. `identity_tokens` (필수)

이미지 프롬프트에 **매 페이지 그대로 반복될 불변 토큰**. 짧고 시각적으로
확정적인 명사구로 쓴다. 여기 없는 특징은 페이지마다 흔들려도 된다는 뜻이다.

| key | 필수 | 설명 |
| --- | --- | --- |
| `face` | 필수 | 얼굴형, 눈매, 수염 등 |
| `hair` | 필수 | 헤어 실루엣과 색 |
| `build` | 필수 | 체형과 키 인상 |
| `outfit` | 필수 | 기본 의상 실루엣 |
| `accessory` | 선택 | 고정 소품 1-2개 (안경, 사원증 등) |
| `signature_colors` | 필수 | 색 토큰 1-3개. hex 또는 색 이름 |
| `height_note` | 선택 | 다른 캐스트 대비 상대 키 |
| `prohibited_drift` | 선택 | 절대 바뀌면 안 되는 것 목록 |

### 4. `voice` (필수)

| key | 필수 | 설명 |
| --- | --- | --- |
| `speech_level` | 필수 | `존댓말` / `반말` / `혼합` |
| `tone` | 필수 | 말의 온도와 태도 |
| `catchphrases` | 필수 | 자주 쓰는 표현. **말버릇은 여기에 넣는다** (예: `가령 ~ 이라고 해보죠`) |
| `verbal_tics` | 선택 | 문장 시작/끝 습관 |
| `vocabulary` | 선택 | 선호 어휘 층위 (비유 중심 / 용어 정확 등) |
| `sentence_length` | 선택 | `짧게` / `보통` / `길게`. 말풍선 길이 예산에 반영 |
| `bubble_style` | 선택 | 말풍선 모양 규칙 (둥근/각진/점선 등) |
| `sample_lines` | 필수 | 상황별 예시 대사 2-4개. `context` + `line` 쌍 |
| `avoid` | 선택 | 이 인물이 절대 쓰지 않는 말투/표현 |

### 5. `teaching` (필수)

| key | 필수 | 설명 |
| --- | --- | --- |
| `speaking_function` | 필수 | 시리즈 안에서의 발화 기능 (근거 제시 / 오개념 발화 / 반례 제기 / 요약) |
| `question_style` | 선택 | learner일 때 질문하는 방식 |
| `typical_misconceptions` | 선택 | 이 인물이 자연스럽게 대변하는 통념 목록 |
| `explanation_devices` | 선택 | 자주 쓰는 설명 장치 (비유, 화이트보드, 수식 등) |

### 6. `reference_images` (선택)

프로필/레퍼런스 이미지 목록. 경로는 `cast/` 기준 상대경로.

| key | 설명 |
| --- | --- |
| `path` | 예: `images/dwayne-01.png` |
| `use` | `identity` / `outfit` / `pose` / `expression` |
| `note` | 이 이미지로 무엇을 고정할지 |

`scripts/render_openai.py`는 `--reference <경로>`로 외부 이미지를 추가 참조로
넘길 수 있다. 캐릭터 시트를 만들 때 여기 이미지를 참조로 넣으면 인물 고정이
쉬워진다.

### 7. `likeness` (실존 인물일 때만 필수)

`real_person: true`이면 반드시 채운다. 레포 정책상 **최대한 닮게** 그리는 것이
목표이므로 일부러 다르게 변형하지 않는다.

| key | 설명 |
| --- | --- |
| `target` | 고정값 `maximum recognizable likeness` |
| `face_tokens` | 실제 얼굴/체형 특징 |
| `hair_tokens` | 실제 헤어 특징 |
| `signature_outfit` | 실제 시그니처 의상 |
| `age_band_as_of` | 기준 시점과 연령대 |
| `stylized_fallback` | 렌더 API가 거절할 때 쓸 대체 묘사 1개 |
| `claim_guard` | 이 인물 입에 넣어도 되는 발화 범위 (클레임 원장 규칙) |

### 8. `render_notes` (선택)

| key | 설명 |
| --- | --- |
| `moderation_risk` | `low` / `medium` / `high` |
| `known_failures` | 과거 렌더에서 깨졌던 부분 |
| `retry_hint` | 실패 시 프롬프트 조정 방향 |

### 9. `relationships`, `usage`, `notes` (선택)

- `relationships[]`: `with`(다른 캐릭터 id) + `dynamic`(관계 성격)
- `usage.good_topics` / `usage.avoid_topics`: 캐스팅 적합도
- `usage.appeared_in[]`: `slug` + `date`(YYYY-MM-DD) + `role`
- `notes`: 자유 메모

## Ensemble File

자주 쓰는 캐스팅 조합을 저장한다.

```yaml
schema_version: 1
id: backend-duo
label: 백엔드 사수-후배
cast:
  - ref: dwayne
    role: explainer
  - ref: mina
    role: learner
tone: 실무 트러블슈팅, 화이트보드 중심
good_topics: [데이터베이스, 분산시스템, 성능]
notes: 마스코트 없이 2인으로 진행. 페이지당 말풍선 4-6개.
```

## Validation Rules

1. `id`는 파일명과 일치해야 한다.
2. `default_role`이 `explainer`인 캐릭터가 앙상블에 최소 1명 있어야 한다.
3. 한 앙상블의 `cast`는 2-4명 (마스코트 포함).
4. `signature_colors`가 서로 다른 캐릭터끼리 충돌하지 않아야 한다 (같은 색 토큰 금지).
5. `age_band`는 모두 성인. 교복/아동 체형 묘사는 넣지 않는다.
6. `real_person: true`인데 `likeness.stylized_fallback`이 비어 있으면 무효.
7. `voice.sample_lines`는 최소 2개.

## How A Run Consumes This

학습만화 런에서:

1. 캐스팅을 제안하기 **전에** `python scripts/cast_usage.py --eligibility`를 돌려
   누가 벤치(쿨다운)이고 누가 콜드(0회)인지 확인한다. 회전 규칙은 `AGENTS.md`의
   Private Cast Library 절이 정본이다: 최근 3개 라이브러리 사용 런에 나온 인물은 벤치,
   콜드 목록이 비지 않은 동안에는 최소 1명을 콜드에서 뽑는다. 벤치 인물을 쓰려면
   왜 대체 불가인지 제안과 `character-bible.md`에 함께 적는다.
2. 주제와 `usage.good_topics`, `expertise`, `blind_spots`, 역할을 대조해 여러 프로필 중에서
   캐스팅을 고른다. 맞는 앙상블이 있으면 그것을 우선 쓴다.
   - 주제 적합도만으로 고르면 매번 같은 인물이 당선된다(argmax). 1번 단계가 그것을 막는다.
   - 맞는 인물이 없거나 `cast/`가 비어 있으면 그냥 새로 설계한다 (기본 동작).
   - 일부만 맞으면 맞는 인물만 재사용하고 나머지 역할만 새로 만든다.
   - 새로 만든 인물이 재사용할 가치가 있으면 런이 끝난 뒤 `cast/`에 저장할지 물어본다.
3. 고른 이유와 회전 규칙이 벤치한 인물을 한 줄로 밝히고 **사용자 승인을 받는다.**
   통보가 아니라 대기하는 게이트다. `character-bible.md`를 쓰기 전, 그리고 반드시
   `character_sheet` 렌더 전에 묻는다 — 시트가 나온 뒤 캐스팅을 바꾸면 그 렌더와
   그것을 참조한 페이지가 전부 버려진다.
   - 반려("이번에는 다른 사람 써보자" 포함)면 남은 풀에서 **다른** 캐스팅을 제안한다.
     반려된 인물은 그 런 안에서 다시 제안하지 않고, 새 근거를 붙여 재설득하지도 않는다.
   - 반려는 그 런 한정이다. 영구 사용 금지가 아니고 쿨다운 집계에도 영향이 없다.
   - 풀이 바닥나면 그 사실을 말하고 나머지 역할을 새로 설계한다. 무한 반복하지 않는다.
   - `cast/`가 비어 있거나 맞는 인물이 아예 없어 처음부터 새로 설계하는 경우에는
     묻지 않는다. 물어볼 결정이 없는데 질문을 만들어내지 않는다.
4. 승인된 캐스팅의 `identity_tokens`를 `character-bible.md`의 Identity Tokens 절에
   **그대로** 복사한다. 런 안에서 임의로 바꾸지 않는다.
5. `voice.catchphrases`와 `sample_lines`를 말풍선 카피 작성 기준으로 쓴다.
6. `real_person: true`이면 `character-bible.md`의 Real-Person Casting 블록과
   `imagegen-checklist.md`의 render risk 항목을 채운다.
7. `reference_images`가 있으면 `handoff.md`에 `--reference` 사용 지시를 적는다.
8. `usage.appeared_in`은 **선택 사항이고 정본이 아니다.** 등장 이력의 정본은
   `_workspace/*/02_storyboard/character-bible.md`의 "Cast library profiles used" 줄이며,
   `scripts/cast_usage.py`가 거기서 역산한다. 수동 필드를 정본으로 삼았을 때 한 번도
   채워지지 않아 회전 규칙이 작동하지 않았던 전례가 있다. 손으로 적고 싶으면 적어도 되지만,
   비어 있어도 결함이 아니고 회전 규칙은 스크립트 결과를 따른다.
9. 반대로 `character-bible.md`의 "Cast library profiles used" 줄은 **반드시** 채운다.
   이 줄이 비면 그 런은 회전 집계에서 누락되어 벤치 규칙이 조용히 무력화된다.
   형식: `` - Cast library profiles used (`cast/<id>.character.yaml`): `<id-1>` (explainer), `<id-2>` (learner) ``
   실제 프로필 id는 비공개다. 이 문서를 포함한 추적 파일에는 예시로도 적지 않는다.

주의: `cast/` 내용은 비공개 자료다. 런 산출물(`_workspace/`, `reports/`)도
gitignore 대상이지만, `cast/`의 원문을 커밋 대상 문서(`README.md`, 템플릿,
스킬 문서)에 붙여넣지 않는다.
