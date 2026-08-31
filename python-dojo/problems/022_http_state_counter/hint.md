# ヒント

- リクエストをまたいで値を覚えておくには、クラス変数（`class Handler: fullness = 0` のようにメソッドの外に書く）を使うと便利です。
- JSONを返すときも `json.dumps({...})` で辞書をJSON文字列に変換してから `.encode("utf-8")` します。
- `self.path` を見ることで、どのURLへのリクエストかを判定できます（`if self.path == "/cat/feed":` のように）。
- 形:
  ```python
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
  ```
- `_reply_json` のような、応答本文をJSONで返す処理を共通化した自作メソッドを用意すると楽です。
