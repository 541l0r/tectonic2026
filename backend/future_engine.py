"""Deterministic cash-flow decision engine for the KBC Future MVP.

The engine deliberately derives financial labels from raw transactions. An LLM
may later explain these results, but it must not decide affordability, mark an
expense essential, or create an action plan.
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


def detect_recurring_patterns(transactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Mark monthly salary/bill patterns using merchant, date and amount regularity."""
    enriched = [classify_transaction(transaction) for transaction in transactions]
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for transaction in enriched:
        groups[(
            (transaction.get("merchant") or "").lower(),
            transaction["category"],
            transaction["transaction_type"],
        )].append(transaction)

    recurring_ids: set[Any] = set()
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
        # direct debits and bank transfers can become calendar events.
        scheduled_method = all(
            (item.get("payment_method") or "").lower()
            in {"direct_debit", "bank_transfer"}
            for item in group
        )
        monthly = all(gap == 1 for gap in gaps)
        days = [item['date'].day for item in group]
        stable_date = max(abs(day - median(days)) for day in days) <= 5
        if monthly and stable_amount and scheduled_method and stable_date:
            recurring_ids.update(item["transaction_id"] for item in group)

    for transaction in enriched:
        transaction["is_recurring"] = transaction["transaction_id"] in recurring_ids
    return enriched


def _recurring_events(enriched: list[dict[str, Any]], as_of: date, horizon_days: int) -> list[dict[str, Any]]:
    by_merchant: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for transaction in enriched:
        if transaction["is_recurring"]:
            by_merchant[(
                (transaction.get("merchant") or "").lower(),
                transaction["category"],
                transaction["transaction_type"],
            )].append(transaction)

    end_date = as_of + timedelta(days=horizon_days)
    events: list[dict[str, Any]] = []
    for transactions in by_merchant.values():
        transactions.sort(key=lambda item: item["date"])
        last = transactions[-1]
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
        if item["is_recurring"] and item["transaction_type"] == "income"
    }
    essential_patterns = {
        item.get("merchant") for item in enriched
        if item["is_recurring"] and item["is_essential"]
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
        if not item["is_flexible"]:
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


def create_support_plan(
    forecast: dict[str, Any], safety_buffer: float, capacities: list[dict[str, Any]], confidence: str
) -> dict[str, Any]:
    gap_amount = max(0.0, round(float(safety_buffer) - forecast["lowest_predicted_balance"], 2))
    if gap_amount == 0:
        return {"status": "safe", "gap_amount": 0.0, "plan": []}
    if confidence == "low":
        return {
            "status": "review_needed",
            "gap_amount": gap_amount,
            "plan": [],
            "message": "Your income pattern is irregular, so KBC Future will not make a firm spending recommendation.",
        }

    # Reductions accrue gradually. Find the daily saving needed to protect
    # EVERY forecast day, then cap it using monthly flexible capacity.
    horizon = len(forecast['days'])
    required_daily = max(max(0, safety_buffer - day['balance']) / offset
                         for offset, day in enumerate(forecast['days'], 1))
    remaining = math.ceil(required_daily * horizon * 100 - 1e-9) / 100
    plan = []
    for capacity in capacities:
        if capacity['category'] not in FLEXIBLE_CATEGORIES:
            continue
        available = math.floor(capacity['reduction_capacity'] * horizon / 30 * 100 + 1e-9) / 100
        reduction = min(remaining, available)
        if reduction > 0:
            plan.append({"category": capacity["category"], "reduce_by": round(reduction, 2)})
            remaining = round(remaining - reduction, 2)
        if remaining <= 0:
            break
    total = round(sum(action['reduce_by'] for action in plan), 2)
    adjusted = [dict(date=day['date'], balance=round(day['balance'] + total * offset / horizon, 2))
                for offset, day in enumerate(forecast['days'], 1)]
    new_lowest = min(day['balance'] for day in adjusted)
    if remaining > 0 or new_lowest < safety_buffer or total / horizon > forecast['daily_variable_spend']:
        return {
            "status": "review_needed",
            "gap_amount": gap_amount,
            "plan": plan,
            "message": "A safe reduction plan cannot fully restore your buffer. Offer a review or human support.",
        }
    return {
        "status": "support_available",
        "gap_amount": gap_amount,
        "plan": plan,
        "new_lowest_predicted_balance": new_lowest,
        "adjusted_days": adjusted,
        "total_reduction": total,
        "start_date": forecast['days'][0]['date'],
        "end_date": forecast['days'][-1]['date'],
        "assumption": "Spending reductions start tomorrow and accrue evenly across the forecast period.",
        "customer_approval_required": True,
    }


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


def future(customer: dict[str, Any], transactions: list[dict[str, Any]], as_of: date,
           horizon_days: int = 30, learning_state=None) -> dict[str, Any]:
    """Standalone tool; caller supplies history, snapshot and optional learned state."""
    if type(horizon_days) is not int or not 1 <= horizon_days <= 90:
        raise ValueError('horizon_days must be between 1 and 90')
    as_of = _as_date(as_of)
    adjustment = 0.0
    if learning_state:
        if learning_state['customer_id'] != customer['customer_id'] or _as_date(learning_state['observation_end']) > as_of:
            raise ValueError('Learning state must belong to this customer and precede the forecast')
        adjustment = float(learning_state['daily_spend_adjustment'])
        if not math.isfinite(adjustment):
            raise ValueError('Invalid learned adjustment')
    enriched = detect_recurring_patterns([row for row in transactions if _as_date(row['transaction_date']) <= as_of])
    forecast = build_forecast(customer["current_balance"], enriched, as_of, horizon_days, adjustment)
    confidence_score, confidence = calculate_confidence(enriched)
    capacities = calculate_reduction_capacity(enriched, as_of)
    plan = create_support_plan(forecast, float(customer["safety_buffer"]), capacities, confidence)

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
        "risk": {
            "buffer_breach": forecast["lowest_predicted_balance"] < float(customer["safety_buffer"]),
            "gap_amount": plan["gap_amount"],
            "drivers": drivers,
        },
        "recommendation": plan,
        "derived_transaction_fields": [
            "transaction_type", "is_recurring", "is_essential", "is_flexible"
        ],
    }
