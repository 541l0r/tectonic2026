# Day-of guide — fill in together from brief to demo

This is the live worksheet for the challenge. Fill it in step by step after the real brief arrives; leave unknown answers blank and mark assumptions. [COMMAND.md](COMMAND.md) explains the method to the team beforehand. The team changes the plan when evidence or time changes. The public preselection window is 18:00–23:00 on 30 September; the working plan budgets four hours and must be adjusted to the actual rules.

## 1. Capture and define the problem (minutes 0–20)

| Item | Answer |
| --- | --- |
| Exact challenge wording / link | [ ] |
| User and concrete pain | [ ] |
| Required outcome and judging criteria | [ ] |
| Available data, tools, and permissions | [ ] |
| Official KBC / event Trusted AI requirements, if provided | [ ] |
| Submission format and deadline | [ ] |
| Unknowns to ask the organizer | [ ] |

**One-sentence problem:** [ ]

**Facts versus assumptions:** [List both; mark each assumption for validation.]

**Existing KBC solution or process to improve:** [ ]

## 2. Create at most three candidate ideas (minutes 20–35)

Use the [global idea list and ten lenses](docs/IDEAS.md) only as prompts when relevant. Ask a mentor or organizer to clarify a material unknown when possible. Fill one row per candidate.

| Idea | User outcome | Combined lenses | Evidence/context | Customer-approved action | Three visible demo steps |
| --- | --- | --- | --- | --- | --- |
| A | [ ] | [ ] | [ ] | [ ] | [ ] |
| B | [ ] | [ ] | [ ] | [ ] | [ ] |
| C | [ ] | [ ] | [ ] | [ ] | [ ] |

## 3. Choose a product direction and describe the vision (by minute 40)

1. Cross out any idea that misses the brief, needs forbidden or unavailable data, or cannot show a useful result in the available time. Record the reason.
2. Compare the remaining ideas in the table. Record the evidence and main uncertainty for each. If scores help the discussion, use 0–2 per column (0 = weak, 1 = plausible, 2 = strong); do not choose by total alone.
3. Let each teammate say which idea they favour and what concerns them. Decide on one direction together, using the actual judging criteria when available. Record the reason and any unresolved concern.
4. Describe the future product vision for that direction. Do not decide its four-hour scope yet.

| Idea | Customer value | Capability leap | Clear demo | Buildable today | KBC fit / integration | Total / 10 | Key uncertainty |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| A | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| B | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| C | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

**Chosen idea and reason:** [ ]

**Team agreement:** [What each of Mathieu, Diana, and Damiens thinks is essential; note any concern.]

**Solution vision (what the mature product would do, not what we claim to build today):**

| Question | Team answer |
| --- | --- |
| What would the complete user experience look like? | [ ] |
| What is the distinctive mechanism, and how is it better than the current approach? | [ ] |
| What changes for the customer and for KBC compared with today? | [ ] |
| What one outcome KPI would show user improvement in real KBC use (population, event, denominator, period)? Is there a baseline and a safety/quality guardrail? | [ ] |
| What data, permissions, trust controls, integrations, or operations would real use require? What remains unknown? | [ ] |

## 4. Select the MVP within that direction (by minute 60)

The direction above is one product idea. Now choose **which part of that product** to build and prove in four hours. Start with one end-to-end journey; compare another scope only if the choice is unclear or contested. These are possible MVP scopes for the same direction, not another round of ideation.

1. State the one user outcome and central claim the prototype needs to prove. Include any mandatory requirement from the brief.
2. For each journey considered, name its starting input, the user action, the visible result, the data or tool it needs, and its main build or integration risk. Cross out a journey that cannot work with allowed inputs or fit the remaining time.
3. Choose the smallest complete journey that still proves the claim. Prefer a working UI → backend/tool → result path over more features that do not connect. All three agree on the choice and the reason.
4. List the capabilities needed for that journey. A capability is **Must** if removing it breaks the MVP promise or a mandatory rule. Put useful but removable capabilities in Should or Could; state Won't explicitly. Check that the Must list is feasible for Diana and Damiens to integrate in time.
5. Write the promise, three demo steps, fallback, and one observable success check. If these cannot be stated clearly, reduce or revise the journey before assigning build tasks.

**Central claim to prove:** [ ]

| Possible MVP journey for this direction | Starting input → user action → visible result | Data/tool needed | Main risk or fallback | Feasible in time? |
| --- | --- | --- | --- | --- |
| A | [ ] | [ ] | [ ] | [ ] |
| B, if needed | [ ] | [ ] | [ ] | [ ] |

