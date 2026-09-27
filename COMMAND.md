# Tectonic — team command sheet

Updated: 27 September 2026. This is the team working agreement. The challenge, data, API contract, architecture, and product scope are decided after the real brief arrives.

## Goal and working rule

We arrive knowing how to build together within the four-hour working window. We do not arrive with a chosen solution, database schema, dataset, API contract, or architecture. The existing UI and API are only a generic connectivity check. Once we know the brief, all three choose the smallest useful MVP that solves one concrete user problem and produces a visible result.

**One sentence pitch:** [Fill in when the challenge is announced.]

**User / pain / measurable result:** [Fill in.]

**Demo path (three steps):** 1. [input] 2. [intelligence] 3. [visible result]

**Cut line:** [The smallest useful result we can demonstrate for the actual challenge.]

**Essential for this brief:** [Agree together after reading the challenge.]

**Optional if time remains:** [Agree together.]

**Whole-demo acceptance criteria and scenarios:** [Mathieu drafts these while the team builds; all three review them. Include the happy path, missing evidence or tool failure, and the fallback.]

## Owners and interfaces

| Owner | Responsibility | First deliverable |
| --- | --- | --- |
| Mathieu | Facilitate the first ideation discussion, watch the clock, bring useful methods and the global view, draft whole-demo acceptance criteria and scenarios, and coordinate integration | Run a brief check-in every 25 minutes; record the shared MVP decision and the next integration check |
| Diana | Frontend, live demo, pitch story, and lead for shared documents and repository coordination | Keep the shared docs and `main` coherent; agree on the MVP interface with Damiens |
| Damiens | Backend and integration architecture after MVP selection | Agree with Diana on the challenge-specific interface; keep the backend runnable |

Use one owner per area. Anyone can propose a change; the API owner confirms contract changes before the frontend and backend branches diverge.

All three decide the MVP and what is essential versus optional. Keep discussions open and respectful; a check-in should surface concerns and help the team make the next decision, not turn into a status ceremony.

If someone finishes early, they help with the current blocker, integration, testing, or the demo. Agree on the backup for each critical task at the first check-in. Diana leads the shared documents and repository while working remotely; branch ownership and merges are coordinated through GitHub.

## Four-hour working plan

Use this as a flexible budget from the moment the challenge is released. Confirm the actual deadline, pitch slot, and rules first. Mathieu facilitates a short check-in about every 25 minutes; the team changes the plan together when needed.

| Time | Team action | Exit check |
| --- | --- | --- |
| 0–20 min | Read the brief; identify problem, user, data, constraints, AI role, decision or action, value, and judging criteria. Ask for clarification where needed. | Everyone can state the same problem. |
| 20–40 min | Generate a few options; all three select the smallest useful MVP and mark essential versus optional. | One user journey, success criterion, cut line, and demo path. |
| 40–60 min | Diana and Damiens agree on the interface and a sample JSON exchange for this MVP. Choose the simplest architecture and integration boundary. | Both can build independently against the same example. |
| 60–150 min | Build the smallest end-to-end path, integrate early, and cut optional work when needed. Mathieu drafts whole-demo checks. | A visible UI → backend → result path runs. |
| 150–195 min | Run acceptance scenarios, fix integration issues, and check the fallback. | The main demo path and one failure path work. |
| 195–240 min | Freeze features, rehearse Diana's pitch, answer likely jury questions, and submit. | The exact demo and submission path have been run. |

The timeboxes are prompts to make decisions, not deadlines for perfect code. Keep a protected final buffer for testing and the demo.

## Technical preparation and integration

Before the event, each person makes the current generic starter run locally. The existing `/api/ask` route and mock response prove only that a React frontend can call a Flask backend. They are not the future product contract. A fallback may be a fixed response matching the **chosen** MVP's interface, created after the brief so frontend and backend can work independently.

Agree on a few conventions now: JSON over HTTP for the local UI/backend boundary; one concrete request and response example after MVP selection; explicit errors and loading states; names that match the chosen domain; server-side credentials in local `.env` only; and a short integration check after every merge. Keep `.env.example` to variable names and placeholders.

Choose tools from the actual need and event permissions. Retrieval, calculation, model calls, or external APIs are options, not a preparation checklist to implement. For each selected tool, record its input, output, failure behavior, and what the demo will show. Never put API keys in the browser or commit them.

