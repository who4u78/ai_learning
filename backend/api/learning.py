from fastapi import APIRouter, HTTPException, BackgroundTasks, File, UploadFile, Form
from fastapi.responses import JSONResponse
from typing import List
from models.schemas import (
    ContentGenerationRequest,
    LearningContent,
    ContentGenerationStatus,
    ChatRequest,
    ChatResponse
)
from services.enhanced_source_parser import EnhancedSourceParser
from services.learning_content_generator import LearningContentGenerator
from services.podcast_service import PodcastService
from services.lecture_service import LectureService
from services.chatbot_service import ChatbotService
import logging
import asyncio

logger = logging.getLogger(__name__)
router = APIRouter()

# 서비스 초기화
source_parser = EnhancedSourceParser()  # 확장된 파서 사용
content_generator = LearningContentGenerator()
podcast_service = PodcastService()
lecture_service = LectureService()
chatbot_service = ChatbotService()

# 생성 상태 추적
generation_status = {}

# 단계별 생성 세션 저장소
generation_sessions = {}


@router.post("/start")
async def start_generation(request: ContentGenerationRequest):
    """
    학습 콘텐츠 생성 시작 - 소스만 파싱하고 세션 생성
    """
    try:
        import uuid
        session_id = str(uuid.uuid4())

        logger.info(f"새 생성 세션 시작: {session_id}")

        # 소스 파싱
        if request.sources:
            parsed_content = await source_parser.parse_multiple([
                {"type": s.type.value, "data": s.data} for s in request.sources
            ])
        else:
            parsed_content = await source_parser.parse(
                source_type=request.source_type,
                source_data=request.source_data
            )

        # 세션 저장
        generation_sessions[session_id] = {
            "session_id": session_id,
            "source_content": parsed_content,
            "title": request.title or parsed_content.get("title", "학습 자료"),
            "generated_content": {},
            "current_step": None,
            "steps_completed": []
        }

        return {
            "session_id": session_id,
            "status": "ready",
            "title": generation_sessions[session_id]["title"],
            "source_length": len(parsed_content.get("text_content", ""))
        }

    except Exception as e:
        logger.error(f"세션 시작 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-step/{session_id}")
