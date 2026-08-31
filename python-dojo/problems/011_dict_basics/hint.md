# ヒント

- 辞書からキーを指定して値を取り出すには `data["name"]` と書けますが、キーが存在しないと `KeyError` になってしまいます。
- キーが存在しないときのデフォルト値を指定できる `data.get("name", "デフォルト値")` を使うと、存在しなければそのデフォルト値が返ります。
- 形:
  ```python
  def get_name(data):
      return data.get("name", "名無し")
  ```
