import conf
import git_remotes
import live_servers

with conf.get_db_connection() as conn:
    git_remotes.create_table(conn)
    live_servers.create_table(conn)