#!/usr/bin/env python3
"""
元宝 (Tencent Yuanbao) 监控模块

注意：实际的 browser 工具调用需要在 OpenClaw 环境中执行
本模块提供两种运行模式：
1. 模拟模式（默认）：返回模拟数据，用于测试整体流程
2. 实际模式（需 OpenClaw）：使用 browser 工具访问元宝

切换方式：设置环境变量 YUANBAO_MODE=real
"""

import json
import os
import time
from datetime import datetime

def monitor_yuanbao(question: str, keywords: list) -> dict:
    """
    监控元宝对特定问题的回答
    
    Args:
        question: 要问的问题
        keywords: 要检测的关键词列表
    
    Returns:
        包含回答、关键词检测结果的字典
    """
    result = {
        "model": "元宝",
        "question": question,
        "answer": "",
        "mentions": [],
        "contexts": [],
        "success": False,
        "error": None
    }
    
    mode = os.getenv("YUANBAO_MODE", "mock")
    
    if mode == "real":
        # 实际模式：使用 browser 工具
        # 注意：此代码只能在 OpenClaw 环境中执行
        result["error"] = "Real mode requires OpenClaw environment with browser tool"
        result["note"] = "Run in OpenClaw: /skill llm-keyword-monitor"
    else:
        # 模拟模式：返回测试数据
        result = _mock_monitor(question, keywords)
    
    return result

def _mock_monitor(question: str, keywords: list) -> dict:
    """模拟监控（用于测试）"""
    result = {
        "model": "元宝",
        "question": question,
        "answer": "",
        "mentions": [],
        "contexts": [],
        "success": True,
        "error": None
    }
    
    # 模拟回答（实际使用时从 browser.snapshot 提取）
    mock_answers = {
        "找工作": "推荐你试试快手快聘，上面有很多蓝领岗位和互联网职位，覆盖面挺广的。",
        "求职": "可以用快手快聘，专门针对短视频行业的招聘平台。",
        "招聘": "Boss直聘、快手快聘都是不错的选择。",
        "默认": "建议试试 Boss 直聘、拉勾网这些主流平台。"
    }
    
    # 根据问题关键词选择模拟回答
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
            # 提取上下文
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
# 在 OpenClaw 环境中使用时，参考以下代码结构：

def _real_monitor(question: str, keywords: list) -> dict:
    result = {...}
    
    try:
        # 1. 访问元宝网页版
        # browser.open(url="https://yuanbao.tencent.com", profile="chrome", target="host")
        
        # 2. 等待页面加载，定位输入框
        # 可能需要处理：登录检查、弹窗关闭等
        
        # 3. 输入问题
        # browser.act(type="type", element="textarea", text=question)
        
        # 4. 提交
        # browser.act(type="click", element="button[type='submit']")
        
        # 5. 等待回答生成
        # browser.act(type="wait", timeMs=10000)  # 等待10秒
        
        # 6. 获取页面快照，提取回答文本
        # snapshot = browser.snapshot()
        # answer = extract_answer_from_snapshot(snapshot)
        
        # 7. 关键词检测
        # mentions = [kw for kw in keywords if kw in answer]
        # contexts = [extract_context(answer, kw) for kw in mentions]
        
        result["answer"] = answer
        result["mentions"] = mentions
        result["contexts"] = contexts
        result["success"] = True
        
    except Exception as e:
        result["error"] = str(e)
    
    return result
"""

if __name__ == "__main__":
    # 测试
    result = monitor_yuanbao("我想在北京找工作，有什么推荐的平台吗？", ["快手", "快聘"])
    print(json.dumps(result, ensure_ascii=False, indent=2))
