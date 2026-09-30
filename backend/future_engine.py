"""Deterministic cash-flow decision engine for the KBC Future MVP.

The engine derives financial labels and validates proposals. An LLM can explain
results and propose preference-based adjustments; this module recalculates every
amount before it can be offered for customer approval. No action is executed.
"""

from __future__ import annotations

import calendar
import math
from collections import defaultdict
from datetime import date, datetime, timedelta
from statistics import median
from typing import Any


ESSENTIAL_CATEGORIES = {
    "rent", "mortgage", "utilities", "insurance", "healthcare",
    "debt_repayment", "groceries", "transport",
}
FLEXIBLE_CATEGORIES = {"dining", "shopping", "leisure", "entertainment"}
REDUCTION_STEP = 5
MINIMUM_REDUCTION = 10
SAVINGS_STEP = 25
MINIMUM_SAVINGS = 50
RECURRING_GRACE_DAYS = 5
HISTORY_DAYS = 90


def _as_date(value: date | datetime | str) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return datetime.fromisoformat(value).date()


def _percentile(values: list[float], fraction: float) -> float:
    """Small dependency-free linear percentile implementation."""
    ordered = sorted(values)
    if not ordered:
        return 0.0
    position = (len(ordered) - 1) * fraction
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def _months_between(first: date, second: date) -> int:
    return (second.year - first.year) * 12 + second.month - first.month


def _next_monthly_date(reference: date, after: date) -> date:
    """Return the next occurrence of reference's day-of-month after `after`."""
    year, month = after.year, after.month
    candidate = date(year, month, min(reference.day, calendar.monthrange(year, month)[1]))
    if candidate <= after:
        month += 1
        if month == 13:
            year, month = year + 1, 1
        candidate = date(year, month, min(reference.day, calendar.monthrange(year, month)[1]))
    return candidate


def classify_transaction(transaction: dict[str, Any]) -> dict[str, Any]:
    """Classify raw data without relying on age, city or other demographics."""
    amount = float(transaction["amount"])
    category = (transaction.get("merchant_category") or "unknown").lower()
    merchant = (transaction.get("merchant") or "").lower()
    method = (transaction.get("payment_method") or "").lower()

    if amount > 0:
        transaction_type = "income"
        if "own account" in merchant or method == "internal_transfer":
            transaction_type = "transfer"
    elif amount < 0:
        transaction_type = "transfer" if method == "internal_transfer" else "expense"
    else:
        transaction_type = "unknown"

    return {
        **transaction,
        "date": _as_date(transaction["transaction_date"]),
        "amount": amount,
        "category": category,
        "transaction_type": transaction_type,
        "is_essential": transaction_type == "expense" and category in ESSENTIAL_CATEGORIES,
        "is_flexible": transaction_type == "expense" and category in FLEXIBLE_CATEGORIES,
    }


def _pattern_key(transaction):
    # Opposite transfer legs must not be merged into one zero-net schedule.
    return ((transaction.get('merchant') or '').lower(), transaction['category'],
            transaction['transaction_type'], transaction['amount'] > 0)


def _pattern_is_current(last_date, as_of):
    next_due = _next_monthly_date(last_date, last_date)
    return as_of <= next_due + timedelta(days=RECURRING_GRACE_DAYS)


