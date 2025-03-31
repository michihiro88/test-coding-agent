#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import xml.etree.ElementTree as ET
from typing import Tuple, Dict, Any
from tool import (
    list_file, read_file, write_file, ask_question, 
    execute_command, complete, ToolResponse,
    ListFileParams, ReadFileParams, WriteFileParams,
    AskQuestionParams, ExecuteCommandParams, CompleteParams
)

# ツールの種類を表す定数
TOOL_TYPE_LIST_FILE = "list_file"
TOOL_TYPE_READ_FILE = "read_file"
TOOL_TYPE_WRITE_FILE = "write_file"
TOOL_TYPE_ASK_QUESTION = "ask_question"
TOOL_TYPE_EXECUTE_COMMAND = "execute_command"
TOOL_TYPE_COMPLETE = "complete"

def parse_and_execute_tool(response: str) -> Tuple[ToolResponse, str, bool]:
    """
    LLMのレスポンスをパースしてツールを実行する
    
    Args:
        response: LLMからのレスポンス文字列
        
    Returns:
        Tuple[ToolResponse, str, bool]: ツールの実行結果、ツールの種類、完了フラグ
    """
    # XMLタグを抽出する正規表現
    pattern = r'<([a-z_]+)>([\s\S]*?)</\1>'
    match = re.search(pattern, response)
    
    if not match:
        return ToolResponse(
            success=False,
            message="有効なツールが見つかりませんでした"
        ), "", False
    
    tool_type = match.group(1)
    tool_content = match.group(2)
    
    # XMLのパースを補助する関数
    def parse_xml(content: str, tool_type: str) -> Dict[str, Any]:
        try:
            root = ET.fromstring(f"<{tool_type}>{content}</{tool_type}>")
            result = {}
            for child in root:
                result[child.tag] = child.text.strip() if child.text else ""
            return result
        except Exception as e:
            return {}
    
    if tool_type == TOOL_TYPE_LIST_FILE:
        params_dict = parse_xml(tool_content, tool_type)
        params = ListFileParams(
            path=params_dict.get("path", ""),
            recursive=params_dict.get("recursive", "false")
        )
        return list_file(params), tool_type, False
    
    elif tool_type == TOOL_TYPE_READ_FILE:
        params_dict = parse_xml(tool_content, tool_type)
        params = ReadFileParams(
            path=params_dict.get("path", "")
        )
        return read_file(params), tool_type, False
    
    elif tool_type == TOOL_TYPE_WRITE_FILE:
        params_dict = parse_xml(tool_content, tool_type)
        params = WriteFileParams(
            path=params_dict.get("path", ""),
            content=params_dict.get("content", "")
        )
        return write_file(params), tool_type, False
    
    elif tool_type == TOOL_TYPE_ASK_QUESTION:
        params_dict = parse_xml(tool_content, tool_type)
        params = AskQuestionParams(
            question=params_dict.get("question", "")
        )
        return ask_question(params), tool_type, False
    
    elif tool_type == TOOL_TYPE_EXECUTE_COMMAND:
        params_dict = parse_xml(tool_content, tool_type)
        params = ExecuteCommandParams(
            command=params_dict.get("command", ""),
            requires_approval=params_dict.get("requires_approval", "true")
        )
        return execute_command(params), tool_type, False
    
    elif tool_type == TOOL_TYPE_COMPLETE:
        params_dict = parse_xml(tool_content, tool_type)
        params = CompleteParams(
            result=params_dict.get("result", "")
        )
        return complete(params), tool_type, True
    
    else:
        return ToolResponse(
            success=False,
            message=f"未知のツールタイプ: {tool_type}"
        ), tool_type, False 