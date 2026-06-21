import sqlite3
from datetime import datetime

DB_PATH = "database/fraud.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        amount REAL,
        time INTEGER,
        transactions_today INTEGER,

        is_foreign INTEGER,
        is_high_risk_country INTEGER,

        prediction INTEGER,

        risk_score REAL,
        risk_level TEXT,

        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("Database Initialized")


def save_transaction(
    amount,
    time,
    transactions_today,
    is_foreign,
    is_high_risk_country,
    prediction,
    risk_score,
    risk_level
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO transactions (
        amount,
        time,
        transactions_today,
        is_foreign,
        is_high_risk_country,
        prediction,
        risk_score,
        risk_level,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        amount,
        time,
        transactions_today,
        is_foreign,
        is_high_risk_country,
        prediction,
        risk_score,
        risk_level,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_all_transactions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM transactions
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_total_transactions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM transactions
    """)

    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_total_frauds():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM transactions
    WHERE prediction = 1
    """)

    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_average_risk():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT AVG(risk_score)
    FROM transactions
    """)

    result = cursor.fetchone()[0]

    conn.close()

    if result is None:
        return 0

    return round(result, 2)


def delete_all_transactions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM transactions
    """)

    conn.commit()
    conn.close()

    print("All records deleted")


def get_latest_transaction():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM transactions
    ORDER BY id DESC
    LIMIT 1
    """)

    row = cursor.fetchone()

    conn.close()

    return row