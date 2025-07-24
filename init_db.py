import sqlite3

with open("share_watchlist_sqlite_schema.sql", "r") as f:
    schema = f.read()

conn = sqlite3.connect("share_watchlist.db")
conn.executescript(schema)
conn.commit()
conn.close()

print("✅ Database initialized successfully.")
