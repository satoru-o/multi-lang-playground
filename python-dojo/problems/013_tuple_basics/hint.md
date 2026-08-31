# ヒント

- 複数の値をまとめて受け取ったデータは、`name, age = cat` のように書くと、一度に複数の変数へ分解して代入できます（分解代入）。
- 形:
  ```python
  def describe_cat(cat):
      name, age = cat
      return f"{name}は{age}歳です"
  ```
