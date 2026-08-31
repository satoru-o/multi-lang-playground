import json
from http.server import BaseHTTPRequestHandler


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers["Content-Length"])
        data = json.loads(self.rfile.read(length))
        action = data.get("action")
        if action == "pet":
            text = "🐱ふにゃ〜ん"
        elif action == "feed":
            text = "🐱もぐもぐ"
        else:
            text = "🐱？"
        self.send_response(200)
        self.end_headers()
        self.wfile.write(text.encode("utf-8"))
