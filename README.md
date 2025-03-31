# AI Coding Agent (OpenAI Agents SDK版)

このプロジェクトは、[Zennの記事](https://zenn.dev/minedia/articles/11822c2b509a79)をベースに、OpenAI Agents SDKを使用して実装されたAI Coding Agentです。ユーザーからのタスクを受け取り、適切なツールを使用してタスクを完了します。

## プロジェクトの背景

このプロジェクトは以下の3つのバージョンで構成されています：

1. **Go版（`go`フォルダ）**
   - [Zennの記事](https://zenn.dev/minedia/articles/11822c2b509a79)のソースコードをベースにしています
   - 記事のライセンスは記事作者に帰属します
   - このプロジェクトでの使用は、記事の内容を参考にした実装例として提供されています
   - XMLベースのツール定義を使用
   - 基本的なファイル操作とコマンド実行機能を提供

2. **Python版（`python`フォルダ）**
   - Go版のコードをPythonに移植したバージョンです
   - XMLベースのツール定義を使用
   - 基本的な機能：
     - ファイル操作（一覧表示、読み取り、書き込み）
     - コマンド実行
     - ユーザーとの対話
     - タスクの完了管理
   - 追加機能：
     - ログ機能（`logs`ディレクトリに保存）
     - 出力管理（`output`ディレクトリに保存）

3. **Agents SDK版（`agents_sdk`フォルダ）**
   - OpenAI Agents SDKを使用した拡張バージョンです
   - プログラムが生成したサンプルアプリケーション：
     - 電卓アプリケーション（`calculator.py`）：AIが生成した電卓プログラムのサンプル
     - カレンダーアプリケーション（`calendar_app.py`）：AIが生成したカレンダープログラムのサンプル
   - デバッグ機能（`debug.py`）
   - 拡張されたツールセットとログ管理機能

## プロジェクト構造

```
.
├── .cursor/              # Cursor IDEの設定ファイル
├── go/                   # Go版のソースコード
│   └── ...              # Go版のファイル構成
├── python/              # Python版のソースコード
│   ├── main.py          # メインエントリポイント
│   ├── tool.py          # ツール定義
│   ├── parser.py        # XMLパーサー
│   ├── requirements.txt # 依存パッケージ
│   ├── logs/           # ログファイル保存ディレクトリ
│   ├── output/         # 出力ファイル保存ディレクトリ
│   └── README.md       # Python版のドキュメント
├── agents_sdk/          # Agents SDK版のソースコード
│   ├── main.py          # メインエントリポイント
│   ├── debug.py         # デバッグ用スクリプト
│   ├── calculator.py    # 電卓アプリケーション
│   ├── calendar_app.py  # カレンダーアプリケーション
│   ├── requirements.txt # 依存パッケージ
│   ├── system_prompt.txt # システムプロンプト定義
│   ├── tools/          # ツール定義
│   ├── log_manager/    # ログ管理
│   ├── config/         # 設定ファイル
│   ├── utils/          # ユーティリティ
│   ├── doc/            # ドキュメント
│   └── logs/           # ログファイル
└── README.md            # このファイル
```

## 必要な環境

- Python 3.8以上
- OpenAI APIキー
- PowerShell（Windows環境）

## セットアップ

1. 必要なパッケージをインストールします：
```powershell
pip install -r requirements.txt
```

2. `.env`ファイルを作成し、OpenAI APIキーを設定します：
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

## ログと出力

- ログは`logs`ディレクトリに保存されます
- 生成されたファイルは`output`ディレクトリに保存されます

## 注意事項

- コマンド実行時は、必要に応じてユーザーの承認が必要です
- ファイル操作は、適切な権限が必要です
- APIキーは安全に管理してください 