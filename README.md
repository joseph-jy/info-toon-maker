# Infographic-Toon

**AI 이미지 생성을 위한 프롬프트 설계 하네스.**  
한 장짜리 인포그래픽 포스터부터 4-8페이지 성인 학습만화까지, 주제 리서치 → 스토리보드 → 프롬프트 팩 → 이미지 렌더링을 하나의 파이프라인으로 연결합니다.

---

## 한눈에 보기

| 단계 | 산출물 | 위치 |
|------|--------|------|
| 입력 | 정규화된 브리프 | `00_input/brief.md` |
| 리서치 | 팩트 요약 + 검증 필요 표시 | `01_research/research-summary.md` |
| 스토리보드 | 블록 분할, 레이아웃 바이블 | `02_storyboard/` |
| 프롬프트 | 원샷 + 블록별 폴백 프롬프트 | `03_prompts/` |
| QA | 렌더 체크리스트 + 핸드오프 문서 | `04_review/` |
| 렌더 (선택) | OpenAI gpt-image-2로 생성된 PNG | `05_renders/` |

---

## 두 가지 제작 트랙

### 1. 인포그래픽 포스터

어두운 시네마틱 톤의 한 장짜리 세로 포스터.  
뉴스룸 긴급 보고, 정부 문서 스탬프, 비교표, 체크리스트 카드 등을 조합합니다.

- 네이비/차콜 배경 + 앰버/골드 강조 + 레드 경고 스탬프
- 좌측 히어로 내러티브 + 우측 정보 카드 스택 + 푸터 슬로건
- 트랙 이름: `editorial-poster` 또는 `vertical-webtoon-page`

### 2. 성인 학습만화

반복 등장하는 성인 캐릭터가 기술 주제를 설명하는 4-8페이지 시리즈.

- 페이지마다 학습 목표 1개, 지식 상태 변화, 중심 시각 모델 1개
- 캐릭터 시트를 먼저 렌더링하고, 이를 레퍼런스로 각 페이지 생성
- 기본 아크: 오개념 표면화 → 대비 모델 → 핵심 증명 → 메커니즘 → 전이 → 회상/정리
- 트랙 이름: `adult-learning-comic`

---

## 빠른 시작

### 1. 환경 설정 (이미지 렌더링 시에만 필요)

```bash
cp .env.sample .env
# .env에 OPENAI_API_KEY 입력

python3 -m venv .venv && source .venv/bin/activate
pip install 'openai>=1.40.0'
```

### 2. 새 런 초기화

```bash
bash scripts/init_infographic_run.sh my-topic
```

`_workspace/my-topic/` 아래에 모든 단계의 템플릿 파일이 생성됩니다.

### 3. Claude Code와 함께 사용

