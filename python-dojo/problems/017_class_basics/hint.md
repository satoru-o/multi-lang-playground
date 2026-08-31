# ヒント

- クラスは `class クラス名:` で定義します。
- `__init__` はインスタンスを作成したときに自動で呼ばれる特別なメソッドです。第一引数は必ず `self`（自分自身）にします。
- インスタンスに値を保存するには `self.属性名 = 値` とします。
- 形:
  ```python
  class Cat:
      def __init__(self, name, age):
          self.name = name
          self.age = age

      def describe(self):
          return f"{self.name}は{self.age}歳です"
  ```
- 使うときは `Cat("たま", 3)` のように書くとインスタンスが作られます。
