# LLM 关键词监控 Skill Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 创建一个 OpenClaw Skill，定时监控国内大模型回答中是否提到快手关键词

**Architecture:** 使用 browser 工具访问各模型网页版，复用 Chrome 登录态，捕获回答并分析，生成对比报告

**Tech Stack:** OpenClaw Skill system, browser tool, Python (for config parsing), Markdown

---

## Task 1: Create Skill Directory Structure

**Files:**
- Create: `~/.openclaw/skills/llm-keyword-monitor/SKILL.md`
- Create: `~/.openclaw/skills/llm-keyword-monitor/config/questions.txt`
- Create: `~/.openclaw/skills/llm-keyword-monitor/config/keywords.txt`
- Create: `~/.openclaw/skills/llm-keyword-monitor/reports/.gitkeep`

**Step 1: Create directory structure**

```bash
mkdir -p ~/.openclaw/skills/llm-keyword-monitor/config
mkdir -p ~/.openclaw/skills/llm-keyword-monitor/reports
touch ~/.openclaw/skills/llm-keyword-monitor/reports/.gitkeep
```

**Step 2: Create default questions.txt**

```
我想在北京找工作，有什么推荐的平台吗？
应届毕业生求职用什么APP比较好？
互联网行业的招聘信息去哪里找？
蓝领工人怎么找工作？
```

**Step 3: Create default keywords.txt**

```
快手
快聘
Kuaishou
```

**Step 4: Commit**

```bash
git add ~/.openclaw/skills/llm-keyword-monitor/
git commit -m "chore: create llm-keyword-monitor skill structure"
```

---

## Task 2: Create Main SKILL.md

**Files:**
- Create: `~/.openclaw/skills/llm-keyword-monitor/SKILL.md`

**Step 1: Write SKILL.md**

```markdown
---
name: llm-keyword-monitor
description: Monitor domestic LLMs for mentions of Kuaishou keywords in their responses
---

# LLM 关键词监控

监控国内主流大模型（元宝、DeepSeek、Kimi、豆包、通义千问）在回答特定问题时是否提到快手关键词。

## 首次使用准备

1. 在 Chrome 中打开以下网址并完成登录：
   - 元宝: https://yuanbao.tencent.com
   - DeepSeek: https://chat.deepseek.com
   - Kimi: https://kimi.moonshot.cn
   - 豆包: https://www.doubao.com
   - 通义千问: https://tongyi.aliyun.com

2. 确保 OpenClaw Browser Relay 扩展已连接

## 配置

编辑 `config/questions.txt` 添加监控问题（一行一个）
编辑 `config/keywords.txt` 添加监控关键词（一行一个）

## 运行

```bash
openclaw skill llm-keyword-monitor
```

## 输出

- Markdown 报告保存到 `reports/YYYY-MM-DD-HH-mm-ss-llm-monitor.md`
- Kim 消息通知
```

**Step 2: Commit**

```bash
git add ~/.openclaw/skills/llm-keyword-monitor/SKILL.md
git commit -m "docs: add skill documentation"
```

---

## Task 3: Implement Yuanbao (元宝) Monitor

**Files:**
- Create: `~/.openclaw/skills/llm-keyword-monitor/yuanbao.py`

**Step 1: Create yuanbao.py with browser automation**

```python
#!/usr/bin/env python3
"""
元宝 (Tencent Yuanbao) 监控模块
"""

import json
import time
from datetime import datetime

def monitor_yuanbao(question: str, keywords: list) -> dict:
    """
    使用 OpenClaw browser 工具访问元宝并获取回答
    
    Returns:
        {
            "model": "元宝",
            "question": question,
            "answer": "完整回答文本",
            "mentions": ["快手", "快聘"],  # 检测到的关键词
            "contexts": ["...上下文..."],  # 关键词上下文
            "success": True/False,
            "error": "错误信息（如有）"
        }
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
    
    try:
        # 这些将由 browser 工具执行
        # 1. 访问 https://yuanbao.tencent.com
        # 2. 等待输入框可用
        # 3. 输入问题
        # 4. 提交
        # 5. 等待回答完成
        # 6. 提取回答文本
        
        # 实际实现将在 executing-plans 中完成
        pass
        
    except Exception as e:
        result["error"] = str(e)
    
    return result

if __name__ == "__main__":
    # 测试
    result = monitor_yuanbao("我想找工作", ["快手", "快聘"])
    print(json.dumps(result, ensure_ascii=False, indent=2))
```

**Step 2: Commit**

