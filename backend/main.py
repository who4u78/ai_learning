from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from api import content, audio, video, courses, learning

@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작/종료 시 실행되는 코드"""
    # 시작 시 디렉토리 생성
    directories = [
        os.getenv("SOURCES_DIR", "../data/sources"),
        os.getenv("CONTENT_DIR", "../data/content"),
        os.getenv("AUDIO_DIR", "../data/audio"),
        os.getenv("VIDEOS_DIR", "../data/videos"),
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    print("🚀 AI Learning Platform Backend Started")
    yield
    print("👋 Shutting down...")

# FastAPI 앱 초기화
app = FastAPI(
    title="한글 AI 학습 플랫폼 API",
    description="""
    HTML/텍스트를 완전한 한글 학습 자료로 변환하는 AI 플랫폼

    포함 내용:
    - 10분 2인 팟캐스트
    - 20분+ 강의 비디오 (슬라이드 포함)
    - 10분 읽기 자료
    - 심화 사고 질문 3개
    - 4지선다 퀴즈 10문제
    - 단답형 퀴즈 5문제
    - 서술형 문제 2개
    - 실시간 학습 챗봇
    """,
    version="2.0.0",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(learning.router, prefix="/api/learning", tags=["learning"])  # 새로운 통합 API
app.include_router(content.router, prefix="/api/content", tags=["content"])  # 하위 호환성
app.include_router(audio.router, prefix="/api/audio", tags=["audio"])
app.include_router(video.router, prefix="/api/video", tags=["video"])
app.include_router(courses.router, prefix="/api/courses", tags=["courses"])

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "한글 AI 학습 플랫폼 API v2.0",
        "version": "2.0.0",
        "features": [
            "2인 팟캐스트 (10분)",
            "강의 비디오 (20분+)",
            "읽기 자료 (10분)",
            "다양한 퀴즈 (4지선다 10개, 단답형 5개, 서술형 2개)",
            "심화 질문 (3개)",
            "실시간 챗봇"
        ],
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "anthropic_key_set": bool(os.getenv("ANTHROPIC_API_KEY")),
        "fish_audio_key_set": bool(os.getenv("FISH_AUDIO_API_KEY"))
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "True") == "True"
    )
