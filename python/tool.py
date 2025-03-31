#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import glob
from dataclasses import dataclass
from typing import List, Optional

# データクラスの定義
@dataclass
class ListFileParams:
    path: str
    recursive: str

@dataclass
class ReadFileParams:
    path: str

@dataclass
class WriteFileParams:
    path: str
    content: str

@dataclass
class AskQuestionParams:
    question: str

@dataclass
class ExecuteCommandParams:
    command: str
    requires_approval: str

@dataclass
class CompleteParams:
    result: str

@dataclass
class ToolResponse:
    success: bool
    message: str

# 1. ListFile - ディレクトリ内のファイル一覧を取得
def list_file(params: ListFileParams) -> ToolResponse:
    path = params.path
    recursive = params.recursive.lower() == "true"
    
    try:
        files = []
        if recursive:
            for file_path in glob.glob(os.path.join(path, "**"), recursive=True):
                files.append(file_path)
        else:
            for file_path in glob.glob(os.path.join(path, "*")):
                files.append(file_path)
        
        result = f"ディレクトリ {path} のファイル一覧:\n"
        for file in files:
            result += f"- {file}\n"
        
        return ToolResponse(
            success=True,
            message=result
        )
    except Exception as e:
        return ToolResponse(
            success=False,
            message=f"ディレクトリの読み取りに失敗しました: {str(e)}"
        )

# 2. ReadFile - ファイルの内容を読み取る
def read_file(params: ReadFileParams) -> ToolResponse:
    try:
        with open(params.path, "r", encoding="utf-8") as f:
            content = f.read()
        
        return ToolResponse(
            success=True,
            message=content
        )
    except Exception as e:
        return ToolResponse(
            success=False,
            message=f"ファイルの読み取りに失敗しました: {str(e)}"
        )

# 3. WriteFile - ファイルに内容を書き込む
def write_file(params: WriteFileParams) -> ToolResponse:
    try:
        # ディレクトリが存在しない場合は作成
        os.makedirs(os.path.dirname(params.path), exist_ok=True)
        
        with open(params.path, "w", encoding="utf-8") as f:
            f.write(params.content)
        
        return ToolResponse(
            success=True,
            message=f"ファイル {params.path} に書き込みました"
        )
    except Exception as e:
        return ToolResponse(
            success=False,
            message=f"ファイルの書き込みに失敗しました: {str(e)}"
        )

# 4. AskQuestion - ユーザーに質問する
def ask_question(params: AskQuestionParams) -> ToolResponse:
    print(f"\n質問: {params.question}")
    print("回答: ", end="")
    
    answer = input()
    
    return ToolResponse(
        success=True,
        message=f"ユーザーの回答: {answer}"
    )

# 5. ExecuteCommand - コマンドを実行する
def execute_command(params: ExecuteCommandParams) -> ToolResponse:
    requires_approval = params.requires_approval.lower() == "true"
    
    if requires_approval:
        print(f"\n以下のコマンドを実行しますか？\n{params.command}")
        print("[y/n]: ", end="")
        
        answer = input()
        
        if answer.lower() != "y":
            return ToolResponse(
                success=False,
                message="コマンドの実行がキャンセルされました"
            )
    
    try:
        # PowerShell上でコマンドを実行
        process = subprocess.Popen(
            ["powershell.exe", "-Command", params.command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            return ToolResponse(
                success=False,
                message=f"コマンドの実行に失敗しました: 終了コード {process.returncode}\n出力: {stdout}\nエラー: {stderr}"
            )
        
        return ToolResponse(
            success=True,
            message=f"コマンドの実行結果:\n{stdout}"
        )
    except Exception as e:
        return ToolResponse(
            success=False,
            message=f"コマンドの実行中にエラーが発生しました: {str(e)}"
        )

# 6. Complete - タスクの完了を示す
def complete(params: CompleteParams) -> ToolResponse:
    return ToolResponse(
        success=True,
        message=f"タスク完了: {params.result}"
    ) 