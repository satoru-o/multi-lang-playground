# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""python-dojo: 1分でできるPython練習問題システムのCLI本体。

使い方:
    uv run dojo.py today   # 今日の問題を出す（未解決ならもう一度同じ問題を表示）
    uv run dojo.py hint    # 今日の問題のヒントを表示
    uv run dojo.py check   # workspace/answer.py を採点する
    uv run dojo.py answer  # 模範解答を表示（確認プロンプトあり）
    uv run dojo.py skip    # 今日の問題をスキップして次へ進めるようにする
    uv run dojo.py show ID # 任意の問題文を状態を変えずに表示する
    uv run dojo.py log     # 進捗サマリを表示する
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROBLEMS_DIR = ROOT / "problems"
STATE_DIR = ROOT / "state"
WORKSPACE_DIR = ROOT / "workspace"
TODAY_STATE_PATH = STATE_DIR / "today.json"
PROGRESS_LOG_PATH = STATE_DIR / "progress.jsonl"
ANSWER_PATH = WORKSPACE_DIR / "answer.py"


def load_problem(problem_id: str) -> dict:
    matches = list(PROBLEMS_DIR.glob(f"{problem_id}_*"))
    if not matches:
        print(f"問題 {problem_id} が見つかりません。")
        sys.exit(1)
    problem_dir = matches[0]
    with open(problem_dir / "problem.json", encoding="utf-8") as f:
        problem = json.load(f)
    problem["_dir"] = problem_dir
    return problem


def all_problems() -> list[dict]:
    problems = []
    for problem_json in sorted(PROBLEMS_DIR.glob("*/problem.json")):
        with open(problem_json, encoding="utf-8") as f:
            problem = json.load(f)
        problem["_dir"] = problem_json.parent
        problems.append(problem)
    problems.sort(key=lambda p: p["order"])
    return problems


