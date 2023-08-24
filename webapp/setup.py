import uuid
import subprocess
import os
import shutil

def fetch_remote_branch(remote_url, remote_branch_name, BASE_DIR):
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
    return local_branch_name

def build_remote_branch(BASE_DIR, TARGET_DIR):
    NODE_PATH=f'/home/{os.environ["USER"]}/.nvm/versions/node/v16.12.0/bin'
    environment = {
        'PATH': NODE_PATH + ';' + os.environ['PATH'],
    }
    subprocess.run(
        ['npm', '-v'],
        check=True,
        env=environment,
        cwd=BASE_DIR
    )
    shutil.copytree(BASE_DIR+'/dist/genstuff', TARGET_DIR, dirs_exist_ok=True)

# use_remote_branch('https://github.com/lagold27/homebrew-oh-my-posh.git', 'main', 'test-repo')