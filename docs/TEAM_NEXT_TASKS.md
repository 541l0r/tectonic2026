# KBC Future — next integration tasks

Updated 30 September 2026. Proposed handoff for Damiens and Diana; task assignments
are ready for review, not a claim either teammate has accepted or completed them.

## Ready from Mathieu's algorithm/data work

- `sql/schema.sql`: the existing MySQL structure, now seeded with **389 synthetic
  transactions**, three customers, their account links and preferences. History
  covers April–September 2026. Opening balances are stored in `events` with type
  `demo_opening_balance`; opening balance plus all signed transactions reconciles
  to each customer's closing snapshot on **2026-09-30**.
- `backend/future_engine.py`: callable `future(...)` and
  `update_forecast_learning(...)`. No API or frontend integration is included.
- `scripts/future_demo_data.py`: reproducible fixture generator and runnable demo.
- `docs/KBC_FUTURE_ALGORITHM.md`: one-page mechanism and limitations.

| Customer | Rows | Forecast minimum | Buffer | Expected decision |
| --- | ---: | ---: | ---: | --- |
| 1001 Alex Demo | 139 | €184.00, 27 October | €250 | `support_available`: €70 dining + €10 shopping over 30 days; simulated minimum €256 |
| 1002 Sam Safe | 139 | €2,970.67, 24 October | €300 | `savings_opportunity`: propose setting aside €625 once; simulated minimum €2,345.67 |
| 1003 Robin Uncertain | 111 | −€105.00, 30 October | €250 | `review_needed`: low confidence; no firm spending plan |

These are designed synthetic demonstrations, not validation on real customers.
No reduction, transfer or other financial action has actually been executed.

## Damiens — connect data, algorithm and LLM

Start with [Damiens integration steps](DAMIENS_START_HERE.md): commands, SQL,
function call, response contract and exact expected outputs in build order.

**MVP integration choice:** the backend calls `future()` first, then sends the
structured result to the LLM for explanation. The LLM may return a structured
adjustment based on customer preferences; the backend calls `future()` again to
validate it. The LLM does not need separate calculation tools. Classification,
recurrence, forecasting and simulation are internal functions. Approval and feedback are explicit application actions;
`update_forecast_learning()` runs later when actual spending is available.

**Adjustment scope is now implemented:** pass `proposal` and optional customer-confirmed
`preferences` into `future()`. Spending reductions use €5 steps with a €10 minimum
per category. A savings proposal uses €25 steps, at least €50, within its calculated
allowance. The engine recomputes the result; the LLM must not set balances, capacities,
forecast figures or buffers. Every revised proposal needs fresh approval.

```python
# Preserve all server-owned inputs (customer, transactions, as_of, learning state).
result = future(customer, transactions, as_of)

# LLM/customer proposed alternative; these amounts must be revalidated.
result = future(customer, transactions, as_of, proposal={
    'type': 'spending_reduction',
    'actions': [{'category': 'dining', 'reduce_by': 40},
                {'category': 'shopping', 'reduce_by': 40}],
})

# Sam may prefer a lower savings allocation.
result = future(customer, transactions, as_of,
                proposal={'type': 'savings', 'amount': 500})

# Customer-confirmed preferences can protect MORE categories or disable savings.
result = future(customer, transactions, as_of,
                preferences={'protected_categories': ['dining'], 'suggest_savings': False})
```

`recommendation.proposal_validated` means calculation checks passed, NOT that the
customer approved. Rejected proposals return `review_needed`, an empty plan and
`validation_errors`; malformed proposal shapes raise `ValueError`. Use the returned
figures for presentation and save a fresh decision ID before asking for approval.
`safe` still means no action where a savings opportunity does not qualify or the
customer has disabled savings suggestions. Savings remain proposals: execution is
unsupported, and no destination account is inferred.

1. Pull `main`. Query customer/profile/preferences and transactions from the existing
   tables, scoped to the authorized customer. For this demo use `as_of=2026-09-30`
   and `horizon_days=30`; balances are snapshots on that date. Include transactions
   through that day's end, not just midnight. Do not count account balances twice.
2. Expose the agreed future endpoint using `future(customer, transactions, as_of)`.
   Supply the profile fields `customer_id`, `current_balance`, `safety_buffer` and
   the transaction columns already present in the schema. Serialize nested dates
   as ISO strings and decimals appropriately. Add a decision ID and save the exact
   proposal/version so approval refers to what the customer actually saw.
