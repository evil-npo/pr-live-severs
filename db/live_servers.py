import sqlite3

def create_table(con: sqlite3.Connection):
    cursor = con.cursor()
    cursor.execute("CREATE TABLE live_servers()")