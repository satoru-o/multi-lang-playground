# ヒント

- 新しいリストを空で用意し（`result = []`）、ループの中で条件に合うものだけ `result.append(x)` します。
- 形:
  ```python
  def even_only(numbers):
      result = []
      for n in numbers:
          if n % 2 == 0:
              result.append(n)
      return result
  ```
