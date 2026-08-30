# ヒント

- 3つ以上に分岐したいときは `elif` を使います。
- 形:
  ```python
  if score >= 80:
      print("合格")
  elif score >= 50:
      print("もう少し")
  else:
      print("要復習")
  ```
- 上から順に条件を評価し、最初に条件が True になったブロックだけが実行されます。