```bash
git add ~/.openclaw/skills/llm-keyword-monitor/yuanbao.py
git commit -m "feat: add yuanbao monitor scaffold"
```

---

## Task 4: Implement DeepSeek Monitor

**Files:**
- Create: `~/.openclaw/skills/llm-keyword-monitor/deepseek.py`

**Step 1: Create deepseek.py**

```python
#!/usr/bin/env python3
"""
DeepSeek 监控模块
"""

import json
from datetime import datetime

def monitor_deepseek(question: str, keywords: list) -> dict:
    """监控 DeepSeek"""
    return {
        "model": "DeepSeek",
        "question": question,
        "answer": "",
        "mentions": [],
        "contexts": [],
        "success": False,
        "error": None
    }
```

**Step 2: Commit**

```bash
git add ~/.openclaw/skills/llm-keyword-monitor/deepseek.py
git commit -m "feat: add deepseek monitor scaffold"
```

---

## Task 5: Implement Kimi Monitor

**Files:**
- Create: `~/.openclaw/skills/llm-keyword-monitor/kimi.py`

**Step 1: Create kimi.py**

```python
#!/usr/bin/env python3
"""
Kimi (Moonshot) 监控模块
"""

import json

def monitor_kimi(question: str, keywords: list) -> dict:
    """监控 Kimi"""
    return {
        "model": "Kimi",
        "question": question,
        "answer": "",
        "mentions": [],
        "contexts": [],
        "success": False,
        "error": None
    }
```

**Step 2: Commit**

```bash
git add ~/.openclaw/skills/llm-keyword-monitor/kimi.py
git commit -m "feat: add kimi monitor scaffold"
```

---

## Task 6: Implement Doubao (豆包) Monitor

**Files:**
- Create: `~/.openclaw/skills/llm-keyword-monitor/doubao.py`

**Step 1: Create doubao.py**

```python
#!/usr/bin/env python3
"""
豆包 (ByteDance Doubao) 监控模块
"""

import json

def monitor_doubao(question: str, keywords: list) -> dict:
    """监控 豆包"""
    return {
        "model": "豆包",
        "question": question,
        "answer": "",
        "mentions": [],
        "contexts": [],
        "success": False,
        "error": None
    }
```

**Step 2: Commit**

```bash
git add ~/.openclaw/skills/llm-keyword-monitor/doubao.py
git commit -m "feat: add doubao monitor scaffold"
```

---

## Task 7: Implement Tongyi (通义千问) Monitor

**Files:**
- Create: `~/.openclaw/skills/llm-keyword-monitor/tongyi.py`

**Step 1: Create tongyi.py**

```python
#!/usr/bin/env python3
"""
通义千问 (Alibaba Tongyi) 监控模块
"""

import json

def monitor_tongyi(question: str, keywords: list) -> dict:
    """监控 通义千问"""
    return {
        "model": "通义千问",
        "question": question,
        "answer": "",
        "mentions": [],
        "contexts": [],
        "success": False,
        "error": None
    }
```

**Step 2: Commit**

```bash
git add ~/.openclaw/skills/llm-keyword-monitor/tongyi.py
git commit -m "feat: add tongyi monitor scaffold"
```

---

## Task 8: Create Config Loader

**Files:**
- Create: `~/.openclaw/skills/llm-keyword-monitor/config_loader.py`

**Step 1: Create config_loader.py**

```python
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
```

**Step 2: Test config loading**

```bash
cd ~/.openclaw/skills/llm-keyword-monitor
python3 config_loader.py
```

**Expected:** 打印出默认的问题和关键词列表

**Step 3: Commit**

```bash
git add ~/.openclaw/skills/llm-keyword-monitor/config_loader.py
git commit -m "feat: add config loader"
```

---

## Task 9: Create Report Generator

**Files:**
- Create: `~/.openclaw/skills/llm-keyword-monitor/report_generator.py`

**Step 1: Create report_generator.py**

