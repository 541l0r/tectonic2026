"""Verify the shared demo fixtures, ledger reconciliation and engine outcomes."""

from datetime import date
from pathlib import Path
import json
import subprocess
import sys
import unittest

from future_demo_data import AS_OF, START, build_data, run_demo, seed_sql
from future_engine import future


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
        demos = [run_demo(customer_id=customer_id) for customer_id in (1001, 1002, 1003)]
        self.assertEqual([demo['result']['recommendation']['status'] for demo in demos],
                         ['support_available', 'savings_opportunity', 'review_needed'])
        self.assertEqual(demos[0]['result']['risk']['gap_amount'], 66.0)
        self.assertEqual(demos[1]['result']['recommendation']['plan'], [])
        self.assertEqual(demos[2]['result']['forecast']['confidence'], 'low')
        self.assertEqual(demos[2]['result']['recommendation']['plan'], [])

    def test_alex_rounded_plan_and_llm_adjustment_are_recalculated(self):
        customers, transactions = build_data()
        rows = [row for row in transactions if row['customer_id'] == 1001]
        original = future(customers[0], rows, AS_OF)['recommendation']
        self.assertEqual(original['plan'], [{'category': 'dining', 'reduce_by': 70},
                                           {'category': 'shopping', 'reduce_by': 10}])
        revised = future(customers[0], rows, AS_OF, proposal={
            'type': 'spending_reduction',
            'actions': [{'category': 'dining', 'reduce_by': 40}, {'category': 'shopping', 'reduce_by': 40}],
        })['recommendation']
        self.assertTrue(revised['proposal_validated'])
        self.assertEqual(revised['new_lowest_predicted_balance'], 256)
        self.assertTrue(revised['customer_approval_required'])
        blocked = future(customers[0], rows, AS_OF,
                         preferences={'protected_categories': ['dining']},
                         proposal={'type': 'spending_reduction', 'actions': original['plan']})
        self.assertFalse(blocked['recommendation']['proposal_validated'])

    def test_sam_savings_can_be_reduced_but_not_increased_past_allowance(self):
        customers, transactions = build_data()
        rows = [row for row in transactions if row['customer_id'] == 1002]
        original = future(customers[1], rows, AS_OF)['recommendation']
        self.assertEqual(original['savings_amount'], 625)
        self.assertEqual(original['new_lowest_predicted_balance'], 2345.67)
        revised = future(customers[1], rows, AS_OF, proposal={'type': 'savings', 'amount': 500})['recommendation']
        self.assertTrue(revised['proposal_validated'])
        self.assertEqual(revised['new_lowest_predicted_balance'], 2470.67)
        excessive = future(customers[1], rows, AS_OF, proposal={'type': 'savings', 'amount': 650})['recommendation']
        self.assertFalse(excessive['proposal_validated'])
        opted_out = future(customers[1], rows, AS_OF, preferences={'suggest_savings': False},
                           proposal={'type': 'savings', 'amount': 500})['recommendation']
        self.assertFalse(opted_out['proposal_validated'])

    def test_mixed_customer_input_is_rejected_before_forecasting(self):
        customers, transactions = build_data()
        for customer in customers:
            with self.subTest(customer=customer['customer_id']):
                own_rows = [row for row in transactions if row['customer_id'] == customer['customer_id']]
                self.assertEqual(future(customer, own_rows, AS_OF)['customer_id'], customer['customer_id'])
                with self.assertRaisesRegex(ValueError, 'mixed input is not allowed'):
                    future(customer, transactions, AS_OF)

    def test_single_customer_demo_returns_only_selected_customer(self):
        for customer_id in (1001, 1002, 1003):
            demo = run_demo(customer_id=customer_id)
            self.assertIsInstance(demo, dict)
            self.assertEqual(demo['result']['customer_id'], customer_id)
            self.assertEqual(demo['customer']['customer_id'], customer_id)
        with self.assertRaises(ValueError):
            run_demo(customer_id=9999)

    def test_transactions_without_ownership_fail_explicitly(self):
        customers, transactions = build_data()
        row = dict(transactions[0])
        del row['customer_id']
        with self.assertRaisesRegex(ValueError, 'Every transaction must include'):
            future(customers[0], [row], AS_OF)

    def test_customer_ids_are_not_coerced_or_guessed(self):
        customers, transactions = build_data()
        for invalid in (None, True, '1001', 1001.0):
            with self.subTest(customer_id=invalid), self.assertRaises(ValueError):
                future({**customers[0], 'customer_id': invalid}, transactions, AS_OF)

    def test_foreign_only_history_is_not_silently_treated_as_empty(self):
        customers, transactions = build_data()
        others = [row for row in transactions if row['customer_id'] != customers[0]['customer_id']]
        with self.assertRaisesRegex(ValueError, 'must all belong'):
            future(customers[0], others, AS_OF)

    def test_customer_group_is_rejected(self):
        customers, transactions = build_data()
        with self.assertRaisesRegex(ValueError, 'exactly one customer object'):
            future(customers, transactions, AS_OF)

    def test_cli_requires_customer_and_emits_one_object(self):
        script = str(Path(__file__).with_name('future_demo_data.py'))
        missing = subprocess.run([sys.executable, script], capture_output=True, text=True)
        self.assertNotEqual(missing.returncode, 0)
        self.assertEqual(missing.stdout, '')
        selected = subprocess.run([sys.executable, script, '--customer-id', '1001'],
                                  capture_output=True, text=True, check=True)
        result = json.loads(selected.stdout)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['customer']['customer_id'], 1001)
        self.assertEqual(result['result']['customer_id'], 1001)
        self.assertNotIn('Sam Safe', selected.stdout)
        self.assertNotIn('Robin Uncertain', selected.stdout)


if __name__ == '__main__':
    unittest.main()