def detect_recurring_patterns(transactions: list[dict[str, Any]], as_of=None) -> list[dict[str, Any]]:
    """Mark monthly salary/bill patterns using merchant, date and amount regularity."""
    enriched = [classify_transaction(transaction) for transaction in transactions]
    groups = defaultdict(list)
    for transaction in enriched:
        groups[_pattern_key(transaction)].append(transaction)

    recurring_ids: set[Any] = set()
    active_ids: set[Any] = set()
    for group in groups.values():
        group.sort(key=lambda item: item["date"])
        if len(group) < 3:
            continue
        gaps = [
            _months_between(group[index - 1]["date"], group[index]["date"])
            for index in range(1, len(group))
        ]
        amounts = [abs(item["amount"]) for item in group]
        average = sum(amounts) / len(amounts)
        stable_amount = average > 0 and max(abs(value - average) / average for value in amounts) <= 0.15
        # Card merchants such as a supermarket may recur, but are variable
        # spending rather than a scheduled obligation. For this MVP only
        # direct debits and transfers can become calendar events. A transfer
        # affects the supplied balance scope but is not spending or salary.
        scheduled_method = all(
            (item.get("payment_method") or "").lower()
            in {"direct_debit", "bank_transfer", "internal_transfer"}
            for item in group
        )
        monthly = all(gap == 1 for gap in gaps)
        days = [item['date'].day for item in group]
        stable_date = max(abs(day - median(days)) for day in days) <= 5
        if monthly and stable_amount and scheduled_method and stable_date:
            recurring_ids.update(item["transaction_id"] for item in group)
            if as_of is None or _pattern_is_current(group[-1]['date'], _as_date(as_of)):
                active_ids.update(item['transaction_id'] for item in group)

    for transaction in enriched:
        transaction["is_recurring"] = transaction["transaction_id"] in recurring_ids
        transaction['is_recurring_active'] = transaction['transaction_id'] in active_ids
    return enriched


def _recurring_events(enriched: list[dict[str, Any]], as_of: date, horizon_days: int) -> list[dict[str, Any]]:
    by_merchant = defaultdict(list)
    for transaction in enriched:
        if transaction["is_recurring"]:
            by_merchant[_pattern_key(transaction)].append(transaction)

    end_date = as_of + timedelta(days=horizon_days)
    events: list[dict[str, Any]] = []
    for transactions in by_merchant.values():
        transactions.sort(key=lambda item: item["date"])
        last = transactions[-1]
        if not _pattern_is_current(last['date'], as_of):
            continue
        expected_amount = round(sum(item["amount"] for item in transactions) / len(transactions), 2)
        event_date = _next_monthly_date(last["date"], as_of)
        while event_date <= end_date:
            events.append({
                "date": event_date,
                "amount": expected_amount,
                "merchant": last.get("merchant"),
                "category": last["category"],
                "transaction_type": last["transaction_type"],
                "is_essential": last["is_essential"],
            })
            event_date = _next_monthly_date(last["date"], event_date)
    return events


def _daily_variable_spend(enriched: list[dict[str, Any]], as_of: date) -> float:
    start = as_of - timedelta(days=90)
    total = sum(
        abs(item["amount"])
        for item in enriched
        if start <= item["date"] <= as_of
        and item["transaction_type"] == "expense"
        and not item["is_recurring"]
    )
    return total / 90


def build_forecast(
    current_balance: float,
    enriched: list[dict[str, Any]],
    as_of: date,
    horizon_days: int = 30,
    daily_spend_adjustment: float = 0.0,
) -> dict[str, Any]:
    """Forecast balances from recurring events and a conservative personal spend rate."""
    events_by_date: dict[date, list[dict[str, Any]]] = defaultdict(list)
    for event in _recurring_events(enriched, as_of, horizon_days):
        events_by_date[event["date"]].append(event)

    baseline_spend = _daily_variable_spend(enriched, as_of)
    daily_variable_spend = max(0.0, baseline_spend + daily_spend_adjustment)
    balance = float(current_balance)
    days: list[dict[str, Any]] = []
    for offset in range(1, horizon_days + 1):
        forecast_date = as_of + timedelta(days=offset)
        recurring_amount = sum(event["amount"] for event in events_by_date[forecast_date])
        balance += recurring_amount - daily_variable_spend
        days.append({
            "date": forecast_date.isoformat(),
            "balance": round(balance, 2),
            "recurring_events": events_by_date[forecast_date],
        })

    lowest = min(days, key=lambda item: item["balance"])
    return {
        "days": days,
        "lowest_predicted_balance": lowest["balance"],
        "lowest_balance_date": lowest["date"],
        "daily_variable_spend": round(daily_variable_spend, 2),
        "baseline_daily_variable_spend": round(baseline_spend, 2),
        "daily_spend_adjustment": round(daily_spend_adjustment, 4),
    }


