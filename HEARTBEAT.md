# HEARTBEAT.md - AI Daily News Task
# 每天早上 11 点生成 AI 日报

## 任务：AI 日报生成
- cron: 0 11 * * *
- command: cd ~/.openclaw/workspace && python3 ai_daily_news.py
- notify: true
- notify_message: 📰 AI 日报已生成！请查看最新资讯

## 任务：LLM 关键词监控
- cron: 0 9,14,19 * * *
- command: cd ~/.openclaw/workspace && python3 skills/llm-keyword-monitor/run.py
- notify: true
- notify_message: 📊 LLM 关键词监控报告已生成