```python
#!/usr/bin/env python3
"""
报告生成模块
"""

from datetime import datetime
from pathlib import Path

def extract_context(answer: str, keyword: str, context_len: int = 50) -> str:
    """提取关键词周围的上下文"""
    idx = answer.lower().find(keyword.lower())
    if idx == -1:
        return ""
    start = max(0, idx - context_len)
    end = min(len(answer), idx + len(keyword) + context_len)
    context = answer[start:end]
    if start > 0:
        context = "..." + context
    if end < len(answer):
        context = context + "..."
    return context

def analyze_results(results: list, keywords: list) -> dict:
    """
    分析所有模型的回答结果
    
    Returns:
        {
            "question": "问题文本",
            "model_results": [
                {
                    "model": "元宝",
                    "mentions": ["快手"],
                    "contexts": ["...上下文..."],
                    "success": True
                }
            ]
        }
    """
    # 按问题分组
    by_question = {}
    for result in results:
        q = result["question"]
        if q not in by_question:
            by_question[q] = []
        by_question[q].append(result)
    
    return by_question

def generate_markdown_report(results: list, keywords: list) -> str:
    """生成 Markdown 格式的对比报告"""
    by_question = analyze_results(results, keywords)
    
    lines = [
        "# LLM 关键词监控报告",
        "",
        f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"监控关键词：{', '.join(keywords)}",
        "",
        "---",
        ""
    ]
    
    total_mentions = 0
    total_models = 0
    
    for i, (question, model_results) in enumerate(by_question.items(), 1):
        lines.append(f"## 问题 {i}：{question}")
        lines.append("")
        lines.append("| 模型 | 提到关键词 | 上下文 |")
        lines.append("|------|-----------|--------|")
        
        for r in model_results:
            total_models += 1
            mentions = ", ".join(r["mentions"]) if r["mentions"] else "无"
            contexts = " / ".join(r["contexts"]) if r["contexts"] else "-"
            if len(contexts) > 100:
                contexts = contexts[:100] + "..."
            
            status = "✅" if r["success"] else "❌"
            lines.append(f"| {r['model']} {status} | {mentions} | {contexts} |")
            
            if r["mentions"]:
                total_mentions += 1
        
        lines.append("")
    
    # 总结
    coverage = (total_mentions / total_models * 100) if total_models > 0 else 0
    lines.append("---")
    lines.append("")
    lines.append("## 总结")
    lines.append("")
    lines.append(f"- **监控模型数**：{len(set(r['model'] for r in results))}")
    lines.append(f"- **问题数**：{len(by_question)}")
    lines.append(f"- **总回答数**：{total_models}")
    lines.append(f"- **提到关键词**：{total_mentions}/{total_models} ({coverage:.1f}%)")
    lines.append("")
    
    return "\n".join(lines)

def save_report(content: str) -> Path:
    """保存报告到文件"""
    reports_dir = Path(__file__).parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-llm-monitor.md")
    filepath = reports_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath

if __name__ == "__main__":
    # 测试
    test_results = [
        {
            "model": "元宝",
            "question": "我想找工作",
            "answer": "推荐你试试快手快聘",
            "mentions": ["快手", "快聘"],
            "contexts": ["推荐你试试快手快聘"],
            "success": True
        },
        {
            "model": "DeepSeek",
            "question": "我想找工作",
            "answer": "推荐 Boss 直聘",
            "mentions": [],
            "contexts": [],
            "success": True
        }
    ]
    
    report = generate_markdown_report(test_results, ["快手", "快聘"])
    print(report)
    
    filepath = save_report(report)
    print(f"\n报告已保存到: {filepath}")
```

**Step 2: Test report generation**

```bash
cd ~/.openclaw/skills/llm-keyword-monitor
python3 report_generator.py
```

**Step 3: Commit**

```bash
git add ~/.openclaw/skills/llm-keyword-monitor/report_generator.py
git commit -m "feat: add report generator"
```

---

## Task 10: Create Main Runner

**Files:**
- Create: `~/.openclaw/skills/llm-keyword-monitor/run.py`

**Step 1: Create run.py (main entry point)**

