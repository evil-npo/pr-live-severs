from concurrent.futures import ThreadPoolExecutor
from threading import Lock

from flask import Flask, render_template, send_from_directory, request

from webapp.serve import close_httpd, create_httpd, run_httpd
from webapp.build import fetch_remote_branch, build_remote_branch
from db.git_remotes import add_new_remote_branch, delete_remote_branch, get_all_servers, get_live_server_port, reset_all_servers, start_live_server, stop_live_server
from db.nm_status import does_require_install, set_require_install

BASE_DIR = '../sample-web-app/src'
TARGET_DIR = '../builds'
HOST_PORT = ('0.0.0.0', 8800)

executor = ThreadPoolExecutor(8)
servers = {}
fs_lock = Lock()

app = Flask(__name__)

@app.route('/')
def home():
    servers = get_all_servers()
    return render_template('home.html', servers=servers)

@app.route('/static/<filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.post('/create')
def create_server():
    remote_url = request.form['remote_url']
    remote_branch_name = request.form['remote_branch_name']
    request_require_install = request.form.get('require-install')
    already_require_install = does_require_install()
    require_install = bool(request_require_install or already_require_install)
    local_branch_name = add_new_remote_branch(remote_url, remote_branch_name)

    if not request_require_install:
        set_require_install(False)
    elif require_install:
        set_require_install(True)

    try:
        print('going to acquire for', remote_branch_name)
        fs_lock.acquire(blocking=True)
        print('acquired for', remote_branch_name)
        fetch_remote_branch(remote_url, remote_branch_name, local_branch_name, BASE_DIR)
        build_remote_branch(BASE_DIR, TARGET_DIR + '/' + local_branch_name, refresh_dependencies=require_install)
        success = {
            'remote': f'{remote_url} : {remote_branch_name}',
            'local': local_branch_name
        }
        print('going to release for', remote_branch_name)
        fs_lock.release()
        print('released for', remote_branch_name)
        return render_template('server-created.html', success=success)
    except Exception as e:
        delete_remote_branch(local_branch_name)
        return render_template('server-created.html', error=e)

@app.route('/start/<local_branch_name>')
def start_server(local_branch_name):
    port = get_live_server_port(local_branch_name)
    if not port:
        httpd = create_httpd(TARGET_DIR + '/' + local_branch_name)
        port = httpd.server_address[1]
        executor.submit(run_httpd, httpd)
        servers[port] = httpd
        start_live_server(local_branch_name, port)
    return render_template('server-started.html', local_branch_name=local_branch_name, port=port)

@app.route('/stop/<local_branch_name>')
def stop_server(local_branch_name, in_flask=True):
    port = get_live_server_port(local_branch_name)
    if port:
        if port not in servers:
            return Exception('no such server running')
        httpd = servers[port]
        close_httpd(httpd)
        stop_live_server(local_branch_name)
    if in_flask:
        return render_template('server-stopped.html', local_branch_name=local_branch_name, port=port)

try:
    reset_all_servers()
    app.run(*HOST_PORT)
finally:
    for server in servers:
        stop_server(server, False)
    print('\rClosed all servers.')