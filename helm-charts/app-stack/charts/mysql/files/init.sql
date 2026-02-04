CREATE DATABASE IF NOT EXISTS app_db;
USE app_db;

CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO items (name, description, price) VALUES
    ('Laptop', 'High-performance laptop', 999.99),
    ('Mouse', 'Wireless mouse', 49.99),
    ('Keyboard', 'Mechanical keyboard', 129.99);
