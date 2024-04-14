#!/usr/bin/python3
import os
import socket
import http.server
import socketserver
import time
from functools import partial
from sys import argv

server_bin = "/usr/bin/http-server"
local_hostname = socket.gethostname()
local_address = socket.gethostbyname(local_hostname)

def notify(title, description=""):
    return os.popen(f"notify-send '{title}' '{description}' --app-name='Live Server' --icon=document-send")

class DirectoryListing(http.server.SimpleHTTPRequestHandler):
    def __init__(self, directory, *args, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

def decide_port():
    with socket.socket() as sock:
        sock.bind(('', 0))
        return sock.getsockname()[1]

def start_server(directory, port):
    directory = os.path.abspath(directory)
    server_address = ('', port)
    handler = partial(DirectoryListing, directory)
    httpd = http.server.HTTPServer(server_address, handler)
    return httpd

def share(directory):
    directory = os.path.abspath(directory)
    basename = os.path.basename(directory)
    try:
        port = decide_port()
        print(port)
        try:
            server = start_server(directory, port)
            print("Started server on %s (%s)" % (port, directory))
            notify("Sharing %s" % (basename), description=f"http://{local_address}:{port}/")
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        server.server_close()
        notify("Stopped sharing %s" % (basename))
        print("Server stopped %s (%s)" % (port, directory))
    except Exception as e:
        notify("Sharing failed", description=repr(e))
        print(repr(e))


if __name__ == '__main__':
    share(argv[1])
