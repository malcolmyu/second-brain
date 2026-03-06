#!/usr/bin/env python3
"""
通义千问 (Alibaba Tongyi) 监控模块

模拟模式返回测试数据
实际模式需要 OpenClaw 环境 + Chrome 登录态
"""

import json
import os

def monitor_tongyi(question: str, keywords: list) -> dict:
    """监控 通义千问"""
    mode = os.getenv("TONGYI_MODE", "mock")
    
    if mode == "real":
        return {
            "model": "通义千问",
            "question": question,
            "answer": "",
            "mentions": [],
            "contexts": [],
            "success": False,
            "error": "Real mode requires OpenClaw + login at https://tongyi.aliyun.com"
        }
    
    # 模拟模式
    result = {
        "model": "通义千问",
        "question": question,
        "answer": "",
        "mentions": [],
        "contexts": [],
        "success": True,
        "error": None
    }
    
    # 模拟回答
    mock_answers = {
        "找工作": "推荐以下平台：Boss直聘（互联网）、智联招聘（综合）、快手快聘（蓝领）。建议多渠道投递。",
        "求职": "主流平台包括：Boss直聘、智联招聘、前程无忧。蓝领岗位可以关注快手快聘。",
        "招聘": "根据岗位类型选择合适平台。互联网行业推荐 Boss 直聘，蓝领推荐快手快聘。",
        "默认": "主流招聘平台有 Boss 直聘、智联招聘、前程无忧等。"
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
    result = monitor_tongyi("我想在北京找工作，有什么推荐的平台吗？", ["快手", "快聘"])
    print(json.dumps(result, ensure_ascii=False, indent=2))