**Chosen MVP journey and why:** [ ]

**Other journeys left outside this MVP and why:** [ ]

**Team agreement / remaining concern:** [ ]

**MVP promise:** [For this user, the four-hour product helps with this problem by producing this visible result.]

**Three demo steps:** [1. Starting situation/input → 2. User action and system work → 3. Visible useful result.]

**Cut line:** [The smallest end-to-end version that still proves the central claim.]

**Must (promise and mandatory rules):** [ ]

**Should (valuable, but the main journey can work without it):** [ ]

**Could (optional improvement):** [ ]

**Won't (explicitly outside this MVP):** [ ]

**Fallback:** [A minimal path for this MVP if the model, data source, or integration fails.]

**One observable success check:** [Given a concrete sample input and user action, what result must appear in the integrated product? Add the full feature and product criteria after this choice.]

**Value claim demonstrated now / assumption to validate later:** [What sample input and visible result support the demo claim?] / [What real-world KPI still needs measurement at KBC?]

**Trusted AI decisions for this MVP:** [Diana and the team record the relevant data, grounding, fairness, approval, security, transparency, and failure controls; add Must-have checks where needed. Follow official requirements in the brief.] Use the [working checklist](PREPARATION.md#10-kbc-trusted-ai-checklist) as a prompt.

## 5. Build and adapt

| Checkpoint | Decision to record | Owner |
| --- | --- | --- |
| By minute 60 | Have Diana and Damiens agreed on the MVP's request/response example and integration boundary? | Diana + Damiens |
| During the build | Is the UI → backend → visible result working? If no, cut optional scope until it is. | Diana + Damiens |
| After the first working slice | Does one mechanism prove the capability leap (tool, retrieval, calculation, or coordination)? If no, agree on the strongest one. | All three |
| Every 25 minutes | What works, what is blocked, how is everyone doing, and what is the next smallest visible improvement? Mathieu keeps this brief and tracks time; the team decides scope changes. If a blocker persists 15 minutes, use the mock boundary and move on. | Mathieu facilitates; all three decide |
| 45 minutes before deadline | Freeze new features. Verify the demo path, output, and fallback. | All three |
| 30 minutes before deadline | Rehearse the pitch and run the exact submission path. | Diana + Mathieu |

| Owner | Next task | File / interface | Done when | Status |
| --- | --- | --- | --- | --- |
| Mathieu | [ ] | [ ] | [ ] | [ ] |
| Diana | [ ] | [ ] | [ ] | [ ] |
| Damiens | [ ] | [ ] | [ ] | [ ] |

**MVP interface agreed by Diana and Damiens:** [Link or paste request and response JSON after selecting the MVP.]

**Latest working demo command / URL:** [ ]

**Current blocker and decision:** [ ]

**Feature and whole-product acceptance criteria:** [Mathieu drafts after MVP selection; all three agree on the checks. Verify Must-have features, then run the complete journey and relevant failure/fallback on the integrated build.] Use the short method and run sheet in [docs/ACCEPTANCE_CRITERIA.md](docs/ACCEPTANCE_CRITERIA.md).

**Integration check:** [Branch/build state, UI → API result, owner of next fix, and next run time.]

## 6. Final proof

- [ ] The pitch says what the future solution could do at KBC, for whom, and why it matters.
- [ ] The pitch names the distinctive mechanism and explains how it improves on today's approach.
- [ ] The live demo shows the central claim working on the current build; simulated parts and remaining limits are named.
- [ ] Must-have feature checks pass, and the complete product journey passes on the integrated build.
- [ ] Diana and the team have checked the relevant Trusted AI requirements; required controls appear in the build and acceptance scenarios.
- [ ] A new teammate can follow the three demo steps without an explanation.
- [ ] The visible result shows the claimed customer benefit and what evidence or tool produced it.
- [ ] Any consequential action has an explicit approval step; the demo can safely use mock actions.
- [ ] The fallback chosen for this MVP works if an external service fails.
- [ ] Diana can tell the problem, mechanism, result, and limitation within the allotted pitch time.
- [ ] The submission format and deadline have been checked against the actual rules.

This board is a practical adaptation for a four-hour working budget, not a proven recipe for winning. The [winner interview study](https://arxiv.org/html/2206.04744v1) supports exploring and defining a relevant problem before choosing a solution, checking rules and judges, and showing a demonstrable result. A [corporate hackathon case study](https://research.tue.nl/en/publications/utilizing-hackathons-to-foster-sustainable-product-innovation-the/) linked project continuation with focused preparation, a functioning prototype, customer fit, and ease of integration; it did not study Tectonic judging.
