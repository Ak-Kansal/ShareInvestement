import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql2024",
        database="share_watchlist"
    )
#db connection