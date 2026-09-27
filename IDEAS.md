# Global view — Kate 3.0 rehearsal ideas

Working hypotheses for the KBC track, 27 September 2026. The challenge is still hidden. These are discussion prompts, not predictions, selected solutions, or tasks to build before the event. Use the actual brief and judging criteria to choose or discard them. [COMMAND.md](COMMAND.md) records Diana's KBC sources and the ten innovation lenses; [WORKFLOW_TEMPLATE.md](WORKFLOW_TEMPLATE.md) is the day-of decision board.

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