def calculate_confidence(enriched: list[dict[str, Any]]) -> tuple[float, str]:
    income_patterns = {
        item.get("merchant") for item in enriched
        if item.get('is_recurring_active', item['is_recurring']) and item["transaction_type"] == "income"
    }
    essential_patterns = {
        item.get("merchant") for item in enriched
        if item.get('is_recurring_active', item['is_recurring']) and item["is_essential"]
    }
    score = min(0.95, 0.35 + 0.30 * bool(income_patterns) + 0.15 * min(2, len(essential_patterns)))
    label = "high" if score >= 0.75 else "medium" if score >= 0.60 else "low"
    return round(score, 2), label


def calculate_reduction_capacity(enriched: list[dict[str, Any]], as_of: date) -> list[dict[str, Any]]:
    """Use the individual's own low-but-achieved monthly spend as a safe floor."""
    monthly_by_category: dict[str, dict[tuple[int, int], float]] = defaultdict(lambda: defaultdict(float))
    # Only the latest three complete calendar months; partial months would
    # artificially lower the spending floor.
    last_complete = as_of if as_of.day == calendar.monthrange(as_of.year, as_of.month)[1] else date(as_of.year, as_of.month, 1) - timedelta(days=1)
    for item in enriched:
        if not item["is_flexible"] or item.get("is_recurring", False):
            continue
        month_key = (item["date"].year, item["date"].month)
        if 0 <= _months_between(item["date"], last_complete) < 3:
            monthly_by_category[item["category"]][month_key] += abs(item["amount"])

    capacities = []
    for category, month_values in monthly_by_category.items():
        values = list(month_values.values())
        if len(values) < 3:
            continue
        expected = sum(values) / len(values)
        personal_floor = _percentile(values, 0.20)
        capacity = max(0.0, expected - personal_floor)
        capacities.append({
            "category": category,
            "expected_monthly_spend": round(expected, 2),
            "personal_floor": round(personal_floor, 2),
            "reduction_capacity": round(capacity, 2),
        })
    return sorted(capacities, key=lambda item: item["reduction_capacity"], reverse=True)


def _money(value):
    if isinstance(value, bool):
        raise ValueError('Expected a finite amount')
    try:
        amount = float(value)
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError('Expected a finite amount') from error
    if not math.isfinite(amount):
        raise ValueError('Expected a finite amount')
    return amount


def _review(forecast, safety_buffer, message):
    return dict(status='review_needed', gap_amount=max(0, round(safety_buffer - forecast['lowest_predicted_balance'], 2)),
                plan=[], proposal_validated=False, validation_errors=[message], message=message)


def _period_capacities(capacities, horizon):
    return {item['category']: max(0, math.floor(item['reduction_capacity'] * horizon / 30 / REDUCTION_STEP + 1e-9) * REDUCTION_STEP)
            for item in capacities if item['category'] in FLEXIBLE_CATEGORIES}


def validate_support_plan(forecast, safety_buffer, capacities, actions, confidence):
    """Validate untrusted category adjustments from a customer or an LLM.

    Caller supplies freshly computed forecast/capacities; never trust copies
    supplied by the LLM. Validation is NOT customer approval or execution.
    """
    if confidence == 'low':
        return _review(forecast, safety_buffer, 'The forecast is too uncertain for a firm spending plan.')
    if not isinstance(actions, list) or not 1 <= len(actions) <= len(FLEXIBLE_CATEGORIES):
        return _review(forecast, safety_buffer, 'Provide one to four flexible spending adjustments.')
    horizon = len(forecast['days'])
    limits = _period_capacities(capacities, horizon)
    seen, plan = set(), []
    for action in actions:
        if not isinstance(action, dict) or set(action) != {'category', 'reduce_by'}:
            return _review(forecast, safety_buffer, 'Each adjustment needs only category and reduce_by.')
        category = action['category']
        if not isinstance(category, str) or category not in limits or category in seen:
            return _review(forecast, safety_buffer, 'Category is protected, unavailable, unknown or repeated.')
        seen.add(category)
        try:
            amount = _money(action['reduce_by'])
        except ValueError as error:
            return _review(forecast, safety_buffer, str(error))
        if amount < MINIMUM_REDUCTION or amount % REDUCTION_STEP != 0:
            return _review(forecast, safety_buffer, 'Use reductions of at least €10 in €5 steps.')
        if amount > limits[category]:
            return _review(forecast, safety_buffer, 'Reduction exceeds the personal capacity for this period.')
        plan.append(dict(category=category, reduce_by=amount))
    total = sum(action['reduce_by'] for action in plan)
    adjusted = [dict(date=day['date'], balance=round(day['balance'] + total * offset / horizon, 2))
                for offset, day in enumerate(forecast['days'], 1)]
    new_lowest = min(day['balance'] for day in adjusted)
    if new_lowest < safety_buffer or total / horizon > forecast['daily_variable_spend']:
        return _review(forecast, safety_buffer, 'These adjustments do not protect every forecast day within available spending.')
    return dict(status='support_available', kind='spending_reduction',
                gap_amount=max(0, round(safety_buffer - forecast['lowest_predicted_balance'], 2)),
                plan=plan, proposal_validated=True, new_lowest_predicted_balance=new_lowest,
                adjusted_days=adjusted, total_reduction=total,
                start_date=forecast['days'][0]['date'], end_date=forecast['days'][-1]['date'],
                assumption='Spending reductions start tomorrow and accrue evenly across the forecast period.',
                customer_approval_required=True)


