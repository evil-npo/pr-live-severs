import sqlite3
db_file_name = "web_app_prs.db"

def execute_query(query: str):
    with sqlite3.connect(db_file_name) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query)
        return result.fetchall()