# Day-of guide — fill in together from brief to demo

This is the live worksheet for the challenge. Fill it in step by step after the real brief arrives; leave unknown answers blank and mark assumptions. [COMMAND.md](COMMAND.md) explains the method to the team beforehand. The team changes the plan when evidence or time changes. The public preselection window is 18:00–23:00 on 30 September; the working plan budgets four hours and must be adjusted to the actual rules.

## 1. Capture and define the problem

Mathieu leads the [opening ideation method](IDEATION_METHOD.md); use this section to record its first exit check.

**Target: 00:00–00:10.** Each person writes a problem statement before the team compares them.

| Item | Answer |
| --- | --- |
| Exact challenge wording / link | KBC Challenge: demonstrate a scalable personalization approach that understands each customer’s signals, situation, behaviour and intent; detects the right moment; and provides the most relevant support or guidance for potentially 2.3m+ customers. Source link: not yet supplied. |
| User and concrete pain | Customers discover cash-flow pressure only after their balance is already low. A current balance does not show whether upcoming commitments and normal spending will leave them financially unsafe before the next income. |
| Required outcome and judging criteria | Prove one compelling personalized scenario; show signal → context/intent → need → decision → personalized experience/channel; demonstrate creativity, working technology, challenge fit and security. An Aikido security audit is required; security is 10% of assessment. |
| Available data, tools, and permissions | Assumption for PoC: synthetic, consented transaction histories; current balance; product/buffer information; customer preferences. Real KBC data, APIs and permissions are unknown. |
| Official KBC / event Trusted AI requirements, if provided | Not supplied. Apply consent, data minimisation, explanation, customer approval, audit logging, fairness and safe failure by default. |
| Submission format and deadline | Unknown; validate with organizer. |
| Unknowns to ask the organizer | Exact data access; permitted external APIs/models; Trusted AI checklist; Aikido audit process; demo/submission requirements; deadline. |

**Individual problem statements before discussion (Mathieu / Diana / Damiens):** KBC should help a customer avoid an upcoming cash-flow gap before it happens. / Use a personal forecasting model, not a generic budget feature, to make advice relevant. / Prove an end-to-end, secure scenario with synthetic data and visible reasoning.

**Agreed one-sentence problem:** How might KBC proactively predict a customer’s upcoming cash-flow pressure and offer the smallest realistic, customer-controlled action before it becomes a problem?

**Why the shared statement above was chosen; any unresolved difference:** It starts from a clear customer need and moment, while naturally demonstrating a reusable decision engine across KBC products and channels. Exact data availability and required controls remain unresolved.

**Facts versus assumptions:** Facts: the brief prioritises scalable personalization, customer signals/context/intent, cross-product/channel relevance, working technology and security. Assumptions to validate: transaction data can be used with consent; synthetic data is acceptable for the PoC; customer-defined safety buffer is available; the system may provide advice but does not execute financial actions automatically.

**Existing KBC solution or process to improve:** Reactive balance checking, static budgeting and generic notifications. KBC Future adds a forward-looking, personal cash-flow forecast and an explained next-best-support decision.

## 2. Brainstorm and turn ideas into concepts

Write a word or short phrase on each post-it, then brainstorm together. Afterward, group duplicates and keep distinct angles visible. All three can still add or combine ideas while discussing preferences. Give each shortlisted candidate one clear concept sentence here; assess its demo, data, and feasibility in section 3. Use the [global idea list and ten lenses](IDEAS.md) only as prompts when relevant. Ask a mentor or organizer to clarify a material unknown when possible.

**Numbered groups / angles (or attach a photo of the wall):** 1. Reactive budgeting → proactive financial resilience. 2. Current balance → predicted future balance. 3. Generic category averages → personal financial rhythm. 4. Product recommendation → least-disruptive customer support. 5. One app screen → reusable cross-channel decision engine.

**Initial preferences and reasons (Mathieu / Diana / Damiens):** A: it starts with a clear, proactive customer need and can scale beyond a feature. / A: it gives a visual, explainable end-to-end demo while preserving customer control. / A: it has a small deterministic backend core and an honest synthetic-data fallback.