def create_support_plan(forecast, safety_buffer, capacities, confidence):
    gap_amount = max(0.0, round(float(safety_buffer) - forecast['lowest_predicted_balance'], 2))
    if confidence == 'low':
        return _review(forecast, safety_buffer, 'The forecast is too uncertain for a firm spending plan.')
    if gap_amount == 0:
        return dict(status='safe', gap_amount=0.0, plan=[])
    horizon = len(forecast['days'])
    required_daily = max(max(0, safety_buffer - day['balance']) / offset
                         for offset, day in enumerate(forecast['days'], 1))
    remaining = math.ceil(required_daily * horizon / REDUCTION_STEP - 1e-9) * REDUCTION_STEP
    plan = []
    for category, available in _period_capacities(capacities, horizon).items():
        if available < MINIMUM_REDUCTION:
            continue
        reduction = min(available, max(MINIMUM_REDUCTION, remaining))
        plan.append(dict(category=category, reduce_by=reduction))
        remaining -= reduction
        if remaining <= 0:
            break
    if remaining > 0:
        return _review(forecast, safety_buffer, 'No practical spending plan can restore the buffer within the estimated capacity.')
    return validate_support_plan(forecast, safety_buffer, capacities, plan, confidence)


def create_savings_proposal(forecast, current_balance, safety_buffer, confidence,
                            eligible=True, proposed_amount=None):
    """Suggest a one-off allocation to savings, never a transfer execution.

    Demo policy: retain the buffer plus max(€100, seven days of variable spend),
    suggest 25% of remaining headroom rounded down to €25, minimum €50.
    An edited proposal may use at most that same conservative allowance.
    """
    if confidence == 'low':
        return _review(forecast, safety_buffer, 'The forecast is too uncertain for a savings proposal.')
    reserve = round(max(100, 7 * forecast['daily_variable_spend']), 2)
    headroom = max(0, min(float(current_balance), forecast['lowest_predicted_balance']) - safety_buffer - reserve)
    allowance = math.floor(headroom * 0.25 / SAVINGS_STEP) * SAVINGS_STEP
    available = eligible and confidence == 'high' and len(forecast['days']) >= 30 and allowance >= MINIMUM_SAVINGS
    if not available:
        if proposed_amount is not None:
            return _review(forecast, safety_buffer, 'A savings proposal is unavailable with this history, forecast or preference.')
        return dict(status='safe', gap_amount=0.0, plan=[])
    try:
        amount = allowance if proposed_amount is None else _money(proposed_amount)
    except ValueError as error:
        return _review(forecast, safety_buffer, str(error))
    if amount < MINIMUM_SAVINGS or amount % SAVINGS_STEP != 0 or amount > allowance:
        return _review(forecast, safety_buffer, 'Savings amount must be at least €50, in €25 steps, within the calculated allowance.')
    adjusted = [dict(date=day['date'], balance=round(day['balance'] - amount, 2)) for day in forecast['days']]
    return dict(status='savings_opportunity', kind='savings', gap_amount=0.0, plan=[],
                savings_amount=amount, max_savings_proposal=allowance, extra_reserve=reserve,
                new_lowest_predicted_balance=min(day['balance'] for day in adjusted),
                adjusted_days=adjusted, proposal_validated=True,
                start_date=forecast['days'][0]['date'], end_date=forecast['days'][-1]['date'],
                assumption='One allocation to savings at the start of the forecast; no interest or automatic monthly repetition.',
                customer_approval_required=True, execution_supported=False)


