# Global view — Kate 3.0 rehearsal ideas

Working hypotheses for the KBC track, 27 September 2026. The challenge is still hidden. These are discussion prompts, not predictions, selected solutions, or tasks to build before the event. Use the actual brief and judging criteria to choose or discard them. KBC source leads and the ten innovation lenses are collected below; [WORKFLOW_TEMPLATE.md](../WORKFLOW_TEMPLATE.md) is the day-of decision board.

## What would feel like a capability leap?

**Customer goal → relevant context → options or plan → approved action → checked outcome.** Each idea below should show at least one nontrivial step between understanding and answering: retrieval, calculation, decision, tool use, coordination, or verification. Name the current KBC feature it improves before claiming novelty.

| Direction | Customer problem and proposed leap | Smallest visible demo | Lenses |
| --- | --- | --- | --- |
| **Life-event navigator** | A customer planning a home purchase has fragmented questions. Kate detects the intent from a consented signal, gathers relevant facts, compares affordability scenarios, then proposes a next step for approval. | Change one mock income or property price; the options and reason change; customer approves a mock appointment or checklist item. | Detection, data fusion, simulation, decision, orchestration. |
| **Financial resilience planner** | A customer sees cash pressure too late. Kate spots a likely shortfall, simulates two responses with trade-offs, and tracks the selected plan. | Mock transactions trigger a forecast; compare two scenarios; save a mock alert and verify the projected balance. | Detection, simulation, decision, memory, verification. |
| **Kate answer assurance** | An answer may sound confident without enough support. A quality layer retrieves approved source material, checks the answer against it, marks uncertainty, and routes unresolved questions. | Ask one supported and one unsupported policy question; show source excerpts, a check result, and a human handoff for the second. | Retrieval/data fusion, control, system coordination. |
| **Onboarding case guide** | A new customer does not know which step is blocking progress. Kate assembles a case state from mock form and document data, explains missing evidence, and prepares an approved next action. | Submit an incomplete case; see the precise gap, the rule/source behind it, and a mock upload or review request. | Knowledge, orchestration, decision, verification. |
| **Document contradiction resolver** | Facts across documents disagree and cause rework. Kate extracts fields, models their relationships, flags contradictions, and routes only the uncertain case for review. | Two mock documents disagree on one field; show provenance, conflict, and a review task; resolve it and update case status. | Knowledge, data fusion, detection, coordination, verification. |
| **Scam interruption coach** | A customer under pressure may need guidance before a risky payment. Kate explains a suspicious pattern in plain language, prompts an independent check, and supports an approved escalation. | A mock payment narrative triggers an explanation and verification step; customer chooses a mock trusted-person review or pause. | Detection, context, decision, human coordination. |
| **Customer rule composer** | Customers repeat the same preferences and checks. Kate turns a plain-language goal into a transparent, editable rule with a test run and an approval gate. | Customer says “warn me if this bill rises”; show generated rule, simulated trigger, editable threshold, and a mock alert. | Programmability, memory, detection, control. |
| **Cross-service journey coordinator** | A multi-step goal spans banking, insurance, and outside services. Kate builds a plan, calls mock tools, tracks dependencies, and verifies completion after each approved step. | Select a home move; show a three-step plan, one mock tool result, a blocked dependency, and a revised next step. | Orchestration, system coordination, knowledge, verification. |

## Optional discussion prompts

These three invented briefs can be used to walk through the decision method without implementing a solution.

| Invented brief | What the team would discuss | Possible proof if a real brief called for it |
| --- | --- | --- |
| “Help customers decide what to do when they may buy a home.” | Tests intent, context, trade-offs, and an approved next action. | A scenario calculation whose output changes with an input. |
| “Make Kate's answers more trustworthy.” | Tests retrieval, source handling, uncertainty, and escalation. | One grounded answer and one explicit “insufficient evidence” result. |
| “Reduce customer onboarding delays caused by inconsistent documents.” | Tests extraction, a simple knowledge model, workflow, and review. | A contradiction detected across two mock records with provenance. |

For a discussion walkthrough, practise defining the user problem, one observable benefit, MVP cut line, and three demo steps. Do not prepare a challenge-specific dataset, API, or implementation from these prompts.

## Parking lot

Possible later variants: proactive life-event monitoring; adaptive plans that remember customer preferences; multi-agent coordination; a digital twin for cash-flow decisions; self-correcting workflows that check their own tool results. Promote a variant only when it solves a problem in the released brief and fits the available time.

The KBC track is confirmed; Kate 3.0 is a working hypothesis until the brief arrives. These notes help us understand the context, not choose a solution in advance.

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

Use [WORKFLOW_TEMPLATE.md](../WORKFLOW_TEMPLATE.md) as the fillable decision board once the brief arrives. The ideas above can prompt discussion if relevant, but none is a preselected solution.

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
| What are the three visible demo steps and the fallback for this MVP? | [ ] |

## Hackathon research note

A [study of 32 hackathon winners and five organizers](https://arxiv.org/html/2206.04744v1) found a recurring sequence: explore and define a real user problem, consider alternative solutions, then deliver a demonstrable prototype and clear pitch. The authors recommend checking rules, judging criteria, and existing solutions. These are interview findings, not a causal formula for winning. A separate [corporate hackathon case study](https://research.tue.nl/en/publications/utilizing-hackathons-to-foster-sustainable-product-innovation-the/) associated project continuation with focused preparation, a functioning prototype, current-customer fit, and ease of integration. Its outcome was continuation after the event, not a hackathon prize. The decision board applies these ideas to the team's four-hour working budget.
