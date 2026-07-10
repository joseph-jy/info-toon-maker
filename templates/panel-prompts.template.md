# Panel Prompt Pack

## Usage
- `editorial-poster` 모드에서는 `block_XX` 슬롯을 사용한다.
- `vertical-webtoon-page` 모드에서는 `panel_XX` 슬롯을 사용한다.
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

### panel_01
- purpose:
- story beat:
- crop:
- baked text:
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
- page region:
- caption/speech placement:
- cast continuity:
- camera or framing:
- transition to next panel:
- risk note:
- prompt:
- negative:

## Render Mapping
- block_00 -> hero
- block_01 -> comparison or risk card
- panel_01 -> first webtoon panel (baseline / past state)
- panel_02 -> escalation panel
- panel_03 -> concept reveal panel
- panel_04 -> consequence or next-page hook

## Recommended Render Order
- Pass 1: hero + text-light dramatic cards (or PAGE title bar + panel_01)
- Pass 2: medium-density analysis cards (or middle panels)
- Pass 3: only attempt text-heavy cards if needed (or closing panel with footnote)
