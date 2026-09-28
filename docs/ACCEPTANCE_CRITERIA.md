# Acceptance criteria — first draft

*Preparation guide for Mathieu and the team. Fill in the actual criteria only after the challenge and MVP are known.*

## What we mean

Acceptance criteria are the conditions **Mathieu, Diana, and Damiens agree must be met** before calling a feature or the hackathon product ready. They connect the brief and our Must-have scope to observable results. They describe behaviour and outcomes, not which component or library implements them.

| Level | What it answers | Example of the check |
| --- | --- | --- |
| **Feature criterion** | Does this particular Must-have capability behave as agreed? | Given a valid input, does the feature show the expected result? |
| **Product criterion** | Do the features work together to deliver the MVP promise and respect the brief? | Can the user complete the whole UI → backend → result journey, including a relevant failure path? |

Feature criteria feed the product decision, but they do not automatically add up to an accepted product. Individually working features may still fail when connected, miss a mandatory constraint, or produce no useful end result.

A criterion is an expected behaviour; a test scenario supplies a concrete input and checks whether that behaviour occurs. The criteria also set a limit on the pitch: we should not claim a capability that the build cannot show or explain with evidence.

## Five-minute method after MVP selection

1. **State the promise together:** “For [user], the MVP helps with [problem] by producing [useful result or decision].” Check it against the released brief and judging criteria.
2. **Check each Must-have feature:** Write one or two observable criteria for what that capability must do. Avoid criteria for optional features until the core product works.
3. **Check the product as a whole:** Add a small number of criteria for the complete user journey, the promised useful result, and mandatory brief constraints. Include a relevant failure/fallback or approval path where needed.
4. **Make each criterion checkable:** Write the situation or input, the user's action, and the visible result. Specify any necessary source, constraint, or limitation. If “pass” is debatable, make the expected result more concrete.
5. **Link and run:** Show which product result each feature supports. Mathieu drafts the checks; Diana and Damiens review them. Run feature scenarios as parts are built, then run product scenarios on the integrated build. Record failures, fix Must-haves first, and rerun before the pitch.

## When we use them

- **After choosing the MVP (around minutes 40–60):** Agree on the Must-have feature and product criteria before the build goes far. At this point, the **criteria are agreed**, not yet passed.
- **During the build and first integrated slice:** Check a feature when it is ready, then check the whole UI → backend → result path as soon as it connects. A failed check shows what to fix or what scope the three of us must explicitly change.
- **Before the demo (during the testing buffer):** Run all Must-have feature checks and product-level scenarios on the current build, including a relevant failure path and fallback. The **product is accepted for the demo** only when those checks pass, or the team has jointly narrowed the promise and updated the criteria and pitch.

We do not wait until the end to discover what “done” means. The final check confirms the agreement made earlier.

## Writing rule

> **Given** [situation or input], **when** [user action], **then** [observable result]. **Pass if** [specific check, including evidence or constraint when needed].

For example, “the AI gives a useful answer” is too vague to accept. After the real MVP is chosen, replace it with the particular result the user must see and the evidence or rule it must respect. Do not prewrite challenge-specific criteria now.

## Worked example — fictional document-status brief

This is a **practice example**, not a prediction of the KBC challenge or a feature chosen for our product. Suppose the brief asks us to help a customer understand what is missing from an application. Our four-hour MVP promise is: **a customer can check a sample application and see which required document is missing, or see that its status cannot currently be verified**. For this example, the only Must-have feature is comparing the required and received document lists. A polished upload flow is outside the MVP.

The sample application `DEMO-01` requires `ID` and `proof of address`; only `ID` is recorded as received. These invented records contain no real customer data.

| ID / level | Criterion agreed before building | Concrete scenario and pass check |
| --- | --- | --- |
| F1 — feature | **Given** an application's required and received document lists, **when** its status is checked, **then** show the required documents that have not been received. | Use `DEMO-01`. **Pass if** the result names `proof of address` as missing and does not name `ID` as missing. |
| P1 — product | **Given** the customer opens the application page, **when** they check `DEMO-01`, **then** the UI calls the backend and displays the missing document with a clear next step. | Run the actual UI → backend → result journey. **Pass if** the page shows `proof of address` and tells the customer to provide it. A correct backend response alone does not pass P1. |
| P2 — product failure | **Given** the status service is unavailable, **when** the customer checks the application, **then** the UI explains that the status cannot be verified and does not claim the application is complete. | Simulate a service error through the agreed demo path. **Pass if** the uncertainty is visible and no success or completion message appears. |

F1 tests the feature's rule; P1 tests the product journey; P2 tests what the product claims when the result is unavailable. The **criterion** is the agreed behaviour in the middle column. The **test scenario** supplies the concrete sample, action, and pass check in the last column. All three would agree these before building; during development we would record actual results in the run sheet below. This example has **not been run** and does not make the fictional product accepted.

## Questions to ask when drafting

- Does the normal journey produce the **one useful result** the MVP promises?
- What should the user see when required information is missing or uncertain?
- If a selected tool or model fails, what does the user see and what is our agreed fallback?
- Does the result respect the brief's data, business, and safety constraints? Is approval visible before a consequential action, if relevant?
- Can we demonstrate each Must-have with the actual integrated build, and does the pitch describe only what we can show?

## Run sheet — copy after the brief

**Challenge / MVP promise:** [ ]

**Must-have scope and relevant constraints:** [ ]

**Agreed fallback, if needed:** [ ]

| ID / level | Feature or product result supported | Given / when: example situation and action | Then: expected result / pass check | Actual result | Status / fix owner |
| --- | --- | --- | --- | --- | --- |
| F1 — feature | [Must-have feature → product result] | [ ] | [ ] | [ ] | Not run / [ ] |
| F2 — feature, if needed | [Must-have feature → product result] | [ ] | [ ] | [ ] | Not run / [ ] |
| P1 — product | [MVP promise / complete journey] | [ ] | [ ] | [ ] | Not run / [ ] |
| P2 — product, if relevant | [Failure, fallback, or mandatory constraint] | [ ] | [ ] | [ ] | Not run / [ ] |

**Final team check:** [ ] Must-have features pass their checks. [ ] The integrated product passes its whole-journey and mandatory-constraint checks. [ ] Diana's demo and pitch match the observed behaviour. [ ] Remaining limits are stated clearly.
