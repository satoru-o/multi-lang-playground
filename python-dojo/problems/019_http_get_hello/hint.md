# ヒント

- ファイルの先頭で `from http.server import BaseHTTPRequestHandler` を書いて import してください。
- GETリクエストに応答するには `do_GET` メソッドを実装します。
- レスポンスの返し方は3ステップです: (1) `self.send_response(200)` でステータスコードを送る、(2) `self.end_headers()` でヘッダー部分を終える、(3) `self.wfile.write(...)` で本文を送る（`bytes` で渡す必要があるので `文字列.encode("utf-8")` を使います）。
- 形:
  ```python
  from http.server import BaseHTTPRequestHandler


  class Handler(BaseHTTPRequestHandler):
      def do_GET(self):
          self.send_response(200)
          self.end_headers()
          self.wfile.write("🐱ねこサーバーです".encode("utf-8"))
  ```
- サーバーを自分で起動する必要はありません（`uv run dojo.py check` が裏で自動的にテスト用サーバーを立てて確認します）。
