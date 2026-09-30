# Tectonic — team method (working draft)

Updated: 28 September 2026. This is the method Mathieu can explain to the team before the challenge. The separate [day-of guide](WORKFLOW_TEMPLATE.md) is filled in together as the work progresses. Both are working drafts for now. The challenge, data, API contract, architecture, and product scope are decided after the real brief arrives.

## 1. Purpose and shared rules

We arrive knowing how to build together within the four-hour working window. We do not arrive with a chosen solution, database schema, dataset, API contract, or architecture. The existing UI and API are only a generic connectivity check. Once we know the brief, all three choose a proposed KBC product concept, then a small working proof of one important part of it.

Our method is **brief → understand the user problem → generate ideas → turn promising ideas into concepts → choose the concept for a proposed future KBC product → choose one small four-hour proof → build, check, and demo that proof**. We can revisit an earlier decision when new evidence or time pressure requires it. [WORKFLOW_TEMPLATE.md](WORKFLOW_TEMPLATE.md) is the fillable board for the event; this sheet explains how to use it.

## 2. Shared vocabulary

| Term | Meaning for this hackathon |
| --- | --- |
| Challenge brief | The organizer's actual request, rules, and judging criteria. It takes precedence over our preparation ideas. |
| User | The specific person whose situation we want to improve. |
| Useful outcome | What that user can understand, decide, or accomplish with the solution. |
| Idea | A rough spark on a post-it. It can be a word, a feature, or a possible approach; it need not be complete or feasible yet. |
| Concept | A promising idea or combination of ideas made clear enough to discuss: user, desired outcome, and main approach. Two or three concepts reach the assessment step. |
| User journey | The few steps from the user's starting situation to that useful outcome; the demo should make this journey visible. |
| Selected KBC product concept and vision | The concept we propose as the basis of a future KBC product, plus the fuller experience it could become: who uses it, what differs from today, and the value it could create. Selection is a proposal for the challenge, not a claim that KBC has approved or built it. |
| Four-hour proof of concept (hackathon MVP) | A small working prototype of one important journey or mechanism from the selected product concept. It demonstrates a claim about the proposed product; it is not the complete future KBC product. |
| Product scope | What our hackathon product actually lets the user do, the constraints it respects, and what it excludes. A list of screens alone does not define it. |
| Build tasks | The activities assigned to teammates to create and check the product, such as building a screen, connecting an API, or running a scenario. These are actions by us, not capabilities for the user. |
| Feature | A capability we might build. It is Must-have only if the MVP promise or journey fails without it. |
| Must / Should / Could / Won't | A way to sort proposed product features and requirements, not teammate tasks. Must: necessary for the MVP promise or required by the brief. Should: important but the main journey can work without it. Could: optional improvement. Won't: explicitly outside this MVP. Mandatory event rules are always Must. |
| Cut line | The boundary between capabilities the hackathon product needs and optional capabilities we can drop when time is short. |
| Vertical slice | A small but complete part of the journey, from UI action through the necessary backend or tool to a visible result. |
| Interface contract | The agreed example request, response, and error behaviour that lets Diana and Damiens connect their work. The actual contract is chosen after the MVP. |
| Acceptance criterion | An observable condition agreed for a feature or for the whole hackathon product. Feature checks feed the product decision; the complete journey and mandatory constraints also need their own checks. |
| Test scenario | A concrete input, action, and expected result used to check an acceptance criterion, including a relevant failure case. |
| Integration | The frontend, backend, and any selected tool working together to produce the visible result. Start it early. |
| Fallback | The agreed, honest demo path if a selected service or tool fails. Define it for the actual MVP, not before the brief. |
| Done / Integrated / Verified | Done: the owner has completed a task. Integrated: it works with the other parts. Verified: its relevant feature criteria pass on the current build. |
| Product accepted for demo | All three have seen the Must-have feature checks and whole-product scenarios pass on the current integrated build, or have jointly narrowed the promise and updated the criteria and pitch. |
| Demo claim | The specific part of the vision we can show working now, with a clear distinction between live, simulated, and future capabilities. |

## 3. Roles and decisions

| Owner | Responsibility | First deliverable |
| --- | --- | --- |
| Mathieu | Facilitate ideation and scope discussions; explore feature options and research questions from the brief; track time and integration; draft feature and whole-product acceptance criteria; support frontend or backend coding on agreed, bounded tasks | Bring evidence and options to the shared MVP decision; record the next integration check and help with the current build blocker |
| Diana | Frontend, live demo, pitch story, KBC Trusted AI review, and lead for shared documents and repository coordination | Keep the shared docs and `main` coherent; bring the trust checklist into MVP and interface decisions with Damiens |
| Damiens | Backend and integration architecture after MVP selection | Agree with Diana on the challenge-specific interface; keep the backend runnable |

