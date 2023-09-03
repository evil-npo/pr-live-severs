from db import git_remotes
from db import nm_status

git_remotes.create_table()

nm_status.create_table()
nm_status.init_table()