import sqlite3
import git_remotes
import live_servers
from conf import db_file_name

try:
    connection = sqlite3.connect(db_file_name)
    git_remotes.create_table(connection)
    live_servers.create_table(connection)
except Exception as e:
    print('could not set up db', e)
finally:
    connection.close()