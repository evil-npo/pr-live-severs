from sqlite3 import Connection

def create_table(con: Connection):
    cursor = con.cursor()
    cursor.execute("CREATE TABLE live_servers()")