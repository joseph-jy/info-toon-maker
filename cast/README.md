# Cast Library (Private)

여러 학습만화 런에서 재사용하는 **개인 캐릭터 원장**이다.

> 이 디렉터리의 실제 캐릭터 파일은 `.gitignore` 대상이라 레포에 올라가지 않는다.
> 추적되는 파일은 이 `README.md`와 `EXAMPLE.character.yaml` 두 개뿐이다.

## 사용법

1. `templates/cast-profile.template.yaml`을 복사한다.
2. `cast/<id>.character.yaml`로 저장하고 값을 채운다.
3. 필드 의미는 `references/cast-library-format.md`를 본다.
4. 레퍼런스 이미지는 `cast/images/<id>-NN.png`에 둔다.
5. 자주 쓰는 조합은 `cast/<id>.ensemble.yaml`로 저장한다.

## 레이아웃

```
cast/
  README.md                  <- 추적됨
  EXAMPLE.character.yaml     <- 추적됨 (가상 인물 예시)
  dwayne.character.yaml      <- 무시됨
  mina.character.yaml        <- 무시됨
  backend-duo.ensemble.yaml  <- 무시됨
  images/
    dwayne-01.png            <- 무시됨
```

## 런에서 어떻게 쓰이는가

성인 학습만화(`adult-learning-comic`)를 시작할 때, 에이전트는 캐릭터를 새로
발명하기 전에 `cast/`를 먼저 확인한다. 맞는 인물이 있으면 그 프로필의
`identity_tokens`와 `voice`를 `_workspace/<slug>/02_storyboard/character-bible.md`로
복사해 시리즈 간 인물 일관성을 유지한다. 없으면 평소대로 새로 설계하고,
재사용할 가치가 있으면 여기에 프로필로 저장하도록 제안한다.

`cast/`가 비어 있어도 기존 워크플로는 그대로 동작한다.

## 비공개 규칙

- `cast/` 내용을 커밋 대상 파일(README, 템플릿, 스킬 문서, 커밋 메시지)에
  붙여넣지 않는다.
- 실존 인물 프로필은 개인적·비상업적 용도로만 쓴다.
