from conf import get_db_connection

def create_table():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE git_remotes(
            remote_url TEXT,
            remote_branch_name TEXT,
            local_branch_name TEXT PRIMARY KEY,
            server_is_live INTEGER DEFAULT 0
        )
        ''')

def add_new_remote(remote_url, remote_branch_name, local_branch_name):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
        INSERT INTO TABLE git_remotes
        (remote_url, local_branch_name, server_is_live)
        VALUES
        ({remote_url}, {remote_branch_name}, {local_branch_name})
        ''')

def start_live_server(local_branch_name):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
        UPDATE TABLE git_remotes
        SET server_is_live = 1
        WHERE local_branch_name = {local_branch_name}
        ''')

def stop_live_server(local_branch_name):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
        UPDATE TABLE git_remotes
        SET server_is_live = 0
        WHERE local_branch_name = {local_branch_name}
        ''')

def reset_live_server_status():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE TABLE git_remotes SET server_is_live = 0')

def get_live_servers():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        result = cursor.execute('SELECT * FROM git_remotes WHERE server_is_live = 1')
        return result.fetchall()