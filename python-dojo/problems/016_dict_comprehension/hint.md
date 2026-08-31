# ヒント

- 辞書内包表記の形: `{キー式: 値式 for 変数 in リスト}`
- 文字列の文字数は `len(word)` で求められます。
- 形:
  ```python
  def word_lengths(words):
      return {word: len(word) for word in words}
  ```
