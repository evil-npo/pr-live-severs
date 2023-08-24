from sqlite3 import Connection

def create_table(con: Connection):
    cursor = con.cursor()
    cursor.execute("CREATE TABLE git_remotes(remote_url, remote_branch_name, local_branch_name)")

def get_all_local_branch_names(con: Connection):
    cursor = con.cursor()
    result = cursor.execute("SELECT DISTINCT local_branch_name from git_remotes")
    return result.fetchall()