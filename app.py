from concurrent.futures import ThreadPoolExecutor

from flask import Flask, render_template, send_from_directory, request
from webapp.serve import close_httpd, create_httpd, run_httpd
from webapp.build import fetch_remote_branch
from db.git_remotes import add_new_remote_branch

BASE_DIR = '../sample-web-app/src'
HOST_PORT = ('0.0.0.0', 8800)

executor = ThreadPoolExecutor(8)
servers = {}

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/static/<filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.post('/create')
def create_server():
    remote_url = request.form['remote_url']
    remote_branch_name = request.form['remote_branch_name']
    local_branch_name = fetch_remote_branch(remote_url, remote_branch_name, BASE_DIR)
    add_new_remote_branch(remote_url, remote_branch_name, local_branch_name)
    return f'''
        <h1>All good for { remote_url } and { remote_branch_name }</h1>
        <h1>Local branch : { local_branch_name } </h1>
    '''

@app.route('/start')
def start_server():
    httpd = create_httpd(BASE_DIR)
    port = httpd.server_address[1]
    executor.submit(run_httpd, httpd)
    servers[port] = httpd
    return {'port': port}

@app.route('/stop/<int:port>')
def stop_server(port):
    if port not in servers:
        return Exception('no such server running')
    httpd = servers[port]
    close_httpd(httpd)
    return f'stopped {port}'

try:
    app.run(*HOST_PORT)
finally:
    for server in servers:
        stop_server(server)
    print('\rClosed all servers.')