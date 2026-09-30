-- ============================================
-- CUSTOMERS
-- ============================================

CREATE TABLE customers (
    customer_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NULL,
    safety_buffer INT NOT NULL,
    city VARCHAR(100) NULL,
    country VARCHAR(100) NULL,

    CONSTRAINT chk_customer_age
        CHECK (age IS NULL OR age >= 0)
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

CREATE INDEX idx_events_type
    ON events(event_type);

CREATE INDEX idx_events_date
    ON events(event_date);

CREATE INDEX idx_customer_events_customer
    ON customer_events(customer_id);

CREATE INDEX idx_customer_events_event
    ON customer_events(event_id);
