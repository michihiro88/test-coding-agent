#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ユーザー対話ツール

このモジュールには、ユーザーとの対話に関連するツール関数が含まれています。
"""

import os
import sys
from typing import Dict, Any
from agents import function_tool, RunContextWrapper

# 相対インポートを絶対インポートに変更
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from log_manager import logger

@function_tool
async def ask_question(ctx: RunContextWrapper[Any], question: str) -> str:
    """ユーザーに質問します。
    
    Args:
        question: 質問内容
        
    Returns:
        ユーザーの回答
    """
    try:
        # 質問を表示してユーザー入力を取得
        print(f"\n質問: {question}")
        print("回答: ", end="")
        answer = input().strip()
        
        # ログに記録
        logger.log_tool_result("ask_question", {
            "question": question,
            "answer_length": len(answer)
        })
        
        return answer
    
    except Exception as e:
        error_message = f"ユーザー質問中にエラーが発生しました: {str(e)}"
        logger.log_error(error_message, e)
        return error_message

@function_tool
async def complete(ctx: RunContextWrapper[Any], result: str) -> str:
    """タスクの完了を示します。
    
    Args:
        result: タスクの結果や成果物の説明
        
    Returns:
        完了メッセージ
    """
    try:
        # 完了メッセージの作成
        message = f"タスクが完了しました: {result}"
        
        # ログに記録
        logger.log_tool_result("complete", {
            "result": result
        })
        
        return message
    
    except Exception as e:
        error_message = f"タスク完了処理中にエラーが発生しました: {str(e)}"
        logger.log_error(error_message, e)
        return error_message 