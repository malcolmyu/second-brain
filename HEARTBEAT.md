# HEARTBEAT.md - 定时任务配置

## 每日 AI 资讯追踪
# 每天早上 9 点生成 AI 日报并保存到 docs 目录
- cron: 0 9 * * *
- command: cd ~/.openclaw/skills/second-number-updater && python3 run.py daily
- notify: true
- notify_message: 📰 每日 AI 资讯已生成，已更新到 docs 目录

## OpenClaw GitHub 更新监控
# 每天早上 10:30 检查 OpenClaw 仓库更新
- cron: 30 10 * * *
- command: cd ~/.openclaw/workspace/skills/github-monitor && node check-openclaw.js
- notify: true
- notify_on_success_only: true
- notify_message: 🐙 OpenClaw GitHub 有更新
