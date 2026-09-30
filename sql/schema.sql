-- ============================================
-- CUSTOMERS
-- ============================================

CREATE TABLE customers (
    customer_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    current_balance DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    age INT NULL,
    safety_buffer INT NOT NULL,
    city VARCHAR(100) NULL,
    country VARCHAR(100) NULL,

    CONSTRAINT chk_customer_age
        CHECK (age IS NULL OR age >= 0)
) ENGINE=InnoDB;


-- ============================================
-- CUSTOMER PREFERENCES
-- ============================================

CREATE TABLE customer_preferences (
    customer_id BIGINT UNSIGNED PRIMARY KEY,
    advice_opt_in BOOLEAN NOT NULL DEFAULT TRUE,
    notification_preference VARCHAR(50) NOT NULL DEFAULT 'in_app',

    CONSTRAINT fk_preferences_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
        ON DELETE CASCADE
) ENGINE=InnoDB;


-- ============================================
-- PRODUCTS
-- ============================================

CREATE TABLE products (
    product_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    product_type VARCHAR(100) NOT NULL,
    product_amount DECIMAL(18,2) NULL,

    CONSTRAINT chk_product_amount
        CHECK (product_amount IS NULL OR product_amount >= 0)
) ENGINE=InnoDB;


-- ============================================
-- CUSTOMER / PRODUCT LINK
-- ============================================

CREATE TABLE client_product_link (
    client_product_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT UNSIGNED NOT NULL,
    product_id BIGINT UNSIGNED NOT NULL,

    CONSTRAINT fk_cpl_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_cpl_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE,

    CONSTRAINT uq_customer_product
        UNIQUE (customer_id, product_id)
) ENGINE=InnoDB;


-- ============================================
-- TRANSACTIONS
-- ============================================

CREATE TABLE transactions (
    transaction_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT UNSIGNED NOT NULL,
    product_id BIGINT UNSIGNED NOT NULL,
    transaction_date DATETIME NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    merchant VARCHAR(255) NULL,
    merchant_category VARCHAR(100) NULL,
    payment_method VARCHAR(50) NULL,

    CONSTRAINT fk_transactions_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    CONSTRAINT fk_transactions_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
) ENGINE=InnoDB;


-- ============================================
-- EVENTS
-- ============================================

CREATE TABLE events (
    event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL,
    event_date DATETIME NOT NULL,
    event_value TEXT NULL
) ENGINE=InnoDB;


-- ============================================
-- CUSTOMER EVENTS
-- ============================================

