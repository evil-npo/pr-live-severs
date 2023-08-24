import sqlite3
db_file_name = "web_app_prs.db"

def get_db_connection():
    return sqlite3.connect(db_file_name)