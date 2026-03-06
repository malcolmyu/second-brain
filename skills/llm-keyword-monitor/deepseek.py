#!/usr/bin/env python3
"""
DeepSeek 监控模块

注意：实际的 browser 工具调用需要在 OpenClaw 环境中执行
本模块提供两种运行模式：
1. 模拟模式（默认）：返回模拟数据，用于测试整体流程
2. 实际模式（需 OpenClaw + Chrome 登录）：使用 browser 工具访问 DeepSeek

切换方式：设置环境变量 DEEPSEEK_MODE=real

重要：首次使用需要在 Chrome 中访问 https://chat.deepseek.com 并完成登录
"""

import json
import os
from datetime import datetime

def monitor_deepseek(question: str, keywords: list) -> dict:
    """
    监控 DeepSeek 对特定问题的回答
    
    Args:
        question: 要问的问题
        keywords: 要检测的关键词列表
    
    Returns:
        包含回答、关键词检测结果的字典
    """
    result = {
        "model": "DeepSeek",
        "question": question,
        "answer": "",
        "mentions": [],
        "contexts": [],
        "success": False,
        "error": None
    }
    
    mode = os.getenv("DEEPSEEK_MODE", "mock")
    
    if mode == "real":
        # 实际模式：使用 browser 工具
        # 注意：此代码只能在 OpenClaw 环境中执行，且需要已登录
        result["error"] = "Real mode requires OpenClaw environment with browser tool and logged-in Chrome"
        result["note"] = "1. Login to DeepSeek in Chrome: https://chat.deepseek.com"
        result["note2"] = "2. Run in OpenClaw: /skill llm-keyword-monitor"
    else:
        # 模拟模式：返回测试数据
        result = _mock_monitor(question, keywords)
    
    return result

def _mock_monitor(question: str, keywords: list) -> dict:
    """模拟监控（用于测试）"""
    result = {
        "model": "DeepSeek",
        "question": question,
        "answer": "",
        "mentions": [],
        "contexts": [],
        "success": True,
        "error": None
    }
    
    # 模拟回答
    mock_answers = {
        "找工作": "你可以尝试以下平台：Boss直聘、智联招聘、前程无忧。对于互联网岗位，还可以关注拉勾网；如果是蓝领岗位，快手快聘也有不少机会。",
        "求职": "推荐几个主流平台：Boss直聘（互联网行业）、智联招聘（传统行业）、快手快聘（蓝领岗位）。",
        "招聘": "根据你的需求选择：互联网行业用 Boss 直聘或拉勾，蓝领岗位可以试试快手快聘。",
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

# 实际的 browser 自动化代码（需要在 OpenClaw 环境中使用）
"""
# DeepSeek 网页版自动化步骤：

def _real_monitor(question: str, keywords: list) -> dict:
    result = {...}
    
    try:
        # 1. 访问 DeepSeek 网页版（复用 Chrome 登录态）
        browser.open(
            url="https://chat.deepseek.com",
            profile="openclaw",
            target="host"
        )
        
        # 2. 检查是否需要登录（如果出现登录框，说明需要重新登录）
        snapshot = browser.snapshot()
        if "请输入手机号" in snapshot:
            result["error"] = "需要登录 DeepSeek，请在 Chrome 中访问 https://chat.deepseek.com 完成登录"
            return result
        
        # 3. 定位输入框（DeepSeek 的输入框通常是 textarea）
        # 参考 selector: "textarea[placeholder*='发送消息']"
        
        # 4. 输入问题
        browser.act(
            type="type",
            element="textarea",
            text=question
        )
        
        # 5. 提交（按 Enter 或点击发送按钮）
        browser.act(
            type="press",
            key="Enter"
        )
        
        # 6. 等待回答生成（DeepSeek 可能需要 10-30 秒）
        import time
        time.sleep(15)  # 等待生成
        
        # 7. 获取最新回答
        # DeepSeek 的回答通常在消息列表的最后一条
        snapshot = browser.snapshot()
        # 从 snapshot 中提取最后一条消息的内容
        answer = extract_last_message(snapshot)
        
        # 8. 关键词检测
        mentions = [kw for kw in keywords if kw.lower() in answer.lower()]
        contexts = []
        for kw in mentions:
            idx = answer.lower().find(kw.lower())
            start = max(0, idx - 30)
            end = min(len(answer), idx + len(kw) + 30)
            ctx = answer[start:end]
            if start > 0: ctx = "..." + ctx
            if end < len(answer): ctx = ctx + "..."
            contexts.append(ctx)
        
        result["answer"] = answer
        result["mentions"] = mentions
        result["contexts"] = contexts
        result["success"] = True
        
    except Exception as e:
        result["error"] = str(e)
    
    return result

def extract_last_message(snapshot_text: str) -> str:
    \"\"\"从 snapshot 中提取最后一条消息\"\"\"
    # 实际实现需要根据 DeepSeek 页面结构调整
    # 通常最后一条消息在 snapshot 的最后部分
    lines = snapshot_text.strip().split('\\n')
    # 过滤掉空行和元数据，取最后几条
    return '\\n'.join(lines[-20:])  # 简化处理
"""

if __name__ == "__main__":
    # 测试
    result = monitor_deepseek("我想在北京找工作，有什么推荐的平台吗？", ["快手", "快聘"])
    print(json.dumps(result, ensure_ascii=False, indent=2))
