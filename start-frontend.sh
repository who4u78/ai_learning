#!/bin/bash

echo "🚀 한글 AI 학습 플랫폼 Frontend 시작..."

# Frontend 디렉토리로 이동
cd frontend

# node_modules 확인
if [ ! -d "node_modules" ]; then
    echo "📦 의존성 설치 중..."
    npm install
fi

# .env.local 파일 확인
if [ ! -f ".env.local" ]; then
    echo "📝 .env.local 파일 생성..."
    cp .env.local.example .env.local
fi

# 개발 서버 시작
echo "✨ Frontend 개발 서버 시작 (http://localhost:3000)"
npm run dev
