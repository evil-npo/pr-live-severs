# node modules status
from .conf import execute_query

def create_table():
    execute_query('''
        CREATE TABLE node_modules_status(
            require_install INTEGER
        )
    ''')

def init_table():
    execute_query('INSERT INTO node_modules_status (require_install) values (0)')

def does_require_install():
    rows = execute_query('SELECT require_install from node_modules_status')
    print(rows)
    return bool(rows[0][0])

def set_require_install(ri: bool):
    execute_query('''
        UPDATE node_modules_status
        SET require_install = ?
    ''', (ri,))