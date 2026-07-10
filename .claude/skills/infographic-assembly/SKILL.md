---
name: infographic-assembly
description: "레거시 이름이지만 현재는 페이지 조립이 아니라 이미지 생성 핸드오프 보조 스킬이다. render order, risk notes, downstream handoff 문서를 정리할 때만 제한적으로 사용한다."
---

# Infographic Handoff

이 스킬은 더 이상 HTML 조립을 하지 않는다. 현재 역할은 **이미지 생성 하네스의 마지막 검수/핸드오프 정리**다.

## Required Outputs

- `_workspace/<slug>/04_review/imagegen-checklist.md`
- `_workspace/<slug>/04_review/handoff.md`

## Handoff Rules

### 1. Preserve Scope
이 리포는 HTML을 만들지 않는다. downstream 조립 담당자가 무엇을 별도 합성해야 하는지만 남긴다.

### 2. Record Render Order
`handoff.md`에는 반드시 다음을 적는다.
- hero first
- text-light blocks second
- text-dense or comparison-heavy blocks last
- adult learning comic: character sheet -> page 01 smoke test -> remaining pages in order

### 3. Be Honest About Asset State
`imagegen-checklist.md`에는 다음을 기록한다.
- prompt pack only인지
- 일부 PNG가 실제로 생성되었는지
- dense Korean baked-text risk가 어디에 있는지

### 4. Keep Downstream Notes Short
`handoff.md`는 다음 렌더러나 조립 담당자가 바로 읽고 실행할 수 있어야 한다.

## QA Checklist

- storyboard와 prompt pack이 같은 블록 구조를 공유하는가
- render mode가 layout bible과 checklist에 일치하는가
- 실제 없는 PNG를 생성 완료처럼 주장하지 않았는가
- downstream composition이 필요한 영역이 명시되었는가
- adult learning comic의 페이지 수와 learning design이 일치하는가
- 첫 페이지의 오개념이 마지막 페이지에서 해결되는가
- 캐릭터 시트를 모든 페이지의 identity reference로 사용했는가

## Anti-Patterns

- HTML/CSS 책임까지 이 스킬에 다시 밀어 넣는 것
- long-form Korean body copy를 baked text로 무리하게 넘기는 것
- asset placeholder를 실제 렌더처럼 표현하는 것
