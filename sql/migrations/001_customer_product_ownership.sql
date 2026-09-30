-- Existing databases only; schema.sql already contains the new constraint.
-- Run with a client that STOPS on errors (never mysql --force).
-- Preserves rows. MySQL DDL auto-commits; back up before applying.
-- Refuses ambiguous table layouts or mismatched ownership before renaming.
DROP PROCEDURE IF EXISTS kbc_future_migrate_001;
DELIMITER //
CREATE PROCEDURE kbc_future_migrate_001()
BEGIN
    DECLARE legacy_exists INT DEFAULT 0;
    DECLARE current_exists INT DEFAULT 0;
    DECLARE invalid_rows BIGINT DEFAULT 0;
    DECLARE ownership_fk_exists INT DEFAULT 0;

    SELECT COUNT(*) INTO legacy_exists FROM information_schema.tables
      WHERE table_schema = DATABASE() AND table_name = 'client_product_link';
    SELECT COUNT(*) INTO current_exists FROM information_schema.tables
      WHERE table_schema = DATABASE() AND table_name = 'customer_product';
    IF legacy_exists + current_exists <> 1 THEN
        SIGNAL SQLSTATE '45000'
          SET MESSAGE_TEXT = 'Expected exactly one ownership table; reconcile manually before migration';
    END IF;

    IF legacy_exists = 1 THEN
        SELECT COUNT(*) INTO invalid_rows FROM transactions t
        LEFT JOIN client_product_link cp
          ON cp.customer_id = t.customer_id AND cp.product_id = t.product_id
        WHERE cp.customer_id IS NULL;
    ELSE
        SELECT COUNT(*) INTO invalid_rows FROM transactions t
        LEFT JOIN customer_product cp
          ON cp.customer_id = t.customer_id AND cp.product_id = t.product_id
        WHERE cp.customer_id IS NULL;
    END IF;
    IF invalid_rows > 0 THEN
        SIGNAL SQLSTATE '45000'
          SET MESSAGE_TEXT = 'Transaction ownership mismatch; no records changed, repair source data first';
    END IF;

    IF legacy_exists = 1 THEN
        RENAME TABLE client_product_link TO customer_product;
    END IF;
    SELECT COUNT(*) INTO ownership_fk_exists FROM information_schema.table_constraints
      WHERE constraint_schema = DATABASE() AND table_name = 'transactions'
        AND constraint_name = 'fk_transactions_customer_product'
        AND constraint_type = 'FOREIGN KEY';
    IF ownership_fk_exists = 0 THEN
        ALTER TABLE transactions
          ADD CONSTRAINT fk_transactions_customer_product
          FOREIGN KEY (customer_id, product_id)
          REFERENCES customer_product(customer_id, product_id)
          ON DELETE RESTRICT ON UPDATE RESTRICT;
    END IF;
END//
DELIMITER ;
CALL kbc_future_migrate_001();
DROP PROCEDURE kbc_future_migrate_001;