## Testing, trusted AI, and demo

Mathieu drafts whole-demo acceptance criteria as the team builds; all three review and run them. Test the main user journey, invalid or missing input, a tool/model failure if applicable, and the fallback. Check what evidence supports each important claim in the demo.

Before showing anything as trusted AI, ask: Are we using allowed data? Are claims grounded or clearly uncertain? Are consequential actions approved by the user? Are secrets kept private? Can a person review or stop the action? Does the system show what happened when a tool fails? Apply the checks that fit the released challenge.

Diana's pitch follows **problem → why this approach → live three-step demo → user value → limitation or next step**. Prepare short answers to likely jury questions: why this problem, what is new, where the data came from, what works live, how safety is handled, and what would be needed in production.

## Repository workflow

```text
main             always demoable
feat/frontend    Diana's UI changes
feat/backend     API and data changes
feat/product     Mathieu's acceptance checks or discussion notes
feat/pitch       Diana's pitch story
```

We will not use pull requests. Each owner pulls the latest `main`, works on their own branch, makes small commits, and pushes that branch. Diana coordinates repository changes and names the integrator for each merge. The integrator merges one branch at a time into `main` locally, runs the full demo check, then pushes `main`. Everyone pulls `main` again after a merge. Avoid simultaneous edits to the same file and do not force-push shared branches.

```bash
git switch main
git pull --ff-only origin main
git switch -c feat/my-task              # first time only
# edit, then git add and git commit
git push -u origin feat/my-task

# integrator, after checking the branch
git switch main
git pull --ff-only origin main
git fetch origin
git merge --no-ff origin/feat/my-task
# run the full demo check
git push origin main
```

Put decisions and current blockers here, not across chat threads. Give coding agents one bounded task, exact files, expected behavior, and a verification command. Integrate their output yourself.

Before the event: each person clones the shared remote, runs both services, sends a request, opens the UI, and proves Git push access by pushing their own branch. Keep `.env` private and use `.env.example` for names only.

+The KBC track is confirmed; Kate 3.0 is a working hypothesis until the brief arrives. These notes help us understand the context, not choose a solution in advance.

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
| What are the three visible demo steps and the fallback for this MVP? | [ ] |

## Hackathon research note

A [study of 32 hackathon winners and five organizers](https://arxiv.org/html/2206.04744v1) found a recurring sequence: explore and define a real user problem, consider alternative solutions, then deliver a demonstrable prototype and clear pitch. The authors recommend checking rules, judging criteria, and existing solutions. These are interview findings, not a causal formula for winning. A separate [corporate hackathon case study](https://research.tue.nl/en/publications/utilizing-hackathons-to-foster-sustainable-product-innovation-the/) associated project continuation with focused preparation, a functioning prototype, current-customer fit, and ease of integration. Its outcome was continuation after the event, not a hackathon prize. The decision board applies these ideas to the team's four-hour working budget.


## Current preparation checklist

- [x] Local repository and baseline mock vertical slice
- [ ] Confirm access to `git@github.com:541l0r/tectonic2026.git` for each teammate
- [x] Publish the starter on `main`
- [ ] Each teammate clones, runs both services, and pushes their own branch
- [ ] Confirm challenge rules, allowed tools/data, presentation time, and submission format from the organizer
- [ ] Confirm registration, location, schedule, and case-release process with the organizer
- [ ] Agree on Git ownership, backups, JSON/error conventions, and the integration check
- [ ] Diana and Damiens agree on generic interface conventions while leaving the MVP contract open
- [ ] Review the trusted AI questions, acceptance-criteria template, and demo outline above
- [ ] Diana prepares a reusable three-step demo and pitch outline
- [ ] Decide model/provider, data, architecture, and deployment only after the brief and event constraints are known
- [ ] All three walk through [WORKFLOW_TEMPLATE.md](WORKFLOW_TEMPLATE.md) together without committing to an invented solution

## Day-of log

**Brief:** [Paste exact wording or link.]

**Chosen idea and reason:** [One sentence.]

**Current demo status:** [Working / blocked; link or command.]

**Next three actions:** 1. [owner + action] 2. [owner + action] 3. [owner + action]

**Risks and fallback:** [What could break; what fallback proves the chosen MVP's useful result.]

**Pitch (Diana):** [Problem → insight → working demo → measurable benefit.]
