import json
from http.server import BaseHTTPRequestHandler


class Handler(BaseHTTPRequestHandler):
    fullness = {}

    def _read_json(self):
        length = int(self.headers["Content-Length"])
        return json.loads(self.rfile.read(length))

    def _reply_json(self, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        data = self._read_json()
        name = data["name"]
        if self.path == "/cat/feed":
            Handler.fullness[name] = Handler.fullness.get(name, 0) + 1
        self._reply_json({"name": name, "満腹度": Handler.fullness.get(name, 0)})
