# Source Report Guide

Use this guide to write the dry, source-backed report that becomes the factual input to an infographic-toon poster or adult learning comic. The report does not need polished prose or visual directions. It must make every important claim traceable and show how confidently it may be stated.

## 1. What The Report Must Do

The report must let a downstream creator answer five questions without guessing:

1. What happened or what concept is being explained?
2. Which statements are verified facts, attributed claims, analysis, or speculation?
3. Which source supports each statement?
4. What must not be simplified into a stronger claim?
5. What should the reader understand or decide after reading?

The report is the factual boundary. Do not mix facts and opinions in one bullet, hide uncertainty in footnotes, or list sources without connecting them to claims.

## 2. Required Sections

### Metadata

Include:

- title
- authoring date
- information cutoff date
- topic
- intended audience
- central question
- included scope
- excluded scope

Use an explicit cutoff date for news, policy, law, products, companies, research, or other time-sensitive subjects.

### Executive Summary

Write 5-10 numbered items. Put one claim or conclusion in each item. Keep facts, party positions, and analysis in separate items.

### Terms And Actors

List important people, organizations, systems, policies, products, and technical terms. Note naming ambiguity or sensitivity.

### Timeline Or Explanation Order

Use a timeline for incidents and policy stories. Use a mechanism sequence for technical or conceptual subjects. If a date is unknown, write `날짜 미확인`; do not invent an order.

### Claim Ledger

Give every material claim a stable ID and connect it to one or more source IDs.

| Status | Meaning | Allowed treatment |
| --- | --- | --- |
| `verified` | Supported by a suitable primary source or strong corroboration | May use a direct factual sentence within the reported scope |
| `reported` | Reported by a publication but not independently established here | Attribute to the publication |
| `party-claim` | Said by a government, company, witness, or other interested party | Attribute to the speaker |
| `analysis` | An inference or interpretation | Mark as analysis or possibility |
| `speculation` | A hypothesis, rumor, or community suspicion | Mark as suspicion; never stage as fact |
| `needs verification` | Missing, inadequate, contradictory, or unstable support | Keep out of assertive baked text |

For each claim include:

- ID
- one-sentence claim
- status
- source IDs
- allowed wording
- caveat or prohibited strengthening

### Viewpoints And Counterarguments

Separate each actor's position. Record evidence offered, strongest counterargument, and unresolved point. Keep official positions separate from community commentary.

### Causes, Results, And Implications

Separate:

- trigger or mechanism
- directly observed result
- second-order impact
- longer-term implication

Do not present a forecast or implication as an observed result.

### Exact Names And Numbers

List names, dates, numbers, formulas, code, and technical labels that must be copied exactly. Note units, versions, jurisdictions, and time ranges.

### Uncertainties And Prohibited Wording

List open questions. Then list sentences the visual artifact must not say. This is the easiest way to prevent dramatic art direction from laundering uncertainty into fact.

### Final Takeaway

State:

- the most important conclusion
- the distinction the reader must remember
- the practical implication or decision
- what would be an overinterpretation

### Sources

For every source include title, publisher, author when available, date, URL or document location, source type, connected claim IDs, relevant summary, and reliability note.

## 3. Writing Rules

- Prefer short factual bullets and tables over essay prose.
- Put one proposition in each claim-ledger row.
- Use exact dates such as `2026-07-10`, not `recently`.
- Preserve attribution in `allowed wording`.
- Give separate IDs to the event, its alleged cause, and its interpreted meaning.
- Record disagreement between sources rather than choosing silently.
- Keep source excerpts short; summarize unless exact wording is essential.
- Do not include art style, panel layout, camera direction, character design, or speech-bubble copy. Those belong to the production skill.

## 4. Blank Template

