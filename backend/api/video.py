from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from models.schemas import VideoGenerationRequest, VideoGenerationResponse
from services.video_service import VideoService
import logging
import os

logger = logging.getLogger(__name__)
router = APIRouter()

# 비디오 서비스 초기화
video_service = VideoService()


@router.post("/generate", response_model=VideoGenerationResponse)
async def generate_video(
    request: VideoGenerationRequest,
    background_tasks: BackgroundTasks
):
    """
    콘텐츠로부터 학습 비디오를 생성합니다.

    - **content_id**: 콘텐츠 ID
    - **section_ids**: 포함할 섹션 ID 목록 (선택사항, None이면 전체)
    - **include_subtitles**: 자막 포함 여부
    - **resolution**: 비디오 해상도 (기본: 1280x720)
    """
    try:
        logger.info(f"비디오 생성 요청: {request.content_id}")

        # 비디오 생성 (시간이 오래 걸림)
        video_response = await video_service.generate(
            content_id=request.content_id,
            section_ids=request.section_ids,
            include_subtitles=request.include_subtitles,
            resolution=request.resolution,
            fps=request.fps
        )

        logger.info(f"비디오 생성 완료: {video_response.file_path}")
        return video_response

    except Exception as e:
        logger.error(f"비디오 생성 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"비디오 생성 실패: {str(e)}")


@router.get("/file/{filename}")
async def get_video_file(filename: str):
    """생성된 비디오 파일을 스트리밍합니다."""
    video_dir = os.getenv("VIDEOS_DIR", "../data/videos")
    file_path = os.path.join(video_dir, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="비디오 파일을 찾을 수 없습니다")

    return FileResponse(
        file_path,
        media_type="video/mp4",
        filename=filename
    )


@router.get("/status/{content_id}")
async def get_video_status(content_id: str):
    """비디오 생성 상태를 확인합니다."""
    try:
        status = await video_service.get_status(content_id)
        return status
    except Exception as e:
        logger.error(f"비디오 상태 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"상태 조회 실패: {str(e)}")


@router.delete("/file/{filename}")
async def delete_video_file(filename: str):
    """비디오 파일을 삭제합니다."""
    video_dir = os.getenv("VIDEOS_DIR", "../data/videos")
    file_path = os.path.join(video_dir, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="비디오 파일을 찾을 수 없습니다")

    try:
        os.remove(file_path)
        return {"message": "비디오 파일이 삭제되었습니다", "filename": filename}
    except Exception as e:
        logger.error(f"비디오 파일 삭제 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"파일 삭제 실패: {str(e)}")
