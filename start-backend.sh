#!/bin/bash

echo "🚀 한글 AI 학습 플랫폼 Backend 시작..."

# Backend 디렉토리로 이동
cd backend

# 가상환경 확인
if [ ! -d "venv" ]; then
    echo "📦 가상환경 생성 중..."
    python3 -m venv venv
fi

# 가상환경 활성화
echo "🔧 가상환경 활성화..."
source venv/bin/activate

# 의존성 설치
echo "📥 의존성 설치 중..."
pip install -r requirements.txt

# .env 파일 확인
if [ ! -f ".env" ]; then
    echo "⚠️  .env 파일이 없습니다. .env.example을 복사하여 API 키를 설정하세요."
    cp .env.example .env
    echo "❌ API 키를 .env 파일에 설정한 후 다시 실행하세요."
    exit 1
fi

# API 키 확인
if grep -q "your_anthropic_api_key_here" .env; then
    echo "⚠️  ANTHROPIC_API_KEY를 설정해주세요!"
fi

if grep -q "your_fish_audio_api_key_here" .env; then
    echo "⚠️  FISH_AUDIO_API_KEY를 설정해주세요!"
fi

# 서버 시작
echo "✨ Backend 서버 시작 (http://localhost:8000)"
echo "📚 API 문서: http://localhost:8000/docs"
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