Use one owner per area. Anyone can propose a change. Diana and Damiens agree on any request, response, or error change before their frontend and backend branches diverge. Mathieu can implement a frontend or backend slice after agreeing on the task, files, and interface with the relevant owner; Diana and Damiens keep ownership of their areas.

All three decide the MVP and what is essential versus optional. Keep discussions open and respectful; a check-in should surface concerns and help the team make the next decision, not turn into a status ceremony.

If someone finishes early, they help with the current blocker, integration, testing, or the demo. Agree on the backup for each critical task at the first check-in. Diana leads the shared documents and repository while working remotely; branch ownership and merges are coordinated through GitHub.

## 4. Git and communication

```text
main             always demoable
feat/frontend    Diana's UI changes
feat/backend     API and data changes
feat/product     Mathieu's acceptance checks or discussion notes
feat/pitch       Diana's pitch story
```

We will not use pull requests. Each owner pulls the latest `main`, works on their own branch, makes small commits, and pushes that branch. Diana coordinates repository changes and names the integrator for each merge. The integrator merges one branch at a time into `main` locally, runs the full demo check, then pushes `main`. Everyone pulls `main` again after a merge. Avoid simultaneous edits to the same file and do not force-push shared branches.

When Mathieu helps with frontend or backend code, agree with Diana or Damiens on the branch and exact files first. The area owner reviews the result before integration, so support work does not create competing edits.

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

Record decisions and current blockers in the [day-of guide](WORKFLOW_TEMPLATE.md), so remote teammates see the same plan. Give coding agents one bounded task, exact files, expected behavior, and a verification command. Review and integrate their output yourself.

Before the event: each person clones the shared remote, runs both services, sends a request, opens the UI, and proves Git push access by pushing their own branch. Keep `.env` private and use `.env.example` for names only.

## 5. Technical working flow

Before the event, each person makes the current generic starter run locally. The existing `/api/ask` route and mock response prove only that a React frontend can call a Flask backend. They are not the future product contract. A fallback may be a fixed response matching the **chosen** MVP's interface, created after the brief so frontend and backend can work independently.

Agree on a few conventions now: JSON over HTTP for the local UI/backend boundary; one concrete request and response example after MVP selection; explicit errors and loading states; names that match the chosen domain; server-side credentials in local `.env` only; and a short integration check after every merge. Keep `.env.example` to variable names and placeholders.

Choose tools from the actual need and event permissions. Retrieval, calculation, model calls, or external APIs are options, not a preparation checklist to implement. For each selected tool, record its input, output, failure behavior, and what the demo will show. Never put API keys in the browser or commit them.

After choosing the MVP, work through this small technical loop:

1. Diana and Damiens write one example request, success response, and failure response for the chosen journey. They agree on who changes the interface if the example must change.
2. Each builds against that same example. A temporary mock can let the UI or backend advance independently; label it and replace or explicitly retain it for the demo.
3. Connect the first UI → backend → visible result path early. Check the actual request and response, loading and error states, and the selected tool's failure behaviour.
4. After each merge, run the journey again on `main`. If the interface or scope changes, tell the other owner and update the example and acceptance checks before continuing.

