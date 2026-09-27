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

- [ ] Prepare a lightweight ideation method.
- [ ] Prepare a fast MVP-selection method.
- [ ] Define Must / Should / Could / Won't criteria.
- [ ] Prepare a simple acceptance-criteria template.
- [ ] Prepare business-value / KPI questions.
- [ ] Review how Prelint could support requirements/specification checking.
- [ ] Prepare the product/business structure for the final pitch.
- [ ] Define how we quickly decide which capabilities are relevant to the challenge.

### During the Hackathon

Lead:

**Challenge → Product direction → Scope → MVP**

Then:

- Maintain scope discipline.
- Define acceptance criteria.
- Prepare test scenarios.
- Track integration status.
- Support coding when needed.
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

Before building, ask:

### MUST

Without this, there is no convincing prototype.

### SHOULD

Important, but the demo still works without it.

### COULD

Only if the core prototype is already stable.

### WON'T

Explicitly excluded from this MVP.

Rule:

**No new feature after the integration deadline unless it replaces something else.**

---

# 12. Flexible 4-Hour Timebox

## 00:00–00:10 — Understand

All three:

- Read challenge
- Identify user
- Identify problem
- Identify constraints

---

## 00:10–00:20 — Direction

Mathieu leads product/MVP direction.

Damiens checks:

- technical feasibility
- likely backend complexity

Diana checks:

- user journey
- frontend/demo feasibility

Goal:

**Choose one direction quickly.**

---

## 00:20–00:30 — Define Interfaces

Mathieu:

- Scope
- Acceptance criteria

Damiens:

- Data/backend needs

Diana + Damiens:

- Agree frontend/backend contract requirements

Goal:

**Start parallel work by \~30 minutes.**

---

## 00:30–02:30 — Parallel Build

### Mathieu

- Product
- Tests
- Business value
- Integration tracking
- Pitch content

### Damiens

- Backend
- Data
- API
- AI/tool integration

### Diana

- Frontend
- UX
- User journey
- Demo structure

---

## 02:30–03:05 — Integration

Connect:

**Frontend ↔ API ↔ Backend ↔ AI/tools**

Fix interface problems.

---

## 03:05–03:30 — Testing

Test:

- Normal case
- Edge case
- Failure case

Check:

- functionality
- security
- explainability
- human control

---

## 03:30–03:50 — Demo & Pitch Rehearsal

No new features unless critical.

Run the exact demo.

Prepare transitions and Q&A.

---

## 03:50–04:00 — Emergency Buffer

Only:

- critical bug fixes
- deployment issues
- demo fallback
- submission

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