async def generate_step(session_id: str, step: str):
    """
    특정 단계의 콘텐츠 생성

    step 옵션:
    - podcast: 팟캐스트
    - video_lecture: 강의 슬라이드
    - reading_material: 읽기 자료
    - quizzes: 퀴즈 (4지선다, 단답형, 서술형)
    - deep_questions: 심화 질문
    """
    try:
        if session_id not in generation_sessions:
            raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다")

        session = generation_sessions[session_id]
        logger.info(f"단계 생성 요청: {session_id} - {step}")

        # 이미 생성된 경우 바로 반환
        if step in session["generated_content"]:
            return {
                "session_id": session_id,
                "step": step,
                "status": "completed",
                "data": session["generated_content"][step]
            }

        # 단계별 생성
        session["current_step"] = step

        if step == "podcast":
            data = await content_generator.generate_podcast(session["source_content"])
        elif step == "video_lecture":
            data = await content_generator.generate_video_lecture(session["source_content"])
        elif step == "reading_material":
            data = await content_generator.generate_reading_material(session["source_content"])
        elif step == "quizzes":
            data = await content_generator.generate_quizzes(session["source_content"])
        elif step == "deep_questions":
            data = await content_generator.generate_deep_questions(session["source_content"])
        else:
            raise HTTPException(status_code=400, detail=f"알 수 없는 단계: {step}")

        # 생성된 콘텐츠 저장
        session["generated_content"][step] = data
        session["steps_completed"].append(step)

        return {
            "session_id": session_id,
            "step": step,
            "status": "completed",
            "data": data
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"단계 생성 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """세션 상태 조회"""
    if session_id not in generation_sessions:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다")

    session = generation_sessions[session_id]
    return {
        "session_id": session_id,
        "title": session["title"],
        "current_step": session["current_step"],
        "steps_completed": session["steps_completed"],
        "available_steps": ["podcast", "video_lecture", "reading_material", "quizzes", "deep_questions"]
    }



@router.post("/generate", response_model=ContentGenerationStatus)
async def generate_learning_content(
    request: ContentGenerationRequest,
    background_tasks: BackgroundTasks
):
    """
    통합 학습 콘텐츠 생성 시작

    백그라운드에서 모든 자료(팟캐스트, 강의, 퀴즈 등)를 생성하고
    상태를 반환합니다.
    """
    try:
        logger.info(f"학습 콘텐츠 생성 요청: {request.source_type}")

        # 임시 ID 생성
        import uuid
        content_id = str(uuid.uuid4())

        # 초기 상태 설정
        generation_status[content_id] = {
            "content_id": content_id,
            "status": "processing",
            "progress": 0,
            "current_task": "소스 파싱 중..."
        }

        # 백그라운드에서 생성
        background_tasks.add_task(
            generate_content_background,
            content_id,
            request
        )

        return ContentGenerationStatus(
            content_id=content_id,
            status="processing",
            progress=0,
            current_task="소스 파싱 중..."
        )

    except Exception as e:
        logger.error(f"콘텐츠 생성 시작 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def generate_content_background(content_id: str, request: ContentGenerationRequest):
    """백그라운드 콘텐츠 생성"""
    try:
        # 1. 소스 파싱 (10%)
        generation_status[content_id].update({
            "progress": 10,
            "current_task": "소스 파싱 중..."
        })

        # 다중 소스 또는 단일 소스 처리
        if request.sources:
            # 여러 소스 결합
            logger.info(f"{len(request.sources)}개의 소스를 결합합니다")
            parsed_content = await source_parser.parse_multiple([
                {"type": s.type.value, "data": s.data} for s in request.sources
            ])
        else:
            # 단일 소스 (하위 호환성)
            parsed_content = await source_parser.parse(
                source_type=request.source_type,
                source_data=request.source_data
            )

        # 2. AI 콘텐츠 생성 (50%)
        generation_status[content_id].update({
            "progress": 20,
            "current_task": "AI가 학습 자료 생성 중... (1-2분 소요)"
        })

        learning_content = await content_generator.generate_all(
            source_content=parsed_content,
            title=request.title
        )

        # 실제 ID로 업데이트
        learning_content.id = content_id
        await content_generator._save_content(content_id, learning_content)

        # 3. 팟캐스트 오디오 생성 (70%)
        if learning_content.podcast:
            generation_status[content_id].update({
                "progress": 50,
                "current_task": "팟캐스트 오디오 생성 중..."
            })

            try:
                podcast_audio = await podcast_service.generate_podcast_audio(learning_content.podcast)
                learning_content.podcast.audio_url = podcast_audio.audio_url
                learning_content.podcast.duration = podcast_audio.duration
            except Exception as e:
                logger.error(f"팟캐스트 생성 실패: {e}")

        # 4. 강의 비디오 생성 (90%)
        if learning_content.video_lecture:
            generation_status[content_id].update({
                "progress": 70,
                "current_task": "강의 비디오 생성 중... (시간이 걸릴 수 있습니다)"
            })

            try:
                lecture_video = await lecture_service.generate_lecture_video(learning_content.video_lecture)
                learning_content.video_lecture.video_url = lecture_video.video_url
                learning_content.video_lecture.total_duration = lecture_video.duration
            except Exception as e:
                logger.error(f"강의 비디오 생성 실패: {e}")

        # 5. 최종 저장
        generation_status[content_id].update({
            "progress": 95,
            "current_task": "저장 중..."
        })

        await content_generator._save_content(content_id, learning_content)

        # 완료
        generation_status[content_id].update({
            "status": "completed",
            "progress": 100,
            "current_task": "완료"
        })

    except Exception as e:
        logger.error(f"백그라운드 생성 실패: {str(e)}")
        generation_status[content_id].update({
            "status": "failed",
            "progress": 0,
            "current_task": "실패",
            "error": str(e)
        })


@router.get("/status/{content_id}", response_model=ContentGenerationStatus)
async def get_generation_status(content_id: str):
    """생성 상태 조회"""
    if content_id not in generation_status:
        raise HTTPException(status_code=404, detail="생성 작업을 찾을 수 없습니다")

    status = generation_status[content_id]
    return ContentGenerationStatus(**status)


@router.get("/{content_id}", response_model=LearningContent)
async def get_learning_content(content_id: str):
    """학습 콘텐츠 조회"""
    try:
        content = await content_generator.get_content(content_id)
        if not content:
            raise HTTPException(status_code=404, detail="콘텐츠를 찾을 수 없습니다")
        return content
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"콘텐츠 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest):
    """챗봇과 대화"""
    try:
        # 콘텐츠 조회
        content = await content_generator.get_content(request.content_id)
        if not content:
            raise HTTPException(status_code=404, detail="콘텐츠를 찾을 수 없습니다")

        # 챗봇 응답 생성
        response = await chatbot_service.chat(
            content=content,
            user_message=request.message,
            conversation_history=request.conversation_history
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"챗봇 응답 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload", response_model=ContentGenerationStatus)
async def upload_and_generate(
    files: List[UploadFile] = File(...),
    background_tasks: BackgroundTasks = None
):
    """
    파일 업로드 후 학습 콘텐츠 생성

    여러 파일을 동시에 업로드할 수 있습니다:
    - PDF, Word, Excel, PowerPoint
    - Markdown, Text
    - 여러 파일을 결합하여 하나의 학습 자료 생성
    """
    import os
    import tempfile
    import uuid

    try:
        logger.info(f"{len(files)}개 파일 업로드 시작")

        # 임시 디렉토리 생성
        temp_dir = tempfile.mkdtemp()
        file_paths = []

        # 모든 파일 저장
        for file in files:
            # 안전한 파일명 생성
            safe_filename = f"{uuid.uuid4()}_{file.filename}"
            file_path = os.path.join(temp_dir, safe_filename)

            # 파일 저장
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)

            file_paths.append(file_path)
            logger.info(f"파일 저장: {file.filename} -> {file_path}")

        # ContentGenerationRequest 생성
        if len(file_paths) == 1:
            # 단일 파일
            request = ContentGenerationRequest(
                source_type="file",
                source_data=file_paths[0]
            )
        else:
            # 다중 파일
            sources = [{"type": "file", "data": path} for path in file_paths]
            request = ContentGenerationRequest(sources=sources)

        # 백그라운드 작업으로 생성 시작
        content_id = str(uuid.uuid4())
        generation_status[content_id] = {
            "content_id": content_id,
            "status": "processing",
            "progress": 0,
            "current_task": "파일 처리 중..."
        }

        background_tasks.add_task(
            generate_content_background,
            content_id,
            request
        )

        return ContentGenerationStatus(**generation_status[content_id])

    except Exception as e:
        logger.error(f"파일 업로드 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"파일 업로드 실패: {str(e)}")
