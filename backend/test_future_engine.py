"""Executable checks for the product algorithm; no database or Flask required."""

from datetime import date
import unittest

from future_engine import (classify_transaction, create_support_plan,
                           detect_recurring_patterns, future, update_forecast_learning)


class KbcFutureEngineTests(unittest.TestCase):
    def setUp(self):
        self.customer = {
            "customer_id": 1,
            "current_balance": 1678.0,
            "safety_buffer": 250.0,
        }
        self.transactions = []
        for month, dining, shopping in ((7, 10, 10), (8, 130, 100), (9, 240, 200)):
            self.transactions.extend([
                self.transaction(f"rent-{month}", month, 3, -900, "Home", "rent", "direct_debit"),
                self.transaction(f"insurance-{month}", month, 12, -180, "KBC Insurance", "insurance", "direct_debit"),
                self.transaction(f"salary-{month}", month, 28, 2100, "Acme", "salary", "bank_transfer"),
                self.transaction(f"grocery-{month}", month, 16, -245, "FreshMart", "groceries", "card"),
                self.transaction(f"dining-{month}", month, 20, -dining, "Bistro", "dining", "card"),
                self.transaction(f"shopping-{month}", month, 22, -shopping, "Shop", "shopping", "card"),
            ])

    @staticmethod
    def transaction(identifier, month, day, amount, merchant, category, method):
        return {
            "transaction_id": identifier,
            "transaction_date": f"2026-{month:02d}-{day:02d}T12:00:00",
            "amount": amount,
            "merchant": merchant,
            "merchant_category": category,
            "payment_method": method,
        }

    def test_gap_customer_gets_a_safe_personal_plan(self):
        result = future(self.customer, self.transactions, date(2026, 9, 30))

        self.assertTrue(result["risk"]["buffer_breach"])
        self.assertEqual(result["recommendation"]["status"], "support_available")
        self.assertTrue(result["recommendation"]["customer_approval_required"])
        self.assertGreaterEqual(
            result["recommendation"]["new_lowest_predicted_balance"],
            self.customer["safety_buffer"],
        )
        proposed_categories = {item["category"] for item in result["recommendation"]["plan"]}
        self.assertTrue(proposed_categories <= {"dining", "shopping"})

    def test_irregular_income_does_not_get_firm_advice(self):
        irregular = [
            self.transaction("pay-1", 7, 8, 980, "Client A", "freelance_income", "bank_transfer"),
            self.transaction("pay-2", 8, 15, 620, "Client B", "freelance_income", "bank_transfer"),
            self.transaction("pay-3", 9, 5, 350, "Client C", "freelance_income", "bank_transfer"),
        ]
        uncertain_customer = {**self.customer, "current_balance": 100.0}
        result = future(uncertain_customer, irregular, date(2026, 9, 30))

        self.assertEqual(result["forecast"]["confidence"], "low")
        self.assertEqual(result["recommendation"]["status"], "review_needed")


    def test_safe_customer_receives_no_reduction_plan(self):
        customer = {**self.customer, "current_balance": 4000.0}
        result = future(customer, self.transactions, date(2026, 9, 30))
        self.assertFalse(result["risk"]["buffer_breach"])
        self.assertEqual(result["recommendation"]["status"], "safe")
        self.assertEqual(result["recommendation"]["plan"], [])

    def test_insufficient_capacity_does_not_claim_gap_is_resolved(self):
        customer = {**self.customer, "current_balance": 500.0}
        result = future(customer, self.transactions, date(2026, 9, 30))
        self.assertEqual(result["recommendation"]["status"], "review_needed")
        self.assertNotIn("new_lowest_predicted_balance", result["recommendation"])

    def test_protected_and_unknown_categories_are_not_flexible(self):
        for category in ("rent", "groceries", "healthcare", "unknown"):
            with self.subTest(category=category):
                row = self.transaction("expense", 9, 3, -50, "Merchant", category, "card")
                classified = classify_transaction(row)
                self.assertFalse(classified["is_flexible"])
                self.assertEqual(classified["is_essential"], category != "unknown")

    def test_card_spending_is_not_scheduled_as_a_monthly_bill(self):
        rows = detect_recurring_patterns(self.transactions)
        groceries = [row for row in rows if row["category"] == "groceries"]
        self.assertTrue(groceries)
        self.assertTrue(all(not row["is_recurring"] for row in groceries))
        rent = [row for row in rows if row["category"] == "rent"]
        self.assertTrue(all(row["is_recurring"] for row in rent))

    def test_late_savings_cannot_repair_an_early_gap(self):
        forecast = dict(lowest_predicted_balance=200, daily_variable_spend=10,
                        days=[dict(date=f'2026-10-{day:02d}', balance=200 if day == 1 else 500)
                              for day in range(1, 31)])
        result = create_support_plan(forecast, 250,
                                     [dict(category='dining', reduction_capacity=100)], 'high')
        self.assertEqual(result['status'], 'review_needed')

    def test_approved_proposal_protects_every_simulated_day(self):
        result = future(self.customer, self.transactions, date(2026, 9, 30))
        plan = result['recommendation']
        self.assertEqual(plan['status'], 'support_available')
        self.assertTrue(all(day['balance'] >= self.customer['safety_buffer'] for day in plan['adjusted_days']))
        self.assertGreater(plan['total_reduction'], result['risk']['gap_amount'])

    def test_learning_changes_next_forecast_and_reduces_error_on_separate_example(self):
        baseline = future(self.customer, self.transactions, date(2026, 9, 30))
        daily = baseline['forecast']['daily_variable_spend']
        # Completed observation: €4/day above the saved prediction.
        state = update_forecast_learning(1, daily * 7, (daily + 4) * 7,
                                         7, date(2026, 9, 30))
        updated = future(self.customer, self.transactions, date(2026, 9, 30), learning_state=state)
        self.assertEqual(state['daily_spend_adjustment'], 1.2)
        self.assertAlmostEqual(updated['forecast']['daily_variable_spend'] - daily, 1.2, places=2)
        # Separate future example, not fed to the updater: same €4/day shift.
        held_out_actual = daily + 4
        self.assertLess(abs(updated['forecast']['daily_variable_spend'] - held_out_actual),
                        abs(daily - held_out_actual))
        self.assertEqual(updated['forecast']['days'][0]['recurring_events'],
                         baseline['forecast']['days'][0]['recurring_events'])

    def test_learning_rejects_repeated_windows_and_wrong_customer(self):
        state = update_forecast_learning(1, 70, 98, 7, date(2026, 9, 30))
        with self.assertRaises(ValueError):
            update_forecast_learning(1, 70, 98, 7, date(2026, 9, 30), state)
        with self.assertRaises(ValueError):
            future({**self.customer, 'customer_id': 2}, self.transactions,
                   date(2026, 9, 30), learning_state=state)

    def test_future_transactions_do_not_leak_into_prediction(self):
        baseline = future(self.customer, self.transactions, date(2026, 9, 30))
        future_row = self.transaction('future', 10, 2, -10000, 'Future Shop', 'shopping', 'card')
        self.assertEqual(baseline, future(self.customer, self.transactions + [future_row], date(2026, 9, 30)))

    def test_variable_monthly_dates_are_not_treated_as_reliable_schedule(self):
        rows = [self.transaction(str(month), month, day, 1000, 'Client', 'income', 'bank_transfer')
                for month, day in [(7, 2), (8, 16), (9, 28)]]
        self.assertTrue(all(not row['is_recurring'] for row in detect_recurring_patterns(rows)))


if __name__ == "__main__":
    unittest.main()
