# OpenAI Agents SDKを使用したAI Coding Agentの再設計

## 1. 概要

この再設計案は、OpenAI Agents SDKを活用して、より堅牢かつ柔軟なAI Coding Agentを実装するためのものです。新しいSDKのパラダイムに合わせて、システム全体を再構築します。

## 2. アーキテクチャ

### 2.1 全体構成

```
agents_sdk/
├── main.py            # メインエントリポイント
├── tools/             # ツール定義
│   ├── __init__.py    
│   ├── file_tools.py   # ファイル操作関連ツール
│   ├── command_tools.py # コマンド実行関連ツール
│   └── interaction_tools.py # ユーザー対話関連ツール
├── logging/           # ログ機能
│   ├── __init__.py
│   └── logger.py      # ログ記録クラス
├── config/            # 設定ファイル
│   ├── __init__.py
│   └── settings.py    # 環境設定管理
├── utils/             # ユーティリティ
│   ├── __init__.py
│   └── helpers.py     # ヘルパー関数
├── .env.sample        # 環境変数サンプル
├── requirements.txt   # 依存パッケージ
└── README.md          # ドキュメント
```

### 2.2 主要コンポーネント

#### 2.2.1 Agent

- OpenAI Agents SDKの`Agent`クラスを使用
- 利用可能なツールの登録
- モデル設定の管理
- ガードレール機能の実装

#### 2.2.2 Runner

- OpenAI Agents SDKの`Runner`クラスを使用
- 対話のセッション管理
- ストリーミング処理の実装
- エラーハンドリング

#### 2.2.3 Tools

- `Tool`クラスを使用した機能定義
- デコレータを活用したツール定義
- ツール実行結果の適切なフォーマット

#### 2.2.4 Logger

- トレース機能を活用した詳細ログ
- 構造化ログフォーマット
- 日付ベースのログローテーション

## 3. フロー詳細

### 3.1 起動フロー

1. 環境変数のロード
2. ロガーの初期化
3. ツールの初期化と登録
4. エージェントの初期化
5. ランナーの初期化
6. ユーザーからのタスク入力受付
7. エージェント実行

### 3.2 タスク実行フロー

1. ユーザーからのタスク入力
2. エージェントへのタスク送信
3. エージェントによるツール選択と実行
4. ツール実行結果のエージェントへのフィードバック
5. 必要に応じてユーザーへの質問
6. タスク完了判定
7. 結果の表示とログ記録

### 3.3 ツール実行フロー

1. エージェントからのツール呼び出し受信
2. ツール引数の検証
3. ツールのビジネスロジック実行
4. 結果のフォーマット
5. エージェントへの結果返送
6. ログへの記録

## 4. 主なツール定義

### 4.1 ファイル操作ツール

```python
@Tool.as_function
def list_file(path: str, recursive: str) -> str:
    """ディレクトリ内のファイル一覧を取得します。"""
    # 実装...
    return "ファイル一覧: ..."

@Tool.as_function
def read_file(path: str) -> str:
    """ファイルの内容を読み取ります。"""
    # 実装...
    return "ファイル内容: ..."

@Tool.as_function
def write_file(path: str, content: str) -> str:
    """ファイルに内容を書き込みます。"""
    # 実装...
    return "書き込み完了: ..."
```

### 4.2 コマンド実行ツール

```python
@Tool.as_function
def execute_command(command: str, requires_approval: str) -> str:
    """コマンドを実行します。"""
    # 実装...
    return "コマンド実行結果: ..."
```

### 4.3 ユーザー対話ツール

```python
@Tool.as_function
def ask_question(question: str) -> str:
    """ユーザーに質問します。"""
    # 実装...
    return "ユーザーの回答: ..."
```

### 4.4 タスク完了ツール

```python
@Tool.as_function
def complete(result: str) -> str:
    """タスクの完了を示します。"""
    # 実装...
    return "タスク完了"
```

## 5. 主なコード構造

### 5.1 メインモジュール

```python
from openai_agents import Agent, Runner
from tools import file_tools, command_tools, interaction_tools
from logging import logger
from config import settings

def main():
    # 環境設定のロード
    api_key = settings.get_api_key()
    
    # ツールの初期化
    tools = [
        file_tools.list_file,
        file_tools.read_file,
        file_tools.write_file,
        command_tools.execute_command,
        interaction_tools.ask_question,
        interaction_tools.complete
    ]
    
    # エージェントの初期化
    agent = Agent(
        model="gpt-4",
        tools=tools,
        options={
            "temperature": 0.2,
            "max_tokens": 2000
        }
    )
    
    # ランナーの初期化
    runner = Runner(agent=agent)
    
    # ユーザーからのタスク入力
    user_task = input("コーディングエージェントにタスクを入力してください: ")
    
    # タスク実行（ストリーミングモード）
    for event in runner.stream(user_task):
        if event.type == "message":
            print(event.content)
        elif event.type == "tool_call":
            print(f"ツール '{event.name}' を実行中...")
        elif event.type == "tool_result":
            print(f"結果: {event.content}")
    
    # 完了メッセージ
    print("タスクが完了しました。")

if __name__ == "__main__":
    main()
```

## 6. ログとトレース

### 6.1 ログ設定

```python
import datetime
from pathlib import Path
from openai_agents.tracing import enable_tracing

def setup_logging():
    # ログディレクトリの作成
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # トレース機能の有効化
    enable_tracing(
        directory=str(log_dir),
        file_prefix=f"agent_trace_{datetime.datetime.now().strftime('%Y%m%d')}"
    )
```

### 6.2 カスタムロガー

```python
def log_event(event_type, data):
    # ログファイルへの書き込み
    log_file = get_log_file()
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "timestamp": datetime.datetime.now().isoformat(),
            "event_type": event_type,
            "data": data
        }, ensure_ascii=False) + "\n")
```

## 7. 特記事項

- **モデル互換性**: 将来的に異なるモデル（Claude、Geminiなど）への切り替えが容易になるよう設計
- **エラーハンドリング**: 各層で適切なエラーハンドリングを実装
- **ストリーミング**: リアルタイムのフィードバックを提供するためにストリーミングモードを優先
- **ガードレール**: エージェントの安全性を確保するためのガードレール機能を活用
- **環境設定**: 柔軟な設定変更が可能となるよう環境変数を活用 