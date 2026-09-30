# KBC Hackathon — Preparation Before Wednesday

## 1. Goal

We are **not preparing the solution before seeing the challenge**.

We are preparing the fastest possible way to go from:

**Challenge → MVP → Working Prototype → Integration → Testing → Live Demo**

Based on the information available about the Tectonic Hackathon, we should expect to **build and demonstrate a functional prototype**, not only describe a theoretical solution.

The goal of this preparation phase is therefore to remove avoidable friction before Wednesday so the 4-hour session can be spent mainly on:

**understanding → deciding → building → integrating → testing → presenting**

---

# 2. What We Prepare Now vs. Wednesday

## BEFORE WEDNESDAY

We can prepare:

- Team workflow and ownership
- GitHub structure and branch conventions
- Local development environments
- Tool documentation and use cases
- Generic technical skeletons with no business logic
- Challenge-decomposition framework
- Fast MVP-selection method
- Generic frontend / UX structure
- Backend/frontend integration conventions
- Error/fallback strategy
- Trusted AI checklist
- Testing structure
- Demo structure
- Pitch structure
- Flexible 4-hour timebox

## ONLY AFTER THE CHALLENGE IS REVEALED

We decide:

- Actual product idea
- Final MVP
- Database schema
- Final API contract
- Business rules
- AI architecture
- Prompts
- Agents / RAG / memory if needed
- Data model
- Challenge-specific security controls
- Final frontend content
- Final KPI

---

# 3. Definition of Success

Our target is NOT:

**A complete production-ready application**

Our target is:

**The smallest working prototype that proves the core idea and can be demonstrated clearly to the jury.**

The prototype should ideally show:

**Input → Processing → Result → Explanation → Action**

If AI is involved:

**Data → Deterministic Facts → AI Reasoning → Decision → Human Control**

---

# 4. Team Ownership

## Mathieu — Product / Scope / Coordination

### Before Wednesday

