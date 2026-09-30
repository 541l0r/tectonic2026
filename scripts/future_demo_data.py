"""Reproducible synthetic fixtures in Damiens's existing SQL structure.

Print SQL with --sql; otherwise require --customer-id and return ONE customer.
--database reads the local Compose database instead. No database or file writes
are performed by this script.
"""

import argparse
from datetime import date
from decimal import Decimal
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from future_engine import future


AS_OF = date(2026, 9, 30)
START = date(2026, 4, 1)


def build_data():
    customers = [
        dict(customer_id=1001, name="Alex Demo", current_balance=Decimal("1940.00"), safety_buffer=250),
        dict(customer_id=1002, name="Sam Safe", current_balance=Decimal("4500.00"), safety_buffer=300),
        dict(customer_id=1003, name="Robin Uncertain", current_balance=Decimal("900.00"), safety_buffer=250),
    ]
    transactions = []

    def add(customer_id, month, day, amount, merchant, category, method="card"):
        transactions.append(dict(
            customer_id=customer_id, product_id=customer_id + 1000,
            transaction_date=f"2026-{month:02d}-{day:02d} 12:00:00",
            amount=Decimal(str(amount)).quantize(Decimal("0.01")),
            merchant=merchant, merchant_category=category, payment_method=method,
        ))

    def spread(customer_id, month, total, days, merchant, category):
        cents = int(Decimal(str(total)) * 100)
        quotient, remainder = divmod(cents, len(days))
        for index, day in enumerate(days):
            add(customer_id, month, day, -Decimal(quotient + (index < remainder)) / 100,
                merchant, category)

    for index, month in enumerate(range(4, 10)):
        # Alex: ordinary bills plus changing discretionary spending. The April
        # repair is outside the current 90-day forecast window, but reconciles
        # the six-month ledger and illustrates a non-recurring transaction.
        add(1001, month, 28, 2100, "Demo Employer A", "salary", "bank_transfer")
        for day, amount, merchant, category in (
            (3, -900, "Demo Housing A", "rent"),
            (12, -90, "Demo Insurer A", "insurance"),
            (18, -100, "Demo Energy A", "utilities"),
        ):
            add(1001, month, day, amount, merchant, category, "direct_debit")
        spread(1001, month, [312, 326, 318, 310, 320, 330][index],
               [2, 6, 10, 14, 18, 22, 26, 29], "Demo Grocer A", "groceries")
        spread(1001, month, 60, [5, 12, 19, 26], "Demo Transit A", "transport")
        spread(1001, month, [140, 180, 220, 80, 200, 320][index],
               [7, 14, 21, 27], "Demo Cafe A", "dining")
        spread(1001, month, [100, 120, 160, 40, 160, 280][index],
               [8, 17, 25], "Demo Shop A", "shopping")

        # Sam: complete everyday-spending history each month, not just salary
        # and rent. A transfer to an unmodelled savings account is explicit.
        add(1002, month, 25, 2800, "Demo Employer B", "salary", "bank_transfer")
        for day, amount, merchant, category in (
            (2, -850, "Demo Housing B", "rent"),
            (11, -80, "Demo Insurer B", "insurance"),
            (18, -110, "Demo Energy B", "utilities"),
        ):
            add(1002, month, day, amount, merchant, category, "direct_debit")
        spread(1002, month, [320, 335, 315, 340, 330, 350][index],
               [2, 6, 10, 14, 18, 22, 26, 29], "Demo Grocer B", "groceries")
        spread(1002, month, 80, [5, 12, 19, 26], "Demo Transit B", "transport")
        spread(1002, month, [100, 110, 90, 120, 100, 110][index],
               [7, 14, 21, 27], "Demo Cafe B", "dining")
        spread(1002, month, [80, 100, 60, 90, 70, 85][index],
               [8, 17, 25], "Demo Shop B", "shopping")

        # Robin: regular essentials but income varies by counterparty, date
        # and amount. No dependable salary is supplied to the model.
        add(1003, month, 4, -620, "Demo Housing C", "rent", "bank_transfer")
        spread(1003, month, [230, 255, 245, 260, 240, 270][index],
               [2, 6, 10, 14, 18, 22, 26, 29], "Demo Grocer C", "groceries")
        spread(1003, month, 45, [5, 12, 19, 26], "Demo Transit C", "transport")
        spread(1003, month, [60, 120, 40, 90, 50, 110][index],
               [7, 14, 21, 27], "Demo Cafe C", "dining")

    add(1001, 4, 29, -1200, "Demo Repair", "home_repair", "bank_transfer")
    add(1002, 6, 29, -5000, "Own account savings", "savings", "internal_transfer")
    for month, day, amount, counterparty in (
        (4, 8, 1500, "A"), (4, 24, 350, "B"), (5, 16, 780, "C"),
        (6, 5, 1200, "A"), (6, 27, 400, "D"), (7, 9, 1050, "B"),
        (8, 19, 720, "A"), (9, 6, 350, "C"), (9, 23, 280, "D"),
    ):
        add(1003, month, day, amount, f"Demo Freelance Client {counterparty}",
            "freelance_income", "bank_transfer")

    transactions.sort(key=lambda row: (row["customer_id"], row["transaction_date"], row["merchant"]))
    for index, row in enumerate(transactions, 1):
        row["transaction_id"] = 900000 + index
    for customer in customers:
        net = sum(row["amount"] for row in transactions if row["customer_id"] == customer["customer_id"])
        customer["opening_balance"] = customer["current_balance"] - net
    return customers, transactions


