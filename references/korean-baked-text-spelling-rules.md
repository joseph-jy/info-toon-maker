# Korean Baked-Text Spelling Rules

How to keep Korean strings from coming out misspelled when the Images API bakes them into a page. This is a **render-reliability** document, not a style document — tone and register live in `korean-copy-voice-rules.md`.

The failures here are not the model misunderstanding the copy. The whitelist string is almost always correct and the render is wrong. So the fix is never "write better Korean"; it is choosing strings that survive rasterization, and guarding the ones you cannot change.

## The core principle

**Substitution beats guarding. Guarding beats re-rendering. Re-rendering is a last resort.**

Accumulated across runs, the ranking is consistent:

1. **Replace the string** with a synonym or a rephrasing that does not contain the fragile syllable. Usually lands correct on the first render.
2. **Positive jamo guard** for strings that cannot be replaced (proper nouns, a claim's exact wording, a required ending). Often lands on the first render.
3. **Re-render unchanged.** A dice roll. Fixes the target sometimes and introduces a new typo elsewhere often.

Choose at authoring time, before the whitelist is frozen. A fragile string caught during the copy pass costs nothing; the same string caught after render costs that page.

## Failure is per-instance, not per-word

The same syllable can render correctly in one place on a page and wrong in another. Observed: `흑` correct in a speech bubble and `혹` in a narration box on the same page; `비둘기` correct in the page title, the panel caption, and the thumbnail while the short arrow label on that same page rendered `비들기` twice in a row.

Consequences:

- "This word is risky" is not a sufficient guard. Write **how many times the syllable appears on the page and that every instance must be the identical glyph**.
- Checking one occurrence does not clear the others. Inspect each.
- A string that rendered fine on page 3 can fail on page 5. Do not treat an earlier success as coverage.

## Size is an independent variable

Small labels and large display type fail differently.

- **Smallest labels are the most fragile.** Arrow labels, axis numbers, badges, and one-or-two-word captions fail more than 30pt bubble text on the same page, and they resist guards that work on longer strings. Give them the *most* conservative wording, not the least — the temptation is to treat them as trivial.
- **Large display type breaks compound final consonants.** `ㄺ ㄵ ㄶ ㄼ ㅄ` collapse into an unreadable glyph at thumbnail-title weight even with a jamo guard in place, while the same syllable is fine at body size. Author page titles and thumbnail phrases **without compound finals**. Re-check any word promoted from body copy to a title.

## Writing a positive guard

Only for strings you cannot replace.

- Decompose the correct form: `린 = ㄹ + the VERTICAL vowel ㅣ + final ㄴ`. Name the stroke direction — `ㅜ` has a tail hanging **down**, `ㅡ` does not; `ㅓ` has **one** short stroke, `ㅕ` has **two**.
- State the instance count and demand identical glyphs across them.
- Ask for a syllable-by-syllable read-back before drawing: `마-이-크-로-월-드`.
- For an ending or morpheme that recurs across the whole series, declare it **once** in the shared prompt policy, not per page.

### Do not prime the error

Writing `never 롤` or `no 곰` puts the wrong form into the prompt, and it has been observed to make that wrong form appear **somewhere else on the same page** that was previously correct. Two rules that look contradictory, reconciled:

- A `never X` / negative-list guard may be used on the **first** attempt.
- The moment a typo **moves to a new location** after a guarded re-render, switch to positive-only guards (correct jamo decomposition, no wrong form anywhere in the prompt) and start replacing strings.

## Known fragile patterns

Vowel pairs that swap: `ㅜ↔ㅗ` · `ㅜ↔ㅡ` · `ㅓ↔ㅏ` · `ㅓ↔ㅕ` · `ㅔ↔ㅐ` · `ㅕㅣ↔ㅏㅣ`.

Recorded misrenders, useful as a fragility smell test rather than a blocklist:

| Correct | Rendered | Class |
|---|---|---|
| 품질 · 금 · 불을 · 끄는 | 폼질 · 곰 · 불울 · 고는 | vowel / tense consonant |
| 훅은 · 룰이 | 혹은 · 롤이 | single-syllable noun + particle |
| 거든요 · 예요 | 가든요 · 에요 | sentence ending |
| 측정 · 저는 · 번질 · 잴 | 축정 · 지는 · 번절 · 젤 | body copy |
| 흑백개발자 | 혹백개발자 | one instance of two |
| 긁어도 | (illegible `ㄺ`) | compound final at display size |
| 틀린 · 마이크로월드 · 읽어야 | 틀라 · (malformed 크) · 읽여야 | small label / narration |
| 비둘기 · 실제로 · 이번 주에 | 비들기 · 설제로 · 이번 주애 | small label |

Single-syllable nouns carrying a particle (`훅은`, `룰이`, `잴`) are disproportionately fragile — a compound or a rephrasing usually fixes them (`훅` inside `자동 체크 훅` rendered correctly every time while standalone `훅은` failed twice).

## Numbers and diagram text

- Digits inside a string drift (`5개` → `4개`). State the digit and forbid the neighbours.
- **Do not ask for a value to be placed at a position on a scale.** Percentage-of-axis-length instructions have been observed to miss by 8-10 percentage points even when the prompt says "do not guess". When the point is comparing two numbers, compare **lengths** instead: two bars whose relative length carries the meaning, no axis, no ticks, no scale endpoints. Reserve a ticked axis for showing a single value.
- Keep any curve or trend that needs no numbers in a **separate inset** with no numbers at all. Mixing a numbered axis and a trend curve in one frame is what lets a value land on the wrong gradation.

## Re-render stopping rule

Each re-render round fixes its targets and rolls fresh dice on every other string. Observed rates: a round fixing 4 defects introduced 1 new typo; another introduced 1 while a guarded string failed again.

- Before re-rendering, apply the substitution/guard ladder above. Re-rendering with an unchanged prompt is not a fix.
- If a string fails **twice** under a guard, stop guarding it and replace it. Two consecutive failures mean the guard is not the lever.
- When typos start **moving between locations** rather than shrinking in count, stop the loop.
- Record what you stop on. Surviving defects become **accepted defects** in `handoff.md` with the correct string written beside the rendered one, so the next reader knows the whitelist was right. Particle- and label-level typos that do not change a claim's status are acceptable to ship; a typo inside a number, a name, or an attribution is not.

## Where this fits the workflow

- Author the whitelist with this document in hand, during the same pass as `korean-copy-voice-rules.md` and **before** the whitelist is frozen. The two passes pull in different directions — voice wants natural phrasing, this wants robust glyphs — and the cheapest resolution is finding a phrasing that satisfies both while the copy is still soft.
- **The claim ledger outranks both.** Never substitute a string in a way that changes a claim's attribution, status marker, or hedge. If the only robust phrasing would weaken a `party-claim` or drop a `speculation` marker, keep the exact wording, guard it, and accept the render risk.
- Inspect renders by cropping the region at source resolution and enlarging it. Vowel errors are invisible in a fit-to-window view.
