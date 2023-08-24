import sqlite3
db_file_name = "web_app_prs.db"

def get_db_connection():
    return sqlite3.connect(db_file_name)

def execute_query(query: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        result = cursor.execute(query)
        return result.fetchall()