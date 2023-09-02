import uuid
from .conf import execute_query

def create_table():
    execute_query('''
        CREATE TABLE git_remotes(
            remote_url TEXT NOT NULL,
            remote_branch_name TEXT NOT NULL,
            local_branch_name TEXT PRIMARY KEY,
            server_port INTEGER
        )
    ''')

def add_new_remote_branch(remote_url, remote_branch_name):
    rows = execute_query(
        'SELECT local_branch_name FROM git_remotes WHERE remote_url = ? AND remote_branch_name = ?',
        (remote_url, remote_branch_name)
    )
    if rows:
        return rows[0][0]
    local_branch_name = uuid.uuid4()
    execute_query('''
        INSERT INTO git_remotes
        (remote_url, remote_branch_name, local_branch_name)
        VALUES
        (?, ?, ?)
    ''', (remote_url, remote_branch_name, local_branch_name))
    return local_branch_name

def delete_remote_branch(local_branch_name):
    execute_query('DELETE FROM git_remotes WHERE local_branch_name = ?', (local_branch_name,))

def start_live_server(local_branch_name, port):
    execute_query('''
        UPDATE TABLE git_remotes
        SET server_port = ?
        WHERE local_branch_name = ?
    ''', (port, local_branch_name))

def stop_live_server(local_branch_name):
    execute_query('''
        UPDATE TABLE git_remotes
        SET server_port = NULL
        WHERE local_branch_name = ?
    ''', (local_branch_name))

def reset_all_servers():
    execute_query('UPDATE TABLE git_remotes SET server_port = NULL')

def get_live_servers():
    return execute_query('SELECT * FROM git_remotes WHERE server_port IS NOT NULL')

def get_all_servers():
    return execute_query('SELECT * FROM git_remotes WHERE server_port IS NOT NULL')