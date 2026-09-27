# Tectonic hackathon — preparation workspace

Working draft, 27 September 2026. The KBC track is confirmed; a Kate 3.0 theme is our working hypothesis until the actual brief arrives. Use [COMMAND.md](COMMAND.md) for the team working agreement and day-of log. We prepare the collaboration method and local environments now; challenge-specific data, schema, API contract, architecture, and solution wait for the brief.

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

### KBC signals found by Diana

These five themes are research leads, not predictions of the hidden case or implementation tasks. A vacancy shows work inside KBC; it does not tell us what the hackathon brief will ask.

| Theme | What the linked KBC source supports | Rehearsal probe / caveat |
| --- | --- | --- |
| Customer intent and next action | The indexed [Kate Intent Factory vacancy](https://www.kbc.be/jobs/nl/vacatures/ID89573.html) describes detecting a customer's likely intent from relevant data and selecting suitable communication. That page currently returns 404; a [KBC Global Services job posting](https://cz.linkedin.com/jobs/view/data-engineer-at-kbc-global-services-4420412769) also names the project. Preserve this as a lead to recheck. | Mock a life-event signal, explain the evidence, and compare possible next actions. Lenses: detection, context, decision. |
| AI quality for Kate | The [AI Prompt Engineer vacancy](https://www.kbc.be/jobs/nl/vacatures/ID90924.html) explicitly covers testing prompts and improving the correctness, consistency, usefulness, speed, and reliability of Kate's AI output. | Build a small quality gate that checks evidence, uncertainty, and escalation. Lenses: control and verification. |
| Customer onboarding | The [Customer Handling role](https://www.kbc.be/jobs/nl/vacatures/ID90503.html) says onboarding must balance customer experience, compliance, and operational efficiency. It does not specify an AI onboarding project. | Mock missing-information detection and a review path. Lenses: orchestration, context, verification. |
| Customer documents | The [internship listing](https://www.kbc.be/jobs/nl/stages/ID91001.html) says KBC handles hundreds of thousands of customer documents monthly through several applications and AI-supported solutions. The internship itself concerns Java test automation for a coordinating application. | Mock extraction, conflicting facts, and routing, without claiming this is KBC's requested project. Lenses: knowledge, system coordination, verification. |
| Fraud and social engineering | KBC's [Guardian Angel announcement](https://newsroom.kbc.com/kbc-brings-guardian-angel-to-more-than-4-million-customers-in-belgium) describes a live trusted-person review for suspicious payments. KBC says its detection system checks more than 150 signals and 700 patterns. | Explore an extension that explains or verifies a risk; do not pitch Guardian Angel itself as new. Lenses: detection, human coordination, verification. |

When the brief arrives, match its wording against these themes. If none fits, set them aside and start from the actual user problem.

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

## Challenge-decomposition method

Use [WORKFLOW_TEMPLATE.md](WORKFLOW_TEMPLATE.md) as the fillable decision board once the brief arrives. [IDEAS.md](IDEAS.md) can prompt discussion if relevant, but no idea there is a preselected solution.

1. Pick one customer situation and one measurable problem. Write it without naming a technology.
2. Generate several ideas by combining two or three lenses. For each idea, describe the sequence: **trigger → context/evidence → options → customer-approved action → verification**.
3. Fill in one idea card per candidate. Reject ideas that only add a response or UI feature without changing the customer's outcome.
4. Compare candidates on customer value, capability leap, evidence/data availability, feasibility for a working demo, and fit with the released brief. Mark unknowns rather than guessing.
5. After all three agree on the MVP, choose the smallest end-to-end proof and its integration fallback. Design the data, interface, and architecture for that proof.

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

### What the hackathon research suggests

A [study of 32 hackathon winners and five organizers](https://arxiv.org/html/2206.04744v1) found a recurring sequence: explore and define a real user problem, consider alternative solutions, then deliver a demonstrable prototype and clear pitch. The authors recommend checking rules, judging criteria, and existing solutions. These are interview findings, not a causal formula for winning. A separate [corporate hackathon case study](https://research.tue.nl/en/publications/utilizing-hackathons-to-foster-sustainable-product-innovation-the/) associated project continuation with focused preparation, a functioning prototype, current-customer fit, and ease of integration. Its outcome was continuation after the event, not a hackathon prize. The decision board applies these ideas to the team's four-hour working budget.

- [ ] Mathieu: confirm the exact registration, location, schedule, case-release process, rules, data access, and submission format with the organizer.
- [ ] Mathieu, Diana, and Damiens: each clone the GitHub repository, run the demo, and push a small branch. Use the direct branch merge workflow in [COMMAND.md](COMMAND.md).
- [ ] Diana: lead the shared documents and repository coordination remotely; agree with the team on branch ownership and the merge integrator.
- [ ] Diana and Damiens: agree on general JSON, error, environment-variable, and integration conventions; leave the challenge-specific API contract open.
- [ ] Diana: prepare a reusable three-step demo and pitch outline; adapt both to the chosen case.
- [ ] All three: walk through the challenge-decomposition and MVP decision method. Mathieu facilitates the first discussion and 25-minute check-ins; the team chooses the MVP together when the real brief arrives.
- [ ] All three: when the real brief arrives, replace the Kate 3.0 hypothesis and score concepts against the actual problem before committing to one.