```md
# Source Report

## 1. Metadata
- Title:
- Authoring date:
- Information cutoff date:
- Topic:
- Intended audience:
- Central question:
- Included scope:
- Excluded scope:

## 2. Executive Summary
1.
2.
3.
4.
5.

## 3. Terms And Actors
| Name | Type | Definition or role | Naming or accuracy note |
| --- | --- | --- | --- |
|  |  |  |  |

## 4. Timeline Or Explanation Order
| Date or step | Event or mechanism | Actors | Claim/source IDs |
| --- | --- | --- | --- |
|  |  |  |  |

## 5. Claim Ledger
| ID | Claim | Status | Sources | Allowed wording | Caveat / prohibited strengthening |
| --- | --- | --- | --- | --- | --- |
| C01 |  | `verified` / `reported` / `party-claim` / `analysis` / `speculation` / `needs verification` | S01 |  |  |

## 6. Viewpoints And Counterarguments

### Viewpoint A
- Actor:
- Position:
- Evidence offered:
- Strongest counterargument:
- Unresolved point:

### Viewpoint B
- Actor:
- Position:
- Evidence offered:
- Strongest counterargument:
- Unresolved point:

## 7. Causes, Results, And Implications
- Trigger or mechanism:
- Directly observed result:
- Second-order impact:
- Long-term implication:

## 8. Exact Names And Numbers
| Item | Exact value or spelling | Source | Accuracy note |
| --- | --- | --- | --- |
|  |  |  |  |

## 9. Uncertainties And Prohibited Wording

### Open Questions
-

### Do Not Say
-

## 10. Final Takeaway
- Most important conclusion:
- Distinction to remember:
- Practical implication or decision:
- Overinterpretation to avoid:

## 11. Sources

### S01
- Title:
- Publisher:
- Author:
- Date:
- URL or location:
- Source type: primary / government / company / paper / press / community
- Connected claims:
- Relevant summary:
- Reliability note:
```

## 5. Condensed Example

This example demonstrates structure only. It does not verify that the named models, government action, project, or alleged motives exist. Missing source details remain visibly unresolved.