def load_today_state() -> dict:
    if not TODAY_STATE_PATH.exists():
        return {"current_id": None, "status": None, "assigned_at": None, "resolved_at": None}
    with open(TODAY_STATE_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_today_state(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with open(TODAY_STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
        f.write("\n")


def read_progress_ids() -> set[str]:
    if not PROGRESS_LOG_PATH.exists():
        return set()
    ids = set()
    with open(PROGRESS_LOG_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            ids.add(json.loads(line)["id"])
    return ids


def append_progress(problem: dict, result: str) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "id": problem["id"],
        "order": problem["order"],
        "title": problem["title"],
        "result": result,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }
    with open(PROGRESS_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def reset_answer_file(problem: dict) -> None:
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    header = (
        f"# 問題 {problem['id']}: {problem['title']}\n"
        f"# お題: {problem['prompt']}\n"
        f"#\n"
        f"# ヒント: uv run dojo.py hint\n"
        f"# 採点:   uv run dojo.py check\n"
        f"\n"
    )
    with open(ANSWER_PATH, "w", encoding="utf-8") as f:
        f.write(header)


def print_prompt(problem: dict) -> None:
    print(f"[{problem['id']}] {problem['title']}")
    print(problem["prompt"])


def cmd_today(args: argparse.Namespace) -> None:
    state = load_today_state()

    if state["current_id"] and state["status"] == "assigned":
        problem = load_problem(state["current_id"])
        print("今日の問題はまだ未解決です（先にこれを解いてください）:")
        print_prompt(problem)
        return

    if args.random:
        solved_ids = {
            json.loads(line)["id"]
            for line in PROGRESS_LOG_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip() and json.loads(line)["result"] == "solved"
        } if PROGRESS_LOG_PATH.exists() else set()
        if not solved_ids:
            print("復習できる解答済みの問題がまだありません。")
            return
        import random

        problem = load_problem(random.choice(sorted(solved_ids)))
        print("復習問題（ランダム出題）:")
        print_prompt(problem)
        return

    done_ids = read_progress_ids()
    remaining = [p for p in all_problems() if p["id"] not in done_ids]
    if not remaining:
        print("全問クリアしました！ `uv run dojo.py today --random` で復習できます。")
        return

    problem = remaining[0]
    save_today_state(
        {
            "current_id": problem["id"],
            "status": "assigned",
            "assigned_at": datetime.now().isoformat(timespec="seconds"),
            "resolved_at": None,
        }
    )
    reset_answer_file(problem)
    print("今日の問題:")
    print_prompt(problem)
    print(f"\n{ANSWER_PATH.relative_to(ROOT)} に答えを書いて `uv run dojo.py check` で採点してください。")


def cmd_hint(args: argparse.Namespace) -> None:
    state = load_today_state()
    if not state["current_id"]:
        print("今日の問題がまだありません。先に `uv run dojo.py today` を実行してください。")
        return
    problem = load_problem(state["current_id"])
    hint_path = problem["_dir"] / "hint.md"
    print(hint_path.read_text(encoding="utf-8"))


def cmd_answer(args: argparse.Namespace) -> None:
    state = load_today_state()
    if not state["current_id"]:
        print("今日の問題がまだありません。先に `uv run dojo.py today` を実行してください。")
        return
    reply = input("本当に模範解答を表示しますか？ [y/N]: ").strip().lower()
    if reply != "y":
        print("キャンセルしました。")
        return
    problem = load_problem(state["current_id"])
    solution_path = problem["_dir"] / "solution.py"
    print(solution_path.read_text(encoding="utf-8"))


def run_stdout_check(check: dict) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            [sys.executable, str(ANSWER_PATH)],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except subprocess.TimeoutExpired:
        return False, "実行がタイムアウトしました。"

    if result.returncode != 0:
        return False, f"実行時にエラーが発生しました:\n{result.stderr}"

    expected = check["expected_stdout"].rstrip("\n")
    actual = result.stdout.rstrip("\n")
    if actual == expected:
        return True, ""
    return False, f"出力が一致しません。\n  期待値: {expected!r}\n  実際の出力: {actual!r}"


def run_function_check(check: dict) -> tuple[bool, str]:
    spec = importlib.util.spec_from_file_location("answer", ANSWER_PATH)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        return False, f"実行時にエラーが発生しました: {e!r}"

    fn = getattr(module, check["function"], None)
    if fn is None:
        return False, f"関数 {check['function']} が定義されていません。"

    lines = []
    all_ok = True
    for case in check["cases"]:
        args = case.get("args", [])
        kwargs = case.get("kwargs", {})
        try:
            actual = fn(*args, **kwargs)
            ok = actual == case["expected"]
        except Exception as e:
            actual = f"<例外発生: {e!r}>"
            ok = False
        all_ok = all_ok and ok
        mark = "OK" if ok else "NG"
        lines.append(f"  [{mark}] {check['function']}({', '.join(map(repr, args))}) -> {actual!r} (期待値: {case['expected']!r})")
    return all_ok, "\n".join(lines)


def cmd_check(args: argparse.Namespace) -> None:
    state = load_today_state()
    if not state["current_id"]:
        print("今日の問題がまだありません。先に `uv run dojo.py today` を実行してください。")
        return
    if state["status"] != "assigned":
        print("今日の問題はすでに解決済みです。`uv run dojo.py today` で次の問題に進んでください。")
        return

    problem = load_problem(state["current_id"])
    check = problem["check"]

    if check["mode"] == "stdout":
        ok, detail = run_stdout_check(check)
    elif check["mode"] == "function":
        ok, detail = run_function_check(check)
    else:
        print(f"未対応のチェックモードです: {check['mode']}")
        return

    if detail:
        print(detail)

    if ok:
        print("\n合格！お疲れさまでした。")
        state["status"] = "solved"
        state["resolved_at"] = datetime.now().isoformat(timespec="seconds")
        save_today_state(state)
        append_progress(problem, "solved")
        print("`uv run dojo.py today` で次の問題に進めます。")
    else:
        print("\n不合格。workspace/answer.py を直してもう一度 `uv run dojo.py check` してください。")


def cmd_skip(args: argparse.Namespace) -> None:
    state = load_today_state()
    if not state["current_id"] or state["status"] != "assigned":
        print("スキップ対象の問題がありません。")
        return
    problem = load_problem(state["current_id"])
    state["status"] = "skipped"
    state["resolved_at"] = datetime.now().isoformat(timespec="seconds")
    save_today_state(state)
    append_progress(problem, "skipped")
    print(f"問題 {problem['id']} をスキップしました。`uv run dojo.py today` で次の問題に進めます。")


def cmd_show(args: argparse.Namespace) -> None:
    problem = load_problem(args.id)
    print_prompt(problem)


def cmd_log(args: argparse.Namespace) -> None:
    problems = all_problems()
    total = len(problems)
    records = []
    if PROGRESS_LOG_PATH.exists():
        with open(PROGRESS_LOG_PATH, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))

    solved = sum(1 for r in records if r["result"] == "solved")
    skipped = sum(1 for r in records if r["result"] == "skipped")

    print(f"進捗: {solved}/{total} 完了 (skipped: {skipped})")
    for r in records:
        date = r["timestamp"].split("T")[0]
        label = "合格" if r["result"] == "solved" else "スキップ"
        print(f"  {r['id']}  {date}  {label}  {r['title']}")

    done_ids = {r["id"] for r in records}
    remaining = [p["id"] for p in problems if p["id"] not in done_ids]
    if remaining:
        print(f"残り: {', '.join(remaining)}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="python-dojo CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_today = subparsers.add_parser("today", help="今日の問題を出す")
    p_today.add_argument("--random", action="store_true", help="解答済みの問題からランダムに復習出題する")
    p_today.set_defaults(func=cmd_today)

    p_hint = subparsers.add_parser("hint", help="今日の問題のヒントを表示")
    p_hint.set_defaults(func=cmd_hint)

    p_answer = subparsers.add_parser("answer", help="模範解答を表示（確認あり）")
    p_answer.set_defaults(func=cmd_answer)

    p_check = subparsers.add_parser("check", help="workspace/answer.py を採点する")
    p_check.set_defaults(func=cmd_check)

    p_skip = subparsers.add_parser("skip", help="今日の問題をスキップする")
    p_skip.set_defaults(func=cmd_skip)

    p_show = subparsers.add_parser("show", help="任意の問題文を表示（状態は変更しない）")
    p_show.add_argument("id", help="問題ID（例: 003）")
    p_show.set_defaults(func=cmd_show)

    p_log = subparsers.add_parser("log", help="進捗サマリを表示")
    p_log.set_defaults(func=cmd_log)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
