"""Executable checks for the product algorithm; no database or Flask required."""

from datetime import date
import unittest

from future_engine import (classify_transaction, create_support_plan,
                           create_savings_proposal, detect_recurring_patterns,
                           future, update_forecast_learning)


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
            "customer_id": 1,
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


    def test_safe_customer_with_savings_disabled_receives_no_plan(self):
        customer = {**self.customer, "current_balance": 4000.0}
        result = future(customer, self.transactions, date(2026, 9, 30),
                        preferences={'suggest_savings': False})
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

    def test_default_reductions_are_practical_amounts(self):
        result = future(self.customer, self.transactions, date(2026, 9, 30))
        for action in result['recommendation']['plan']:
            self.assertGreaterEqual(action['reduce_by'], 10)
            self.assertEqual(action['reduce_by'] % 5, 0)

    def test_savings_proposal_protects_buffer_and_extra_reserve(self):
        customer = {**self.customer, 'current_balance': 4000}
        result = future(customer, self.transactions, date(2026, 9, 30))
        plan = result['recommendation']
        self.assertEqual(plan['status'], 'savings_opportunity')
        self.assertEqual(plan['savings_amount'] % 25, 0)
        self.assertTrue(all(day['balance'] >= 250 + plan['extra_reserve'] for day in plan['adjusted_days']))
        self.assertTrue(plan['customer_approval_required'])
        self.assertFalse(plan['execution_supported'])

    def test_savings_cannot_spend_future_income_before_it_arrives(self):
        forecast = dict(lowest_predicted_balance=2000, daily_variable_spend=10,
                        days=[dict(date=f'2026-10-{day:02d}', balance=2000) for day in range(1, 31)])
        plan = create_savings_proposal(forecast, 260, 250, 'high')
        self.assertEqual(plan['status'], 'safe')

    def test_low_confidence_and_short_horizon_do_not_offer_savings(self):
        customer = {**self.customer, 'current_balance': 4000}
        short = future(customer, self.transactions, date(2026, 9, 30), horizon_days=7)
        self.assertNotEqual(short['recommendation']['status'], 'savings_opportunity')
        sparse = future(customer, [], date(2026, 9, 30))
        self.assertNotEqual(sparse['recommendation']['status'], 'savings_opportunity')

    def test_llm_cannot_reduce_protected_unknown_duplicate_or_tiny_categories(self):
        proposals = [
            [{'category': 'rent', 'reduce_by': 100}],
            [{'category': 'mystery', 'reduce_by': 100}],
            [{'category': 'dining', 'reduce_by': 1.34}],
            [{'category': 'dining', 'reduce_by': -20}],
            [{'category': 'dining', 'reduce_by': float('nan')}],
            [{'category': 'dining', 'reduce_by': 20}, {'category': 'dining', 'reduce_by': 20}],
            [{'category': 'shopping', 'reduce_by': 10000}],
        ]
        for actions in proposals:
            with self.subTest(actions=actions):
                result = future(self.customer, self.transactions, date(2026, 9, 30),
                                proposal={'type': 'spending_reduction', 'actions': actions})
                self.assertFalse(result['recommendation']['proposal_validated'])
                self.assertEqual(result['recommendation']['plan'], [])

    def test_savings_proposal_cannot_be_used_to_fix_a_cash_gap(self):
        result = future(self.customer, self.transactions, date(2026, 9, 30),
                        proposal={'type': 'savings', 'amount': 50})
        self.assertEqual(result['recommendation']['status'], 'review_needed')
        self.assertFalse(result['recommendation']['proposal_validated'])

    def test_stopped_salary_is_not_projected_or_counted_as_reliable(self):
        rows = [row for row in self.transactions if row['merchant_category'] != 'salary']
        rows += [self.transaction(f'old-salary-{month}', month, 28, 2100,
                                  'Acme', 'salary', 'bank_transfer') for month in (4, 5, 6)]
        result = future(self.customer, rows, date(2026, 9, 30))
        events = [event for day in result['forecast']['days'] for event in day['recurring_events']]
        self.assertFalse(any(event['transaction_type'] == 'income' for event in events))
        self.assertEqual(result['forecast']['confidence'], 'low')
        self.assertEqual(result['recommendation']['status'], 'review_needed')
        self.assertTrue(any('overdue' in warning for warning in result['data_quality']['warnings']))

    def test_recurring_freshness_expires_after_due_date_plus_grace(self):
        rows = [self.transaction(f'salary-{month}', month, 28, 2100,
                                 'Acme', 'salary', 'bank_transfer') for month in (6, 7, 8)]
        self.assertTrue(all(row['is_recurring_active'] for row in
                            detect_recurring_patterns(rows, date(2026, 10, 3))))
        expired = detect_recurring_patterns(rows, date(2026, 10, 4))
        self.assertTrue(all(row['is_recurring'] for row in expired))
        self.assertFalse(any(row['is_recurring_active'] for row in expired))

    def test_stopped_bill_requires_review_instead_of_claiming_extra_savings(self):
        rows = [row for row in self.transactions if row['merchant_category'] != 'rent']
        rows += [self.transaction(f'old-rent-{month}', month, 3, -900,
                                  'Home', 'rent', 'direct_debit') for month in (4, 5, 6)]
        result = future({**self.customer, 'current_balance': 10000}, rows, date(2026, 9, 30))
        self.assertEqual(result['recommendation']['status'], 'review_needed')
        self.assertNotIn('savings_amount', result['recommendation'])

    def test_recurring_outgoing_transfers_reduce_balance_but_are_not_spending(self):
        customer = {**self.customer, 'current_balance': 4000}
        transfers = [self.transaction(f'transfer-{month}', month, 15, -2900,
                                     'Own account savings', 'savings', 'internal_transfer')
                     for month in (7, 8, 9)]
        base = future(customer, self.transactions, date(2026, 9, 30))
        result = future(customer, self.transactions + transfers, date(2026, 9, 30))
        self.assertEqual(result['forecast']['daily_variable_spend'], base['forecast']['daily_variable_spend'])
        for index, day in enumerate(result['forecast']['days']):
            expected = base['forecast']['days'][index]['balance'] - (2900 if index >= 14 else 0)
            self.assertAlmostEqual(day['balance'], expected, places=2)
        self.assertTrue(result['risk']['buffer_breach'])
        self.assertNotEqual(result['recommendation']['status'], 'savings_opportunity')
        self.assertTrue(all(not row['is_flexible'] and not row['is_essential']
                            for row in detect_recurring_patterns(transfers)))

    def test_both_transfer_legs_cancel_within_same_balance_scope(self):
        transfers = [self.transaction(f'transfer-{month}-{amount}', month, 15, amount,
                                     'Own account transfer', 'savings', 'internal_transfer')
                     for month in (7, 8, 9) for amount in (-500, 500)]
        base = future(self.customer, self.transactions, date(2026, 9, 30))
        result = future(self.customer, self.transactions + transfers, date(2026, 9, 30))
        self.assertEqual([day['balance'] for day in result['forecast']['days']],
                         [day['balance'] for day in base['forecast']['days']])
        events = result['forecast']['days'][14]['recurring_events']
        self.assertEqual(sorted(event['amount'] for event in events), [-500, 500])
        self.assertTrue(all(event['transaction_type'] == 'transfer' for event in events))

    def test_incoming_transfers_do_not_substitute_for_salary_confidence(self):
        rows = [row for row in self.transactions if row['merchant_category'] != 'salary']
        rows += [self.transaction(f'incoming-{month}', month, 28, 2100,
                                  'Own account transfer', 'savings', 'internal_transfer')
                 for month in (7, 8, 9)]
        result = future({**self.customer, 'current_balance': 4000}, rows, date(2026, 9, 30))
        self.assertNotEqual(result['forecast']['confidence'], 'high')
        self.assertNotEqual(result['recommendation']['status'], 'savings_opportunity')

    def test_empty_short_stale_and_future_only_history_require_review(self):
        histories = [[], [row for row in self.transactions if '-09-' in row['transaction_date']],
                     [row for row in self.transactions if '-07-' in row['transaction_date']],
                     [self.transaction('future', 10, 2, -50, 'Shop', 'shopping', 'card')]]
        for rows in histories:
            for proposal in (None, {'type': 'savings', 'amount': 50},
                             {'type': 'spending_reduction', 'actions': [{'category': 'dining', 'reduce_by': 20}]}):
                with self.subTest(rows=len(rows), proposal=proposal):
                    result = future({**self.customer, 'current_balance': 10000}, rows,
                                    date(2026, 9, 30), proposal=proposal)
                    self.assertEqual(result['recommendation']['status'], 'review_needed')
                    self.assertFalse(result['recommendation']['proposal_validated'])
                    self.assertEqual(result['recommendation']['plan'], [])
                    self.assertTrue(result['data_quality']['warnings'])

    def test_low_confidence_without_gap_is_not_labelled_safe(self):
        rows = [self.transaction(f'pay-{month}', month, 1, amount,
                                 'Client', 'freelance_income', 'bank_transfer')
                for month, amount in ((7, 500), (8, 1700), (9, 800))]
        result = future({**self.customer, 'current_balance': 10000}, rows, date(2026, 9, 30),
                        preferences={'suggest_savings': False})
        self.assertEqual(result['data_quality']['warnings'], [])
        self.assertEqual(result['recommendation']['status'], 'review_needed')


if __name__ == "__main__":
    unittest.main()
