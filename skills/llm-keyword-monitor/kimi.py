#!/usr/bin/env python3
"""
Kimi (Moonshot) 监控模块

模拟模式返回测试数据
实际模式需要 OpenClaw 环境 + Chrome 登录态
"""

import json
import os

def monitor_kimi(question: str, keywords: list) -> dict:
    """监控 Kimi"""
    mode = os.getenv("KIMI_MODE", "mock")
    
    if mode == "real":
        return {
            "model": "Kimi",
            "question": question,
            "answer": "",
            "mentions": [],
            "contexts": [],
            "success": False,
            "error": "Real mode requires OpenClaw + login at https://kimi.moonshot.cn"
        }
    
    # 模拟模式
    result = {
        "model": "Kimi",
        "question": question,
        "answer": "",
        "mentions": [],
        "contexts": [],
        "success": True,
        "error": None
    }
    
    # 模拟回答
    mock_answers = {
        "找工作": "推荐几个求职平台：Boss直聘适合互联网，智联招聘覆盖面广，快手快聘在蓝领招聘方面做得不错。",
        "求职": "可以试试这些：校招用牛客网、实习僧；社招用 Boss 直聘；蓝领岗位推荐快手快聘。",
        "招聘": "根据岗位类型选择：互联网用 Boss 直聘或拉勾，传统行业用智联，蓝领用快手快聘。",
        "默认": "主流平台有 Boss 直聘、智联招聘、前程无忧等。"
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
    result = monitor_kimi("我想在北京找工作，有什么推荐的平台吗？", ["快手", "快聘"])
    print(json.dumps(result, ensure_ascii=False, indent=2))
