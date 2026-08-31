# ヒント

- `do_GET` の代わりに `do_POST` を実装する点以外は019とほぼ同じです。
- 今回はリクエストの中身（本文）を読む必要はありません。
- 形:
  ```python
  from http.server import BaseHTTPRequestHandler


  class Handler(BaseHTTPRequestHandler):
      def do_POST(self):
          self.send_response(200)
          self.end_headers()
          self.wfile.write("🐱ふにゃ〜ん".encode("utf-8"))
  ```
