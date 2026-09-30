# Damiens integration steps

Your first deliverable is **Alex's real calculation returned by one HTTP endpoint**.
Then add the LLM explanation and approval recording. The algorithm is already
implemented; you do not need to recreate it or expose each internal function.

## 1 Pull and check the data

```bash
git pull --ff-only origin main
python3 -m unittest discover -s backend -p 'test_future_engine.py'
python3 -m unittest discover -s scripts -p 'test_future_demo_data.py'
docker compose up -d mysql
docker compose exec -T mysql mysql -uapp -papp app_dev -e "SELECT customer_id, COUNT(*) FROM transactions GROUP BY customer_id;"
```

Expected counts: Alex `1001` → 139, Sam `1002` → 139, Robin `1003` → 111.
Your new Compose SQL mount initializes an **empty MySQL volume automatically**.
It does not migrate an existing volume. Do not reload the schema into populated
tables or delete data. The current link table is `customer_product`; an older
database may still need a migration from `client_product_link`.

To check the data and algorithm together without any API work:

```bash
python3 scripts/future_demo_data.py --database --customer-id 1001
```

## 2 Connect one endpoint to the calculation

Proposed shared contract: `POST /api/future`, body `{"customer_id": 1001}`.
Agree this name with Diana before she connects it. Use the existing SQLAlchemy
engine in `backend/app.py`. The current `/api/ask` response is still a static mock.

Read the profile and consent using a parameterized query:

```sql
SELECT c.customer_id, c.name, c.current_balance, c.safety_buffer, p.advice_opt_in
FROM customers c
JOIN customer_preferences p ON p.customer_id = c.customer_id
WHERE c.customer_id = :customer_id;
```

Then read that customer's history:

```sql
SELECT transaction_id, customer_id, transaction_date, amount, merchant,
       merchant_category, payment_method
FROM transactions
WHERE customer_id = :customer_id AND transaction_date < :history_end
ORDER BY transaction_date, transaction_id;
```

For the frozen demo, bind `history_end` to **2026-10-01 00:00:00**. Balances are
snapshots at the close of **2026-09-30**; do not silently use today's date.
Validate customer ID, reject missing/non-consenting customers, and use the
authorized customer identity in any real session.

Every transaction must now include `customer_id`. Filter to the authorized customer
in SQL before calling `future()`. The engine rejects mixed-customer input and rows
without ownership before doing any calculation. It accepts exactly one customer object. The demo
also requires `--customer-id` and returns one object, never all customer results.
This is defense in depth: the endpoint must still authorize the selected customer
and filter the SQL query. Do not trust an arbitrary client-supplied ID as permission.

```python
from datetime import date
from future_engine import future

# customer_row and transaction_rows are SQLAlchemy .mappings() query results.
result = future(
    dict(customer_row),
    [dict(row) for row in transaction_rows],
    as_of=date(2026, 9, 30),
    horizon_days=30,
)
```

Return `result` as JSON, converting nested dates to ISO strings. Map input
`ValueError` to a clear client error and database failures to an unavailable state.
First prove this endpoint works without the LLM.

| Customer | Exact expected calculation |
| --- | --- |
| Alex 1001 | Minimum €184; gap €66; `support_available`; €70 dining + €10 shopping; adjusted minimum €256 |
| Sam 1002 | Minimum €2,970.67; `savings_opportunity`; suggest saving €625 once; adjusted minimum €2,345.67 |
| Robin 1003 | Minimum −€105; `review_needed`; low confidence; empty plan |

## 3 Add the LLM explanation

Call your chosen LLM server-side with the calculated result, constraints and
customer message. Ask it to explain the outcome briefly, mention assumptions,
and ask whether the customer wants to save the proposal. It must use the engine's
numbers. Keep credentials on the server and use a template if the LLM fails.

Return one envelope that Diana can use:

```text
decision_id: a new ID identifying the saved proposal/version
customer_id: the customer associated with that proposal
result: the unchanged engine output
explanation: the customer-facing explanation
```

Store the exact result under that decision ID before offering approval.
`proposal_validated=true` means the calculation passed; it does not mean the
customer has approved. Initially you can support Approve and Dismiss only.

## 4 Record the customer response

Agree a feedback endpoint with Diana, for example `POST /api/future/feedback`:

```json
{"decision_id": "the-displayed-id", "response": "accepted"}
```

Allow `accepted` or `dismissed`, check ownership/version, and store the response
and timestamp against the saved proposal. Repeated requests must not duplicate
the event. Existing `events` plus `customer_events` can store this record. Approval
saves a budget/savings intention only; it must not execute a transfer.

## 5 Add adjustments after the first journey works

If the LLM proposes new amounts, call the SAME function with the same server-owned
customer/history/date and a structured proposal:

```python
# Alex: an alternative distribution of the same total reduction.
result = future(customer, transactions, as_of, proposal={
    'type': 'spending_reduction',
    'actions': [{'category': 'dining', 'reduce_by': 40},
                {'category': 'shopping', 'reduce_by': 40}],
})

# Sam: a smaller savings allocation.
result = future(customer, transactions, as_of,
                proposal={'type': 'savings', 'amount': 500})
```

Do not accept LLM-provided balances, buffers or forecasts. Use customer-confirmed
preferences, such as `protected_categories`, from your stored context. If the
proposal fails validation, show the returned reason; do not offer it for approval.
A successful adjustment gets a fresh saved decision ID and fresh customer approval.

**Finish line:** Diana can select Alex, see calculated figures and an explanation,
approve the plan, and see that approval recorded. Then verify Sam and Robin.
Automatic forecast-learning persistence is a later integration task; do not let
it block this first working journey.
# Database review fixes

For an existing local database, back up first, then run:

```sh
docker compose exec -T -e MYSQL_PWD=app mysql mysql -uapp app_dev < sql/migrations/001_customer_product_ownership.sql
```

This preserves data, renames legacy `client_product_link` to `customer_product`, and enforces transaction ownership with a composite foreign key. It is repeatable and stops on mismatched ownership or ambiguous tables; do not use `--force`, reset the volume, or rerun the seed. Fresh databases use the updated `sql/schema.sql` directly.

`future()` now returns `data_quality.warnings` and `review_needed` for insufficient/stale history or expired recurring patterns. Pass these warnings to the LLM/UI; do not describe such forecasts as safe. Balance and transaction history must share the same account scope. Recurring transfers affect the balance but do not count as income or flexible spending.
