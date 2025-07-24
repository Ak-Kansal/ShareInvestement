
-- SQLite schema for Share Watchlist project

PRAGMA foreign_keys = ON;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- Shares table
CREATE TABLE IF NOT EXISTS shares (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    symbol TEXT NOT NULL,
    company_name TEXT,
    quantity INTEGER DEFAULT 0,
    avg_price REAL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    symbol TEXT,
    transaction_type TEXT CHECK(transaction_type IN ('BUY', 'SELL')) NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Watchlist table
CREATE TABLE IF NOT EXISTS watchlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    symbol TEXT NOT NULL,
    company_name TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
