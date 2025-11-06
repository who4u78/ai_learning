#!/bin/bash

echo "🚀 한글 AI 학습 플랫폼 전체 시작..."
echo ""

# tmux 설치 확인
if ! command -v tmux &> /dev/null; then
    echo "⚠️  tmux가 설치되어 있지 않습니다."
    echo "   설치: sudo apt-get install tmux (Ubuntu/Debian)"
    echo "   설치: brew install tmux (macOS)"
    exit 1
fi

# tmux 세션 생성
SESSION_NAME="ai_learning"

# 기존 세션이 있으면 종료
tmux has-session -t $SESSION_NAME 2>/dev/null
if [ $? == 0 ]; then
    echo "기존 세션 종료 중..."
    tmux kill-session -t $SESSION_NAME
fi

# 새 세션 생성
tmux new-session -d -s $SESSION_NAME

# Backend 윈도우
tmux rename-window -t $SESSION_NAME:0 'Backend'
tmux send-keys -t $SESSION_NAME:0 './start-backend.sh' C-m

# Frontend 윈도우
tmux new-window -t $SESSION_NAME:1 -n 'Frontend'
tmux send-keys -t $SESSION_NAME:1 './start-frontend.sh' C-m

echo ""
echo "✅ 서버가 시작되었습니다!"
echo ""
echo "📍 Backend:  http://localhost:8000"
echo "📍 Frontend: http://localhost:3000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "🔍 로그 확인: tmux attach -t $SESSION_NAME"
echo "🛑 종료:      tmux kill-session -t $SESSION_NAME"
echo ""

# tmux 세션에 연결
tmux attach -t $SESSION_NAME
