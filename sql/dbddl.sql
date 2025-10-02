CREATE DATABASE retail;
CREATE TABLE receipts (
    doc_id VARCHAR(64) PRIMARY KEY,
    shop_num INT NOT NULL,
    cash_num INT NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    doc_id VARCHAR(64) REFERENCES receipts(doc_id),
    item VARCHAR(255),
    category VARCHAR(100),
    amount INT,
    price NUMERIC(10,2),
    discount NUMERIC(10,2)
);