def update_forecast_learning(customer_id, predicted_variable_spend, actual_variable_spend,
                             observed_days, observation_end, previous_state=None, learning_rate=0.3):
    """Update a customer-specific daily bias after a completed observation window.

    Predicted spend is the saved prediction INCLUDING the previous correction.
    Actual spend must cover the same variable categories and dates. The caller
    persists the returned state; feedback clicks are not training observations.
    """
    if type(observed_days) is not int or observed_days <= 0:
        raise ValueError('observed_days must be a positive integer')
    values = [float(predicted_variable_spend), float(actual_variable_spend), float(learning_rate)]
    if not all(math.isfinite(value) for value in values) or min(values[:2]) < 0 or not 0 < learning_rate <= 1:
        raise ValueError('Expected finite nonnegative spending and learning_rate in (0, 1]')
    state = previous_state or {}
    end = _as_date(observation_end)
    if state:
        if state['customer_id'] != customer_id:
            raise ValueError('Learning state belongs to another customer')
        start = end - timedelta(days=observed_days - 1)
        if start <= _as_date(state['observation_end']):
            raise ValueError('Observation windows must not overlap or repeat')
    daily_error = (float(actual_variable_spend) - float(predicted_variable_spend)) / observed_days
    return dict(customer_id=customer_id,
                daily_spend_adjustment=round(float(state.get('daily_spend_adjustment', 0)) + learning_rate * daily_error, 4),
                observation_end=end.isoformat(),
                observation_count=state.get('observation_count', 0) + 1,
                last_daily_error=round(daily_error, 4))


def filter_customer_transactions(customer_id, transactions):
    """Enforce single-customer input before calculation or explanation.

    The caller must still enforce authorization and filter the database query.
    Missing ownership must not silently be treated as the selected customer's.
    """
    if type(customer_id) is not int or customer_id <= 0:
        raise ValueError('customer_id must be a positive integer')
    selected = []
    for row in transactions:
        owner = row.get('customer_id')
        if type(owner) is not int or owner <= 0:
            raise ValueError('Every transaction must include a positive integer customer_id')
        if owner != customer_id:
            raise ValueError('Transactions must all belong to the selected customer; mixed input is not allowed')
        selected.append(row)
    return selected


