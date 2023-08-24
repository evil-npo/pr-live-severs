import uuid
import subprocess

def use_remote_branch(remote_url, remote_branch_name, BASE_DIR):
    local_branch_name = str(uuid.uuid4())
    subprocess.run(
        ['git', 'fetch', remote_url, f'{remote_branch_name}:{local_branch_name}'],
        check=True,
        cwd=BASE_DIR
    )
    subprocess.run(
        ['git', 'checkout', local_branch_name],
        check=True,
        cwd=BASE_DIR
    )

use_remote_branch('https://github.com/lagold27/homebrew-oh-my-posh.git', 'main', 'test-repo')