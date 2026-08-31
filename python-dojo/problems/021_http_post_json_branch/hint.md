# ヒント

- ファイルの先頭で `import json` も必要です。
- リクエストの本文を読むには、まず長さを知る必要があります: `length = int(self.headers["Content-Length"])`。
- その長さ分だけ `self.rfile.read(length)` で読み取ると、本文のバイト列が手に入ります。
- `json.loads(バイト列)` でPythonの辞書に変換できます。
- 辞書からは `.get("action")` でキーの値を取り出せます（011の辞書の基本を思い出してください）。
- 形:
  ```python
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
  ```
