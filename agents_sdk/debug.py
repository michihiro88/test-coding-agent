#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
デバッグ用スクリプト
"""

import sys
import traceback
import os

# カレントディレクトリをPythonパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from agents import Agent
    
    # Agentクラスのパラメータを確認
    print("Agentクラスの初期化パラメータ:")
    print(Agent.__init__.__code__.co_varnames)
    
    # エージェントを作成してみる
    agent = Agent(
        name="Test Agent",
        tools=[],
        instructions="This is a test"
    )
    print("エージェントの作成に成功しました。")
    
except Exception as e:
    error_message = f"エラー: {e}\n"
    error_message += traceback.format_exc()
    print(error_message)
    
    # エラーをファイルに書き出す
    with open("debug_error.log", "w", encoding="utf-8") as f:
        f.write(error_message) 