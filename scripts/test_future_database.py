"""Opt-in MySQL integration checks; only UUID-named scratch databases are changed.

Run: KBC_TEST_MYSQL=1 python3 -m unittest discover -s scripts -p 'test_future_database.py'
Uses the repository's local Compose MySQL and its development root credentials.
"""

import os
from pathlib import Path
import re
import subprocess
import unittest
import uuid


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = (ROOT / 'sql/schema.sql').read_text()
MIGRATION = (ROOT / 'sql/migrations/001_customer_product_ownership.sql').read_text()
OWNERSHIP_FK = '''ALTER TABLE transactions DROP FOREIGN KEY fk_transactions_customer_product;'''


@unittest.skipUnless(os.environ.get('KBC_TEST_MYSQL') == '1', 'requires opt-in local MySQL')
class FutureDatabaseTests(unittest.TestCase):
    def mysql(self, sql, database=True, check=True):
        command = ['docker', 'compose', 'exec', '-T', '-e', 'MYSQL_PWD=root',
                   'mysql', 'mysql', '-uroot', '--batch', '--skip-column-names']
        if database:
            command.append(self.database)
        result = subprocess.run(command, input=sql, text=True, capture_output=True, cwd=ROOT)
        if check:
            self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def setUp(self):
        self.database = 'kbc_future_test_' + uuid.uuid4().hex
        self.mysql(f'CREATE DATABASE `{self.database}`;', database=False)
        self.addCleanup(self.drop_scratch_database)
        self.mysql(SCHEMA)

    def drop_scratch_database(self):
        # Never allow this helper to target app_dev or a supplied database name.
        if not re.fullmatch(r'kbc_future_test_[0-9a-f]{32}', self.database):
            raise ValueError('Refusing to drop a non-test database')
        self.mysql(f'DROP DATABASE `{self.database}`;', database=False)

    def snapshot(self):
        return self.mysql('''
            SELECT customer_id, current_balance FROM customers ORDER BY customer_id;
            SELECT * FROM transactions ORDER BY transaction_id;
            SELECT customer_id, product_id FROM customer_product ORDER BY customer_id, product_id;
        ''').stdout

    def assert_ownership_enforced(self):
        for sql in (
            "INSERT INTO transactions (customer_id, product_id, transaction_date, amount) VALUES (1001, 2002, '2026-09-30', -1);",
            'UPDATE transactions SET product_id = 2002 WHERE transaction_id = 900001;',
            'DELETE FROM customer_product WHERE customer_id = 1001 AND product_id = 2001;',
        ):
            with self.subTest(sql=sql):
                result = self.mysql(sql, check=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('fk_transactions_customer_product', result.stderr)

    def test_fresh_schema_enforces_ownership_and_migration_is_repeatable(self):
        before = self.snapshot()
        self.mysql(MIGRATION)
        self.mysql(MIGRATION)
        self.assert_ownership_enforced()
        self.assertEqual(self.snapshot(), before)

    def test_legacy_database_is_migrated_without_changing_rows(self):
        before = self.snapshot()
        self.mysql(OWNERSHIP_FK + '\nRENAME TABLE customer_product TO client_product_link;')
        self.mysql(MIGRATION)
        self.mysql(MIGRATION)
        self.assertEqual(self.snapshot(), before)
        self.assert_ownership_enforced()
        self.assertNotIn('client_product_link', self.mysql('SHOW TABLES;').stdout)

    def test_current_table_without_constraint_is_upgraded(self):
        before = self.snapshot()
        self.mysql(OWNERSHIP_FK)
        self.mysql(MIGRATION)
        self.assert_ownership_enforced()
        self.assertEqual(self.snapshot(), before)

    def test_invalid_legacy_rows_stop_migration_before_rename(self):
        self.mysql(OWNERSHIP_FK + '''
            UPDATE transactions SET product_id = 2002 WHERE transaction_id = 900001;
            RENAME TABLE customer_product TO client_product_link;
        ''')
        result = self.mysql(MIGRATION, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Transaction ownership mismatch', result.stderr)
        tables = self.mysql('SHOW TABLES;').stdout.splitlines()
        self.assertIn('client_product_link', tables)
        self.assertNotIn('customer_product', tables)
        self.assertEqual(self.mysql('SELECT product_id FROM transactions WHERE transaction_id = 900001;').stdout.strip(), '2002')
        self.mysql('UPDATE transactions SET product_id = 2001 WHERE transaction_id = 900001;')
        self.mysql(MIGRATION)
        self.assert_ownership_enforced()

    def test_ambiguous_table_layout_requires_manual_resolution(self):
        before = self.snapshot()
        self.mysql('CREATE TABLE client_product_link LIKE customer_product;')
        result = self.mysql(MIGRATION, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Expected exactly one ownership table', result.stderr)
        self.assertEqual(self.snapshot(), before)


if __name__ == '__main__':
    unittest.main()
