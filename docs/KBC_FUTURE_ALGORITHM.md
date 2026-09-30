# KBC Future — the algorithm in one page

**Purpose.** Help a customer see cash-flow pressure before it happens and identify
possible spending adjustments. The financial digital twin is a personal model
of income, commitments and everyday spending, recalculated from transaction history.

**Main tool:** `future(customer, transactions, as_of, horizon_days=30)` in
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
| 2. `detect_recurring_patterns` | Groups by merchant, category and type. Requires at least three transactions in consecutive months, amounts within 15% of their mean, and bank-transfer/direct-debit payment methods. |
| 3. `build_forecast` | Schedules recurring payments using their last observed day of the month and average amount. Spreads non-recurring expenses from the last 90 days into an average daily spend. Calculates each future daily balance. |
| 4. `calculate_confidence` | Produces a heuristic score from recurring income and essential-payment patterns. This is a regularity indicator, not a measured probability of forecast accuracy. |
| 5. `calculate_reduction_capacity` | For flexible categories with at least three recorded months, subtracts the historical 20th-percentile monthly spend from the average monthly spend. This estimates a possible reduction; past low spending does not prove it is feasible today. |
| 6. `create_support_plan` | Takes reductions from the largest available capacities until they cover the buffer gap. If capacity is insufficient or confidence is low, returns `review_needed`. Otherwise returns a proposal requiring approval. |

```text
Daily balance = previous balance + recurring flows − expected variable spend
Buffer gap    = max(0, chosen buffer − lowest predicted balance)
```

**Example.** A forecast low point of €200 against a €250 buffer gives a €50 gap.
If estimated flexible capacity covers €50, the engine proposes that reduction.
If the forecast stays above the buffer, it returns `safe` and no spending plan.
These are conditional estimates; a buffer breach is different from an overdraft.

**How it improves.** Today, new transactions change the recalculated patterns and
averages. Automatic training and advice-outcome learning are future work. The next
version should save dated forecasts, compare them with actual balances on unseen
days, measure error, and adopt model updates only when they improve validation
results. Customer corrections and accepted/adjusted/dismissed advice can inform
preferences; acceptance alone does not establish that advice caused improvement.

**MVP limits.** Recurrence checks consecutive months but not day-of-month variation.
The forecast has no uncertainty band. The plan adds estimated savings to the low
point without simulating when those savings occur; timing must be verified before
claiming it prevents a gap. Positive receipts can include refunds, and category
labels need customer review. The code executes no financial action.

**Run the checks:** `python3 -m unittest discover -s backend -p 'test_future_engine.py' -v`
