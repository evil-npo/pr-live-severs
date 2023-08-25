from concurrent.futures import ThreadPoolExecutor

from flask import Flask, render_template, send_from_directory
from webapp.serve import close_httpd, create_httpd, run_httpd

BASE_DIR = './dist/genstuff'
HOST_PORT = ('0.0.0.0', 8800)

executor = ThreadPoolExecutor(8)
servers = {}

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/static/<filename>')
def create_server(filename):
    return send_from_directory('static', filename)

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