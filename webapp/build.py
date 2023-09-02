import subprocess
import os
import shutil

def fetch_remote_branch(remote_url, remote_branch_name, local_branch_name, BASE_DIR):
    subprocess.run(
        ['git', 'checkout', 'main'],
        check=True,
        cwd=BASE_DIR
    )
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
    NODE_PATH=f'/home/{os.environ["USER"]}/.nvm/versions/node/v16.13.2/bin'
    environment = {
        'PATH': NODE_PATH + ';' + os.environ['PATH'],
    }
    subprocess.run(
        ['npm', 'run', 'build'],
        check=True,
        env=environment,
        cwd=BASE_DIR
    )
    shutil.copytree(BASE_DIR+'/dist', TARGET_DIR, dirs_exist_ok=True)
