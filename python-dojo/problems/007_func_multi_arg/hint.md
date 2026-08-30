# ヒント

- 引数は `def larger(a, b):` のようにカンマで区切って複数受け取れます。
- 「同じ値なら a を返す」ので、`b > a` のときだけ b を返す、という条件にすると自然に満たせます。
- 形:
  ```python
  def larger(a, b):
      if b > a:
          return b
      return a
  ```
