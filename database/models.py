from database.db import get_db_connection


def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loan_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_type TEXT,
            years_in_operation INTEGER,
            annual_revenue REAL,
            monthly_cashflow REAL,
            loan_amount_requested REAL,
            credit_score INTEGER,
            existing_loans INTEGER,
            debt_to_income_ratio REAL,
            collateral_value REAL,
            repayment_history TEXT,
            risk_score REAL,
            risk_category TEXT,
            decision TEXT,
            confidence TEXT,
            reasons TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def create_user_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)

    conn.commit()
    conn.close()