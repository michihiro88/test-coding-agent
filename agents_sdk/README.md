# AI Coding Agent (OpenAI Agents SDK版)

このプロジェクトは、OpenAI Agents SDKを使用して実装されたAI Coding Agentです。ユーザーからのタスクを受け取り、適切なツールを使用してタスクを完了します。

## 機能

- ファイル操作（一覧表示、読み取り、書き込み）
- コマンド実行（安全性チェック機能付き）
- ユーザーとの対話
- タスクの完了管理
- トレース機能付きログ記録
- OS環境に応じた処理の最適化

## 必要な環境

- Python 3.8以上
- OpenAI APIキー
- OpenAI Agents SDK（0.1.0以上）
- PowerShell（Windows環境）

## セットアップ

1. 必要なパッケージをインストールします：
```powershell
pip install -r requirements.txt
```

2. `.env`ファイルを作成し、OpenAI APIキーを設定します（`.env.sample`をコピーして使用できます）：
```
OPENAI_API_KEY=your-api-key-here
```

## 使用方法

1. プログラムを実行します：
```powershell
python main.py
```

2. タスクを入力します。例：
```
電卓アプリを作成してください。
```

3. エージェントがタスクを実行し、必要に応じて質問をします。

4. タスクが完了すると、結果が表示されます。

## プロジェクト構造

```
agents_sdk/
├── main.py                # メインエントリポイント
├── tools/                 # ツール定義
│   ├── __init__.py        # パッケージ初期化ファイル
│   ├── file_tools.py      # ファイル操作関連ツール
│   ├── command_tools.py   # コマンド実行関連ツール
│   └── interaction_tools.py # ユーザー対話関連ツール
├── log_manager/           # ロギング機能
│   ├── __init__.py        # パッケージ初期化ファイル
│   └── logger.py          # ログ記録モジュール
├── config/                # 設定ファイル
│   ├── __init__.py        # パッケージ初期化ファイル
│   ├── settings.py        # 環境設定管理
│   └── forbidden_commands.json # 禁止コマンドリスト
├── utils/                 # ユーティリティ
│   ├── __init__.py        # パッケージ初期化ファイル
│   └── helpers.py         # ヘルパー関数
├── .env.sample            # 環境変数サンプル
├── system_prompt.txt      # システムプロンプト定義
├── requirements.txt       # 依存パッケージ
└── README.md              # ドキュメント
```

## ログとトレース

- ログは`logs`ディレクトリに保存されます
- ログファイルは日付ごとに作成されます（`agent_log_YYYYMMDD.jsonl`）
- OpenAI Agents SDKのトレース機能が有効な場合、詳細なトレース情報も記録されます

## セキュリティ機能

### コマンド実行の安全性チェック

- コマンド実行前に安全性チェックを実施
- 外部設定ファイル（`config/forbidden_commands.json`）から禁止コマンドリストを読み込み
- OS環境（WindowsまたはLinux）に応じた禁止コマンドを適用
- コマンド実行時は、必要に応じてユーザーの承認が必要

### 禁止コマンドリストのカスタマイズ

`config/forbidden_commands.json`を編集することで、禁止コマンドリストをカスタマイズできます：

```json
{
  "common": ["危険なコマンド1", "危険なコマンド2"],
  "windows": ["Windowsの危険なコマンド"],
  "linux": ["Linuxの危険なコマンド"]
}
```

## カスタマイズ

### モデルの変更

`.env`ファイルの`MODEL_NAME`を変更することで、使用するモデルを変更できます：
```
MODEL_NAME=gpt-4
```

### トレース機能の無効化

トレース機能を無効にする場合は、`.env`ファイルで設定を変更します：
```
ENABLE_TRACING=false
```

### システムプロンプトの変更

`system_prompt.txt`を編集することで、エージェントの指示を変更できます。

## OpenAI Agents SDKの利用

このプロジェクトは[OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)を使用しています。主な使用方法は以下の通りです：

- `@function_tool`デコレータによるツール関数の定義
- `Agent`クラスによるエージェントの作成
- `Runner.run`によるエージェントの実行

## 注意事項

- コマンド実行は安全性チェックを実施しますが、完全な保証はできません
- ファイル操作は、適切な権限が必要です
- APIキーは安全に管理してください 