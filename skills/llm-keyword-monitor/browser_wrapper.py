#!/usr/bin/env python3
"""
OpenClaw Browser 工具包装器

这个模块定义了如何使用 browser 工具与各个 LLM 网页版交互
实际执行时需要 OpenClaw 环境
"""

# 各模型网页版配置
MODEL_CONFIGS = {
    "yuanbao": {
        "name": "元宝",
        "url": "https://yuanbao.tencent.com",
        "input_selector": "textarea[placeholder*='输入']",
        "submit_selector": "button[type='submit']",
        "answer_selector": ".message-content",
    },
    "deepseek": {
        "name": "DeepSeek",
        "url": "https://chat.deepseek.com",
        "input_selector": "textarea",
        "submit_selector": "button[type='submit']",
        "answer_selector": ".message-content",
    },
    "kimi": {
        "name": "Kimi",
        "url": "https://kimi.moonshot.cn",
        "input_selector": "textarea",
        "submit_selector": "button[type='submit']",
        "answer_selector": ".message-content",
    },
    "doubao": {
        "name": "豆包",
        "url": "https://www.doubao.com",
        "input_selector": "textarea",
        "submit_selector": "button[type='submit']",
        "answer_selector": ".message-content",
    },
    "tongyi": {
        "name": "通义千问",
        "url": "https://tongyi.aliyun.com",
        "input_selector": "textarea",
        "submit_selector": "button[type='submit']",
        "answer_selector": ".message-content",
    }
}

def get_model_config(model_id: str) -> dict:
    """获取模型配置"""
    return MODEL_CONFIGS.get(model_id, {})