CREATE TABLE customer_events (
    customer_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    event_id BIGINT UNSIGNED NOT NULL,
    customer_id BIGINT UNSIGNED NOT NULL,

    CONSTRAINT fk_customer_events_event
        FOREIGN KEY (event_id)
        REFERENCES events(event_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_customer_events_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
        ON DELETE CASCADE,

    CONSTRAINT uq_customer_event
        UNIQUE (customer_id, event_id)
) ENGINE=InnoDB;


-- ============================================
-- INDEXES
-- ============================================

CREATE INDEX idx_cpl_customer
    ON client_product_link(customer_id);

CREATE INDEX idx_cpl_product
    ON client_product_link(product_id);

CREATE INDEX idx_transactions_customer
    ON transactions(customer_id);

CREATE INDEX idx_transactions_product
    ON transactions(product_id);

CREATE INDEX idx_transactions_date
    ON transactions(transaction_date);

CREATE INDEX idx_transactions_customer_date
    ON transactions(customer_id, transaction_date);

CREATE INDEX idx_events_type
    ON events(event_type);

CREATE INDEX idx_events_date
    ON events(event_date);

CREATE INDEX idx_customer_events_customer
    ON customer_events(customer_id);

CREATE INDEX idx_customer_events_event
    ON customer_events(event_id);


-- ============================================
-- KBC FUTURE: SYNTHETIC DEMO DATA ONLY
-- ============================================
-- The Future service derives transaction type, recurring commitments and
-- essential/flexible status from this raw data. Do not add those derived
-- labels to the raw transactions table.

INSERT INTO customers (
    customer_id, name, current_balance, safety_buffer
) VALUES
    (1001, 'Alex Demo', 1260.00, 250),
    (1002, 'Sam Safe', 2100.00, 300),
    (1003, 'Robin Uncertain', 700.00, 250);

INSERT INTO customer_preferences (
    customer_id, advice_opt_in, notification_preference
) VALUES
    (1001, TRUE, 'in_app'),
    (1002, TRUE, 'in_app'),
    (1003, TRUE, 'in_app');

INSERT INTO products (product_id, product_type, product_amount) VALUES
    (2001, 'current_account', 1260.00),
    (2002, 'current_account', 2100.00),
    (2003, 'current_account', 700.00);

INSERT INTO client_product_link (customer_id, product_id) VALUES
    (1001, 2001),
    (1002, 2002),
    (1003, 2003);

-- Alex: main demo. As of 30 September 2026, recurring commitments and normal
-- flexible spend create a forecast low point of €155 before salary, €95 below
-- the selected €250 buffer.
INSERT INTO transactions (
    customer_id, product_id, transaction_date, amount,
    merchant, merchant_category, payment_method
) VALUES
    (1001, 2001, '2026-07-03 08:00:00', -900.00, 'Brussels Housing', 'rent', 'direct_debit'),
    (1001, 2001, '2026-07-12 08:00:00', -180.00, 'KBC Insurance', 'insurance', 'direct_debit'),
    (1001, 2001, '2026-07-28 08:00:00', 2100.00, 'Acme NV', 'salary', 'bank_transfer'),
    (1001, 2001, '2026-07-06 18:00:00', -82.00, 'FreshMart', 'groceries', 'card'),
    (1001, 2001, '2026-07-13 18:00:00', -78.00, 'FreshMart', 'groceries', 'card'),
    (1001, 2001, '2026-07-09 20:00:00', -55.00, 'City Bistro', 'dining', 'card'),
    (1001, 2001, '2026-07-23 20:00:00', -60.00, 'City Bistro', 'dining', 'card'),
    (1001, 2001, '2026-07-17 14:00:00', -40.00, 'Urban Store', 'shopping', 'card'),
    (1001, 2001, '2026-08-03 08:00:00', -900.00, 'Brussels Housing', 'rent', 'direct_debit'),
    (1001, 2001, '2026-08-12 08:00:00', -180.00, 'KBC Insurance', 'insurance', 'direct_debit'),
    (1001, 2001, '2026-08-28 08:00:00', 2100.00, 'Acme NV', 'salary', 'bank_transfer'),
    (1001, 2001, '2026-08-06 18:00:00', -79.00, 'FreshMart', 'groceries', 'card'),
    (1001, 2001, '2026-08-13 18:00:00', -84.00, 'FreshMart', 'groceries', 'card'),
    (1001, 2001, '2026-08-08 20:00:00', -65.00, 'City Bistro', 'dining', 'card'),
    (1001, 2001, '2026-08-22 20:00:00', -55.00, 'City Bistro', 'dining', 'card'),
    (1001, 2001, '2026-08-16 14:00:00', -55.00, 'Urban Store', 'shopping', 'card'),
    (1001, 2001, '2026-09-03 08:00:00', -900.00, 'Brussels Housing', 'rent', 'direct_debit'),
    (1001, 2001, '2026-09-12 08:00:00', -180.00, 'KBC Insurance', 'insurance', 'direct_debit'),
    (1001, 2001, '2026-09-28 08:00:00', 2100.00, 'Acme NV', 'salary', 'bank_transfer'),
    (1001, 2001, '2026-09-06 18:00:00', -85.00, 'FreshMart', 'groceries', 'card'),
    (1001, 2001, '2026-09-13 18:00:00', -80.00, 'FreshMart', 'groceries', 'card'),
    (1001, 2001, '2026-09-07 20:00:00', -70.00, 'City Bistro', 'dining', 'card'),
    (1001, 2001, '2026-09-21 20:00:00', -70.00, 'City Bistro', 'dining', 'card'),
    (1001, 2001, '2026-09-18 14:00:00', -60.00, 'Urban Store', 'shopping', 'card');

-- Sam: control case. Regular income and a large enough balance mean Future
-- should forecast no buffer breach and avoid sending unnecessary advice.
INSERT INTO transactions (
    customer_id, product_id, transaction_date, amount,
    merchant, merchant_category, payment_method
) VALUES
    (1002, 2002, '2026-07-02 08:00:00', -850.00, 'Antwerp Housing', 'rent', 'direct_debit'),
    (1002, 2002, '2026-07-25 08:00:00', 2800.00, 'Bright Studio', 'salary', 'bank_transfer'),
    (1002, 2002, '2026-08-02 08:00:00', -850.00, 'Antwerp Housing', 'rent', 'direct_debit'),
    (1002, 2002, '2026-08-25 08:00:00', 2800.00, 'Bright Studio', 'salary', 'bank_transfer'),
    (1002, 2002, '2026-09-02 08:00:00', -850.00, 'Antwerp Housing', 'rent', 'direct_debit'),
    (1002, 2002, '2026-09-25 08:00:00', 2800.00, 'Bright Studio', 'salary', 'bank_transfer'),
    (1002, 2002, '2026-09-07 18:00:00', -90.00, 'FreshMart', 'groceries', 'card'),
    (1002, 2002, '2026-09-14 18:00:00', -95.00, 'FreshMart', 'groceries', 'card'),
    (1002, 2002, '2026-09-21 18:00:00', -92.00, 'FreshMart', 'groceries', 'card');

-- Robin: uncertainty case. Irregular income means Future should show a low
-- confidence forecast and offer review/support rather than firm advice.
INSERT INTO transactions (
    customer_id, product_id, transaction_date, amount,
    merchant, merchant_category, payment_method
) VALUES
    (1003, 2003, '2026-07-08 08:00:00', 980.00, 'Freelance Client A', 'freelance_income', 'bank_transfer'),
    (1003, 2003, '2026-07-30 08:00:00', 450.00, 'Freelance Client B', 'freelance_income', 'bank_transfer'),
    (1003, 2003, '2026-08-15 08:00:00', 620.00, 'Freelance Client A', 'freelance_income', 'bank_transfer'),
    (1003, 2003, '2026-09-05 08:00:00', 350.00, 'Freelance Client C', 'freelance_income', 'bank_transfer'),
    (1003, 2003, '2026-07-04 08:00:00', -620.00, 'Shared Home', 'rent', 'bank_transfer'),
    (1003, 2003, '2026-08-09 08:00:00', -620.00, 'Shared Home', 'rent', 'bank_transfer'),
    (1003, 2003, '2026-09-01 08:00:00', -620.00, 'Shared Home', 'rent', 'bank_transfer'),
    (1003, 2003, '2026-09-10 18:00:00', -120.00, 'FreshMart', 'groceries', 'card'),
    (1003, 2003, '2026-09-22 20:00:00', -160.00, 'City Bistro', 'dining', 'card');
