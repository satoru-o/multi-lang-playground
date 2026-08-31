# ヒント

- Cat クラスは017と同じ形で大丈夫です。
- 複数のインスタンスをリストに入れるには `cats = [Cat("たま", 3), Cat("ミケ", 5), Cat("クロ", 1)]` のように書きます。
- 平均年齢は、for文か内包表記で各インスタンスの `.age` を集めて `sum(...) / len(...)` で計算できます。
  ```python
  ages = [cat.age for cat in cats]
  average_age = sum(ages) / len(ages)
  print(average_age)
  ```
