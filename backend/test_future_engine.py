"""Executable checks for the product algorithm; no database or Flask required."""

from datetime import date
import unittest

from future_engine import classify_transaction, detect_recurring_patterns, future


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


if __name__ == "__main__":
    unittest.main()
