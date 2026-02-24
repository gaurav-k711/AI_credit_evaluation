from database.db import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

cursor.execute("""
    INSERT OR IGNORE INTO users (username, password, role)
    VALUES ('underwriter1', 'password123', 'underwriter')
""")

conn.commit()
conn.close()

print("Underwriter user created")