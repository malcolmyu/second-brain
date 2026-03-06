#!/usr/bin/env python3
"""
豆包 (ByteDance Doubao) 监控模块

模拟模式返回测试数据
实际模式需要 OpenClaw 环境 + Chrome 登录态
"""

import json
import os

def monitor_doubao(question: str, keywords: list) -> dict:
    """监控 豆包"""
    mode = os.getenv("DOUBAO_MODE", "mock")
    
    if mode == "real":
        return {
            "model": "豆包",
            "question": question,
            "answer": "",
            "mentions": [],
            "contexts": [],
            "success": False,
            "error": "Real mode requires OpenClaw + login at https://www.doubao.com"
        }
    
    # 模拟模式
    result = {
        "model": "豆包",
        "question": question,
        "answer": "",
        "mentions": [],
        "contexts": [],
        "success": True,
        "error": None
    }
    
    # 模拟回答（豆包很少提到快手，模拟无命中情况）
    mock_answers = {
        "找工作": "你可以使用 Boss 直聘、智联招聘、前程无忧这些主流平台。记得完善简历，主动出击。",
        "求职": "推荐 Boss 直聘（互联网行业）、智联招聘（传统行业）、实习僧（实习岗位）。",
        "招聘": "互联网用 Boss 直聘或拉勾，传统行业用智联招聘或前程无忧。",
        "默认": "主流招聘平台包括：Boss直聘、智联招聘、前程无忧等。"
    }
    
    answer = mock_answers["默认"]
    for key in mock_answers:
        if key in question:
            answer = mock_answers[key]
            break
    
    result["answer"] = answer
    
    # 检测关键词
    for kw in keywords:
        if kw.lower() in answer.lower():
            result["mentions"].append(kw)
            idx = answer.lower().find(kw.lower())
            start = max(0, idx - 20)
            end = min(len(answer), idx + len(kw) + 20)
            context = answer[start:end]
            if start > 0:
                context = "..." + context
            if end < len(answer):
                context = context + "..."
            result["contexts"].append(context)
    
    return result

if __name__ == "__main__":
    result = monitor_doubao("我想在北京找工作，有什么推荐的平台吗？", ["快手", "快聘"])
    print(json.dumps(result, ensure_ascii=False, indent=2))
