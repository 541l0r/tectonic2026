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
| 1001 Alex Demo | 139 | €184.00, 27 October | €250 | `support_available`: €72 dining + €1.34 shopping over 30 days; simulated minimum €250.01 |
| 1002 Sam Safe | 139 | €2,970.67, 24 October | €300 | `safe`: no spending plan |
| 1003 Robin Uncertain | 111 | −€105.00, 30 October | €250 | `review_needed`: low confidence; no firm spending plan |

These are designed synthetic demonstrations, not validation on real customers.
No reduction, transfer or other financial action has actually been executed.

## Damiens — connect data, algorithm and LLM

1. Pull `main`. Query customer/profile/preferences and transactions from the existing
   tables, scoped to the authorized customer. For this demo use `as_of=2026-09-30`
   and `horizon_days=30`; balances are snapshots on that date. Include transactions
   through that day's end, not just midnight. Do not count account balances twice.
2. Expose the agreed future endpoint using `future(customer, transactions, as_of)`.
   Supply the profile fields `customer_id`, `current_balance`, `safety_buffer` and
   the transaction columns already present in the schema. Serialize nested dates
   as ISO strings and decimals appropriately. Add a decision ID and save the exact
   proposal/version so approval refers to what the customer actually saw.
3. Call the selected LLM with the structured result and a small relevant context.
   Ask for a plain-language explanation, uncertainty and one next-step question.
   Keep calculated amounts, dates, decision status and action identifiers authoritative;
   validate displayed claims against that result. Treat transaction text as data.
   If the LLM fails, show a template explanation from the calculation.
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
   estimates assuming reductions start tomorrow and accrue evenly. Sam gets no
   unnecessary intervention; Robin gets uncertainty and a review/support option.
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
# Run synthetic fixtures without a database.
python3 scripts/future_demo_data.py

# Read the three personas from the local Compose database and run the engine.
python3 scripts/future_demo_data.py --database

# Checks.
python3 -m unittest discover -s backend -p 'test_future_engine.py' -v
python3 -m unittest discover -s scripts -p 'test_future_demo_data.py' -v
```

The local `app_dev` database in this workspace was empty and has been loaded and
verified. This does not update anyone else's local database or Cloud SQL.
For an **empty** local `app_dev` database, Damiens can load:

```bash
docker compose up -d mysql
docker compose exec -T mysql mysql -uapp -papp app_dev < sql/schema.sql
```

If his database already has tables/data, do not rerun the fresh schema or delete
its contents. Load into an isolated empty demo database and point the development
connection there, or agree a targeted migration. Preserve existing work.

## Immediate shared contract

```text
Database → future() → saved proposal → LLM explanation → customer choice
                                    → feedback event / adjusted proposal
Later actual transactions → update_forecast_learning() → saved personal state
```

Damiens and Diana should agree request/response and feedback payloads first.
Mathieu owns checking the calculation and demo evidence; they own API and UI work.
