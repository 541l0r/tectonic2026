"""Verify the shared demo fixtures, ledger reconciliation and engine outcomes."""

from datetime import date
from pathlib import Path
import unittest

from future_demo_data import AS_OF, START, build_data, run_demo, seed_sql


class DemoDataTests(unittest.TestCase):
    def test_schema_contains_exact_generated_seed(self):
        schema = (Path(__file__).resolve().parents[1] / "sql/schema.sql").read_text()
        self.assertTrue(schema.endswith(seed_sql()))

    def test_history_is_complete_for_six_months_and_balances_reconcile(self):
        customers, transactions = build_data()
        self.assertEqual(len(transactions), 389)
        self.assertEqual(len({row['transaction_id'] for row in transactions}), 389)
        for customer in customers:
            rows = [row for row in transactions if row['customer_id'] == customer['customer_id']]
            self.assertEqual(customer['opening_balance'] + sum(row['amount'] for row in rows),
                             customer['current_balance'])
            self.assertEqual({row['transaction_date'][5:7] for row in rows},
                             {'04', '05', '06', '07', '08', '09'})
            self.assertTrue(all(START <= date.fromisoformat(row['transaction_date'][:10]) <= AS_OF
                                for row in rows))
            for month in range(4, 10):
                monthly = [row for row in rows if row['transaction_date'][5:7] == f'{month:02d}']
                self.assertTrue(any(row['merchant_category'] == 'groceries' for row in monthly))
                self.assertTrue(any(row['amount'] > 0 for row in monthly))

    def test_three_intended_outcomes(self):
        demos = run_demo()
        self.assertEqual([demo['result']['recommendation']['status'] for demo in demos],
                         ['support_available', 'safe', 'review_needed'])
        self.assertEqual(demos[0]['result']['risk']['gap_amount'], 66.0)
        self.assertEqual(demos[1]['result']['recommendation']['plan'], [])
        self.assertEqual(demos[2]['result']['forecast']['confidence'], 'low')
        self.assertEqual(demos[2]['result']['recommendation']['plan'], [])


if __name__ == '__main__':
    unittest.main()