- [x] Prepare a lightweight ideation method ([opening method](IDEATION_METHOD.md) and [day-of decision board](WORKFLOW_TEMPLATE.md#2-brainstorm-and-turn-ideas-into-concepts)).
- [x] Prepare a fast MVP-selection method ([general rule](COMMAND.md#6-from-brief-to-mvp) and [day-of selection template](WORKFLOW_TEMPLATE.md#4-select-the-four-hour-proof-within-that-product-concept)).
- [x] Define Must / Should / Could / Won't criteria ([definitions, boundary test, and worked example](COMMAND.md#6-from-brief-to-mvp); [day-of fields](WORKFLOW_TEMPLATE.md#4-select-the-four-hour-proof-within-that-product-concept)).
- [x] Prepare a simple acceptance-criteria template ([method, worked example, and run sheet](ACCEPTANCE_CRITERIA.md)).
- [x] Prepare business-value / KPI questions ([KBC-track questions](COMMAND.md#6-from-brief-to-mvp) and [day-of KPI fields](WORKFLOW_TEMPLATE.md#3-choose-the-kbc-product-concept-and-outline-its-vision)).
- [x] Review how Prelint could support requirements/specification checking ([review and decision](PRELINT.md)); connect the eventual check to the acceptance criteria.
- [x] Prepare the product/business structure for the final pitch ([jury questions and business story](COMMAND.md#8-acceptance-and-jury-story); [day-of proof checks](WORKFLOW_TEMPLATE.md#6-final-proof)).
- [x] Define how we quickly decide which capabilities are relevant to the challenge ([scope and capability gate](COMMAND.md#6-from-brief-to-mvp); [MVP selection steps](WORKFLOW_TEMPLATE.md#4-select-the-four-hour-proof-within-that-product-concept)).

### During the Hackathon

Lead:

**Challenge → Product direction → Scope → MVP**

Then:

- Maintain scope discipline.
- Explore feature options and run targeted searches to answer questions raised by the real brief; share findings with the team.
- Define acceptance criteria.
- Prepare test scenarios.
- When integration or a scope change raises doubt, run the lightweight [product-alignment check](PRELINT.md#our-simpler-alignment-check) against the agreed Must-have acceptance criteria.
- Track integration status.
- Support frontend or backend coding on bounded tasks agreed with Diana or Damiens, including the files and interface to touch.
- Prepare business value and KPI.
- Support final pitch and Q&A.
- Prevent unnecessary feature expansion.

---

## Damiens — Technical Lead / Backend

### Before Wednesday

- [ ] Confirm local Python + Flask environment is ready.
- [ ] Prepare a minimal reusable Flask project skeleton with no business logic.
- [ ] Confirm JSON request/response handling.
- [ ] Prepare generic error handling.
- [ ] Prepare environment-variable handling.
- [ ] Understand the likely Google Cloud / AI integration workflow.
- [ ] Read relevant Aikido documentation.
- [ ] Prepare a basic technical fallback strategy.
- [ ] Document how to start the backend quickly.
- [ ] Be ready to define the final API contract with Diana once the MVP is known.

### During the Hackathon

Once the MVP is selected:

**MVP requirements**
↓
**Database/data structure**
↓
**API contract with frontend**
↓
**Backend implementation**
↓
**AI / tool integration**
↓
**Technical testing**

Own:

- Python / Flask backend
- Data processing
- Database/data structures if required
- API implementation
- AI/tool connections
- Technical integration
- Technical troubleshooting

The final database schema and business-specific API must NOT be designed before the real challenge is known.

---

## Diana — Preparation Coordination / Frontend / Demo

### Before Wednesday

- [ ] Maintain this preparation checklist and owners.
- [ ] Prepare challenge-decomposition framework.
- [ ] Prepare reusable frontend / UX skeleton.
- [ ] Prepare frontend data-needs template.
- [ ] Prepare a lightweight design system.
- [ ] Prepare demo-journey structure.
- [ ] Prepare pitch template.
- [ ] Prepare KBC Trusted AI checklist.
- [ ] Prepare flexible 4-hour timebox.
- [ ] Prepare likely jury-question categories.
- [ ] Understand how frontend will communicate with Flask through HTTP/JSON.

### During the Hackathon

Own:

**User journey**
↓
**Frontend**
↓
**Result presentation**
↓
**Explainability / human control**
↓
**Live demo**

Coordinate with Damiens on:

- API request
- API response
- Error states
- Loading states
- Required frontend fields

Prepare the presentation in parallel with development instead of waiting until the prototype is finished.

---

# 5. Challenge-Decomposition Framework

When the challenge appears, answer these questions quickly:

## Problem

What exactly are we solving?

## User

Who experiences the problem?

## Current Pain

What happens today?

## Data

What information is available?

## Constraints

What technical, business, regulatory or time constraints exist?

## Deterministic Logic

What can normal software establish reliably?

## AI Role

What genuinely requires AI interpretation or reasoning?

## Decision / Output

What does the system actually produce?

## Human Control

Which actions require confirmation or review?

## Action

What happens after the system produces a result?

## Customer Value

What becomes better for the user?

## KBC Value

Why should KBC care?

## KPI

How would success be measured?

---

# 6. Capability Selection

We do NOT automatically use every AI capability.

Once the challenge is known, select only what solves a real need.

Possible capabilities:

- Calculation & Simulation
- Data Representation & Knowledge
- Decision & Trade-offs
- Orchestration & Planning
- Data Fusion & Context
- Memory & Adaptation
- Detection & Proactivity
- Programmability & Composition
- System Coordination
- Control & Verification

Rule:

**Complexity must be earned by the problem.**

RAG, memory, agents, graphs, orchestration, voice, etc. are optional capabilities — not requirements.

---

# 7. Tool Strategy

We may have access to:

- Google Cloud
- Cursor
- Aikido Security
- Prelint
- ElevenLabs
- AI credits

We do NOT need to use all tools.

For every tool ask:

**Does this help solve the actual challenge or strengthen the prototype?**

---

## Google Cloud

Possible role:

- AI/model access
- Cloud services
- Hosting/deployment
- Data services

Before Wednesday:

Understand the likely integration path.

During the challenge:

Use only the services actually required.

---

## Cursor

Role:

**Development accelerator**

Possible uses:

- Generate boilerplate
- Refactor
- Debug
- Write tests
- Build repetitive components

Cursor supports development but is not itself part of the product value.

---

## Aikido Security

Role:

**Cross-cutting security layer**

Possible checks:

- Exposed secrets/API keys
- Vulnerable dependencies
- Code vulnerabilities
- Security issues

Typical workflow:

**Build → GitHub → Aikido scan → Fix critical findings → Demo**

Aikido does not solve the KBC business problem. It helps protect the solution we build.

---

## Prelint

Possible role:

Check whether implementation remains aligned with:

- Product requirements
- Business rules
- Architecture decisions
- Constraints

Especially useful if the challenge contains strict rules or compliance requirements.

Mathieu's [one-page Prelint review](PRELINT.md) explains its capabilities and why we do not plan to use it in our four-hour, no-PR workflow.

---

## ElevenLabs

Possible role:

- Voice interface
- Accessibility
- Spoken explanation
- Conversational interaction

Only use if voice genuinely improves the solution.

Do NOT add voice only because the tool is available.

---

# 8. Frontend / UX Skeleton

The frontend should be adaptable to different challenges.

Generic flow:

**INPUT**
↓
**ANALYSE**
↓
**DETECTED FACTS**
↓
**SYSTEM / AI ASSESSMENT**
↓
**CONFIDENCE / RISK**
↓
**WHY?**
↓
**RECOMMENDED ACTION**
↓
**HUMAN DECISION**

Possible reusable UI components:

- Input/upload area
- Analyse button
- Result card
- Fact/signal list
- Confidence indicator
- Risk/status badge
- Explanation box
- Recommended-action card
- Human-confirmation buttons
- Error/loading states

---

# 9. Frontend ↔ Backend Integration

The final API contract is decided Wednesday.

Beforehand we only agree on communication conventions:

**HTTP + JSON**

A possible generic frontend-needs template:

```json
{
  "facts": [],
  "result": "",
  "confidence": null,
  "explanation": [],
  "recommended_actions": [],
  "human_review_required": false,
  "error": null
}
```

This is NOT the final API.

It is only a reference for the discussion once the challenge is known.

---

# 10. KBC Trusted AI Checklist

If AI is materially involved, check:

## Data Protection & Privacy

Are we using only the data needed?

## Diversity & Fairness

Could the system create systematic unfairness or discrimination?

## Accountability

Can we understand what happened and who remains responsible?

## Safety & Security

Is the application and AI workflow protected against misuse or vulnerabilities?

## Transparency & Explainability

Can we explain the result to the user?

## Human Control

Does a human/customer remain in control of consequential actions?

---

# 11. MVP Gate

Before building, classify proposed **product features and requirements**, not teammate tasks. Mandatory brief and event constraints are Must-haves, not optional choices.

### MUST

Without this, the MVP promise fails or a mandatory constraint is missed.

### SHOULD

Important, but the main user journey still works without it.

### COULD

Only if the core prototype is already stable.

### WON'T

Explicitly excluded from this MVP.

Rule:

**No new feature after the integration deadline unless it replaces something else.**

---

# 12. Four-hour working rhythm

Confirm the actual deadline, pitch slot, and rules when the challenge is released. The opening has one handoff target: **about 40 minutes to reach the interface discussion**. Move sooner when the team is ready; resolve a material rule or data question before committing to a dependent build. The [opening method](IDEATION_METHOD.md) and [day-of guide](WORKFLOW_TEMPLATE.md) hold the detailed prompts.

## 00:00–00:10 — Understand

All three read the brief individually and each writes a one-sentence user problem. Compare the statements, agree on the user, pain, desired outcome, and mandatory constraints, and mark assumptions that need checking.

## 00:10–00:40 — Mathieu facilitates ideas to first proof

All three write short ideas on post-its, brainstorm freely without criticism, group duplicates while keeping distinct angles, and turn promising ideas into two or three concepts. Discuss them live and choose **one concept as the basis of the proposed future KBC product**. Describe how that complete product would be used and why it would matter. Then choose **one small journey or mechanism** the four-hour prototype can prove, with a sample input and visible result. Mathieu facilitates; Diana and Damiens contribute throughout. The steps inside these 30 minutes have no fixed quotas.

## From about 00:40 — Interface, then first code

Diana and Damiens agree on one request, success result, and failure result for the chosen proof. Begin the first UI → backend/tool → visible result path as soon as that example is clear. Mathieu records the product claim, first Must-have checks, and any unresolved assumption while supporting a bounded build task if needed. Complete the longer vision and worksheet fields as the build proceeds.

## Build and verify throughout

Connect the first working slice early, run its relevant scenario whenever parts join, and cut optional work when integration is at risk. Check the main journey, a relevant invalid or missing input, and the fallback for a selected service or tool. Track what is integrated and what is verified on the [day-of board](WORKFLOW_TEMPLATE.md#5-build-and-adapt).

## Protect the final demo window

About 45 minutes before the deadline, freeze optional features and verify the exact demo path and fallback. About 30 minutes before, rehearse the pitch, answer likely jury questions, and run the submission path. Use the remaining buffer for critical fixes and submission.

---

# 13. Demo Structure

The demo should prove the idea, not show every feature.

## 1. Problem

“Today, [USER] faces [PROBLEM].”

## 2. Input

Show real/synthetic challenge input.

## 3. System

Show what the system actually does.

## 4. Result

Show the core output.

## 5. Explainability

Show why the result was produced.

## 6. Human Control

Show where the user remains in control.

## 7. Value

Explain customer + KBC value.

---

# 14. Pitch Skeleton

## Opening

**“The problem is…”**

## User

**“Our user is…”**

## Solution

**“We built…”**

## Demo

**“Let me show you.”**

## Technical Principle

**“We use deterministic logic for \_\_\_ and AI for \_\_\_.”**

## Trust

**“Sensitive actions remain under human control.”**

## Value

**“For the customer…”**

**“For KBC…”**

## Measurement

**“We would measure success using…”**

## Closing

**“We turn \_\_\_ into \_\_\_.”**

---

# 15. Demo Fallback

A live demo must have a fallback.

Possible strategy:

**LIVE MODE**
Frontend → API → Backend → AI

If something fails:

**FALLBACK MODE**
Frontend → saved structured response → same user journey

The fallback should demonstrate the intended workflow without pretending that a failed integration is working.

---

# 16. Working Principle

We are not arriving with a pre-built answer.

We are arriving with:

- clear ownership
- prepared environments
- known tools
- reusable structures
- integration conventions
- a demo strategy
- a time strategy

So when the challenge appears, our energy goes into:

**solving the problem, not organizing ourselves.**

# 17. Operational readiness checklist

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
