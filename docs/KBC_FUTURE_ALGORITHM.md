# KBC Future — the algorithm in one page

**Purpose.** Help a customer see cash-flow pressure before it happens and identify
possible spending adjustments. The financial digital twin is a personal model
of income, commitments and everyday spending, recalculated from transaction history.

**Main tool:** `future(customer, transactions, as_of, horizon_days=30, learning_state=None)` in
[`backend/future_engine.py`](../backend/future_engine.py). It returns daily balances,
the forecast low point, a buffer-gap amount, payment drivers and a proposed plan.
It runs independently of the database, API and interface; Damiens supplies the data.

**Inputs.** Customer ID, balance at the forecast date and chosen safety buffer;
historical transaction ID, date, signed amount, merchant, category and payment method.
Supply only transactions through `as_of`, with about three months of complete
history. Merchant categories are supplied enrichment, not inferred by this code.

| Step / function | What the current implementation does |
| --- | --- |
| 1. `classify_transaction` | Uses amount direction and transfer metadata to label income, expense or transfer. Category rules protect rent, utilities, insurance, groceries, transport, healthcare and debt payments. Dining, shopping, leisure and entertainment are candidates for reduction. Unknown categories are excluded from reductions. |
| 2. `detect_recurring_patterns` | Groups by merchant, category and type. Requires at least three consecutive months, amounts within 15% of their mean, dates within five days of the median day, and bank-transfer/direct-debit methods. |
| 3. `build_forecast` | Schedules recurring payments using their last observed day of the month and average amount. Spreads non-recurring expenses from the last 90 days into an average daily spend. Calculates each future daily balance. |
| 4. `calculate_confidence` | Produces a heuristic score from recurring income and essential-payment patterns. This is a regularity indicator, not a measured probability of forecast accuracy. |
| 5. `calculate_reduction_capacity` | Uses the last three complete months. For flexible categories recorded in all three, subtracts the 20th-percentile monthly spend from the average. This estimates possible reductions; past low spending does not prove present feasibility. |
| 6. `create_support_plan` | Returns `safe` when there is no predicted gap. Otherwise spreads reductions across forecast days and checks every balance against the buffer. Uses the largest capacities first, scaled to the period length. A gap with insufficient capacity or low confidence returns `review_needed`; a feasible plan requires approval. |

```text
Daily balance = previous balance + recurring flows − expected variable spend
Buffer gap    = max(0, chosen buffer − lowest predicted balance)
```

**Verified demo (30 days from 30 September 2026).** Alex's forecast reaches €184 on 27 October: €66 below his €250
buffer. Reducing dining by €72 and shopping by €1.34 across 30 days brings the
simulated minimum to €250.01. The plan exceeds €66 because savings accrue gradually.
Sam gets `safe`; Robin's irregular income leads to `review_needed`.

**How it improves.** `update_forecast_learning` compares saved predicted variable
spending with actual spending over the same completed period. By default it adds 30% of the
daily error to a personal correction, which `future(..., learning_state=state)`
applies next time. Example: spending underestimated by €28 over seven days produces
a +€1.20/day correction. Repeated/overlapping windows and another customer's state
are rejected when the previous state is supplied. Damiens must persist the state and observations. A synthetic held-out
example verifies reduced error for a stable spending shift; improvement in real
use still needs measurement. Advice acceptance is feedback, not proof of benefit.

**LLM and customer.** The planned LLM explains the calculated result, then asks for
approval, adjustment or dismissal; it must not invent figures or execute actions.
The UI/backend will record these responses. The algorithm provides the evidence.

**MVP limits.** Confidence is heuristic; there is no uncertainty band. Reductions
assume even daily savings starting tomorrow. Positive receipts may include refunds;
categories need review. A learned correction can become stale as habits change.
`safe` means no gap in this forecast, not guaranteed affordability. The code
executes no financial action and does not yet learn advice preferences.

**Verification:** 12 algorithm checks and three shared-fixture checks pass. Run
`python3 -m unittest discover -s backend -p 'test_future_engine.py' -v` and
`python3 -m unittest discover -s scripts -p 'test_future_demo_data.py' -v`.
Run the actual database scenarios with `python3 scripts/future_demo_data.py --database`.
