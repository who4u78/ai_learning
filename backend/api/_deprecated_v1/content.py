from fastapi import APIRouter, HTTPException, BackgroundTasks
from models.schemas import (
    ContentGenerationRequest,
    GeneratedContent,
    ContentSourceType
)
from services.content_generator import ContentGenerator
from services.source_parser import SourceParser
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# 서비스 초기화
content_generator = ContentGenerator()
source_parser = SourceParser()


@router.post("/generate", response_model=GeneratedContent)
async def generate_content(
    request: ContentGenerationRequest,
    background_tasks: BackgroundTasks
):
    """
    소스로부터 학습 콘텐츠를 생성합니다.

    - **source_type**: url, html, text, file
    - **source_data**: 소스 데이터 (URL, HTML 문자열, 또는 텍스트)
    - **title**: 콘텐츠 제목 (선택사항)
    - **include_quiz**: 퀴즈 포함 여부
    - **include_summary**: 요약 포함 여부
    """
    try:
        logger.info(f"콘텐츠 생성 요청: {request.source_type}")

        # 1. 소스 파싱
        parsed_content = await source_parser.parse(
            source_type=request.source_type,
            source_data=request.source_data
        )

        # 2. AI로 학습 콘텐츠 생성
        generated_content = await content_generator.generate(
            source_content=parsed_content,
            title=request.title,
            language=request.language,
            include_quiz=request.include_quiz,
            include_summary=request.include_summary,
            include_examples=request.include_examples
        )

        logger.info(f"콘텐츠 생성 완료: {generated_content.id}")
        return generated_content

    except Exception as e:
        logger.error(f"콘텐츠 생성 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"콘텐츠 생성 실패: {str(e)}")


@router.get("/{content_id}", response_model=GeneratedContent)
async def get_content(content_id: str):
    """콘텐츠 ID로 생성된 콘텐츠를 조회합니다."""
    try:
        content = await content_generator.get_content(content_id)
        if not content:
            raise HTTPException(status_code=404, detail="콘텐츠를 찾을 수 없습니다")
        return content
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"콘텐츠 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"콘텐츠 조회 실패: {str(e)}")


@router.delete("/{content_id}")
async def delete_content(content_id: str):
    """생성된 콘텐츠를 삭제합니다."""
    try:
        success = await content_generator.delete_content(content_id)
        if not success:
            raise HTTPException(status_code=404, detail="콘텐츠를 찾을 수 없습니다")
        return {"message": "콘텐츠가 삭제되었습니다", "content_id": content_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"콘텐츠 삭제 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"콘텐츠 삭제 실패: {str(e)}")


@router.get("/")
async def list_contents(skip: int = 0, limit: int = 10):
    """생성된 콘텐츠 목록을 조회합니다."""
    try:
        contents = await content_generator.list_contents(skip=skip, limit=limit)
        return {
            "contents": contents,
            "total": len(contents),
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        logger.error(f"콘텐츠 목록 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"콘텐츠 목록 조회 실패: {str(e)}")