```python
#!/usr/bin/env python3
"""
LLM 关键词监控主程序

使用方式:
    cd ~/.openclaw/skills/llm-keyword-monitor
    python3 run.py
"""

import json
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from config_loader import load_questions, load_keywords
from report_generator import generate_markdown_report, save_report

# 导入各模型监控模块
from yuanbao import monitor_yuanbao
from deepseek import monitor_deepseek
from kimi import monitor_kimi
from doubao import monitor_doubao
from tongyi import monitor_tongyi

def main():
    """主函数"""
    print("=" * 60)
    print("LLM 关键词监控")
    print("=" * 60)
    
    # 加载配置
    questions = load_questions()
    keywords = load_keywords()
    
    print(f"\n监控问题 ({len(questions)} 个):")
    for i, q in enumerate(questions, 1):
        print(f"  {i}. {q}")
    
    print(f"\n监控关键词: {', '.join(keywords)}")
    print("\n" + "-" * 60)
    
    # 定义监控函数列表
    monitors = [
        monitor_yuanbao,
        monitor_deepseek,
        monitor_kimi,
        monitor_doubao,
        monitor_tongyi
    ]
    
    all_results = []
    
    # 遍历每个问题
    for q_idx, question in enumerate(questions, 1):
        print(f"\n[{q_idx}/{len(questions)}] 提问: {question}")
        
        # 遍历每个模型
        for monitor in monitors:
            model_name = monitor.__name__.replace("monitor_", "")
            print(f"  → 检查 {model_name}...", end=" ", flush=True)
            
            try:
                result = monitor(question, keywords)
                all_results.append(result)
                
                if result["success"]:
                    mentions = len(result["mentions"])
                    print(f"✅ (提到 {mentions} 个关键词)")
                else:
                    print(f"❌ ({result.get('error', '未知错误')})")
                    
            except Exception as e:
                print(f"❌ (异常: {e})")
                all_results.append({
                    "model": model_name,
                    "question": question,
                    "answer": "",
                    "mentions": [],
                    "contexts": [],
                    "success": False,
                    "error": str(e)
                })
    
    print("\n" + "=" * 60)
    print("生成报告...")
    
    # 生成报告
    report_content = generate_markdown_report(all_results, keywords)
    report_path = save_report(report_content)
    
    print(f"✅ 报告已保存: {report_path}")
    
    # 输出报告摘要到控制台
    print("\n" + "=" * 60)
    print("报告摘要")
    print("=" * 60)
    print(report_content[:2000])  # 打印前2000字符
    print("\n... (完整报告请查看文件)")
    
    return report_path, report_content

if __name__ == "__main__":
    main()
```

**Step 2: Commit**

```bash
git add ~/.openclaw/skills/llm-keyword-monitor/run.py
git commit -m "feat: add main runner"
```

---

## Task 11: Create Browser Automation Wrapper

**Files:**
- Create: `~/.openclaw/skills/llm-keyword-monitor/browser_wrapper.py`

**Step 1: Create browser_wrapper.py**

```python
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
        "input_selector": "textarea[placeholder*=\"输入\"]",  # 需要实际确认
        "submit_selector": "button[type=\"submit\"]",  # 需要实际确认
        "answer_selector": ".message-content",  # 需要实际确认
    },
    "deepseek": {
        "name": "DeepSeek",
        "url": "https://chat.deepseek.com",
        "input_selector": "textarea",
        "submit_selector": "button[type=\"submit\"]",
        "answer_selector": ".message-content",
    },
    "kimi": {
        "name": "Kimi",
        "url": "https://kimi.moonshot.cn",
        "input_selector": "textarea",
        "submit_selector": "button[type=\"submit\"]",
        "answer_selector": ".message-content",
    },
    "doubao": {
        "name": "豆包",
        "url": "https://www.doubao.com",
        "input_selector": "textarea",
        "submit_selector": "button[type=\"submit\"]",
        "answer_selector": ".message-content",
    },
    "tongyi": {
        "name": "通义千问",
        "url": "https://tongyi.aliyun.com",
        "input_selector": "textarea",
        "submit_selector": "button[type=\"submit\"]",
        "answer_selector": ".message-content",
    }
}

def get_model_config(model_id: str) -> dict:
    """获取模型配置"""
    return MODEL_CONFIGS.get(model_id, {})

# 实际的 browser 操作将在 SKILL.md 中定义
# 使用 browser.open, browser.act, browser.snapshot 工具
```

**Step 2: Commit**

```bash
git add ~/.openclaw/skills/llm-keyword-monitor/browser_wrapper.py
git commit -m "feat: add browser wrapper config"
```

---

## Task 12: Update SKILL.md with Implementation

**Files:**
- Modify: `~/.openclaw/skills/llm-keyword-monitor/SKILL.md`

**Step 1: Replace SKILL.md with full implementation**

```markdown
---
name: llm-keyword-monitor
description: Monitor domestic LLMs for mentions of Kuaishou keywords
---

# LLM 关键词监控

监控国内主流大模型（元宝、DeepSeek、Kimi、豆包、通义千问）在回答特定问题时是否提到快手关键词。

## 首次使用准备

1. 在 Chrome 中打开以下网址并完成登录：
   - [元宝](https://yuanbao.tencent.com)
   - [DeepSeek](https://chat.deepseek.com)
   - [Kimi](https://kimi.moonshot.cn)
   - [豆包](https://www.doubao.com)
   - [通义千问](https://tongyi.aliyun.com)

2. 点击 OpenClaw Browser Relay 扩展，确保显示 "ON"

## 配置

编辑 `config/questions.txt` 添加监控问题（一行一个）
编辑 `config/keywords.txt` 添加监控关键词（一行一个）

## 运行

```bash
cd ~/.openclaw/workspace
python3 ~/.openclaw/skills/llm-keyword-monitor/run.py
```

或使用 OpenClaw:
```
/skill llm-keyword-monitor
```

## 输出

- Markdown 报告保存到 `reports/YYYY-MM-DD-HH-mm-ss-llm-monitor.md`
- Kim 消息通知（自动发送）

---

## Implementation

### Step 1: Load Configuration

```python
from skills.llm-keyword-monitor.config_loader import load_questions, load_keywords