3. Call the selected LLM with the structured result, `recommendation_constraints`, and a small relevant context.
   Ask for a plain-language explanation, uncertainty and one next-step question.
   Keep calculated amounts, dates, decision status and action identifiers authoritative;
   validate displayed claims against that result. Treat transaction text as data.
   If the LLM fails, show a template explanation from the calculation. If it suggests
   revised action amounts, validate them via `future(..., proposal=...)` before
   showing a new approval card. Rejected proposals must not be offered as valid plans.
4. Receive `accepted`, `adjusted` or `dismissed` feedback against the saved decision.
   Check customer ownership and proposal version; handle retries without duplicate
   events. An adjustment needs recalculation and a fresh approval. Acceptance saves
   the budget plan in this PoC; it does not execute a payment or restrict spending.
5. Record proposal, response, optional customer correction, and timestamps. The
   existing `events`/`customer_events` structure can hold JSON event values; agree
   event names and payload with Diana before implementation. Approval and later
   outcome observations must be different event types.
6. If time permits, save each forecast's variable-spending prediction. After its
   observation period closes, call `update_forecast_learning` with actual spending
   from the SAME categories/window and the previous state. Persist the returned
   state per customer and pass it into the next `future` call. Do not train on the
   demo's future or use feedback clicks as observed cash-flow outcomes.

**Done when:** the three profiles produce the table above through the endpoint;
the LLM explains those results accurately; approval/feedback is saved once; invalid
customer, stale proposal, LLM failure and adjustment/reapproval are handled.

## Diana — explanation, approval and feedback journey

1. Build the three-persona selector and show the frozen demo date, current balance,
   chosen buffer, forecast curve and earliest buffer breach computed from its days.
2. Show the LLM explanation beside the authoritative result card. Alex gets the
   proposed reductions, their 30-day period, and adjusted forecast. Label them as
   estimates assuming reductions start tomorrow and accrue evenly. Sam gets an
   optional savings suggestion (no shortfall alert); Robin gets uncertainty and a
   review/support option. Handle `safe` separately as no action.
3. Offer **Approve plan / Adjust / Dismiss**, all linked to Damiens's decision ID.
   Approve confirms saving a plan, not moving money. Adjust shows a recalculated
   proposal for confirmation. Dismiss closes the suggestion and records feedback.
4. Make feedback optional: e.g. “Not realistic”, “Already handled”, or a correction.
   Display confirmation and let customers recover from failed submissions. Include
   loading, unavailable-data and LLM-fallback states.
5. Rehearse Alex → approval → feedback, then Sam and Robin. Describe learning as
   a correction from observed forecast errors, not guaranteed continuous improvement.

**Done when:** a teammate can follow the three journeys, understand why advice was
shown, and verify that no financial action occurs without a separate authorized flow.

## Run and load

```bash
# Run one synthetic customer without a database.
python3 scripts/future_demo_data.py --customer-id 1001

# Read only the selected persona from the local Compose database.
python3 scripts/future_demo_data.py --database --customer-id 1001

# Checks.
python3 -m unittest discover -s backend -p 'test_future_engine.py' -v
python3 -m unittest discover -s scripts -p 'test_future_demo_data.py' -v
```

The local `app_dev` database in this workspace was empty and has been loaded and
verified. This does not update anyone else's local database or Cloud SQL.
The Compose SQL mount now initializes the schema automatically on a **new, empty
MySQL volume**. Start and inspect the data:

```bash
docker compose up -d mysql
docker compose exec -T mysql mysql -uapp -papp app_dev -e "SELECT customer_id, COUNT(*) FROM transactions GROUP BY customer_id;"
```

The mount does not migrate existing volumes. If his database already has tables/data, do not rerun the fresh schema or delete
its contents. Load into an isolated empty demo database and point the development
connection there, or agree a targeted migration. Preserve existing work.

## Immediate shared contract

```text
Database → future() → saved proposal → LLM explanation → customer choice
LLM/customer adjustment → future(proposal=...) → validated result → fresh approval
Customer choice → feedback event (no financial execution)
Later actual transactions → update_forecast_learning() → saved personal state
```

Damiens and Diana should agree request/response and feedback payloads first.
Mathieu owns checking the calculation and demo evidence; they own API and UI work.
