#!/usr/bin/env python3
"""
Star Office 集成模块
在日报生成过程中自动更新像素办公室状态
"""

import json
import os
import sys
from datetime import datetime

# Star Office 路径
STAR_OFFICE_DIR = os.path.expanduser("~/.openclaw/workspace/star-office")
STATE_FILE = os.path.join(STAR_OFFICE_DIR, "state.json")
MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory")

# 确保目录存在
os.makedirs(MEMORY_DIR, exist_ok=True)

VALID_STATES = [
    "idle",
    "writing", 
    "receiving",
    "replying",
    "researching",
    "executing",
    "syncing",
    "error"
]

def update_state(state_name, detail=""):
    """更新 Star Office 状态"""
    if state_name not in VALID_STATES:
        print(f"[Star Office] 无效状态: {state_name}")
        return False
    
    try:
        # 读取当前状态
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
        else:
            # 从 sample 复制
            sample_file = os.path.join(STAR_OFFICE_DIR, "state.sample.json")
            if os.path.exists(sample_file):
                with open(sample_file, "r", encoding="utf-8") as f:
                    state = json.load(f)
            else:
                state = {
                    "state": "idle",
                    "detail": "待命中...",
                    "progress": 0,
                    "updated_at": datetime.now().isoformat()
                }
        
        # 更新状态
        state["state"] = state_name
        state["detail"] = detail
        state["updated_at"] = datetime.now().isoformat()
        
        # 保存
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        
        print(f"[Star Office] 状态更新: {state_name} - {detail}")
        return True
        
    except Exception as e:
        print(f"[Star Office] 状态更新失败: {e}")
        return False

def save_daily_note(content, date=None):
    """
    保存日报为"昨日小记"
    Star Office 会自动从 memory/*.md 读取
    """
    if date is None:
        date = datetime.now()
    
    # 保存为今天的日报（作为明天的"昨日小记"）
    filename = date.strftime('%Y-%m-%d') + "_daily.md"
    filepath = os.path.join(MEMORY_DIR, filename)
    
    # 添加标题
    note_content = f"""# {date.strftime('%Y年%m月%d日')} AI 日报

{content}

---
生成时间: {datetime.now().strftime('%H:%M')}
"""
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(note_content)
        print(f"[Star Office] 日报已保存: {filepath}")
        return True
    except Exception as e:
        print(f"[Star Office] 日报保存失败: {e}")
        return False

def get_summary_for_note(articles_count, highlights):
    """生成昨日小记的摘要"""
    today = datetime.now()
    summary = f"""今日共收录 {articles_count} 篇 AI 资讯。

重点内容：
"""
    for i, h in enumerate(highlights[:5], 1):
        summary += f"{i}. {h['title']} ({h['source']})\n"
    
    summary += f"\n详情查看: {today.strftime('%Y%m%d')}_v1.md"
    return summary

# 快捷函数
def start_researching():
    """开始研究 - 抓取 RSS"""
    return update_state("researching", "正在抓取 RSS 源...")

def start_executing():
    """开始执行 - 处理数据"""
    return update_state("executing", "正在生成日报...")

def start_syncing():
    """开始同步 - 保存文件"""
    return update_state("syncing", "正在保存日报...")

def set_idle(message="待命中，准备生成日报"):
    """空闲状态"""
    return update_state("idle", message)

def set_error(message):
    """错误状态"""
    return update_state("error", message)

def set_writing(message):
    """写作状态"""
    return update_state("writing", message)

if __name__ == "__main__":
    # 测试
    if len(sys.argv) >= 2:
        state = sys.argv[1]
        detail = sys.argv[2] if len(sys.argv) > 2 else ""
        update_state(state, detail)
    else:
        print("用法: python star_office_integration.py <state> [detail]")
        print(f"状态选项: {', '.join(VALID_STATES)}")
