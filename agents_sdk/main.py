#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AI Coding Agent メインモジュール

OpenAI Agents SDKを使用したAI Coding Agentのメインモジュールです。
"""

import os
import sys
import asyncio
from pathlib import Path

# sys.pathにプロジェクトのルートディレクトリを追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# OpenAI Agents SDKのインポート
from agents import Agent, Runner
from typing import Dict, Any

# 内部モジュールのインポート
from config import settings
from log_manager import logger
from tools import file_tools, command_tools, interaction_tools

# システムプロンプトを外部ファイルから読み込む
def load_system_prompt():
    """システムプロンプトをファイルから読み込む
    
    Returns:
        str: システムプロンプト
    """
    prompt_file = Path(__file__).parent / "system_prompt.txt"
    
    # ファイルが存在しない場合はデフォルトのプロンプトを作成
    if not prompt_file.exists():
        create_default_system_prompt(prompt_file)
    
    # ファイルを読み込む
    with open(prompt_file, "r", encoding="utf-8") as f:
        return f.read()

def create_default_system_prompt(path):
    """デフォルトのシステムプロンプトファイルを作成"""
    prompt = """あなたはコーディングエージェントです。以下のツールを使ってタスクを完了してください：

# ListFile
ディレクトリ内のファイル一覧を取得します。
```python
@function_tool
async def list_file(ctx: RunContextWrapper[Any], path: str, recursive: str) -> str:
    \"\"\"ディレクトリ内のファイル一覧を取得します。\"\"\"
```

# ReadFile
ファイルの内容を読み取ります。
```python
@function_tool
async def read_file(ctx: RunContextWrapper[Any], path: str) -> str:
    \"\"\"ファイルの内容を読み取ります。\"\"\"
```

# WriteFile
ファイルに内容を書き込みます。
```python
@function_tool
async def write_file(ctx: RunContextWrapper[Any], path: str, content: str) -> str:
    \"\"\"ファイルに内容を書き込みます。\"\"\"
```

# AskQuestion
ユーザーに質問します。
```python
@function_tool
async def ask_question(ctx: RunContextWrapper[Any], question: str) -> str:
    \"\"\"ユーザーに質問します。\"\"\"
```

# ExecuteCommand
コマンドを実行します。
```python
@function_tool
async def execute_command(ctx: RunContextWrapper[Any], command: str, requires_approval: str) -> str:
    \"\"\"コマンドを実行します。\"\"\"
```

# Complete
タスクの完了を示します。
```python
@function_tool
async def complete(ctx: RunContextWrapper[Any], result: str) -> str:
    \"\"\"タスクの完了を示します。\"\"\"
```

重要な指示：
1. 必ず上記のいずれかのツールを使用してください。
2. ツールを使わずに直接回答することは絶対に禁止です。
3. 直接コードを提示するのではなく、WriteFileツールを使用してファイルを作成してください。
4. タスクが完了したらCompleteツールを使用して明示的に終了を示してください。
5. タスクが複雑な場合は、まずAskQuestionツールを使用して詳細を確認してください。
"""
    
    # ディレクトリが存在しない場合は作成
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # ファイルを書き込む
    with open(path, "w", encoding="utf-8") as f:
        f.write(prompt)

def initialize_agent():
    """エージェントの初期化
    
    Returns:
        Agent: 初期化されたエージェント
    """
    # APIキーの取得
    api_key = settings.get_api_key()
    if not api_key:
        print("エラー: OPENAI_API_KEYが設定されていません。")
        print(".envファイルにAPIキーを設定するか、環境変数として設定してください。")
        sys.exit(1)
    
    # システムプロンプトを読み込む
    system_prompt = load_system_prompt()
    
    # ツールの設定
    tools = [
        file_tools.list_file,
        file_tools.read_file,
        file_tools.write_file,
        command_tools.execute_command,
        interaction_tools.ask_question,
        interaction_tools.complete
    ]
    
    # エージェントの作成
    agent = Agent(
        name="AI Coding Agent",
        tools=tools,
        instructions=system_prompt,
        model=settings.get_model_name()
    )
    
    return agent

async def main_async():
    """非同期メイン関数"""
    # ロギングの初期化
    logger.setup_logging()
    logger.logger.info("AI Coding Agentを起動しています...")
    
    try:
        # エージェントの初期化
        agent = initialize_agent()
        logger.logger.info("エージェントの初期化が完了しました。")
        
        # ユーザーからのタスク入力
        print("===== AI Coding Agent =====")
        print("コーディングエージェントにタスクを入力してください:")
        user_task = input()
        
        print("\nAI Coding Agentを初期化しています...")
        print("このエージェントは与えられたタスクを解決するためにツールを使用します。")
        print("処理には少し時間がかかる場合があります。しばらくお待ちください。\n")
        
        # タスク実行
        result = await Runner.run(agent, user_task)
        
        # 最終出力の表示
        print(f"\n\n最終結果: {result.final_output}\n")
        
        print("\n\nAI Coding Agentのタスクが完了しました。")
    
    except KeyboardInterrupt:
        print("\n\nユーザーによって処理が中断されました。")
    except Exception as e:
        print(f"\n\nエラーが発生しました: {str(e)}")
        logger.log_error("プログラム実行中にエラーが発生しました", e)
    
    finally:
        print("\n===== 終了 =====")

def main():
    """メイン関数"""
    # asyncioでasyncのmain関数を実行
    asyncio.run(main_async())

if __name__ == "__main__":
    main() 