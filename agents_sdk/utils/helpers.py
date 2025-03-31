#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ヘルパーユーティリティ

このモジュールには、共通のユーティリティ関数が含まれています。
"""

import os
import sys
import json
import subprocess
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

def ensure_directory(path: Union[str, Path]) -> Path:
    """ディレクトリの存在を確認し、存在しない場合は作成
    
    Args:
        path: ディレクトリパス
        
    Returns:
        Path: ディレクトリパスのPathオブジェクト
    """
    path_obj = Path(path)
    path_obj.mkdir(parents=True, exist_ok=True)
    return path_obj

def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """安全にJSONをロード
    
    Args:
        json_str: JSON文字列
        default: エラー時のデフォルト値
        
    Returns:
        ロードされたオブジェクト、またはデフォルト値
    """
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default

def safe_json_dumps(obj: Any, ensure_ascii: bool = False, default: Any = None) -> str:
    """安全にJSONをダンプ
    
    Args:
        obj: ダンプするオブジェクト
        ensure_ascii: ASCII文字のみ使用するかどうか
        default: JSON変換できないオブジェクトの変換関数
        
    Returns:
        JSON文字列
    """
    try:
        return json.dumps(obj, ensure_ascii=ensure_ascii, default=default)
    except (TypeError, OverflowError):
        return "{}"

def is_windows() -> bool:
    """Windowsプラットフォームかどうかを判定
    
    Returns:
        Windowsの場合True
    """
    return sys.platform.startswith("win")

def run_command(command: str, shell: bool = True, check: bool = False) -> subprocess.CompletedProcess:
    """コマンドを実行
    
    Args:
        command: 実行するコマンド
        shell: シェル経由で実行するかどうか
        check: エラー時に例外を発生させるかどうか
        
    Returns:
        実行結果
    """
    if is_windows():
        # Windows環境ではPowerShellを使用
        process = subprocess.run(
            ["powershell.exe", "-Command", command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            check=check
        )
    else:
        # その他の環境
        process = subprocess.run(
            command,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            check=check
        )
    
    return process

def normalize_path(path: Union[str, Path]) -> Path:
    """パスを正規化
    
    Args:
        path: 正規化するパス
        
    Returns:
        正規化されたパス
    """
    return Path(os.path.normpath(os.path.expanduser(str(path))))

def read_file_safe(path: Union[str, Path], encoding: str = "utf-8", default: str = "") -> str:
    """安全にファイルを読み取り
    
    Args:
        path: ファイルパス
        encoding: エンコーディング
        default: エラー時のデフォルト値
        
    Returns:
        ファイル内容、またはデフォルト値
    """
    try:
        with open(path, "r", encoding=encoding) as f:
            return f.read()
    except (IOError, UnicodeDecodeError):
        return default

def write_file_safe(path: Union[str, Path], content: str, encoding: str = "utf-8") -> bool:
    """安全にファイルを書き込み
    
    Args:
        path: ファイルパス
        content: 書き込む内容
        encoding: エンコーディング
        
    Returns:
        成功した場合True
    """
    try:
        # ディレクトリが存在しない場合は作成
        ensure_directory(Path(path).parent)
        
        with open(path, "w", encoding=encoding) as f:
            f.write(content)
        return True
    except (IOError, UnicodeEncodeError):
        return False

def to_bool(value: Any) -> bool:
    """値をブール値に変換
    
    Args:
        value: 変換する値
        
    Returns:
        ブール値
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.lower() in ("yes", "true", "t", "1", "on", "y")
    return bool(value)

def load_config_file(file_name: str, default: Any = None) -> Any:
    """設定ファイルを読み込みます。
    
    Args:
        file_name: 設定ファイル名（config/ディレクトリ内）
        default: 読み込みに失敗した場合のデフォルト値
        
    Returns:
        読み込んだ設定データ、または失敗時にはデフォルト値
    """
    config_path = Path(__file__).parents[1] / "config" / file_name
    
    try:
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                if file_name.endswith(".json"):
                    return json.load(f)
                else:
                    return f.read()
        else:
            print(f"警告: 設定ファイル '{file_name}' が見つかりません")
            return default
    except (IOError, json.JSONDecodeError) as e:
        print(f"警告: 設定ファイル '{file_name}' の読み込みに失敗しました: {e}")
        return default

def is_command_safe(command: str) -> bool:
    """コマンドが安全に実行できるかどうかを確認します。
    外部の設定ファイルから禁止コマンドリストを読み取ります。
    
    Args:
        command: 実行するコマンド
        
    Returns:
        bool: コマンドが安全であればTrue、そうでなければFalse
    """
    # デフォルトの禁止コマンド（設定ファイルが見つからない場合に使用）
    default_forbidden = {
        "common": [
            "rm -rf", "deltree", "format", "del /s", "del /q",
            "shutdown", "reboot", "halt"
        ],
        "windows": [],
        "linux": []
    }
    
    # 禁止コマンドリストの読み込み
    config = load_config_file("forbidden_commands.json", default_forbidden)
    
    # 共通の禁止コマンド
    forbidden_commands = config.get("common", [])
    
    # OS固有の禁止コマンド
    if is_windows():
        os_specific_commands = config.get("windows", [])
    else:
        os_specific_commands = config.get("linux", [])
    
    # コマンドを小文字に変換
    command_lower = command.lower()
    
    # 共通の禁止コマンドをチェック
    for forbidden in forbidden_commands:
        if forbidden.lower() in command_lower:
            return False
    
    # OS固有の禁止コマンドをチェック
    for forbidden in os_specific_commands:
        if forbidden.lower() in command_lower:
            return False
    
    return True 