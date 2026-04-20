import os
import json
import urllib.request
import urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler

PASSWORD = os.environ.get('DASHBOARD_PASSWORD', '')
API_KEY  = os.environ.get('TS_API_KEY', '')

class Handler(SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/config':
            self._json({'password': PASSWORD})

        elif self.path == '/api/devices':
            if not API_KEY:
                self._json({'error': 'TS_API_KEY not set'}, 500)
                return
            try:
                req = urllib.request.Request(
                    'https://api.tailscale.com/api/v2/tailnet/-/devices?fields=all',
                    headers={'Authorization': 'Bearer ' + API_KEY}
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read())
                self._json(data)
            except urllib.error.HTTPError as e:
                self._json({'error': str(e)}, e.code)
            except Exception as e:
                self._json({'error': str(e)}, 500)

        else:
            self.directory = '/app'
            super().do_GET()

    def _json(self, data, code=200):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f'Starting server on port {port}')
    HTTPServer(('0.0.0.0', port), Handler).serve_forever()
