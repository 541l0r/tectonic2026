# Tectonic hackathon — preparation workspace

Working draft, 27 September 2026. The KBC track is confirmed; a Kate 3.0 theme is our working hypothesis until the actual brief arrives. Use [COMMAND.md](COMMAND.md) for team roles, the demo contract, and the day-of log.

## Aim

Explore a step change in what an assistant can accomplish for a customer. A candidate should connect a real need to relevant evidence, a decision or plan, an action approved by the customer, and a visible result. A new screen or one extra answer is not enough by itself.

## Source notes

| Status | What we know | Source / implication |
| --- | --- | --- |
| Confirmed | The Tectonic hackathon has a KBC track. Preselection is 30 September, 18:00–23:00; the final is 20 October. Registration closes 29 September. | [Tectonic hackathon](https://www.tectonicconf.eu/hackathon). Confirm registration and location for all three teammates. |
| Confirmed | Kate already uses generative AI. KBC describes future Kate as more personalised and proactive and says it is exploring agentic AI with explicit customer approval. | [KBC, Kate: five years and five milestones](https://newsroom.kbc.com/kate-five-years-and-five-milestones). A proposal needs a concrete capability and outcome beyond adding a model to chat. |
| Confirmed | Kate already supports banking and insurance questions, practical help, and other services within KBC Mobile. | [KBC 2025 annual report, people and technology](https://www.kbc.com/content/dam/kbccom/doc/investor-relations/Results/jvs-2025/csr-vas-2025-en.pdf). Check existing functions before claiming an idea is new. |
| Hypothesis | The KBC case may concern Kate 3.0. | The public hackathon page names KBC but does not state the exact case. Replace this hypothesis with the released brief. |

When adding a source, record its date, the claim it supports, and whether the claim is confirmed or inferred. Keep customer data and event-provided material out of public notes unless the rules allow it.

## Ten innovation lenses

These are ways to generate and assess ideas, not ten separate features to build.

| Lens | Capability question |
| --- | --- |
| Calculation & Simulation | Can Kate predict, optimize, compare scenarios, or model consequences? |
| Data Representation & Knowledge | Can it understand relationships among people, products, events, and constraints? |
| Decision & Trade-offs | Can it help choose between actions, goals, risks, and future outcomes? |
| Orchestration & Planning | Can it break a goal into steps, use tools, and revise a plan? |
| Data Fusion & Context | Can it combine sources and select what matters now? |
| Memory & Adaptation | Can it retain useful state and adapt with the customer's knowledge and control? |
| Detection & Proactivity | Can it surface a relevant risk or opportunity before being asked? |
| Programmability & Composition | Can users express rules or combine capabilities into a workflow? |
| System Coordination | Can it coordinate several services or teams toward one outcome? |
| Control & Verification | Can it validate results, explain causes, and check that an action worked? |

## Brainstorm method for a preparation rehearsal

1. Pick one customer situation and one measurable problem. Write it without naming a technology.
2. Generate several ideas by combining two or three lenses. For each idea, describe the sequence: **trigger → context/evidence → options → customer-approved action → verification**.
3. Fill in one idea card per candidate. Reject ideas that only add a response or UI feature without changing the customer's outcome.
4. Compare candidates on customer value, capability leap, evidence/data availability, feasibility for a working demo, and fit with the released brief. Mark unknowns rather than guessing.
5. Build the hardest proof for the top candidate with mock data: one tool call, retrieval result, calculation, or cross-system handoff. Keep the existing deterministic UI/API slice as fallback.

### Idea card

| Question | Draft answer |
| --- | --- |
| Who is the user, and what triggers the need? | [ ] |
| What decision or action is difficult today? | [ ] |
| Which innovation lenses combine here? | [ ] |
| What context and evidence are needed, and where would they come from? | [ ] |
| What options, trade-offs, or forecast will Kate show? | [ ] |
| What action requires customer approval? | [ ] |
| How will Kate verify the outcome and handle failure? | [ ] |
| What measurable customer benefit would the demo show? | [ ] |
| What are the three visible demo steps and the mock-data fallback? | [ ] |

## PM and organization before the event

- [ ] Mathieu: confirm the exact registration, location, schedule, case-release process, rules, data access, and submission format with the organizer.
- [ ] Mathieu, Diana, and Damiens: each clone the GitHub repository, run the demo, and push a small branch. Use the direct branch merge workflow in [COMMAND.md](COMMAND.md).
- [ ] Damiens: prepare one mock tool and one small retrieval dataset so a candidate can demonstrate context, evidence, and action without waiting for live systems.
- [ ] Diana: prepare a reusable three-step demo outline and a 90-second pitch structure; adapt both to the chosen case.
- [ ] Mathieu: run one timed rehearsal using an invented brief and this brainstorm method. Record the chosen idea, rejected alternatives, risks, and the first build tasks.
- [ ] All three: when the real brief arrives, replace the Kate 3.0 hypothesis and score concepts against the actual problem before committing to one.
