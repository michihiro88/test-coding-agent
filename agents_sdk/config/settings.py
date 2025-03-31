#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
設定モジュール

このモジュールは、アプリケーション設定と環境変数の管理を担当します。
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# デフォルト設定
DEFAULT_SETTINGS = {
    "MODEL_NAME": "gpt-4",
    "LOG_LEVEL": "INFO",
    "ENABLE_TRACING": "true",
}

class Settings:
    """設定クラス
    
    アプリケーション設定の管理と環境変数へのアクセスを提供します。
    """
    
    def __init__(self):
        """設定の初期化"""
        # 環境変数をロード
        load_dotenv()
        
        # 設定値の初期化
        self._settings = DEFAULT_SETTINGS.copy()
        
        # 環境変数から設定を更新
        for key in self._settings:
            env_value = os.getenv(key)
            if env_value is not None:
                self._settings[key] = env_value
    
    def get(self, key: str, default: Any = None) -> Any:
        """設定値を取得
        
        Args:
            key: 設定キー
            default: デフォルト値
            
        Returns:
            設定値
        """
        return self._settings.get(key, default)
    
    def get_api_key(self) -> Optional[str]:
        """OpenAI APIキーを取得
        
        Returns:
            APIキー
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("警告: OPENAI_API_KEYが設定されていません")
        return api_key
    
    def get_model_name(self) -> str:
        """使用するモデル名を取得
        
        Returns:
            モデル名
        """
        return self.get("MODEL_NAME")
    
    def is_tracing_enabled(self) -> bool:
        """トレース機能が有効かどうかを取得
        
        Returns:
            トレース機能が有効かどうか
        """
        return self.get("ENABLE_TRACING", "false").lower() == "true"
    
    def get_log_level(self) -> str:
        """ログレベルを取得
        
        Returns:
            ログレベル
        """
        return self.get("LOG_LEVEL")
    
    def get_all(self) -> Dict[str, Any]:
        """すべての設定値を取得
        
        Returns:
            全設定値の辞書
        """
        return self._settings.copy()

# シングルトンインスタンス
_settings = Settings()

# モジュールレベルの関数

def get_api_key() -> Optional[str]:
    """OpenAI APIキーを取得"""
    return _settings.get_api_key()

def get_model_name() -> str:
    """使用するモデル名を取得"""
    return _settings.get_model_name()

def is_tracing_enabled() -> bool:
    """トレース機能が有効かどうかを取得"""
    return _settings.is_tracing_enabled()

def get_log_level() -> str:
    """ログレベルを取得"""
    return _settings.get_log_level()

def get(key: str, default: Any = None) -> Any:
    """設定値を取得"""
    return _settings.get(key, default)

def get_all() -> Dict[str, Any]:
    """すべての設定値を取得"""
    return _settings.get_all() 