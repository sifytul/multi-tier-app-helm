-- Create database if not exists
CREATE DATABASE IF NOT EXISTS app_db;
USE app_db;

-- Create items table
CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create application user
CREATE USER IF NOT EXISTS 'app_user'@'%' IDENTIFIED BY 'app_password';
GRANT ALL PRIVILEGES ON app_db.* TO 'app_user'@'%';
FLUSH PRIVILEGES;

-- Insert sample data
INSERT INTO items (name, description, price) VALUES
    ('Laptop', 'High-performance laptop with 16GB RAM', 999.99),
    ('Mouse', 'Wireless ergonomic mouse', 49.99),
    ('Keyboard', 'Mechanical keyboard with RGB lighting', 129.99),
    ('Monitor', '27-inch 4K monitor', 399.99),
    ('Headphones', 'Noise-canceling wireless headphones', 249.99);
