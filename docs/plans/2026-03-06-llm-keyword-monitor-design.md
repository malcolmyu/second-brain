# LLM 关键词监控 Skill 设计文档

日期：2026-03-06

## 概述

一个 OpenClaw Skill，用于监控国内主流大模型（元宝、DeepSeek、Kimi、豆包、通义千问）在回答特定问题时是否提到快手的搜索关键词。

## 目标

- 每天定时向各模型提问
- 捕获并分析回答内容
- 生成对比报告，显示哪些模型推荐了快手/快聘
- 发送 Kim 通知

## 架构

```
~/.openclaw/skills/llm-keyword-monitor/
├── SKILL.md                      # Skill 定义
├── config/
│   ├── questions.txt             # 问题列表（一行一个）
│   └── keywords.txt              # 监控关键词列表（一行一个）
└── reports/                      # 生成的对比报告
```

## 支持的模型

| 模型 | 网页版 URL | 登录方式 |
|------|-----------|----------|
| 元宝 | yuanbao.tencent.com | 微信扫码 |
| DeepSeek | chat.deepseek.com | 手机号 |
| Kimi | kimi.moonshot.cn | 手机号 |
| 豆包 | www.doubao.com | 抖音/手机号 |
| 通义千问 | tongyi.aliyun.com | 阿里账号 |

## 登录方案

**Chrome 扩展模式**：复用用户已登录的 Chrome 浏览器

1. 首次：用户在 Chrome 中打开各模型网页版并完成登录
2. 运行时：Skill 使用 `profile="chrome"` 复用登录态
3. 过期检测：Skill 检测登录状态，过期时提醒用户刷新

## 工作流程

```
1. 读取配置文件（questions.txt, keywords.txt）
2. 遍历各模型：
   a. 使用 browser.open 访问网页版（复用 Chrome 登录态）
   b. 定位输入框，输入问题
   c. 提交并等待回答完成
   d. 使用 browser.snapshot 捕获回答文本
   e. 保存回答原文
3. 分析：对每个问题，对比所有模型的回答
   - 检测关键词出现情况
   - 提取关键词上下文（前后50字）
4. 生成 Markdown 对比报告
5. 发送 Kim 通知
```

## 输出格式

**Markdown 报告** (`reports/YYYY-MM-DD-HH-mm-ss-llm-monitor.md`)

```markdown
# LLM 关键词监控报告

日期：2026-03-06 09:00

## 问题 1：我想在北京找工作，有什么推荐的平台吗？

| 模型 | 提到关键词 | 上下文 |
|------|-----------|--------|
| 元宝 | 快手、快聘 | "...推荐你试试快手快聘..." |
| DeepSeek | 无 | - |
| Kimi | 快手 | "...短视频平台如快手..." |
| 豆包 | 无 | - |
| 通义千问 | 快聘 | "...快手旗下的快聘平台..." |

## 总结

- **今日覆盖率**：3/5 模型提到快手/快聘
- **高频场景**：找工作、招聘
```

**Kim 通知**

简洁文本版本，包含关键结论。

## 定时配置

添加到 `HEARTBEAT.md`：

```markdown
## 任务：LLM 关键词监控
- cron: 0 9,14,19 * * *
- command: cd ~/.openclaw/workspace && openclaw skill llm-keyword-monitor
- notify: true
```

## 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| 登录态过期 | 检测登录状态，失败时跳过并提醒 |
| 网页结构变化 | 使用稳定的 selectors，添加重试机制 |
| 反爬/验证码 | 增加请求间隔，模拟人类操作 |
| 模型响应慢 | 设置超时，超时则跳过 |

## 配置示例

**questions.txt**
```
我想在北京找工作，有什么推荐的平台吗？
应届毕业生求职用什么APP比较好？
互联网行业的招聘信息去哪里找？
蓝领工人怎么找工作？
```

**keywords.txt**
```
快手
快聘
Kuaishou
```

## 后续优化方向

1. 支持更多模型（文心一言、讯飞星火等）
2. 添加情感分析（推荐/中性/负面）
3. 历史趋势对比（本周 vs 上周覆盖率）
4. 自动化登录（验证码识别等）
