import functools
import os
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from urllib.parse import urlparse


INDEXFILE = 'index.html'
HOST_PORT = ('0.0.0.0', 0)

def create_handler(BASE_DIR: str):
    if not os.access(BASE_DIR, os.R_OK):
        print('cannot find', BASE_DIR)
        exit(1)

    class AngularHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            file_path = self.directory + os.sep + urlparse(self.path).path
            index_path = self.directory + os.sep + INDEXFILE

            # See if the file requested exists
            if os.access(file_path, os.R_OK) and os.path.isfile(file_path):
                # File exists, serve it up
                SimpleHTTPRequestHandler.do_GET(self)
            else:
                # send index.html, but don't redirect
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')  
                self.end_headers()
                with open(index_path, 'rb') as fin:
                    self.copyfile(fin, self.wfile)

    Handler = functools.partial(AngularHandler, directory=BASE_DIR)
    return Handler


def create_httpd(BASE_DIR: str):
    handler = create_handler(BASE_DIR)
    httpd = TCPServer(HOST_PORT, handler)
    return httpd

def run_httpd(httpd: TCPServer):
    httpd.serve_forever()

def close_httpd(httpd: TCPServer):
    httpd.shutdown()
    httpd.server_close()
