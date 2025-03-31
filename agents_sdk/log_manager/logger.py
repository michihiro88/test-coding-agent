#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ロギングモジュール

このモジュールは、ログ記録と追跡機能を提供します。
"""

import os
import json
import datetime
import logging
from typing import Any, Dict, Optional
from pathlib import Path

try:
    from agents.tracing import enable_tracing
    TRACING_AVAILABLE = True
except ImportError:
    TRACING_AVAILABLE = False

# 絶対インポートに変更
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings

# ロガーの設定
logging.basicConfig(
    level=getattr(logging, settings.get_log_level(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("ai_coding_agent")

# ログディレクトリのパス
LOG_DIR = Path("logs")

def setup_logging() -> None:
    """ロギング機能のセットアップ"""
    # ログディレクトリの作成
    LOG_DIR.mkdir(exist_ok=True)
    
    # トレース機能の有効化（利用可能な場合）
    if TRACING_AVAILABLE and settings.is_tracing_enabled():
        # 日付を含むトレースファイル名のプレフィックス
        today = datetime.datetime.now().strftime("%Y%m%d")
        trace_prefix = f"agent_trace_{today}"
        
        try:
            enable_tracing(
                directory=str(LOG_DIR),
                file_prefix=trace_prefix
            )
            logger.info(f"トレース機能を有効化しました: {LOG_DIR}/{trace_prefix}")
        except Exception as e:
            logger.error(f"トレース機能の有効化に失敗しました: {str(e)}")

def get_log_file() -> Path:
    """現在の日付に基づくログファイルパスを取得"""
    today = datetime.datetime.now().strftime("%Y%m%d")
    return LOG_DIR / f"agent_log_{today}.jsonl"

def log_event(event_type: str, data: Any) -> None:
    """イベントをログファイルに記録
    
    Args:
        event_type: イベントの種類
        data: イベントデータ
    """
    try:
        # ログディレクトリの作成（存在しない場合）
        LOG_DIR.mkdir(exist_ok=True)
        
        # ログファイルの取得
        log_file = get_log_file()
        
        # タイムスタンプの生成
        timestamp = datetime.datetime.now().isoformat()
        
        # ログエントリの作成
        log_entry = {
            "timestamp": timestamp,
            "event_type": event_type,
            "data": data
        }
        
        # JSONLファイルへの書き込み
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False, default=_json_serializer) + "\n")
        
        # ロガーにも記録
        logger.debug(f"イベント記録: {event_type}")
    
    except Exception as e:
        logger.error(f"ログの記録中にエラーが発生しました: {str(e)}")

def _json_serializer(obj: Any) -> Any:
    """JSON変換できないオブジェクトをシリアライズする関数
    
    Args:
        obj: シリアライズするオブジェクト
        
    Returns:
        シリアライズされた値
    """
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    try:
        return str(obj)
    except:
        return None

def log_error(message: str, error: Optional[Exception] = None) -> None:
    """エラーをログに記録
    
    Args:
        message: エラーメッセージ
        error: 例外オブジェクト
    """
    error_data = {
        "message": message,
    }
    
    if error:
        error_data["error_type"] = type(error).__name__
        error_data["error_str"] = str(error)
    
    log_event("error", error_data)
    logger.error(message)

def log_request(messages: list) -> None:
    """リクエストをログに記録
    
    Args:
        messages: メッセージリスト
    """
    log_event("request", {"messages": messages})

def log_response(response: Any) -> None:
    """レスポンスをログに記録
    
    Args:
        response: レスポンスデータ
    """
    log_event("response", {"response": response})

def log_tool_call(tool_name: str, arguments: Dict[str, Any]) -> None:
    """ツール呼び出しをログに記録
    
    Args:
        tool_name: ツール名
        arguments: ツール引数
    """
    log_event("tool_call", {
        "tool_name": tool_name,
        "arguments": arguments
    })

def log_tool_result(tool_name: str, result: Any) -> None:
    """ツール実行結果をログに記録
    
    Args:
        tool_name: ツール名
        result: 実行結果
    """
    log_event("tool_result", {
        "tool_name": tool_name,
        "result": result
    }) 