#!/usr/bin/python
# -*- coding:utf-8 -*-

# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
from unittest import case

hostName = "localhost"
serverPort = 80
scripts = ['bitcoin.py', 'picture.py']

import subprocess

os.chdir('.')

def get_current_script():
    fp_script = open("./.current_display_script", "r")
    script = fp_script.read().replace('\n', '')
    fp_script.close()
    return script

def get_current_image():
    fp_image = open("./.current_display_image", "r")
    image = fp_image.read().replace('\n', '')
    fp_image.close()
    return image

def refresh_display():
    subprocess.Popen(['/bin/bash', './runscript.sh'])


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        valid_paths={
            "/": self.home,
            "/refresh": self.refresh_display,
            "/flip-the-script": self.flip_the_script,
        }

        valid_paths.get(self.path, self.send_error)()

    def send_error(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes("<html><head><title>404 not found</title></head><body>", "utf-8"))
        self.wfile.write(bytes("<p>Sorry, this page wasn't found!</p>", "utf-8"))
        self.wfile.write(bytes("<p><a href='/'>Go to home page</a></p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
        self.wfile.close()

    def home(self):
        current_script = get_current_script()

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes("<html><head><title>e-Paper: Home</title></head><body>", "utf-8"))
        self.wfile.write(bytes(f"<p><b>Current script: {current_script}</b></p>", "utf-8"))
        if current_script == 'picture.py':
            self.wfile.write(bytes(f"<p><b>Current image: {get_current_image()}</b></p>", "utf-8"))
        self.wfile.write(bytes("<ul><li><a href='/refresh'>Refresh e-Paper display</a></li><li><a href='/flip-the-script'>Change display script</a></li></ul>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
        self.wfile.close()

    def flip_the_script(self):
        last_script = get_current_script()

        script_index = scripts.index(last_script)
        script_index+=1
        if(script_index >= len(scripts)):
            script_index = 0
        next_script = scripts[script_index]

        fp_last_script = open("./.current_display_script", "w")
        fp_last_script.write(next_script)
        fp_last_script.close()

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes("<html><head><title>e-Paper: Change script</title></head><body>", "utf-8"))
        self.wfile.write(bytes("<p>Flipped that script!</p>", "utf-8"))
        self.wfile.write(bytes(f"<p><b>New script: {next_script}</b></p>", "utf-8"))
        self.wfile.write(bytes("<p><a href='/'>Back to home page</a></p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
        self.wfile.close()

        refresh_display()

    def refresh_display(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        current_script = get_current_script()

        self.wfile.write(bytes("<html><head><title>e-Paper: Refresh</title></head><body>", "utf-8"))
        self.wfile.write(bytes("<p><b>Refreshing e-Paper display...</b></p>", "utf-8"))
        if current_script == 'picture.py':
            self.wfile.write(bytes(f"<p><b>Current image: {get_current_image()}</b></p>", "utf-8"))
        self.wfile.write(bytes("<p><a href='/'>Back to home page</a></p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
        self.wfile.close()

        refresh_display()

if __name__ == "__main__":
    webServer = HTTPServer(server_address=('', serverPort), RequestHandlerClass=MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