**Provisional shortlist order (#1, #2, optional #3) and any disagreement:** #1 A — KBC Future; #2 B — budget dashboard; #3 C — generic recommender. No recorded disagreement; validate this ordering against the official brief and available data.

| Candidate | One-sentence concept: user, outcome, main approach | Complementary ideas combined |
| --- | --- | --- |
| A | KBC Future: a learning financial agent that predicts individual cash flow and gives timely, explainable advice to protect a chosen safety buffer. | Personal baseline, cash-flow forecast, reduction capacity, customer approval. |
| B | Smart budget dashboard that categorises historical spending and shows monthly budgets. | Historical categorisation and spending insights. |
| C | Generic next-best-product recommender based on customer activity. | Notifications and product/channel orchestration. |

## 3. Choose the KBC product concept and outline its vision

Choose the concept that will be the basis of the **proposed future KBC product**. Describe what that product could eventually do for its user. This is a product proposal, not the four-hour prototype or a claim that KBC has adopted it.

1. Cross out any concept that misses the brief or needs forbidden data. Record the reason. A concept can remain even if its full product cannot be built in four hours, provided one important part can be proved.
2. Compare the remaining concepts in the table. Record the future customer benefit, how the product would work, KBC fit, what could be proved, and the main uncertainty. The provisional shortlist order does not select the product.
3. Let each teammate defend a preferred concept and state a concern. Choose the concept for the proposed future KBC product together, using the actual judging criteria when available. Record the reason and any unresolved concern.
4. Before selecting the four-hour proof, state the full product's intended user experience, distinctive mechanism, customer and KBC value, and main data or trust dependency in the short vision below. Add depth later for the pitch without changing what the prototype claims to prove.

| Concept | Future customer benefit and mechanism | Brief / KBC fit | One important claim we could prove | Main dependency or uncertainty |
| --- | --- | --- | --- | --- |
| A | Anticipates a cash-flow gap before it occurs; models income, commitments, personal spending range and buffer; simulates the least-disruptive safe action. | Directly demonstrates signals → context → need → decision → personalized support. Reusable for accounts, savings, advisers and channels. | Given synthetic history, forecast a future buffer breach and produce an explained, realistic support plan. | Access to transaction semantics and required KBC Trusted AI/affordability rules in production. |
| B | Helps customers understand historical spending through a familiar monthly view. | Relevant but mainly reactive; weak fit to proactive decision-engine challenge. | Categorise spend and show a budget. | Not distinctive; does not prove moment detection or adaptive support. |
| C | Can show a customer a potentially relevant product or message. | Cross-channel but risks becoming sales-led rather than customer-need-led personalization. | Rank a generic offer. | Relevance, trust and responsible recommendation are hard to demonstrate in four hours. |

**Chosen future KBC product concept and reason:** **KBC Future** — a continuously learning financial co-pilot. It is selected because it begins with a meaningful customer need, proves the required personalization/decision flow, and can expand beyond one feature or product.

**Team agreement:** [What each of Mathieu, Diana, and Damiens thinks is essential; note any concern.]

**Proposed KBC product vision (the full intended use, separate from the four-hour proof):**

| Question | Team answer |
| --- | --- |
| What would the complete user experience look like? | A customer sets a comfort/safety buffer and sees a forward-looking view: expected income, known commitments, likely variable spend and the lowest predicted balance. When KBC Future detects a credible future buffer breach, it explains why, offers the least-disruptive plan, and lets the customer accept, alter, dismiss or request support. It can appear in app, notification, adviser and relevant KBC journeys. |
| What is the distinctive mechanism, and how is it better than the current approach? | An adaptive personal cash-flow digital twin: it uses each customer’s own transaction history to forecast their next 7–30 days, models uncertainty, identifies historically realistic reduction capacity, and optimizes for the smallest disruption. It learns by comparing forecast with actual outcomes and advice with customer response. Current budgeting is retrospective and generic. |
| What changes for the customer and for KBC compared with today? | Customer: fewer surprises and more control before financial pressure occurs. KBC: a reusable next-best-support engine that can reduce avoidable payment stress and improve trust, engagement and appropriate service routing. |
| What one outcome KPI would show user improvement in real KBC use (population, event, denominator, period)? Is there a baseline and a safety/quality guardrail? | Among opted-in customers receiving a high-confidence buffer-breach alert, measure the percentage whose lowest actual balance stays at or above their selected buffer during the following 30 days, versus a matched no-advice/previous-period baseline. Guardrails: forecast error, alert dismissal rate, false-positive rate, complaints, and no recommendation that targets protected essentials or bypasses customer approval. |
| What data, permissions, trust controls, integrations, or operations would real use require? What remains unknown? | Consent-based transaction and product data; merchant/category enrichment; customer-set buffer/preferences; secure model/feature store; policy engine; notifications/adviser integration; explanation and audit logs; monitoring and human escalation. Unknown: exact KBC data availability, retention rules, regulated policy requirements and operational ownership. |

## 4. Select the four-hour proof within that product concept

The selected concept above describes the proposed future KBC product. Now choose **one small part of that product** to build as the hackathon proof of concept (MVP). The prototype must show evidence for one important claim about the product; it does not have to implement the full vision. Start with one end-to-end journey; compare another scope only if the choice is unclear or contested. These are possible proof scopes for the same product concept, not another round of ideation. **Mathieu's facilitated discussion runs from about 00:10 to 00:40.** At the interface handoff, the minimum is the chosen product concept, one proof journey, a sample input, and a visible result. Complete the remaining worksheet fields as work progresses. Diana and Damiens then agree on the immediate UI/API example and start coding.

1. State the one user outcome and central claim the prototype needs to prove. Include any mandatory requirement from the brief.
2. For each journey considered, name its starting input, the user action, the visible result, the data or tool it needs, and its main build or integration risk. Cross out a journey that cannot work with allowed inputs or fit the remaining time.
3. Choose the smallest complete journey that still proves the claim. Prefer a working UI → backend/tool → result path over more features that do not connect. All three agree on the choice and the reason.
4. List the capabilities needed for that journey. A capability is **Must** if removing it breaks the MVP promise or a mandatory rule. Put useful but removable capabilities in Should or Could; state Won't explicitly. Check that the Must list is feasible for Diana and Damiens to integrate in time.
5. Write the promise, three demo steps, fallback, and one observable success check. If these cannot be stated clearly, reduce or revise the journey before assigning build tasks.

**Central claim to prove:** Using an individual’s transaction history, KBC Future can detect a credible upcoming cash-flow-buffer breach and create a transparent, personally realistic plan that restores the buffer without touching protected essentials.

| Possible MVP journey for this direction | Starting input → user action → visible result | Data/tool needed | Main risk or fallback | Feasible in time? |
| --- | --- | --- | --- | --- |
| A | Synthetic transaction history and current balance → customer opens “See my future” → 30-day balance forecast identifies a future buffer breach, explains its drivers and shows the least-disruptive reduction plan. | Local synthetic dataset; recurring-payment detector; personal baseline; forecast/simulation API; UI. | Classification/forecast is imperfect → use curated labelled synthetic transactions and show confidence plus deterministic calculation. | Yes |
| B, if needed | Same input → customer changes their safety buffer or proposes a discretionary spending amount → UI recalculates whether the future remains safe. | Same as A plus scenario input. | Extra UI scope → use a fixed scenario/default buffer. | Yes, only after A works |

**Chosen MVP journey and why:** Journey A. It is the smallest complete proof of predictive personalization: data → personal understanding → forecast → need detection → decision → explained advice. Journey B is a useful extension but not needed to prove the claim.

**Other journeys left outside this MVP and why:** Customer-entered "what if" simulations, channel optimization, adviser escalation, savings-product support and autonomous actions remain future journeys. They do not need to be built to prove proactive cash-flow detection and advice.

**Team agreement / remaining concern:** The proof must stay focused on one cash-flow-gap persona and a deterministic calculation, not broaden into a generic assistant. Confirm that the real brief permits the synthetic-data demo and learn the official Trusted AI/security criteria.

**MVP promise:** For a customer facing a likely cash-flow-buffer breach, KBC Future turns transaction history into an understandable 30-day forecast and a realistic, customer-controlled plan to prevent it.

**Three demo steps:** 1. Open a synthetic customer whose income, fixed bills and current balance are shown. 2. Select “See my future”; KBC Future detects recurring patterns, forecasts daily balance and checks the customer’s €250 buffer. 3. See the predicted breach date, explanation, confidence and least-disruptive plan (for example, reduce only flexible spend by €95) with accept/adjust/dismiss controls.

**Cut line:** One labelled synthetic customer; deterministic recurring-income/bill detection; 30-day daily forecast; one buffer-breach rule; one simulated, safe reduction plan; one visible explanation. No external integrations or automatic actions.

**Must (promise and mandatory rules):** End-to-end UI → API → result; synthetic data only; personal (not peer-led) baseline; forecasted daily balance; selected safety buffer; buffer-breach detection; protected-essential categories; realistic reduction-capacity calculation; clear explanation/confidence; explicit customer approval; audit-friendly decision output; Aikido security audit.

**Should (valuable, but the main journey can work without it):** Multiple personas; adjustable buffer; forecast chart; accept/adjust/dismiss feedback; personalisation of advice tone/channel; 7/30-day uncertainty band.

**Could (optional improvement):** Natural-language explanation; adviser view; multiple scenario comparison; learning feedback visualisation; model-backed category classification.

**Won't (explicitly outside this MVP):** Live KBC data; actual money transfers; credit decisions or product offers; automated spending changes; sensitive-trait inference; external partner integration.

**Fallback:** Use a bundled, labelled synthetic transaction JSON file and a deterministic calculation service. If the AI/category component fails, show pre-labelled recurring/flexible categories and still run the forecast, gap detection, scenario simulation and explanation.

**One observable success check:** Given the “cash-flow gap” synthetic customer and a €250 safety buffer, clicking “See my future” returns an integrated visible result showing a predicted below-buffer date, its income/bill/spend drivers, a confidence value, and a plan whose recalculated minimum balance is at least €250.

**Value claim demonstrated now / assumption to validate later:** A synthetic customer with a €95 predicted buffer breach receives a tailored plan based on their own historical flexible-spending floor, and the simulation shows the buffer restored. / Real-world forecast accuracy, customer acceptance, prevention of low-balance events, fairness and long-term financial benefit require KBC evaluation.

**Trusted AI decisions for this MVP:** Synthetic data only; no demographic/sensitive inference; recommendations are grounded in displayed transactions and deterministic forecast inputs; use personal history rather than peer stereotypes; protect essential categories; display reason, confidence and limitations; customer approves all actions; no credit decision or automatic transfer; validate/limit API input; log decision inputs/outputs without secrets; provide deterministic fallback; run required Aikido audit. Use the [working checklist](PREPARATION.md#10-kbc-trusted-ai-checklist) as a prompt.

## 5. Build and adapt

| Checkpoint | Decision to record | Owner |
| --- | --- | --- |
| At the first coding task | Have Diana and Damiens agreed on the MVP's request/response example and integration boundary? | Diana + Damiens |
| During the build | Is the UI → backend → visible result working? If no, cut optional scope until it is. | Diana + Damiens |
| After the first working slice | Does one mechanism prove the capability leap (tool, retrieval, calculation, or coordination)? If no, agree on the strongest one. | All three |
| Every 25 minutes | What works, what is blocked, how is everyone doing, and what is the next smallest visible improvement? Mathieu keeps this brief and tracks time; the team decides scope changes. If a blocker persists 15 minutes, use the mock boundary and move on. | Mathieu facilitates; all three decide |
| 45 minutes before deadline | Freeze new features. Verify the demo path, output, and fallback. | All three |
| 30 minutes before deadline | Rehearse the pitch and run the exact submission path. | Diana + Mathieu |

| Owner | Next task | File / interface | Done when | Status |
| --- | --- | --- | --- | --- |
| Mathieu | Draft acceptance scenarios, demo data narrative and pitch evidence; facilitate scope/time checks. | `docs/ACCEPTANCE_CRITERIA.md`, pitch notes, workflow. | The main and fallback journeys have observable pass criteria and the pitch clearly distinguishes live proof from future vision. | To do |
| Diana | Build the KBC Future forecast/result experience; lead Trusted AI UI review and pitch story. | Frontend and shared docs. | User can open a persona, trigger the forecast and see explanation, confidence, plan and approval controls. | To do |
| Damiens | Build the synthetic-data forecast, gap detection and advice API; provide agreed response/fallback. | Backend API and synthetic dataset. | API returns the forecast, buffer breach, drivers, safe plan and decision explanation for the agreed persona. | To do |

**MVP interface agreed by Diana and Damiens:** [Link or paste request and response JSON after selecting the MVP.]

**Latest working demo command / URL:** [ ]

**Current blocker and decision:** [ ]

**Feature and whole-product acceptance criteria:** [Mathieu drafts after MVP selection; all three agree on the checks. Verify Must-have features, then run the complete journey and relevant failure/fallback on the integrated build.] Use the short method and run sheet in [docs/ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md).

**Integration check:** [Branch/build state, UI → API result, owner of next fix, and next run time.]

## 6. Final proof

- [ ] The pitch says what the future solution could do at KBC, for whom, and why it matters.
- [ ] The pitch names the distinctive mechanism and explains how it improves on today's approach.
- [ ] The live demo shows the central claim working on the current build; simulated parts and remaining limits are named.
- [ ] Must-have feature checks pass, and the complete product journey passes on the integrated build.
- [ ] Diana and the team have checked the relevant Trusted AI requirements; required controls appear in the build and acceptance scenarios.
- [ ] A new teammate can follow the three demo steps without an explanation.
- [ ] The visible result shows the claimed customer benefit and what evidence or tool produced it.
- [ ] Any consequential action has an explicit approval step; the demo can safely use mock actions.
- [ ] The fallback chosen for this MVP works if an external service fails.
- [ ] Diana can tell the problem, mechanism, result, and limitation within the allotted pitch time.
- [ ] The submission format and deadline have been checked against the actual rules.

This board is a practical adaptation for a four-hour working budget, not a proven recipe for winning. The [winner interview study](https://arxiv.org/html/2206.04744v1) supports exploring and defining a relevant problem before choosing a solution, checking rules and judges, and showing a demonstrable result. A [corporate hackathon case study](https://research.tue.nl/en/publications/utilizing-hackathons-to-foster-sustainable-product-innovation-the/) linked project continuation with focused preparation, a functioning prototype, customer fit, and ease of integration; it did not study Tectonic judging.