questions = load_questions()
keywords = load_keywords()
```

### Step 2: Monitor Yuanbao

```python
# 使用 browser tool
browser.open(
    url="https://yuanbao.tencent.com",
    profile="chrome",
    target="host"
)

# 等待页面加载
# 定位输入框并输入问题
# 提交并等待回答
# 提取回答文本
```

### Step 3: Analyze Results

```python
from skills.llm-keyword-monitor.report_generator import (
    generate_markdown_report, 
    save_report,
    extract_context
)

# 检测关键词
mentions = [kw for kw in keywords if kw in answer]
contexts = [extract_context(answer, kw) for kw in mentions]

# 生成报告
report = generate_markdown_report(results, keywords)
report_path = save_report(report)
```

### Step 4: Send Notification

```python
message.send(
    target="user:yuminghao",
    message=f"📊 LLM 监控报告已生成\n\n{summary}"
)
```
```

**Step 2: Commit**

```bash
git add ~/.openclaw/skills/llm-keyword-monitor/SKILL.md
git commit -m "docs: update SKILL.md with implementation guide"
```

---

## Task 13: Update HEARTBEAT.md

**Files:**
- Modify: `/Users/yuminghao/.openclaw/workspace/HEARTBEAT.md`

**Step 1: Add cron job to HEARTBEAT.md**

在现有内容后添加：

```markdown

## 任务：LLM 关键词监控
- cron: 0 9,14,19 * * *
- command: cd ~/.openclaw/workspace && python3 ~/.openclaw/skills/llm-keyword-monitor/run.py
- notify: true
- notify_message: 📊 LLM 关键词监控报告已生成
```

**Step 2: Commit**

```bash
git add HEARTBEAT.md
git commit -m "chore: add llm-keyword-monitor cron job"
```

---

## Task 14: Final Integration Test

**Step 1: Verify all files exist**

```bash
ls -la ~/.openclaw/skills/llm-keyword-monitor/
```

**Expected files:**
- SKILL.md
- run.py
- config_loader.py
- report_generator.py
- browser_wrapper.py
- yuanbao.py
- deepseek.py
- kimi.py
- doubao.py
- tongyi.py
- config/questions.txt
- config/keywords.txt
- reports/

**Step 2: Test config loading**

```bash
cd ~/.openclaw/skills/llm-keyword-monitor
python3 -c "from config_loader import *; print('Questions:', load_questions()); print('Keywords:', load_keywords())"
```

**Step 3: Test report generation**

```bash
cd ~/.openclaw/skills/llm-keyword-monitor
python3 report_generator.py
```

**Step 4: Final commit**

```bash
git status
git add -A
git commit -m "feat: complete llm-keyword-monitor skill implementation"
```

---

## Task 15: Implement Browser Automation (Yuanbao Example)

**Files:**
- Modify: `~/.openclaw/skills/llm-keyword-monitor/yuanbao.py`

**Step 1: Implement with browser tool calls**

实际的 browser 自动化需要使用 OpenClaw 的 `browser` 工具，这将在实际执行时完成。

伪代码：

```python
def monitor_yuanbao(question: str, keywords: list) -> dict:
    result = {...}
    
    try:
        # browser.open(url="https://yuanbao.tencent.com", profile="chrome")
        # browser.act(type="click", element="input-selector")
        # browser.act(type="type", element="input-selector", text=question)
        # browser.act(type="click", element="submit-button")
        # browser.act(type="wait", timeMs=5000)
        # snapshot = browser.snapshot()
        # answer = extract_from_snapshot(snapshot)
        pass
    except Exception as e:
        result["error"] = str(e)
    
    return result
```

**Note:** 实际的 browser 工具调用需要在 OpenClaw 环境中执行。

---

## Next Steps After Plan Completion

1. **Test with actual browser automation** - 使用 OpenClaw browser 工具访问各模型
2. **Tune selectors** - 根据实际网页结构调整 CSS selectors
3. **Handle edge cases** - 登录过期、验证码、网络超时等
4. **Add more models** - 文心一言、讯飞星火等
