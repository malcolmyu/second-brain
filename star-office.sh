#!/bin/bash
# Star Office UI 快捷管理脚本

STAR_OFFICE_DIR="$HOME/.openclaw/workspace/star-office"
STATE_FILE="$STAR_OFFICE_DIR/state.json"
PORT=18080

case "$1" in
    start)
        echo "🚀 启动 Star Office UI..."
        cd "$STAR_OFFICE_DIR/backend"
        STAR_BACKEND_PORT=$PORT nohup python3 app.py > ../server.log 2>&1 &
        echo "✅ 服务已启动"
        echo "🌐 本地访问: http://127.0.0.1:$PORT"
        sleep 2
        ;;
    stop)
        echo "🛑 停止 Star Office UI..."
        pkill -f "python3 app.py" 2>/dev/null
        echo "✅ 服务已停止"
        ;;
    status)
        if curl -s http://127.0.0.1:$PORT/status > /dev/null 2>&1; then
            echo "✅ Star Office UI 运行中"
            echo "🌐 本地访问: http://127.0.0.1:$PORT"
            echo ""
            echo "当前状态:"
            curl -s http://127.0.0.1:$PORT/status | python3 -m json.tool 2>/dev/null || cat "$STATE_FILE"
        else
            echo "❌ Star Office UI 未运行"
            echo "运行: ./star-office.sh start"
        fi
        ;;
    idle)
        curl -s -X POST http://127.0.0.1:$PORT/set_state \
            -H "Content-Type: application/json" \
            -d "{\"state\":\"idle\",\"detail\":\"${2:-待命中，随时准备为你服务}\"}"
        echo ""
        ;;
    writing)
        curl -s -X POST http://127.0.0.1:$PORT/set_state \
            -H "Content-Type: application/json" \
            -d "{\"state\":\"writing\",\"detail\":\"${2:-正在处理任务...}\"}"
        echo ""
        ;;
    researching)
        curl -s -X POST http://127.0.0.1:$PORT/set_state \
            -H "Content-Type: application/json" \
            -d "{\"state\":\"researching\",\"detail\":\"${2:-正在研究资料...}\"}"
        echo ""
        ;;
    executing)
        curl -s -X POST http://127.0.0.1:$PORT/set_state \
            -H "Content-Type: application/json" \
            -d "{\"state\":\"executing\",\"detail\":\"${2:-正在执行操作...}\"}"
        echo ""
        ;;
    error)
        curl -s -X POST http://127.0.0.1:$PORT/set_state \
            -H "Content-Type: application/json" \
            -d "{\"state\":\"error\",\"detail\":\"${2:-遇到问题，正在排查}\"}"
        echo ""
        ;;
    syncing)
        curl -s -X POST http://127.0.0.1:$PORT/set_state \
            -H "Content-Type: application/json" \
            -d "{\"state\":\"syncing\",\"detail\":\"${2:-正在同步数据...}\"}"
        echo ""
        ;;
    tunnel)
        echo "🌐 启动 Cloudflare Tunnel（需要已安装 cloudflared）..."
        cloudflared tunnel --url http://localhost:$PORT
        ;;
    *)
        echo "Star Office UI 管理脚本"
        echo ""
        echo "用法: ./star-office.sh <命令> [参数]"
        echo ""
        echo "服务管理:"
        echo "  start     启动服务"
        echo "  stop      停止服务"
        echo "  status    查看状态和当前状态"
        echo ""
        echo "状态切换:"
        echo "  idle [消息]       待命状态"
        echo "  writing [消息]    工作中"
        echo "  researching [消息] 研究中"
        echo "  executing [消息]  执行中"
        echo "  syncing [消息]    同步中"
        echo "  error [消息]      报错中"
        echo ""
        echo "公网访问:"
        echo "  tunnel    创建临时公网隧道（需要 cloudflared）"
        echo ""
        echo "示例:"
        echo "  ./star-office.sh start"
        echo "  ./star-office.sh writing '正在生成日报...'"
        echo "  ./star-office.sh idle '任务完成'"
        ;;
esac
