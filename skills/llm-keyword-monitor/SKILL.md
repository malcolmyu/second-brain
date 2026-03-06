---
name: llm-keyword-monitor
description: Monitor domestic LLMs for mentions of Kuaishou keywords in their responses
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
python3 skills/llm-keyword-monitor/run.py
```

## 输出

- Markdown 报告保存到 `reports/YYYY-MM-DD-HH-mm-ss-llm-monitor.md`
- 控制台输出摘要

## 架构

```
skills/llm-keyword-monitor/
├── SKILL.md                  # 本文件
├── run.py                    # 主入口
├── config_loader.py          # 配置加载
├── report_generator.py       # 报告生成
├── browser_wrapper.py        # 浏览器配置
├── yuanbao.py               # 元宝监控
├── deepseek.py              # DeepSeek监控
├── kimi.py                  # Kimi监控
├── doubao.py                # 豆包监控
├── tongyi.py                # 通义千问监控
├── config/
│   ├── questions.txt        # 问题列表
│   └── keywords.txt         # 关键词列表
└── reports/                 # 报告输出目录
```

## 实现细节

### 监控流程

1. 加载配置（问题列表 + 关键词列表）
2. 遍历每个问题
3. 对每个模型：
   - 使用 browser 工具访问网页版
   - 输入问题并提交
   - 等待回答完成
   - 提取回答文本
   - 检测关键词出现
4. 生成对比报告

### 浏览器自动化

使用 OpenClaw `browser` 工具：

```python
# 伪代码示例
browser.open(url="https://yuanbao.tencent.com", profile="chrome")
browser.act(type="type", element="textarea", text=question)
browser.act(type="click", element="submit-button")
browser.act(type="wait", timeMs=5000)
snapshot = browser.snapshot()
```

### 关键词检测

```python
mentions = [kw for kw in keywords if kw in answer]
contexts = [extract_context(answer, kw) for kw in mentions]
```

## 注意事项

- 首次使用需要在 Chrome 中完成各平台的登录
- 登录态会过期，过期后需要重新登录
- 各平台可能有反爬机制，请求间隔已做处理
- 报告默认保存到 `reports/` 目录

## 定时运行

添加 cron 任务到 `HEARTBEAT.md`：

```markdown
## 任务：LLM 关键词监控
- cron: 0 9,14,19 * * *
- command: cd ~/.openclaw/workspace && python3 skills/llm-keyword-monitor/run.py
- notify: true
- notify_message: 📊 LLM 关键词监控报告已生成
```
