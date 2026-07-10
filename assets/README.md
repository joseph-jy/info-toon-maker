# Assets

이 폴더는 **downstream 참고용**이다. 이 리포의 하네스 산출물이 아니다.

## Scope Rule

- `AGENTS.md`와 `README.md`가 명시하듯, 이 리포는 이미지 생성 규칙, 프롬프트 팩, QA 핸드오프까지만 책임진다.
- HTML/CSS 페이지 조립은 **out of scope**다.
- 여기의 `infographic-template.html`은 downstream(웹 뷰어, 리포트 조립 담당자)이 참조할 수 있는 시각 문법 힌트일 뿐, 하네스 워크플로에서 생성하거나 검증하지 않는다.

## What Not To Do

- 이 HTML 템플릿을 하네스의 최종 산출물로 취급하지 말 것.
- `_workspace/<slug>/`에 이 HTML을 복사해 넣거나, 이 HTML이 있는 것을 렌더 완료로 주장하지 말 것.
- 이 HTML을 수정해서 `.claude/skills/` 워크플로에 끼워 넣지 말 것. skill 규칙과 정면 충돌한다.

## Legit Uses

- downstream 조립자에게 "이런 grid 감으로 조립하면 좋다"고 넘길 때의 예시.
- baked text 정책이 흔들릴 때, 어떤 영역이 HTML-side에서 살아있는 텍스트로 처리될지 감을 잡는 용도.
