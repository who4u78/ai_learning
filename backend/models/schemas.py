from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum


class ContentSourceType(str, Enum):
    """콘텐츠 소스 타입"""
    URL = "url"          # 웹페이지 URL
    HTML = "html"        # HTML 문자열
    TEXT = "text"        # 일반 텍스트
    FILE = "file"        # 파일 경로 (PDF, DOCX, TXT, HTML)
    YOUTUBE = "youtube"  # YouTube URL (자막)


class SourceInput(BaseModel):
    """개별 소스 입력"""
    type: ContentSourceType
    data: str  # URL, 파일 경로, 텍스트 등


class ContentGenerationRequest(BaseModel):
    """콘텐츠 생성 요청"""
    # 단일 소스 (하위 호환성)
    source_type: Optional[ContentSourceType] = None
    source_data: Optional[str] = None

    # 다중 소스 (새 기능)
    sources: Optional[List[SourceInput]] = None

    title: Optional[str] = None
    language: str = "ko"  # 출력 언어


# ============= 팟캐스트 관련 =============

class PodcastDialogue(BaseModel):
    """팟캐스트 대화"""
    speaker: str  # "host" or "guest"
    text: str
    timestamp: Optional[float] = None  # 초 단위


class PodcastScript(BaseModel):
    """팟캐스트 스크립트"""
    title: str
    host_name: str = "진행자"
    guest_name: str = "게스트"
    dialogues: List[PodcastDialogue]
    duration_minutes: int  # 목표 시간


class Podcast(BaseModel):
    """팟캐스트 (2인 대화)"""
    id: str
    script: PodcastScript
    audio_url: Optional[str] = None
    duration: Optional[float] = None  # 실제 재생 시간(초)
    created_at: datetime


# ============= 강의 비디오 관련 =============

class LectureSlide(BaseModel):
    """강의 슬라이드"""
    slide_number: int
    title: str
    content: List[str]  # 슬라이드 내용 (불릿 포인트)
    narration: str  # 나레이션 텍스트
    duration: Optional[float] = None  # 슬라이드 표시 시간(초)
    image_path: Optional[str] = None


class VideoLecture(BaseModel):
    """강의 비디오"""
    id: str
    title: str
    slides: List[LectureSlide]
    video_url: Optional[str] = None
    total_duration: Optional[float] = None  # 총 재생 시간(초)
    created_at: datetime


# ============= 읽기 자료 =============

class ReadingMaterial(BaseModel):
    """읽기 자료"""
    id: str
    title: str
    content: str  # 마크다운 형식
    estimated_reading_time: int  # 예상 읽기 시간(분)
    created_at: datetime


# ============= 질문 및 퀴즈 =============

class DeepThinkingQuestion(BaseModel):
    """심화 사고 질문"""
    question: str
    context: Optional[str] = None  # 질문의 맥락
    hints: Optional[List[str]] = None  # 힌트


class MultipleChoiceQuiz(BaseModel):
    """4지선다형 퀴즈"""
    question: str
    options: List[str]  # 4개의 선택지
    correct_answer: int  # 정답 인덱스 (0-3)
    explanation: str
    difficulty: Optional[str] = "medium"  # easy, medium, hard


class ShortAnswerQuiz(BaseModel):
    """단답형 퀴즈"""
    question: str
    correct_answers: List[str]  # 가능한 정답들 (여러 형태 허용)
    explanation: str
    case_sensitive: bool = False


class EssayQuiz(BaseModel):
    """서술형 문제"""
    question: str
    suggested_answer: str  # 예시 답안
    grading_criteria: List[str]  # 채점 기준
    min_words: Optional[int] = 100


# ============= 챗봇 =============

class ChatMessage(BaseModel):
    """챗봇 메시지"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime


class ChatRequest(BaseModel):
    """챗봇 요청"""
    content_id: str  # 학습 콘텐츠 ID (컨텍스트)
    message: str
    conversation_history: Optional[List[ChatMessage]] = []


class ChatResponse(BaseModel):
    """챗봇 응답"""
    message: str
    timestamp: datetime


# ============= 통합 학습 콘텐츠 =============

class LearningContent(BaseModel):
    """통합 학습 콘텐츠"""
    id: str
    title: str
    description: str

    # 1. 팟캐스트 (10분)
    podcast: Optional[Podcast] = None

    # 2. 강의 비디오 (20분+)
    video_lecture: Optional[VideoLecture] = None

    # 3. 읽기 자료 (10분)
    reading_material: Optional[ReadingMaterial] = None

    # 4. 심화 질문 (3개)
    deep_questions: List[DeepThinkingQuestion] = []

    # 5. 4지선다 퀴즈 (10문제)
    multiple_choice_quizzes: List[MultipleChoiceQuiz] = []

    # 6. 단답형 퀴즈 (5문제)
    short_answer_quizzes: List[ShortAnswerQuiz] = []

    # 7. 서술형 문제 (2개)
    essay_quizzes: List[EssayQuiz] = []

    # 원본 소스 정보
    source_url: Optional[str] = None
    source_text: Optional[str] = None

    created_at: datetime
    updated_at: datetime
    metadata: Optional[Dict[str, Any]] = None


# ============= 기타 =============

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
    include_subtitles: bool = True
    resolution: str = "1280x720"
    fps: int = 30


class VideoGenerationResponse(BaseModel):
    """비디오 생성 응답"""
    video_url: str
    file_path: str
    duration: float
    size_mb: float


class ContentGenerationStatus(BaseModel):
    """콘텐츠 생성 상태"""
    content_id: str
    status: str  # "processing", "completed", "failed"
    progress: int  # 0-100
    current_task: Optional[str] = None
    error: Optional[str] = None
