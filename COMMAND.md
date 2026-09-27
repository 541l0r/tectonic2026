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

## Current preparation checklist

- [x] Local repository and baseline mock vertical slice
- [ ] Confirm access to `git@github.com:541l0r/tectonic2026.git` for each teammate
- [x] Publish the starter on `main`
- [ ] Each teammate clones, runs both services, and pushes their own branch
- [ ] Confirm challenge rules, allowed tools/data, presentation time, and submission format from the organizer
- [ ] Agree on Git ownership, backups, JSON/error conventions, and the integration check
- [ ] Review the trusted AI questions, acceptance-criteria template, and demo outline above
- [ ] Decide model/provider, data, architecture, and deployment only after the brief and event constraints are known
- [ ] Walk through [WORKFLOW_TEMPLATE.md](WORKFLOW_TEMPLATE.md) together without committing to an invented solution

## Day-of log

**Brief:** [Paste exact wording or link.]

**Chosen idea and reason:** [One sentence.]

**Current demo status:** [Working / blocked; link or command.]

**Next three actions:** 1. [owner + action] 2. [owner + action] 3. [owner + action]

**Risks and fallback:** [What could break; what fallback proves the chosen MVP's useful result.]

**Pitch (Diana):** [Problem → insight → working demo → measurable benefit.]