이 프로젝트는 [Claude Code](https://claude.ai/claude-code)의 에이전트 하네스로 설계되었습니다.  
Claude Code에서 자연어로 지시하면 자동으로 워크플로우가 실행됩니다:

```
"인포그래픽 만들어"
"성인용 학습만화로 만들어줘"
"이 주제를 만화로 가르쳐줘"
"조사 메모를 리포트로 정리해줘"
```

주요 슬래시 커맨드:
- `/infographic-orchestrator` — 전체 파이프라인 오케스트레이션
- `/infographic-storyboard` — 스토리보드 설계
- `/infographic-panel-render` — 프롬프트 팩 생성
- `/report-to-infographic-toon` — 조사 메모 → 리포트 정규화 → 검증 → 인포툰 제작

### 4. 검증

```bash
bash scripts/verify_infographic_run.sh _workspace/my-topic
```

종료 코드 `0`이면 모든 필수 파일이 올바르게 존재합니다.

### 5. 이미지 렌더링 (선택)

```bash
# 포스터 원샷
python scripts/render_openai.py --slug my-topic \
  --track editorial-poster --mode oneshot

# 학습만화 시리즈 (캐릭터 시트 → 페이지 순서로 자동 렌더)
python scripts/render_openai.py --slug my-topic \
  --track adult-learning-comic --mode series

# 실제 API 호출 없이 렌더 계획만 확인
python scripts/render_openai.py --slug my-topic \
  --track both --mode all --dry-run
```

출력 파일 (`_workspace/<slug>/05_renders/`):
- 포스터: `final-poster.png`, `block_00.png` ~ `block_05.png`
- 웹툰 페이지: `final-webtoon.png`, `panel_01.png` ~ `panel_04.png`
- 학습만화: `character-sheet.png`, `page-01.png` ~ `page-08.png`

렌더 완료 후 `scripts/render_openai.py`는 토큰 사용량과 추정 비용을
`_workspace/<slug>/04_review/render-cost-report.md`에 기록합니다. API 응답에
`usage`가 포함되면 실제 토큰을 사용하고, 누락된 경우 `gpt-image-2` 출력 토큰
계산식으로 가능한 범위만 추정합니다.

---

## 리포트 퍼스트 워크플로우

조사 메모를 먼저 구조화된 소스 리포트로 정리한 뒤, 그 리포트를 인포툰으로 변환하는 3단계 워크플로우를 지원합니다.

```text
# 1단계: 리포트 정규화 (추가 조사 없이 출처 부족 → needs verification)
"아래 조사 메모를 리포트 작성 가이드 형식으로 정리해줘."

# 2단계: 리포트 검증 (원문 미수정, 누락 항목만 보고)
"이 리포트가 제작 입력으로 충분한지 검증해줘."

# 3단계: 인포툰 제작 (승인된 리포트 → 이미지 렌더링까지)
"위 리포트를 바탕으로 성인용 학습만화를 4~6페이지로 제작해줘."
```

리포트는 `reports/<slug>-source-report.md`에 저장됩니다.

---

## 디렉터리 구조

```
infographic-toon/
├── .claude/
│   ├── agents/          # AI 에이전트 정의 (7종)
│   └── skills/          # 워크플로우 스킬 (5종)
├── .agents/
│   └── skills/          # Codex 호환 스킬 진입점
├── assets/              # HTML 참고 템플릿
├── examples/            # 예제 브리프
├── references/          # 트랙별 이미지 생성 규칙 + 한국어 카피 어투 규칙
├── scripts/
│   ├── init_infographic_run.sh     # 런 초기화
│   ├── verify_infographic_run.sh   # 런 검증
│   └── render_openai.py            # OpenAI 이미지 렌더링
├── templates/           # 각 단계별 마크다운 템플릿 + 캐릭터 프로필 템플릿
├── cast/                # 재사용 캐릭터 프로필 (git 무시, README/EXAMPLE만 추적)
├── _workspace/          # 실제 작업물 (git 무시)
├── reports/             # 소스 리포트 (인포툰 제작 전 단계)
├── CLAUDE.md            # AI 에이전트 지시사항
└── AGENTS.md            # 프로젝트 규칙 SSOT
```

---

## 에이전트 구성

Claude Code 내에서 다음 전문 에이전트들이 협업합니다:

| 에이전트 | 역할 |
|----------|------|
| `brief-analyst` | 사용자 입력을 정규화된 브리프로 정리 |
| `research-synthesizer` | 소스를 시각화 가능한 구조로 압축 |
| `storyboard-architect` | 페이지/블록 구조, 학습 설계, 캐릭터 설계 |
| `art-director` | 팔레트, 그리드, 타이포그래피, 시각 문법 확정 |
| `prompt-smith` | 이미지 생성 프롬프트 작성 |
| `panel-validator` | 프롬프트 팩 정합성 검증 |
| `compositor` | 렌더 순서, 핸드오프 문서 정리 |

---

## 핵심 설계 원칙

### 텍스트 보수주의

AI 이미지 생성에서 긴 한국어 본문은 아직 신뢰도가 낮습니다.

| 안전 (baked 가능) | 위험 (baked 지양) |
|---|---|
| 짧은 한국어 제목 | 긴 본문 단락 |
| 숫자 라벨 | 비교표 전체 |
| 경고 스탬프 | 정확한 법률/기술 문구 |
| 1-6단어 배지 | 여러 줄 체크리스트 |

### 어투도 산출물이다

이미지에 들어가는 한국어 문자열은 짧지만, AI 티는 짧은 문자열에서 더 잘 보입니다.
페이지 제목 6개가 모두 "A가 아니라 B"거나 등장인물 전원이 같은 종결어미를 쓰면
그림 품질과 무관하게 시리즈 전체가 생성물로 읽힙니다.

프롬프트를 확정하기 전에 어투 패스를 한 번 돌리고 `imagegen-checklist.md`에 기록합니다.
규칙은 `references/korean-copy-voice-rules.md`이고,
[epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai)(MIT)의 `humanize-korean`
분류 체계를 만화 카피 조건에 맞게 옮긴 것입니다. 단, **claim ledger가 어투보다 셉니다** —
습관적 완곡은 빼지만 출처·불확실성 표시는 남깁니다. 어투를 다듬어 클레임을 올리면 안 됩니다.

### 프롬프트 퍼스트

이 하네스의 핵심은 **잘 설계된 프롬프트 팩과 QA 문서**를 만드는 것입니다.  
`render_openai.py`는 편의를 위한 선택적 브릿지일 뿐, HTML 페이지 조립은 범위 밖입니다.

### 절대 가짜 결과 없음

`05_renders/`에 파일이 실제로 존재하지 않으면 "이미지가 생성되었습니다"라고 주장하지 않습니다.  
`scripts/render_openai.py`만이 해당 디렉터리에 파일을 쓸 수 있는 유일한 경로입니다.

---

## 렌더 설정 참고

| 환경변수 | 기본값 | 설명 |
|----------|--------|------|
| `OPENAI_API_KEY` | (필수) | OpenAI Images API 키 |
| `OPENAI_IMAGE_MODEL` | `gpt-image-2` | 이미지 모델 |
| `OPENAI_IMAGE_SIZE` | `1536x2048` | 출력 해상도 (3:4 세로) |
| `OPENAI_IMAGE_QUALITY` | `high` | 렌더 품질 |

권장 해상도 프리셋:
- `1024x1536` — 빠른 미리보기 (2:3)
- `1536x2048` — 균형 잡힌 기본값 (3:4, 웹툰 페이지)
- `2048x3072` — 고해상도 포스터 (2:3)

---

## 예제 브리프

- [examples/mythos-fable-brief.md](examples/mythos-fable-brief.md) — AI 프론티어 모델의 지정학적 리스크 포스터
- [examples/database-index-learning-comic-brief.md](examples/database-index-learning-comic-brief.md) — DB 인덱스 6페이지 학습만화

---

## 사용 예제 (프롬프트 모음)

이 프로젝트는 **Claude Code** 또는 **Codex**에서 자연어로 작업을 요청합니다.  
아래는 실제로 사용할 수 있는 프롬프트 예제입니다.

### 인포그래픽 포스터 만들기

```
인포그래픽 만들어.
주제: 2024년 한국 스타트업 투자 트렌드.
청중: 투자심사역, 스타트업 대표.
다크 뉴스룸 톤으로, 연도별 투자액 비교와 업종 TOP 5를 포함해줘.
```

```
아래 내용으로 세로 웹툰 느낌 인포그래픽 포스터 만들어줘.
[본문 붙여넣기]
```

### 성인 학습만화 만들기

```
"HTTP 캐시가 어떻게 작동하는지" 주제로 성인용 학습만화 6페이지 만들어줘.
청중: 주니어 백엔드 개발자.
캐릭터는 시니어 SRE와 주니어 백엔드 개발자 2명으로 해줘.
실제 이미지 렌더링까지 진행해줘.
```

```
이 주제를 만화로 가르쳐줘: "왜 Git rebase와 merge는 다른가"
4페이지, 대화체, 실무 예시 포함.
```

### 리포트 퍼스트 워크플로우 (3단계)

#### 1단계: 조사 메모 → 리포트 정규화

```
아래 조사 메모를 리포트 작성 가이드 형식으로 정리해줘.
추가 조사는 하지 말고 출처가 부족한 주장은 needs verification으로 표시해줘.

---
[조사 메모 붙여넣기]
```

#### 2단계: 리포트 검증

```
이 리포트가 인포툰 제작 입력으로 충분한지 검증해줘.
원문은 수정하지 말고 누락되거나 위험한 항목만 알려줘.
```

#### 3단계: 리포트 → 인포툰 제작

```
위 리포트를 바탕으로 성인용 학습만화를 4~6페이지로 제작해줘.
실제 이미지 렌더링까지 진행해줘.
```

```
위 리포트를 포스터 형태의 웹툰으로 만들어줘.
한 장짜리 세로 인포그래픽으로.
```

### 기존 런 수정하기

```
_workspace/http-cache-comic 런의 3페이지 프롬프트를 수정해줘.
캐릭터 표정을 더 과장되게 하고, 다이어그램에 화살표 라벨 추가.
```

```
mythos-fable 런 검증 실행해줘.
```

### 슬래시 커맨드로 단계별 실행

```
/infographic-orchestrator
→ 전체 파이프라인을 한 번에 실행

/infographic-storyboard
→ 스토리보드만 설계 (브리프가 이미 있을 때)

/infographic-panel-render
→ 프롬프트 팩만 생성 (스토리보드가 이미 있을 때)

/report-to-infographic-toon
→ 리포트 정규화 / 검증 / 제작을 한 스킬로 처리
```

### Codex에서 사용하기

Codex는 `.agents/skills/` 경로를 자동 발견합니다. 새 세션에서 동일하게 자연어로 요청하면 됩니다.

```
# Codex에서도 동일한 자연어 프롬프트 사용 가능
아래 조사 메모를 리포트 작성 가이드 형식으로 정리해줘.
추가 조사는 하지 말고 출처가 부족한 주장은 needs verification으로 표시해줘.
```

현재 세션에서 스킬이 자동 인식되지 않으면 명시적으로 호출:
```
$report-to-infographic-toon
```

---

## 요구사항

- **필수**: [Claude Code](https://claude.ai/claude-code) 또는 Codex (에이전트 오케스트레이션)
- **선택**: Python 3.10+, `openai>=1.40.0` (이미지 렌더링 시)
- **선택**: OpenAI API 키 (gpt-image-2 Images API 접근 권한)
