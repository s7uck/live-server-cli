#!/usr/bin/python3
import os
import socket
import subprocess
import time
from sys import argv

server_bin = "/usr/bin/http-server"
args = ["{directory}", "-p {port}"]
local_hostname = socket.gethostname()
local_address = socket.gethostbyname(local_hostname)

def notify(title, description="", urgency="normal"):
    os.system(f"notify-send {title} {description} --app-name='Live Server' --urgency={urgency} --icon=document-send")

def start_server(directory, port):
    directory = os.path.abspath(directory)
    try:
        server_process = subprocess.Popen(f"{server_bin} {args.join(' ')}".format(directory, port)).read()
        return server_process
    except Exception as e:
        notify("Failed to share folder %" % (directory), description=repr(e), urgency="critical")
        print("Failed to start server: ", repr(e))        

def stop_server(server):
    server.terminate()

def share(directory):
    server = start_server(directory, port)
    print("Started server on % (%, pid %)" % (port, directory, server.pid))

if __name__ = '__main__':
    share(argv[1])