```md
# Source Report

## 1. Metadata
- Title: 미국의 Anthropic 모델 접근 제한 논란과 AI 공급망 리스크
- Authoring date: 2026-07-10
- Information cutoff date: 2026-07-10
- Topic: 사용자 제공 자료에 나타난 Mythos 5 / Fable 5 접근 제한 논란
- Intended audience: AI 전략, 보안, 구매, 플랫폼 담당 실무자
- Central question: 해외 AI API를 핵심 업무에 의존할 때 어떤 통제·연속성 위험을 점검해야 하는가?
- Included scope: 정부 논리, 기업 대응, 커뮤니티 해석, 기업 리스크, 소버린 AI 함의
- Excluded scope: 실제 법률 자문, 모델 성능 평가, 미확인 동기의 사실 판정

## 2. Executive Summary
1. 사용자 자료는 미국 정부가 `Mythos 5`와 `Fable 5`의 외국인 접근을 제한했다고 서술하지만, 이 보고서에는 이를 독립 검증할 원문 링크가 없다.
2. `Project Glasswing`을 통한 SK텔레콤 접근이 개입 계기였다는 내용은 보도 주장으로만 다뤄야 한다.
3. Anthropic이 국적 필터링 대신 전체 고객 비활성화를 택했다는 내용도 기업 발표 또는 신뢰할 수 있는 보도 확인이 필요하다.
4. 공포 마케팅의 역풍과 IPO 견제설은 관측 사실이 아니라 커뮤니티 해석과 의혹이다.
5. 검증 여부와 별개로, 이 시나리오는 외부 AI API 의존이 통제권과 사업 연속성 위험을 만든다는 학습 사례로 사용할 수 있다.

## 3. Terms And Actors
| Name | Type | Definition or role | Naming or accuracy note |
| --- | --- | --- | --- |
| Mythos 5 | AI model | 사용자 자료가 Anthropic 최상위 모델로 지칭 | 공식 모델명 검증 필요 |
| Fable 5 | AI model | 사용자 자료가 함께 제한됐다고 지칭 | 공식 모델명 검증 필요 |
| Project Glasswing | project | 사용자 자료가 보안 협의체로 설명 | 명칭과 성격 검증 필요 |
| SK텔레콤 | company | 접근 권한 논란에 등장하는 한국 통신사 | 중국 연계 추론과 사실을 분리 |
| Sovereign AI | strategy concept | 데이터·인프라·모델 통제권을 자국 또는 조직이 확보하려는 접근 | 단일 제품 또는 완전한 자급과 동일시 금지 |

## 4. Timeline Or Explanation Order
| Date or step | Event or mechanism | Actors | Claim/source IDs |
| --- | --- | --- | --- |
| 날짜 미확인 | SK텔레콤에 모델 접근 권한이 제공됐다는 주장 | Anthropic, SK텔레콤 | C02 / S01 필요 |
| 날짜 미확인 | 미국 정부가 접근 취소를 요구했다는 주장 | 미국 정부, Anthropic | C01-C02 / S01 필요 |
| 날짜 미확인 | Anthropic이 모델을 전체 비활성화했다는 주장 | Anthropic, customers | C03 / S02 필요 |
| 이후 | 기업 의존 위험과 소버린 AI 논의가 제기됐다는 분석 | industry community | C05-C06 / S03 필요 |

## 5. Claim Ledger
| ID | Claim | Status | Sources | Allowed wording | Caveat / prohibited strengthening |
| --- | --- | --- | --- | --- | --- |
| C01 | 미국 정부가 두 모델의 외국인 접근 제한을 요구했다 | `needs verification` | S01 필요 | “사용자 제공 시나리오에서는 접근 제한이 제기된다” | 공식 정책으로 단정 금지 |
| C02 | SK텔레콤 접근이 정부 개입의 계기였다 | `reported` | Wired 원문 필요 | “해당 보도에 따르면 SK텔레콤 접근이 계기로 지목됐다” | 정부 공식 설명으로 강화 금지 |
| C03 | Anthropic은 국적 필터 대신 전체 비활성화를 택했다 | `needs verification` | 회사 발표 또는 보도 필요 | “자료는 전체 비활성화 대응을 서술한다” | 실제 범위와 기간 단정 금지 |
| C04 | Anthropic의 위험 마케팅이 규제를 불렀다 | `analysis` | 커뮤니티 출처 필요 | “일부 커뮤니티는 공포 마케팅의 역풍으로 해석했다” | 인과관계 단정 금지 |
| C05 | IPO를 방해하려는 정치적 의도가 있었다 | `speculation` | 주장 출처 필요 | “정치적 견제 의혹도 제기됐다” | 사실 장면으로 재현 금지 |
| C06 | 외부 AI API 의존은 통제권과 연속성 위험을 만든다 | `analysis` | 별도 사례·정책 자료 권장 | “이 시나리오는 공급망 통제 위험을 보여주는 사고실험이 된다” | 한 사건이 모든 공급자를 대표한다고 일반화 금지 |

## 9. Uncertainties And Prohibited Wording

### Open Questions
- 모델명과 출시 여부
- 정부 조치의 존재, 법적 근거, 적용 대상
- Project Glasswing의 존재와 접근 권한
- 전체 비활성화의 범위와 기간
- IPO 관련 정치적 의도의 존재

### Do Not Say
- “SK텔레콤이 중국에 모델을 유출했다.”
- “미국 정부가 Anthropic의 IPO를 저지했다.”
- “모든 외국인이 해당 모델을 법적으로 사용할 수 없다.”
- “소버린 AI만 구축하면 공급망 위험이 사라진다.”

## 10. Final Takeaway
- Most important conclusion: 핵심 AI 기능을 단일 외부 API에 맡기면 공급자의 기술 장애뿐 아니라 정책·관할권·접근 통제 변화도 사업 연속성 위험이 된다.
- Distinction to remember: 사건에 관한 검증된 사실과 그 사건에서 도출한 공급망 사고실험을 구분한다.
- Practical implication or decision: 기업은 데이터 위치, 접근 통제, 대체 모델, 전환 비용, 중단 대응 계획을 함께 점검해야 한다.
- Overinterpretation to avoid: 소버린 AI를 완전한 자급이나 무조건적인 안전으로 해석하지 않는다.

## 11. Sources

### S01
- Title: Wired article cited by the user
- Publisher: Wired
- Author: 확인 필요
- Date: 확인 필요
- URL or location: 원문 URL 필요
- Source type: press
- Connected claims: C01, C02
- Relevant summary: 사용자 자료는 정부 개입과 SK텔레콤 접근의 연결을 이 기사에 귀속한다.
- Reliability note: 원문을 제공받기 전에는 정확한 표현과 취재 근거를 검증할 수 없다.
```

## 6. Minimal Production Requests

After the report, request one deliverable and one execution depth.

```text
위 리포트를 바탕으로 포스터 형태의 웹툰을 만들어줘. 실제 이미지 렌더링까지 진행해줘.
```

```text
위 리포트를 바탕으로 성인용 학습만화를 4~6페이지 규모로 만들어줘. 실제 이미지 렌더링까지 진행해줘.
```

For a prompt package without image generation:

```text
위 리포트를 바탕으로 성인용 학습만화를 5페이지로 기획해줘. 프롬프트 패키지까지만 만들어줘.
```
