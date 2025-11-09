from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from models.schemas import TTSRequest, TTSResponse
from services.tts_service import TTSService
import logging
import os

logger = logging.getLogger(__name__)
router = APIRouter()

# TTS 서비스 초기화
tts_service = TTSService()


@router.post("/generate", response_model=TTSResponse)
async def generate_audio(
    request: TTSRequest,
    background_tasks: BackgroundTasks
):
    """
    텍스트를 음성으로 변환합니다 (Fish Audio TTS).

    - **text**: 변환할 텍스트
    - **voice_id**: Fish Audio 보이스 ID (선택사항)
    - **speed**: 재생 속도 (기본: 1.0)
    - **format**: 오디오 포맷 (기본: mp3)
    """
    try:
        logger.info(f"음성 생성 요청: {len(request.text)} 글자")

        # TTS 생성
        audio_response = await tts_service.generate(
            text=request.text,
            voice_id=request.voice_id,
            speed=request.speed,
            format=request.format
        )

        logger.info(f"음성 생성 완료: {audio_response.file_path}")
        return audio_response

    except Exception as e:
        logger.error(f"음성 생성 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"음성 생성 실패: {str(e)}")


@router.get("/file/{filename}")
async def get_audio_file(filename: str):
    """생성된 오디오 파일을 다운로드합니다."""
    audio_dir = os.getenv("AUDIO_DIR", "../data/audio")
    file_path = os.path.join(audio_dir, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="오디오 파일을 찾을 수 없습니다")

    return FileResponse(
        file_path,
        media_type="audio/mpeg",
        filename=filename
    )


@router.post("/generate-for-content/{content_id}")
async def generate_audio_for_content(
    content_id: str,
    section_ids: list[str] = None,
    voice_id: str = None
):
    """
    콘텐츠의 모든 섹션에 대해 음성을 생성합니다.

    - **content_id**: 콘텐츠 ID
    - **section_ids**: 특정 섹션만 생성 (선택사항, None이면 전체)
    - **voice_id**: Fish Audio 보이스 ID (선택사항)
    """
    try:
        logger.info(f"콘텐츠 음성 생성 요청: {content_id}")

        audio_files = await tts_service.generate_for_content(
            content_id=content_id,
            section_ids=section_ids,
            voice_id=voice_id
        )

        return {
            "content_id": content_id,
            "audio_files": audio_files,
            "total": len(audio_files)
        }

    except Exception as e:
        logger.error(f"콘텐츠 음성 생성 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"콘텐츠 음성 생성 실패: {str(e)}")


@router.delete("/file/{filename}")
async def delete_audio_file(filename: str):
    """오디오 파일을 삭제합니다."""
    audio_dir = os.getenv("AUDIO_DIR", "../data/audio")
    file_path = os.path.join(audio_dir, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="오디오 파일을 찾을 수 없습니다")

    try:
        os.remove(file_path)
        return {"message": "오디오 파일이 삭제되었습니다", "filename": filename}
    except Exception as e:
        logger.error(f"오디오 파일 삭제 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"파일 삭제 실패: {str(e)}")
