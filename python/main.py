#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import datetime
from pathlib import Path
import openai
from openai import OpenAI
from typing import Dict, List, Tuple, Optional, Any
from tool import (
    list_file, read_file, write_file, ask_question, 
    execute_command, complete, ToolResponse
)
from parser import parse_and_execute_tool, TOOL_TYPE_COMPLETE, TOOL_TYPE_ASK_QUESTION, TOOL_TYPE_EXECUTE_COMMAND

# ログを記録する関数
def log_to_file(log_type: str, data: Any):
    try:
        # ログディレクトリがなければ作成
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # 日付を含むログファイル名を生成
        today = datetime.datetime.now().strftime("%Y%m%d")
        log_file = log_dir / f"agent_log_{today}.jsonl"
        
        # タイムスタンプを生成
        timestamp = datetime.datetime.now().isoformat()
        
        # ログエントリを作成
        log_entry = {
            "timestamp": timestamp,
            "type": log_type,
            "data": data
        }
        
        # ログファイルに追記
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"ログの記録中にエラーが発生しました: {str(e)}")

def main():
    # OpenAI APIキーを環境変数から取得
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEYが設定されていません")
        return
    
    # OpenAI APIクライアントを初期化
    client = OpenAI(api_key=api_key)
    
    # システムプロンプトを設定
    system_prompt = """あなたはコーディングエージェントです。以下のツールを使ってタスクを完了してください：

# ListFile
ディレクトリ内のファイル一覧を取得します。
<list_file>
<path>ディレクトリのパス</path>
<recursive>true または false</recursive>
</list_file>

# ReadFile
ファイルの内容を読み取ります。
<read_file>
<path>ファイルのパス</path>
</read_file>

# WriteFile
ファイルに内容を書き込みます。
<write_file>
<path>ファイルのパス</path>
<content>
書き込む内容
</content>
</write_file>

# AskQuestion
ユーザーに質問します。
<ask_question>
<question>質問内容</question>
</ask_question>

# ExecuteCommand
コマンドを実行します。
<execute_command>
<command>実行するコマンド</command>
<requires_approval>true または false</requires_approval>
</execute_command>

# Complete
タスクの完了を示します。
<complete>
<result>タスクの結果や成果物の説明</result>
</complete>

重要な指示：
1. 必ず上記のいずれかのツールを使用してください。
2. ツールを使わずに直接回答することは絶対に禁止です。
3. 直接コードを提示するのではなく、WriteFileツールを使用してファイルを作成してください。
4. タスクが完了したらCompleteツールを使用して明示的に終了を示してください。
5. タスクが複雑な場合は、まずAskQuestionツールを使用して詳細を確認してください。

例：電卓アプリ作成の場合は、WriteFileツールを使用してcalculator.pyなどのファイルにコードを書き込み、必要に応じてExecuteCommandでテストを実行し、最終的にCompleteで完了を示してください。

回答形式の例：
<write_file>
<path>example.py</path>
<content>
print("Hello World")
</content>
</write_file>
"""

    # ユーザーからのタスク入力を受け取る
    print("コーディングエージェントにタスクを入力してください:")
    user_task = input()
    
    # 初期化メッセージを表示
    print("\nAI Coding Agentを初期化しています...")
    print("このエージェントは与えられたタスクを解決するためにツールを使用します。")
    print("処理には少し時間がかかる場合があります。しばらくお待ちください。\n")
    
    # 会話履歴を初期化
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_task}
    ]
    
    # メインループ
    is_complete = False
    while not is_complete:
        # リクエストデータをログに記録
        log_to_file("request", messages)
        
        # LLMにリクエストを送信
        response = client.chat.completions.create(
            model="gpt-4",  # OpenAIの最新モデルを使用
            messages=messages,
            temperature=0.2,  # より決定論的な応答を促す
            max_tokens=2000,  # 十分な長さの応答を確保
            top_p=0.95        # 出力の多様性を若干制限
        )
        
        # LLMのレスポンスを取得
        assistant_response = response.choices[0].message.content
        
        # レスポンスデータをログに記録
        log_to_file("response", assistant_response)
        
        # レスポンスをパースしてツールを実行
        tool_response, tool_type, complete_flag = parse_and_execute_tool(assistant_response)
        
        # ツールの実行結果をメッセージに追加
        messages.append({
            "role": "assistant",
            "content": assistant_response
        })
        
        # ツールの実行結果をユーザーに表示
        if tool_type != TOOL_TYPE_ASK_QUESTION and tool_type != TOOL_TYPE_EXECUTE_COMMAND:
            print(f"\n[{tool_type}] {tool_response.message}")
        
        # ツールの実行に失敗した場合、AIに具体的なエラーと指示を返す
        if not tool_response.success and tool_type == "":
            error_message = "エラー: 有効なツールが見つかりませんでした。以下のいずれかのツールを使用してください: list_file, read_file, write_file, ask_question, execute_command, complete。適切なXML形式で回答してください。"
            messages.append({
                "role": "user",
                "content": f"[Error] {error_message}"
            })
        else:
            # ツールの実行結果をメッセージに追加
            messages.append({
                "role": "user",
                "content": f"[{tool_type} Result] {tool_response.message}"
            })
        
        # ツールの実行結果をログに記録
        log_to_file("tool_result", {
            "tool_type": tool_type,
            "message": tool_response.message,
            "success": tool_response.success
        })
        
        # Completeツールが実行された場合はループを終了
        if complete_flag:
            is_complete = True

if __name__ == "__main__":
    main() 