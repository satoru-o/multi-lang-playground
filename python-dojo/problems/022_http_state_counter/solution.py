import json
from http.server import BaseHTTPRequestHandler


class Handler(BaseHTTPRequestHandler):
    fullness = 0

    def _reply_json(self, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/cat/status":
            self._reply_json({"満腹度": Handler.fullness})

    def do_POST(self):
        if self.path == "/cat/feed":
            Handler.fullness += 1
            self._reply_json({"満腹度": Handler.fullness})