def sql_value(value):
    if isinstance(value, str):
        return "'" + value.replace("'", "''") + "'"
    return str(value)


def seed_sql():
    customers, transactions = build_data()
    statements = [
        "-- SYNTHETIC DEMO ONLY. Generated by scripts/future_demo_data.py --sql.",
        "-- Six months: 2026-04-01 through 2026-09-30; balances at 2026-09-30 close.",
        "-- Fresh database seed. Do not run against an existing populated database.",
        "START TRANSACTION;",
    ]

    def insert(table, fields, rows):
        statements.append("INSERT INTO " + table + " (" + ", ".join(fields) + ") VALUES\n    "
                          + ",\n    ".join("(" + ", ".join(sql_value(row[field]) for field in fields) + ")" for row in rows) + ";")

    insert("customers", ["customer_id", "name", "current_balance", "safety_buffer"], customers)
    insert("customer_preferences", ["customer_id", "advice_opt_in", "notification_preference"],
           [dict(customer_id=c["customer_id"], advice_opt_in=1, notification_preference="in_app") for c in customers])
    insert("products", ["product_id", "product_type", "product_amount"],
           [dict(product_id=c["customer_id"] + 1000, product_type="current_account", product_amount=c["current_balance"]) for c in customers])
    insert("customer_product", ["customer_id", "product_id"],
           [dict(customer_id=c["customer_id"], product_id=c["customer_id"] + 1000) for c in customers])
    insert("transactions", ["transaction_id", "customer_id", "product_id", "transaction_date", "amount", "merchant", "merchant_category", "payment_method"], transactions)
    insert("events", ["event_id", "event_type", "event_date", "event_value"],
           [dict(event_id=c["customer_id"] + 7000, event_type="demo_opening_balance",
                 event_date="2026-04-01 00:00:00", event_value=str(c["opening_balance"])) for c in customers])
    insert("customer_events", ["event_id", "customer_id"],
           [dict(event_id=c["customer_id"] + 7000, customer_id=c["customer_id"]) for c in customers])
    statements.append("COMMIT;")
    return "\n\n".join(statements) + "\n"


def _check_demo_customer(customer_id):
    if type(customer_id) is not int or customer_id not in (1001, 1002, 1003):
        raise ValueError('Unknown demo customer; choose 1001, 1002 or 1003')


def read_local_database(customer_id):
    """Require a selected customer and scope both database queries to that ID."""
    _check_demo_customer(customer_id)
    # Interpolation is limited to the validated integer demo allowlist above.
    scope = f'= {customer_id}'
    def query(sql):
        process = subprocess.run(
            ["docker", "compose", "exec", "-T", "-e", "MYSQL_PWD=app", "mysql",
             "mysql", "-uapp", "--batch", "--skip-column-names", "app_dev", "-e", sql],
            cwd=Path(__file__).resolve().parents[1],
            check=True, capture_output=True, text=True,
        )
        return [json.loads(line, parse_float=Decimal) for line in process.stdout.splitlines() if line]

    customers = query(f"""
        SELECT JSON_OBJECT('customer_id', customer_id, 'name', name,
          'current_balance', current_balance, 'safety_buffer', safety_buffer)
        FROM customers WHERE customer_id {scope} ORDER BY customer_id;
    """)
    transactions = query(f"""
        SELECT JSON_OBJECT('transaction_id', transaction_id, 'customer_id', customer_id,
          'product_id', product_id, 'transaction_date', transaction_date, 'amount', amount,
          'merchant', merchant, 'merchant_category', merchant_category, 'payment_method', payment_method)
        FROM transactions WHERE customer_id {scope}
          AND transaction_date < '2026-10-01'
        ORDER BY customer_id, transaction_date, transaction_id;
    """)
    if len(customers) != 1:
        raise ValueError("Requested demo customer data is missing from the local database")
    return customers, transactions


def run_demo(customer_id, database=False):
    _check_demo_customer(customer_id)
    customers, transactions = read_local_database(customer_id) if database else build_data()
    customer = next(customer for customer in customers if customer['customer_id'] == customer_id)
    rows = [row for row in transactions if row['customer_id'] == customer_id]
    result = future(customer, rows, AS_OF)
    return dict(customer=customer, transaction_count=len(rows), result=result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--sql", action="store_true", help="Print the full development seed for the existing schema")
    parser.add_argument("--database", action="store_true", help="Read the mocks from local Compose MySQL")
    mode.add_argument("--customer-id", type=int, choices=(1001, 1002, 1003),
                      help="Required for a forecast: return only this customer")
    args = parser.parse_args()
    if args.sql:
        if args.customer_id is not None or args.database:
            parser.error('--sql cannot be combined with --database or --customer-id')
        print(seed_sql())
    else:
        result = run_demo(args.customer_id, database=args.database)
        print(json.dumps(result, default=str, indent=2))
