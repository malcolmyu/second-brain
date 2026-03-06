#!/usr/bin/env python3
"""
配置加载模块
"""

import os
from pathlib import Path

def load_questions() -> list:
    """从 questions.txt 加载问题列表"""
    config_path = Path(__file__).parent / "config" / "questions.txt"
    with open(config_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def load_keywords() -> list:
    """从 keywords.txt 加载关键词列表"""
    config_path = Path(__file__).parent / "config" / "keywords.txt"
    with open(config_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

if __name__ == "__main__":
    print("Questions:", load_questions())
    print("Keywords:", load_keywords())
