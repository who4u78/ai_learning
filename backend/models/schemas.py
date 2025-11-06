from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ContentSourceType(str, Enum):
    """콘텐츠 소스 타입"""
    URL = "url"
    HTML = "html"
    TEXT = "text"
    FILE = "file"


class ContentGenerationRequest(BaseModel):
    """콘텐츠 생성 요청"""
    source_type: ContentSourceType
    source_data: str  # URL, HTML, 또는 텍스트
    title: Optional[str] = None
    language: str = "ko"  # 출력 언어
    include_quiz: bool = True
    include_summary: bool = True
    include_examples: bool = True


class LearningSection(BaseModel):
    """학습 섹션"""
    id: str
    title: str
    content: str
    order: int
    estimated_time: Optional[int] = None  # 예상 학습 시간(분)


class Quiz(BaseModel):
    """퀴즈"""
    question: str
    options: List[str]
    correct_answer: int
    explanation: str


class GeneratedContent(BaseModel):
    """생성된 콘텐츠"""
    id: str
    title: str
    summary: str
    sections: List[LearningSection]
    quizzes: Optional[List[Quiz]] = None
    created_at: datetime
    metadata: Optional[Dict[str, Any]] = None


class TTSRequest(BaseModel):
    """TTS 요청"""
    text: str
    voice_id: Optional[str] = None  # Fish Audio 보이스 ID
    speed: float = 1.0
    format: str = "mp3"


class TTSResponse(BaseModel):
    """TTS 응답"""
    audio_url: str
    duration: float  # 초
    file_path: str


class VideoGenerationRequest(BaseModel):
    """비디오 생성 요청"""
    content_id: str
    section_ids: Optional[List[str]] = None  # None이면 전체 섹션
    include_subtitles: bool = True
    resolution: str = "1280x720"
    fps: int = 30


class VideoGenerationResponse(BaseModel):
    """비디오 생성 응답"""
    video_url: str
    file_path: str
    duration: float
    size_mb: float


class Course(BaseModel):
    """코스"""
    id: str
    title: str
    description: str
    content_ids: List[str]
    created_at: datetime
    updated_at: datetime
    thumbnail_url: Optional[str] = None


class CourseProgress(BaseModel):
    """코스 진행 상황"""
    course_id: str
    user_id: str
    completed_sections: List[str]
    quiz_scores: Dict[str, float]
    progress_percentage: float
    last_accessed: datetime
