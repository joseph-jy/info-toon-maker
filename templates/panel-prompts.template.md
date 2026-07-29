# Panel Prompt Pack

## Usage
- `editorial-poster` 모드에서는 `block_XX` 슬롯을 사용한다.
- `vertical-webtoon-page` 모드에서는 `panel_XX` 슬롯을 사용한다.
- `vertical-webtoon-page`의 카피는 네 채널로 나눈다: 말풍선(패널당 1-2개, 10-40자), 제3자 나레이션 캡션 박스(페이지당 2-4개, 패널당 최대 1개, 25-60자), 자료 인서트(페이지당 1-2개, 장면 안 사물로 그린 문서/화면/메모/미니 표), 짧은 라벨.
- 기본 explanation density는 `extended`(페이지 총량 약 450자, 하드캡 500자)다. 페이지 총량과 density는 `layout-bible.md`의 `## Baked Copy Budget`에 적고, 채널별 상한은 `references/webtoon-page-image-rules.md`를 따른다.
- 두 슬롯을 섞지 않는다. 사용하지 않는 슬롯은 삭제한다.
- `adult-learning-comic`은 이 파일의 panel 슬롯을 사용하지 않고 `series-prompts.md`의 `character_sheet`와 `page_XX` 슬롯을 사용한다.

## Panel Prompt Pack (editorial-poster)

### block_00
- purpose:
- story beat:
- crop:
- baked text:
- poster region:
- caption/speech placement:
- continuity notes:
- risk note:
- prompt:
- negative:

### block_01
- purpose:
- story beat:
- crop:
- baked text:
- poster region:
- caption/speech placement:
- continuity notes:
- risk note:
- prompt:
- negative:

## Panel Prompt Pack (vertical-webtoon-page)

### page_header
- purpose: black PAGE title bar
- baked text: page label, main title, 1-line thesis
- page region: top strip
- risk note:
- prompt:
- negative:

### panel_01
- purpose:
- story beat:
- crop:
- baked text:
- speech bubble copy:
- narration box copy:
- material insert copy and carrier object:
- page region:
- caption/speech placement:
- cast continuity:
- camera or framing:
- transition to next panel:
- risk note:
- prompt:
- negative:

### panel_02
- purpose:
- story beat:
- crop:
- baked text:
- speech bubble copy:
- narration box copy:
- material insert copy and carrier object:
- page region:
- caption/speech placement:
- cast continuity:
- camera or framing:
- transition to next panel:
- risk note:
- prompt:
- negative:

### panel_03
- purpose:
- story beat:
- crop:
- baked text:
- speech bubble copy:
- narration box copy:
- material insert copy and carrier object:
- page region:
- caption/speech placement:
- cast continuity:
- camera or framing:
- transition to next panel:
- risk note:
- prompt:
- negative:

### panel_04
- purpose:
- story beat:
- crop:
- baked text:
- speech bubble copy:
- narration box copy:
- material insert copy and carrier object:
- page region:
- caption/speech placement:
- cast continuity:
- camera or framing:
- transition to next panel:
- risk note:
- prompt:
- negative:

### footer_strip
- purpose: narrow footer note
- baked text: one footnote, warning, or next-page hook (up to 2 sentences, about 80 Korean characters)
- page region: bottom strip
- risk note:
- prompt:
- negative:

## Render Mapping
- block_00 -> hero
- block_01 -> comparison or risk card
- page_header -> black PAGE title bar
- panel_01 -> first webtoon panel (baseline / past state)
- panel_02 -> escalation panel
- panel_03 -> concept reveal panel
- panel_04 -> consequence or next-page hook
- footer_strip -> narrow footer note

## Recommended Render Order
- Pass 1: hero + text-light dramatic cards (or PAGE title bar + panel_01)
- Pass 2: medium-density analysis cards (or middle panels)
- Pass 3: only attempt text-heavy cards if needed (or closing panel with footnote)
