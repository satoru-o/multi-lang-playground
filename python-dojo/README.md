# python-dojo

1分〜数分で終わる、超小さなPython練習問題を「今日は1問だけ」出題する仕組みです。
外部ライブラリは使いません（Python標準ライブラリのみ）。実行には [uv](https://docs.astral.sh/uv/) を使います。

## 基本の使い方

```
uv run dojo.py today   # 今日の問題を表示する（すでに出題中ならそれをもう一度表示）
$EDITOR workspace/answer.py   # 自分の手で答えを書く
uv run dojo.py check   # 採点する（何度でも再実行OK、失敗してもペナルティなし）
```

これで合格すると、次に `uv run dojo.py today` を実行したときに次の問題が出題されます。
「1問だけ」出題する設計なので、今の問題を解く（または `skip` する）まで次には進めません。

## その他のコマンド

```
uv run dojo.py hint       # 今日の問題のヒントを表示
uv run dojo.py answer     # 模範解答を表示（誤って見ないよう確認プロンプトあり）
uv run dojo.py skip       # どうしても詰まったら今日の問題をスキップして次へ
uv run dojo.py show 003   # 過去/任意の問題文を読み返す（状態は変えない）
uv run dojo.py log        # 進捗サマリを表示
uv run dojo.py today --random   # 全問クリア後、解答済みの問題からランダムに復習出題
```

## ディレクトリ構成

- `problems/NNN_.../` — 問題ごとのフォルダ。`problem.json`（お題文とチェック方法）、`hint.md`（ヒント）、`solution.py`（模範解答）。
  `hint`/`answer` コマンド以外ではこれらのファイルは開かないので、`today`/`check` を使う限り誤ってネタバレしません。
- `workspace/answer.py` — 自分が書く答案。常にこの1ファイルだけを使います。
- `state/today.json` — 現在出題中の問題と状態（assigned/solved/skipped）。
- `state/progress.jsonl` — 解答記録（1行1JSON、追記のみ）。

## 出題トピックと採点方式

| 問題 | トピック | 採点方式（`problem.json` の `check.mode`） |
|---|---|---|
| 001〜005 | 変数・条件分岐・ループ | `stdout` — スクリプト全体を実行し、標準出力を比較 |
| 006〜016 | 関数・文字列/リスト操作・辞書・タプル・内包表記 | `function` — `workspace/answer.py` から指定した関数を呼び出して戻り値を比較 |
| 017 | 簡単なクラス定義 | `class` — 指定したクラスをインスタンス化し、属性やメソッドの結果を確認 |
| 018 | クラスの組み合わせ | `stdout` |
| 019〜023 | くだらないHTTP API（`http.server`のみ、フレームワーク不使用） | `http` — `Handler` という名前のクラス（`BaseHTTPRequestHandler`のサブクラス）を、`check`実行時に裏で自動的にサーバーとして起動し、リクエストを送って応答を確認したあとサーバーを閉じる。**サーバーを手動で起動したり別ターミナルで叩いたりする必要はなく、`uv run dojo.py check` を実行するだけで完結します。** |

021以降の問題では `import json` が、019以降では `from http.server import BaseHTTPRequestHandler` が必要になります（001〜018にはimportが不要な問題しかありませんでした）。

## 注意

- `problems/*/solution.py` には模範解答がそのまま書かれています。このリポジトリを公開する場合は、答えが誰でも見える点に留意してください。
