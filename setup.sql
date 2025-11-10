-- WealthWise Portfolio Tracker - Database Setup
-- ===============================================
-- Drop existing tables (for clean re-runs)
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS users;
-- USERS TABLE
-- ==============================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);
-- TRANSACTIONS TABLE
-- ==============================
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    symbol VARCHAR(10) NOT NULL,
    type VARCHAR(10) CHECK (type IN ('BUY', 'SELL')) NOT NULL,
    units NUMERIC(10, 2) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- SAMPLE DATA
-- ==============================
-- Insert sample users
INSERT INTO users (name, email)
VALUES ('John Doe', 'johndoe@gmail.com'),
    ('Jane Smith', 'janesmith@gmail.com');
-- Insert sample transactions
-- John buys and sells stocks
INSERT INTO transactions (user_id, symbol, type, units, price)
VALUES (1, 'AAPL', 'BUY', 10, 180.00),
    (1, 'AAPL', 'BUY', 5, 185.00),
    (1, 'AAPL', 'SELL', 8, 190.00),
    (1, 'TSLA', 'BUY', 3, 250.00),
    (2, 'GOOG', 'BUY', 4, 2700.00);