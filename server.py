import os
import http.server
import json

PASSWORD = os.environ.get('DASHBOARD_PASSWORD', 'changeme')
API_KEY = os.environ.get('TS_API_KEY', '')

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/config':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'password': PASSWORD,
                'apiKey': API_KEY
            }).encode())
        else:
            self.directory = '/app'
            super().do_GET()

    def log_message(self, *args):
        pass

http.server.test(HandlerClass=Handler, port=10000, bind='0.0.0.0')