def future(customer: dict[str, Any], transactions: list[dict[str, Any]], as_of: date,
           horizon_days: int = 30, learning_state=None, preferences=None, proposal=None) -> dict[str, Any]:
    """Caller supplies history and balance for the SAME account/balance scope.

    Include both transfer legs when both accounts belong to the balance scope;
    a transfer leaving that scope must remain a net cash outflow.
    """
    if type(horizon_days) is not int or not 1 <= horizon_days <= 90:
        raise ValueError('horizon_days must be between 1 and 90')
    if not isinstance(customer, dict):
        raise ValueError('Provide exactly one customer object')
    transactions = filter_customer_transactions(customer.get('customer_id'), transactions)
    as_of = _as_date(as_of)
    balance = _money(customer['current_balance'])
    safety_buffer = _money(customer['safety_buffer'])
    if safety_buffer < 0:
        raise ValueError('safety_buffer must be nonnegative')
    preferences = {} if preferences is None else preferences
    if not isinstance(preferences, dict) or set(preferences) - {'protected_categories', 'suggest_savings'}:
        raise ValueError('Unsupported preferences')
    protected = preferences.get('protected_categories', [])
    suggest_savings = preferences.get('suggest_savings', True)
    if not isinstance(protected, list) or not all(isinstance(item, str) for item in protected) or type(suggest_savings) is not bool:
        raise ValueError('Expected protected_categories list and suggest_savings boolean')
    adjustment = 0.0
    if learning_state:
        if learning_state['customer_id'] != customer['customer_id'] or _as_date(learning_state['observation_end']) > as_of:
            raise ValueError('Learning state must belong to this customer and precede the forecast')
        adjustment = float(learning_state['daily_spend_adjustment'])
        if not math.isfinite(adjustment):
            raise ValueError('Invalid learned adjustment')
    enriched = detect_recurring_patterns(
        [row for row in transactions if _as_date(row['transaction_date']) <= as_of], as_of)
    forecast = build_forecast(balance, enriched, as_of, horizon_days, adjustment)
    confidence_score, confidence = calculate_confidence(enriched)
    history_covered = bool(enriched) and min(item['date'] for item in enriched) <= as_of - timedelta(days=HISTORY_DAYS - 1)
    warnings = []
    if not history_covered:
        warnings.append('Insufficient history: supply at least 90 days of transaction history.')
    if enriched and max(item['date'] for item in enriched) < as_of - timedelta(days=35):
        warnings.append('Transaction history is stale; refresh it before relying on this forecast.')
    if any(item['is_recurring'] and not item['is_recurring_active'] for item in enriched):
        warnings.append('A recurring payment is overdue by more than five days; confirm whether it stopped or data is missing.')
    if warnings:
        confidence_score, confidence = min(confidence_score, 0.35), 'low'
    capacities = calculate_reduction_capacity(enriched, as_of)
    capacities = [item for item in capacities if item['category'] not in protected]
    plan = create_support_plan(forecast, safety_buffer, capacities, confidence)
    has_expected_income = any(event['transaction_type'] == 'income'
                              for day in forecast['days'] for event in day['recurring_events'])
    savings_eligible = suggest_savings and history_covered and has_expected_income
    if proposal is not None:
        if not isinstance(proposal, dict):
            raise ValueError('proposal must be an object')
        if proposal.get('type') == 'spending_reduction' and set(proposal) == {'type', 'actions'}:
            if forecast['lowest_predicted_balance'] >= safety_buffer:
                plan = _review(forecast, safety_buffer, 'There is no predicted gap requiring a spending reduction.')
            else:
                plan = validate_support_plan(forecast, safety_buffer, capacities, proposal['actions'], confidence)
        elif proposal.get('type') == 'savings' and set(proposal) == {'type', 'amount'}:
            if forecast['lowest_predicted_balance'] < safety_buffer or proposal['amount'] is None:
                plan = _review(forecast, safety_buffer, 'Savings cannot be proposed while a buffer gap exists or without an amount.')
            else:
                plan = create_savings_proposal(forecast, balance, safety_buffer, confidence,
                                               savings_eligible, proposal['amount'])
        else:
            raise ValueError('Unsupported proposal type or fields')
    elif plan['status'] == 'safe':
        plan = create_savings_proposal(forecast, balance, safety_buffer, confidence, savings_eligible)

    # Neither an LLM proposal nor disabling savings may bypass data quality.
    if warnings:
        plan = _review(forecast, safety_buffer, ' '.join(warnings))

    drivers = []
    for day in forecast["days"]:
        for event in day["recurring_events"]:
            if event["amount"] < 0:
                drivers.append({
                    "merchant": event["merchant"],
                    "category": event["category"],
                    "amount": abs(event["amount"]),
                    "date": day["date"],
                })

    return {
        "customer_id": customer["customer_id"],
        "as_of_date": as_of.isoformat(),
        "safety_buffer": float(customer["safety_buffer"]),
        "forecast": {**forecast, "confidence": confidence, "confidence_score": confidence_score},
        "data_quality": {"history_covered": history_covered, "warnings": warnings},
        "risk": {
            "buffer_breach": forecast["lowest_predicted_balance"] < float(customer["safety_buffer"]),
            "gap_amount": plan["gap_amount"],
            "drivers": drivers,
        },
        "recommendation": plan,
        "recommendation_constraints": {
            "reduction_step": REDUCTION_STEP, "minimum_reduction": MINIMUM_REDUCTION,
            "period_reduction_limits": _period_capacities(capacities, horizon_days),
            "protected_categories": sorted(ESSENTIAL_CATEGORIES | set(protected)),
            "savings_step": SAVINGS_STEP, "minimum_savings": MINIMUM_SAVINGS,
        },
        "derived_transaction_fields": [
            "transaction_type", "is_recurring", "is_essential", "is_flexible"
        ],
    }
