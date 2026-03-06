#!/bin/bash
# AI Daily News - 日报生成并发送通知

WORKSPACE="$HOME/.openclaw/workspace"
DATE=$(date +%Y%m%d)
LOG_FILE="$WORKSPACE/daily_news.log"

echo "=== $(date) ===" >> "$LOG_FILE"
echo "开始生成 AI 日报..." >> "$LOG_FILE"

# 运行日报生成脚本
cd "$WORKSPACE"
python3 ai_daily_news.py >> "$LOG_FILE" 2>&1

# 检查是否成功生成
if [ -f "$WORKSPACE/${DATE}_v1.md" ]; then
    echo "✅ 日报生成成功: ${DATE}_v1.md" >> "$LOG_FILE"
    echo "📰 AI 日报已生成！请查看 ${DATE}_v1.md" >> "$LOG_FILE"
else
    echo "❌ 日报生成失败" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"
