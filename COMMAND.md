# Tectonic — team command sheet

Updated: 27 September 2026. This is the single working document for preparation and the event. Replace assumptions when the actual brief arrives.

## Goal and working rule

When the brief arrives, the three of us choose the smallest useful MVP together. It should solve one concrete user problem, show a meaningful capability beyond a single answer, and produce a visible result. Start with one end-to-end slice and deepen it only if time allows. The current mock banking assistant is a test bed; the challenge brief determines the product.

**One sentence pitch:** [Fill in when the challenge is announced.]

**User / pain / measurable result:** [Fill in.]

**Demo path (three steps):** 1. [input] 2. [intelligence] 3. [visible result]

**Cut line:** The demo still works with mock data and a deterministic response. A live model, real banking data, voice, and advanced hosting are optional integrations.

**Essential for this brief:** [Agree together after reading the challenge.]

**Optional if time remains:** [Agree together.]

**Whole-demo acceptance criteria and scenarios:** [Mathieu drafts these while the team builds; all three review them. Include the happy path, missing evidence or tool failure, and the fallback.]

## Owners and interfaces

| Owner | Responsibility | First deliverable |
| --- | --- | --- |
| Mathieu | Facilitate the first ideation discussion, watch the clock, bring useful methods and the global view, draft whole-demo acceptance criteria and scenarios, and coordinate integration | Run a brief check-in every 25 minutes; record the shared MVP decision and the next integration check |
| Diana | Frontend, live demo, and pitch story | Render the semantic response blocks; write and rehearse the pitch |
| Damiens | Backend API and integration architecture | Keep `/api/ask` contract stable and provide a working mock response |

Use one owner per area. Anyone can propose a change; the API owner confirms contract changes before the frontend and backend branches diverge.

All three decide the MVP and what is essential versus optional. Keep discussions open and respectful; a check-in should surface concerns and help the team make the next decision, not turn into a status ceremony.

## First 75 minutes after the brief

| Time | Team action | Exit check |
| --- | --- | --- |
| 0–15 min | Read the brief and judging criteria. Define one user, problem, and existing KBC process to improve. Mathieu facilitates and tracks time. | Everyone can repeat the same goal. |
| 15–30 min | Generate at most three ideas with [WORKFLOW_TEMPLATE.md](WORKFLOW_TEMPLATE.md); all three choose the smallest useful MVP. Diana writes the pitch and three-step demo path. | Shared choice, essentials, optional work, cut line, and fallback are recorded. |
| 30–40 min | Damiens and Diana agree on request/response JSON. Pick a mock dataset and one useful tool. | One sample request and response committed. |
| 40–55 min | Build independently against that contract. Diana prepares a 90-second narrative; Mathieu drafts whole-demo acceptance criteria and test scenarios. | UI and API each run locally; the demo checks are written down. |
| 55–75 min | Connect UI to API; run the full demo once. | A working vertical slice on `main`. |

After that: make a quick team check-in every 25 minutes, improve the core idea, deploy when stable, rehearse, then keep a final buffer. The team cuts optional work when integration slips.

## Interface contract v0

`POST /api/ask` with `{"message":"What changed in my spending?","user_id":"demo"}` returns:

```json
{
  "answer": "Your spending is up in groceries this month.",
  "blocks": [
    {"type":"metric","label":"Groceries","value":"€420","detail":"+€60 vs previous month"},
    {"type":"list","title":"Possible next steps","items":["Review recent grocery purchases","Set a monthly alert"]}
  ],
  "source": "mock"
}
```

`blocks` is a small semantic UI vocabulary: `text`, `metric`, and `list`. Add a new type only with a sample JSON response and a UI renderer. The server validates input; the UI treats all response text as untrusted. This v0 contract only proves the UI/API connection; it is not the intended final assistant design. Never put API keys in the browser or commit them.

### Interface v1 preparation to-do

Use an invented brief and mock data for these tasks. Adapt the data and tools when the real challenge is announced.

| Area | Preparation task | Done when |
| --- | --- | --- |
| Context | Decide what one request carries: current message, session ID, recent turns, and any allowed user or task context. Define a reset and a size limit. | Two related questions work in sequence, and a reset removes prior context. |
| Tools | Define a small tool registry with typed inputs and outputs, permissions, timeouts, and failure responses. Implement one read-only mock tool. | A request can call the tool, show what it used, and recover from a tool error. |
| RAG | Build a tiny local document set and retrieval path: chunk, index, search, and return source IDs or excerpts. | The assistant answers a document question with a source reference and says when the documents do not support an answer. |
| Response contract | Agree on a v1 JSON example for answer, UI blocks, source references, tool activity, and errors. Keep the same shape for mock and model-backed responses. | Frontend and backend can work independently from the same examples. |
| Orchestration | Decide when to use conversation context, retrieval, or a tool. Keep a deterministic mock path so the demo works without a model or network. | One end-to-end example uses context, one uses retrieval, and one uses a tool. |
| Evaluation | Prepare a small set of checks for follow-up questions, grounded answers, tool failure, missing evidence, and invalid input. | The team can run the same checks after each integration. |

Confirm the event's rules and available data before connecting any real service or changing the v1 examples to fit the challenge.

## Repository workflow

```text
main             always demoable
feat/frontend    Diana's UI changes
feat/backend     API and data changes
feat/product     Mathieu's scope or orchestration notes
feat/pitch       Diana's pitch story
```

We will not use pull requests. Each owner pulls the latest `main`, works on their own branch, makes small commits, and pushes that branch. Mathieu (or a named integrator) merges one branch at a time into `main` locally, runs the full demo check, then pushes `main`. Everyone pulls `main` again after a merge. Avoid simultaneous edits to the same file and do not force-push shared branches.

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

## Current preparation checklist

- [x] Local repository and baseline mock vertical slice
- [ ] Confirm access to `git@github.com:541l0r/tectonic2026.git` for each teammate
- [x] Publish the starter on `main`
- [ ] Each teammate clones, runs both services, and pushes their own branch
- [ ] Confirm challenge rules, allowed tools/data, presentation time, and submission format from the organizer
- [ ] Complete the interface v1 preparation tasks above with mock data
- [ ] Choose model/provider and deployment only after available credentials and event constraints are known
- [ ] Practice a timed 75-minute trial with one invented prompt from [IDEAS.md](IDEAS.md)

## Day-of log

**Brief:** [Paste exact wording or link.]

**Chosen idea and reason:** [One sentence.]

**Current demo status:** [Working / blocked; link or command.]

**Next three actions:** 1. [owner + action] 2. [owner + action] 3. [owner + action]

**Risks and fallback:** [What could break; how the mock slice still demonstrates the idea.]

**Pitch (Diana):** [Problem → insight → working demo → measurable benefit.]
