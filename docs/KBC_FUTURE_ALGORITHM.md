# KBC Future algorithm in one page

**Purpose.** Predict cash-flow pressure and suggest practical action: reduce flexible spending when a gap is forecast, or consider building savings when there is room.

**Main tool.** `future(customer, transactions, as_of, horizon_days=30, learning_state=None, preferences=None, proposal=None)`. Each call accepts exactly one customer and their transactions and returns one result. The backend authorizes that customer and filters the query; the engine rejects mixed-customer history or missing ownership. Categories come from transaction enrichment.

| Stage | What the engine does |
| --- | --- |
| Understand transactions | Derive income, expense and transfer labels. Protect essential expenses and any additional customer-protected categories. Unknown categories are excluded from reductions. |
| Recognise patterns | Detect at least three consecutive monthly payments with similar amounts and dates. Forecast scheduled income and bills alongside average everyday spending. |
| Detect need | Compare every forecast balance with the chosen buffer. Confidence is a pattern-based indicator, not a probability of accuracy. |
| Propose spending reductions | Estimate capacity from the last three complete months of personal flexible spending. Use €5 steps, at least €10 per category, and simulate savings accruing daily. Propose only a plan that protects every forecast day. |
| Propose savings | With high confidence, sufficient history, expected income and at least a 30-day horizon, retain the buffer plus an extra reserve of at least €100 or seven days of variable spending. Suggest 25% of remaining headroom, rounded down to €25, minimum €50. Check today's available balance too. These are configurable-in-code demo rules, not validated affordability policy. |
| Validate an adjustment | Recalculate an LLM/customer proposal against the same forecast, protected categories, personal capacities and savings allowance. Reject unsupported or infeasible changes before approval. |

**Verified examples.** From 30 September 2026, Alex's 30-day forecast reaches €184 against a €250 buffer. Reducing dining by €70 and shopping by €10 produces a simulated minimum of €256. Sam receives a €625 savings proposal, leaving a simulated minimum current-account balance of €2,345.67. Robin's irregular income calls for review. Without a gap or a qualifying savings opportunity, no action is proposed.

**The LLM's role.** Explain why the recommendation matters and propose adjustments based on the customer's stated preferences. For example, Alex could prefer €40 less dining and €40 less shopping; Sam could prefer saving €500. The backend passes that structured proposal back to `future()` for validation. Only validated figures may be presented for fresh customer approval. The LLM must not change balances, forecasts, essential-expense rules or the buffer on its own. No transfer or spending restriction is executed.

**How it improves.** Compare predicted spending with actual spending, then adjust gradually. If €70 was predicted for a week but €98 was spent, the error is €4 per day. The implemented learning calculation adds €1.20 per day to the next forecast by default. The app must still save observations and reuse the returned correction. Learning from Approve/Adjust/Dismiss feedback is not implemented; improvement in accuracy must be measured.

**MVP scope.** The engine calculates and validates recommendations; the LLM explains and adapts proposals for customer approval and feedback. Savings and reductions are estimates, not guarantees. Reductions assume even daily savings from tomorrow; savings proposals simulate one allocation, not a recurring transfer. There is no calibrated uncertainty band, and the MVP executes no financial transactions.

**Verification.** Run `python3 -m unittest discover -s backend -p 'test_future_engine.py'` and `python3 -m unittest discover -s scripts -p 'test_future_demo_data.py'`. Read one customer from the local database with `python3 scripts/future_demo_data.py --database --customer-id 1001`. Omitting the ID fails; no group forecast is available.
