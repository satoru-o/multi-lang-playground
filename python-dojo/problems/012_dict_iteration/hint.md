# ヒント

- `辞書.items()` を使うと、キーと値のペアを順番に取り出せます。
- 形:
  ```python
  def total_price(prices):
      total = 0
      for key, value in prices.items():
          total += value
      return total
  ```
- このお題ではキー（商品名）は使いませんが、`items()` の書き方に慣れるのが目的です。
