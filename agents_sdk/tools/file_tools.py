#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ファイル操作ツール

このモジュールには、ファイル操作に関連するツール関数が含まれています。
"""

import os
import glob
import sys
from typing import List, Union, Any
from pathlib import Path
from agents import function_tool, RunContextWrapper

# 相対インポートを絶対インポートに変更
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from log_manager import logger
from utils import helpers

@function_tool
async def list_file(ctx: RunContextWrapper[Any], path: str, recursive: str) -> str:
    """ディレクトリ内のファイル一覧を取得します。
    
    Args:
        path: ディレクトリのパス
        recursive: 再帰的に検索するかどうか（"true"または"false"）
        
    Returns:
        ファイル一覧の文字列
    """
    try:
        # パスの正規化
        norm_path = helpers.normalize_path(path)
        
        # 再帰的フラグの変換
        is_recursive = helpers.to_bool(recursive)
        
        files = []
        if is_recursive:
            # 再帰的に検索
            for file_path in norm_path.rglob("*"):
                if file_path.is_file():
                    files.append(str(file_path))
        else:
            # 非再帰的に検索
            for file_path in norm_path.glob("*"):
                if file_path.is_file():
                    files.append(str(file_path))
        
        # 結果をフォーマット
        if files:
            result = f"ディレクトリ '{path}' 内のファイル一覧:\n"
            for file in sorted(files):
                result += f"- {file}\n"
        else:
            result = f"ディレクトリ '{path}' 内にファイルはありません。"
        
        # ログに記録
        logger.log_tool_result("list_file", {
            "path": path,
            "recursive": recursive,
            "file_count": len(files)
        })
        
        return result
    
    except Exception as e:
        error_message = f"ファイル一覧の取得中にエラーが発生しました: {str(e)}"
        logger.log_error(error_message, e)
        return error_message

@function_tool
async def read_file(ctx: RunContextWrapper[Any], path: str) -> str:
    """ファイルの内容を読み取ります。
    
    Args:
        path: ファイルのパス
        
    Returns:
        ファイルの内容
    """
    try:
        # パスの正規化
        norm_path = helpers.normalize_path(path)
        
        # ファイルの存在確認
        if not norm_path.exists():
            error_message = f"ファイル '{path}' が見つかりません。"
            logger.log_error(error_message)
            return error_message
        
        # ファイルの読み取り
        content = helpers.read_file_safe(norm_path)
        
        # ログに記録
        logger.log_tool_result("read_file", {"path": path})
        
        return content if content else f"ファイル '{path}' は空です。"
    
    except Exception as e:
        error_message = f"ファイルの読み取り中にエラーが発生しました: {str(e)}"
        logger.log_error(error_message, e)
        return error_message

@function_tool
async def write_file(ctx: RunContextWrapper[Any], path: str, content: str) -> str:
    """ファイルに内容を書き込みます。
    
    Args:
        path: ファイルのパス
        content: 書き込む内容
        
    Returns:
        結果メッセージ
    """
    try:
        # パスの正規化
        norm_path = helpers.normalize_path(path)
        
        # 親ディレクトリの作成
        norm_path.parent.mkdir(parents=True, exist_ok=True)
        
        # ファイルの書き込み
        success = helpers.write_file_safe(norm_path, content)
        
        if success:
            result = f"ファイル '{path}' への書き込みが完了しました。"
        else:
            result = f"ファイル '{path}' への書き込みに失敗しました。"
        
        # ログに記録
        logger.log_tool_result("write_file", {
            "path": path,
            "success": success,
            "content_length": len(content) if content else 0
        })
        
        return result
    
    except Exception as e:
        error_message = f"ファイルの書き込み中にエラーが発生しました: {str(e)}"
        logger.log_error(error_message, e)
        return error_message 