Diana brings the [working KBC Trusted AI checklist](PREPARATION.md#10-kbc-trusted-ai-checklist) into the interface discussion. For the selected MVP, decide what the UI must show about sources, uncertainty, consent or approval, and failures; Damiens checks what the backend can support. Treat any trust or data rule in the released brief as mandatory. The preparation checklist is a prompt, not a claim that we have the official KBC policy.

## 6. From brief to MVP

1. **Understand before choosing:** Read the exact brief, rules, judging criteria, available data, and constraints, including any KBC Trusted AI requirements. Diana highlights relevant trust questions. State the user and problem in one sentence. Mark facts and assumptions separately.
2. **Explore and form concepts:** Generate any number of rough ideas, group and combine them, then turn two or three promising directions into clear concepts. Assess those concepts against the brief, customer value, KBC fit, and whether one useful part can be proved in the event.
3. **Choose and describe the proposed KBC product:** Select one concept as the basis of the future product. Before choosing a prototype, describe who would use the complete product, the future experience, its distinctive mechanism, customer and KBC value, and the main data and trust dependencies. Mark unknowns. This is the product we propose, not a claim that it is built.
4. **Choose the four-hour proof:** Select one MVP journey that demonstrates the most important part of that vision. Write its promise and **cut line**: Must-have capabilities above it; optional improvements and explicit exclusions below it. If removing a feature does not break the MVP promise, it is not a Must-have.
5. **Split vertically:** Build the smallest end-to-end slice that shows the journey: UI input → backend or selected tool → visible result. Diana and Damiens agree on one example request and response so they can work in parallel and connect their parts early. Keep a challenge-specific fallback if an external dependency fails.
6. **Agree on proof:** Mathieu drafts checks for each Must-have feature and for the complete product journey; all three review them before the build goes far. The [acceptance-criteria guide](ACCEPTANCE_CRITERIA.md) explains the two levels and provides a run sheet. Criteria are agreed early; the product is accepted for the demo only after the feature and whole-product checks pass on the current integrated build.

**Quick ideation:** Run the [opening ideation method](IDEATION_METHOD.md): agree on the problem, start with silent writing, brainstorm as many short ideas as possible together, group duplicates while preserving distinct angles, develop two or three concepts, then assess them. Choose one concept as the basis of the proposed KBC product. Use the [innovation lenses](IDEAS.md#ten-innovation-lenses) only if the group needs a prompt.

**Choose the product concept after ideation:** Reject a concept that misses the brief or relies on forbidden data. Compare the others on user value, a distinctive capability, KBC fit, and whether a useful part can be demonstrated in time. Record the reason and key uncertainty; the three of us decide together, using the actual judging criteria when available.

**Select the four-hour proof within that product:** Identify a possible end-to-end journey for the chosen product vision and compare alternatives only if the scope is disputed or unclear. Choose the smallest journey that proves its central claim with available data, a visible result, and a feasible integration path. Define its promise and Must-have features; place everything else below the cut line. All three agree on what the prototype will actually do and what its demo can honestly claim.

**Scope and capability gate:** Mark each proposed feature or requirement Must, Should, Could, or Won't. A Must is needed for the promised journey or a mandatory rule; the others stay below the cut line. For any proposed AI or technical capability, ask: Which user step needs it? What input can we actually use? What result will we demonstrate? What happens when it fails? If the answer is unclear, leave it out of the four-hour product.

**Practice example — document-status assistant:** Suppose our chosen MVP promise were “a customer can check a sample application and understand which document is missing, or see that its status cannot be verified.” This is fictional; it is not a choice for the real challenge. It matches the [worked acceptance-criteria example](ACCEPTANCE_CRITERIA.md#worked-example--fictional-document-status-brief).

| Priority | Proposed product capability | Why it belongs here |
| --- | --- | --- |
| **Must** | Compare the sample application's required and received documents; show the missing document and a clear next step. Show an honest unavailable state if the check fails. | Without these, the promised journey gives no reliable answer. Any mandatory brief or event rule is also Must. |
| **Should** | Explain which requirement makes that document necessary. | Helpful for trust and understanding, but the customer can still see what is missing and what to do next. If the real brief requires this explanation, move it to Must. |
| **Could** | Let the customer upload the document from the same screen. | Convenient, but it does not improve the core proof enough to justify building it before the journey works. |
| **Won't** | Fetch real customer records or submit a live application. | Outside the fictional four-hour MVP; the demo uses invented records and makes no live action. |

To test the **Must / Should boundary**, remove the capability and ask whether the agreed promise or a mandatory constraint now fails. If yes, it is Must. If the promise still works but the experience is materially better with it, it is Should. Recheck the boundary together after reading the real brief; do not promote a feature to Must just because it is impressive or technically interesting.

**Business value and KPI questions for the KBC track:** KBC describes Kate and KBC Mobile in terms of making banking and insurance easier, saving customers time and money, helping with complex decisions, and directing complex cases to colleagues. These are [public context](https://newsroom.kbc.com/kate-five-years-and-five-milestones), not the hidden challenge or its judging criteria. After reading the brief, ask:

1. Which KBC customer or employee is affected, and what do they do today in Kate, KBC Mobile, KBC Live, a branch, or another relevant channel? Do not assume the challenge concerns Kate.
2. What concrete friction improves: time to a useful answer or action, completion, accuracy, avoidable rework, timely intervention, or quality of human handoff? What does KBC already offer, and what changes beyond it?
3. What is the customer benefit **and** the KBC benefit? Could it improve service quality, free colleagues for complex work, reduce preventable risk, or strengthen a relevant customer relationship? Do not claim financial return without evidence.
4. If KBC tested the future product, which **one primary outcome KPI** would show that the user is better off? Define the population, event counted, denominator, and time period; ask whether a current baseline exists. Choose a safety or quality guardrail if optimizing the primary KPI could cause harm.
5. What can the four-hour MVP actually demonstrate as a **proxy** for that outcome? Name the sample input, observable result, and limitation. Keep the demo proof separate from any unmeasured real-world KPI.

This is a short design-and-build cycle, not a formal Scrum sprint. We borrow the useful habits of shared decisions, visible work, early integration, and adapting to evidence. We do not assign Scrum titles or run its formal events.

## 7. Work rhythm and checkpoints

Confirm the actual deadline, pitch slot, and rules first. Use **00:00–00:10 to understand** the brief and agree on the problem. Give Mathieu **00:10–00:40 to facilitate** ideas, concepts, the proposed KBC product, and its first small proof. Diana and Damiens then agree on the immediate request/result example and start coding. The 40-minute interface handoff is a target, not a researched optimum; move earlier when ready or adjust for a material rule in the brief. Mathieu facilitates short check-ins during the build.

| Stage | Team action | Exit check |
| --- | --- | --- |
| 00:00–00:10 — Understand | Read the brief individually; each writes a problem statement, then compare and agree on the shared problem and mandatory constraints. | Everyone can state the same problem. |
| 00:10–00:40 — Mathieu facilitates | Write short ideas independently, brainstorm without a quota, group distinct angles, develop two or three concepts, choose and outline the proposed KBC product, then choose its first small proof. | A coherent product concept and one proof journey with a sample input and visible result; ready to define the interface. |
| From about 00:40 — Define the immediate interface | Diana and Damiens agree on one request, success result, and failure result for that proof. | Both can start their first coding task against the same example. |
| Build and integrate | Connect the smallest UI → backend/tool → visible result path early. Run relevant scenarios as parts connect; cut optional work when needed. | The central proof works on the integrated build. |
| Verify and submit | Protect time to check Must-have features, the complete journey, failure path, pitch, and actual submission. Freeze optional work before this buffer. | The exact demo and submission path have been run. |

Keep a protected final buffer for testing and the demo. If a discussion stalls, state the unresolved question and choose the smallest reversible next step; do not let the worksheet delay a working slice.

Keep one small shared task board in the [day-of guide](WORKFLOW_TEMPLATE.md): **To do → In progress → Integrated → Verified**. A task is integrated when it works with the other parts; it is verified when its relevant scenario passes. Give each active task one owner and a visible "done when" condition. Limit work in progress so the team finishes the main journey before adding features.

At each short check-in, ask: **What works now? What is blocked? What is the next smallest visible improvement?** Mathieu watches the time and records the next decision; the team makes scope changes together. If a blocker persists for about 15 minutes, agree on a simpler path or the MVP-specific fallback rather than letting integration wait. Update the criteria and pitch when the MVP promise changes.

## 8. Acceptance and jury story

Mathieu drafts feature and whole-product acceptance criteria after MVP selection; all three review and run them. Check each Must-have feature, then the main user journey, invalid or missing input, a tool/model failure if applicable, and the fallback. Check what evidence supports each important claim in the demo. Use the [run sheet](ACCEPTANCE_CRITERIA.md#run-sheet--copy-after-the-brief) to record the actual result and the owner of a fix.

Use Diana's [working KBC Trusted AI checklist](PREPARATION.md#10-kbc-trusted-ai-checklist) when choosing the MVP, agreeing on the interface, writing acceptance criteria, and rehearsing the pitch. Ask: Are we using allowed and necessary data? Are claims grounded or clearly uncertain? Could the result create unfairness? Are consequential actions approved by the user? Can a person review or stop the action? Are secrets protected and failures visible? Turn relevant answers into feature or whole-product checks. Apply any official KBC or event rules supplied with the brief first.

Diana's pitch should answer three jury questions in plain language:

| Question | What we need to make clear |
| --- | --- |
| **What could this become at KBC?** | The user, their problem, the future experience, customer and KBC value, and what real deployment would require. |
| **Where is the innovation?** | The specific capability or mechanism that changes the outcome compared with today's approach, not merely the presence of AI. |
| **What did we prove in four hours?** | One live, end-to-end journey with a visible result and the agreed acceptance checks. Say which inputs, tools, or actions are simulated and which limits remain. |

Lead with the **user problem and solution vision**. Use the four-hour MVP as a focused proof that one important mechanism or journey can work, then explain what would be needed to expand it. State clearly what is live, what is simulated, and what is future work. The time limit is the event format; we do not assume that implementation speed itself is a judging criterion. Adapt the balance of vision, demonstration, and technical detail to the actual brief, jury instructions, and pitch time when announced.

Mathieu prepares the business spine for Diana's pitch: **user and current pain → future KBC product → innovation → live proof → customer and KBC value with a possible KPI → limitation and next step**. Diana shapes and delivers the story. “It works” means the demonstrated slice passes its agreed checks on the current build; it does not mean the full future product is production-ready. Prepare short answers on why this problem, where the data came from, how safety and customer control work, and what would be needed to deploy it.

Background research and idea prompts: [IDEAS.md](IDEAS.md). Before-event tasks: [PREPARATION.md](PREPARATION.md). Fill the live decisions and statuses in [WORKFLOW_TEMPLATE.md](WORKFLOW_TEMPLATE.md).
