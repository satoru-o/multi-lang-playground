# ヒント

- 複数の値を1つのタプルとしてまとめて返すには `return 値1, 値2` のようにカンマで区切って書きます（自動的にタプルになります）。
- 合計は `sum(numbers)`、要素数は `len(numbers)` で求められます。
- 形:
  ```python
  def sum_and_avg(numbers):
      total = sum(numbers)
      avg = total / len(numbers)
      return total, avg
  ```
