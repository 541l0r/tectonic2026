# Brief-to-demo workflow — copy for each rehearsal or hackathon round

Use this as a shared decision board. Make one copy for the actual case. The team changes the plan when evidence or time changes; it does not need a separate planning app. The official preselection window is 18:00–23:00 on 30 September, but replace the time boxes below if the released rules differ.

## 1. Capture and define the problem (minutes 0–15)

| Item | Answer |
| --- | --- |
| Exact challenge wording / link | [ ] |
| User and concrete pain | [ ] |
| Required outcome and judging criteria | [ ] |
| Available data, tools, and permissions | [ ] |
| Submission format and deadline | [ ] |
| Unknowns to ask the organizer | [ ] |

**One-sentence problem:** [ ]

**Facts versus assumptions:** [List both; mark each assumption for validation.]

**Existing KBC solution or process to improve:** [ ]

## 2. Create at most three candidate ideas (minutes 15–25)

Use the [global idea list](IDEAS.md) and the ten lenses in [PREPARATION.md](PREPARATION.md) as prompts. Include Diana's KBC leads only when they fit the brief. Ask a mentor or organizer to clarify a material unknown when possible. Fill one row per candidate.

| Idea | User outcome | Combined lenses | Evidence/context | Customer-approved action | Three visible demo steps |
| --- | --- | --- | --- | --- | --- |
| A | [ ] | [ ] | [ ] | [ ] | [ ] |
| B | [ ] | [ ] | [ ] | [ ] | [ ] |
| C | [ ] | [ ] | [ ] | [ ] | [ ] |

## 3. Choose one together (by minute 30)

First reject any idea that misses the brief, needs forbidden or unavailable data, or cannot show a working result with mock data. For the remaining ideas, score each criterion 0–2 (0 = weak, 1 = plausible, 2 = strong). Record why, not only the total. Use the actual judging criteria to break a tie.

| Idea | Customer value | Capability leap | Clear demo | Buildable today | KBC fit / integration | Total / 10 | Key uncertainty |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| A | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| B | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| C | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

**Chosen idea and reason:** [ ]

**Team agreement:** [What each of Mathieu, Diana, and Damiens thinks is essential; note any concern.]

**Cut line:** [The smallest end-to-end version that still proves the idea.]

**Essential:** [ ]

**Optional if time remains:** [ ]

**Fallback:** [What runs if the model, data source, or integration fails.]

**One claim to prove in the demo:** [ ]

## 4. Build and adapt

| Checkpoint | Decision to record | Owner |
| --- | --- | --- |
| By minute 40 | Has Diana and Damiens agreed on one request/response example and the mock data needed? | Diana + Damiens |
| By minute 75 | Is the UI → API → visible result working with mock data? If no, cut scope until it is. | Diana + Damiens |
| After the first working slice | Does one mechanism prove the capability leap (tool, retrieval, calculation, or coordination)? If no, agree on the strongest one. | All three |
| Every 25 minutes | What works, what is blocked, how is everyone doing, and what is the next smallest visible improvement? Mathieu keeps this brief and tracks time; the team decides scope changes. If a blocker persists 15 minutes, use the mock boundary and move on. | Mathieu facilitates; all three decide |
| 60 minutes before deadline | Freeze new features. Verify the demo path, output, and fallback. | All three |
| 30 minutes before deadline | Rehearse the pitch and run the exact submission path. | Diana + Mathieu |

| Owner | Next task | File / interface | Done when | Status |
| --- | --- | --- | --- | --- |
| Mathieu | [ ] | [ ] | [ ] | [ ] |
| Diana | [ ] | [ ] | [ ] | [ ] |
| Damiens | [ ] | [ ] | [ ] | [ ] |

**API example agreed by Diana and Damiens:** [Link or paste request and response JSON.]

**Latest working demo command / URL:** [ ]

**Current blocker and decision:** [ ]

**Whole-demo acceptance criteria and scenarios:** [Mathieu drafts while the team builds. Include the normal path, missing evidence or tool failure, and the fallback; all three review.]

**Integration check:** [Branch/build state, UI → API result, owner of next fix, and next run time.]

## 5. Final proof

- [ ] A new teammate can follow the three demo steps without an explanation.
- [ ] The visible result shows the claimed customer benefit and what evidence or tool produced it.
- [ ] Any consequential action has an explicit approval step; the demo can safely use mock actions.
- [ ] The fallback works if external services fail.
- [ ] Diana can tell the problem, mechanism, result, and limitation within the allotted pitch time.
- [ ] The submission format and deadline have been checked against the actual rules.

This board is a practical adaptation for a five-hour event, not a proven recipe for winning. The [winner interview study](https://arxiv.org/html/2206.04744v1) supports exploring and defining a relevant problem before choosing a solution, checking rules and judges, and showing a demonstrable result. A [corporate hackathon case study](https://research.tue.nl/en/publications/utilizing-hackathons-to-foster-sustainable-product-innovation-the/) linked project continuation with focused preparation, a functioning prototype, customer fit, and ease of integration; it did not study Tectonic judging.
