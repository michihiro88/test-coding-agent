#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
コマンド実行ツール

このモジュールには、コマンド実行に関連するツール関数が含まれています。
"""

import os
import sys
import subprocess
from typing import List, Dict, Any
from agents import function_tool, RunContextWrapper

# 相対インポートを絶対インポートに変更
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from log_manager import logger
from utils import helpers

@function_tool
async def execute_command(ctx: RunContextWrapper[Any], command: str, requires_approval: str) -> str:
    """コマンドを実行します。
    
    Args:
        command: 実行するコマンド
        requires_approval: ユーザー承認が必要かどうか（"true"または"false"）
        
    Returns:
        コマンド実行結果
    """
    try:
        # 承認フラグの変換
        needs_approval = helpers.to_bool(requires_approval)
        
        # 安全性チェック
        is_safe = helpers.is_command_safe(command)
        
        if not is_safe:
            error_message = f"安全でないコマンド '{command}' の実行を拒否しました。"
            logger.log_error(error_message)
            return error_message
        
        # ユーザー承認が必要な場合
        if needs_approval:
            approve = input(f"次のコマンドを実行してもよろしいですか？\n{command}\n(y/n): ")
            if approve.lower() != 'y':
                return "コマンドの実行はユーザーによって拒否されました。"
        
        # コマンド実行
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        # 結果の構築
        output = result.stdout or ""
        errors = result.stderr or ""
        
        if result.returncode == 0:
            status = f"コマンド '{command}' は正常に完了しました。(戻り値: {result.returncode})"
        else:
            status = f"コマンド '{command}' は戻り値 {result.returncode} で終了しました。"
        
        # ログに記録
        logger.log_tool_result("execute_command", {
            "command": command,
            "exit_code": result.returncode,
            "output_length": len(output),
            "error_length": len(errors)
        })
        
        # 結果の整形
        command_result = f"{status}\n\n"
        
        if output:
            command_result += f"出力:\n{output}\n\n"
        
        if errors:
            command_result += f"エラー:\n{errors}\n"
        
        return command_result
    
    except Exception as e:
        error_message = f"コマンド実行中にエラーが発生しました: {str(e)}"
        logger.log_error(error_message, e)
        return error_message 