from concurrent.futures import ThreadPoolExecutor

from flask import Flask
from serve_webapp import close_httpd, create_httpd, run_httpd

BASE_DIR = './dist/genstuff'

executor = ThreadPoolExecutor(8)

servers = {}

app = Flask('my-angular-server-app')

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
    app.run('0.0.0.0', 8800)
except KeyboardInterrupt:
    print('closing')
finally:
    for server in servers:
        stop_server(server)