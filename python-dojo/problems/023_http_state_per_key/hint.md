# ヒント

- 名前ごとに満腹度を管理するには、辞書（`{名前: 満腹度}`）をクラス変数として持つと便利です。
- 存在しない名前の初期値には `dict.get(name, 0)` が使えます（011の辞書の基本を思い出してください）。
- `do_POST` は `/cat/feed` と `/cat/status` の両方に応答するので、`self.path` で分岐しつつ、リクエスト本文の読み取りとJSON応答の組み立ては共通化すると楽です。
- 形:
  ```python
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
  ```
