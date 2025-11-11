"""
비디오 생성 서비스
ffmpeg를 사용하여 텍스트, 음성, 이미지를 결합한 학습 비디오 생성
"""
import os
import uuid
import json
import asyncio
from typing import Optional, List, Dict
from PIL import Image, ImageDraw, ImageFont
import textwrap
from models.schemas import VideoGenerationResponse
from services.content_generator import ContentGenerator
from services.tts_service import TTSService
import logging
import aiofiles

logger = logging.getLogger(__name__)


class VideoService:
    """비디오 생성 서비스"""

    def __init__(self):
        self.video_dir = os.getenv("VIDEOS_DIR", "../data/videos")
        self.temp_dir = os.path.join(self.video_dir, "temp")

        os.makedirs(self.video_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)

        self.content_generator = ContentGenerator()
        self.tts_service = TTSService()

        # 비디오 생성 상태 추적
        self.generation_status: Dict[str, Dict] = {}

    async def generate(
        self,
        content_id: str,
        section_ids: Optional[List[str]] = None,
        include_subtitles: bool = True,
        resolution: str = "1280x720",
        fps: int = 30
    ) -> VideoGenerationResponse:
        """
        콘텐츠로부터 학습 비디오 생성

        Args:
            content_id: 콘텐츠 ID
            section_ids: 포함할 섹션 ID 목록
            include_subtitles: 자막 포함 여부
            resolution: 비디오 해상도
            fps: 초당 프레임 수

        Returns:
            VideoGenerationResponse: 생성된 비디오 정보
        """
        try:
            logger.info(f"비디오 생성 시작: {content_id}")

            # 상태 초기화
            self.generation_status[content_id] = {
                "status": "processing",
                "progress": 0,
                "message": "비디오 생성 중..."
            }

            # 1. 콘텐츠 조회
            content = await self.content_generator.get_content(content_id)
            if not content:
                raise Exception("콘텐츠를 찾을 수 없습니다")

            # 2. 섹션 필터링
            sections = content.sections
            if section_ids:
                sections = [s for s in sections if s.id in section_ids]

            if not sections:
                raise Exception("생성할 섹션이 없습니다")

            # 3. 각 섹션별로 오디오 생성 또는 조회
            self.generation_status[content_id]["progress"] = 10
            self.generation_status[content_id]["message"] = "음성 생성 중..."

            audio_metadata = await self.tts_service.get_audio_metadata(content_id)
            if not audio_metadata:
                audio_files = await self.tts_service.generate_for_content(
                    content_id=content_id,
                    section_ids=section_ids
                )
            else:
                audio_files = audio_metadata

            # 4. 각 섹션별로 이미지 생성
            self.generation_status[content_id]["progress"] = 40
            self.generation_status[content_id]["message"] = "이미지 생성 중..."

            width, height = map(int, resolution.split('x'))
            section_videos = []

            for idx, section in enumerate(sections):
                section_audio = next((a for a in audio_files if a["section_id"] == section.id), None)

                if not section_audio:
                    logger.warning(f"섹션 {section.id}의 오디오를 찾을 수 없습니다. 건너뜁니다.")
                    continue

                # 섹션 이미지 생성
                image_path = await self._create_section_image(
                    section=section,
                    width=width,
                    height=height
                )

                # 섹션 비디오 생성 (이미지 + 오디오)
                section_video_path = await self._create_section_video(
                    image_path=image_path,
                    audio_path=section_audio["file_path"],
                    duration=section_audio["duration"],
                    output_name=f"{content_id}_section_{idx}.mp4",
                    include_subtitles=include_subtitles,
                    subtitle_text=section.content if include_subtitles else None
                )

                section_videos.append(section_video_path)

                progress = 40 + int((idx + 1) / len(sections) * 40)
                self.generation_status[content_id]["progress"] = progress

            # 5. 모든 섹션 비디오를 하나로 결합
            self.generation_status[content_id]["progress"] = 80
            self.generation_status[content_id]["message"] = "비디오 결합 중..."

            final_video_path = await self._concatenate_videos(
                video_paths=section_videos,
                output_name=f"{content_id}_final.mp4"
            )

            # 6. 파일 크기 및 길이 계산
            file_size_mb = os.path.getsize(final_video_path) / (1024 * 1024)
            total_duration = sum(a["duration"] for a in audio_files if any(s.id == a["section_id"] for s in sections))

            video_url = f"/api/video/file/{os.path.basename(final_video_path)}"

            # 7. 임시 파일 정리
            await self._cleanup_temp_files(section_videos)

            self.generation_status[content_id]["status"] = "completed"
            self.generation_status[content_id]["progress"] = 100
            self.generation_status[content_id]["message"] = "비디오 생성 완료"

            logger.info(f"비디오 생성 완료: {final_video_path}")

            return VideoGenerationResponse(
                video_url=video_url,
                file_path=final_video_path,
                duration=total_duration,
                size_mb=round(file_size_mb, 2)
            )

        except Exception as e:
            self.generation_status[content_id] = {
                "status": "failed",
                "progress": 0,
                "message": f"비디오 생성 실패: {str(e)}"
            }
            logger.error(f"비디오 생성 실패: {str(e)}")
            raise

    async def _create_section_image(self, section, width: int, height: int) -> str:
        """섹션 이미지 생성"""
        # 배경 이미지 생성
        img = Image.new('RGB', (width, height), color=(20, 30, 48))  # 다크 블루
        draw = ImageDraw.Draw(img)

        # 폰트 설정 (시스템 폰트 사용)
        try:
            # 리눅스/맥 한글 폰트
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf", 60)
            content_font = ImageFont.truetype("/usr/share/fonts/truetype/nanum/NanumGothic.ttf", 32)
        except:
            # 폰트가 없으면 기본 폰트 사용
            logger.warning("한글 폰트를 찾을 수 없어 기본 폰트 사용")
            title_font = ImageFont.load_default()
            content_font = ImageFont.load_default()

        # 제목 그리기
        title_lines = textwrap.wrap(section.title, width=20)
        y_offset = 100

        for line in title_lines[:2]:  # 최대 2줄
            draw.text((width // 2, y_offset), line, font=title_font, fill=(255, 255, 255), anchor="mm")
            y_offset += 80

        # 내용 그리기 (요약)
        y_offset += 50
        content_lines = textwrap.wrap(section.content[:300], width=40)

        for line in content_lines[:8]:  # 최대 8줄
            draw.text((width // 2, y_offset), line, font=content_font, fill=(200, 200, 200), anchor="mm")
            y_offset += 50

        # 이미지 저장
        image_filename = f"{uuid.uuid4()}.png"
        image_path = os.path.join(self.temp_dir, image_filename)
        img.save(image_path)

        logger.info(f"섹션 이미지 생성: {image_path}")
        return image_path

    async def _create_section_video(
        self,
        image_path: str,
        audio_path: str,
        duration: float,
        output_name: str,
        include_subtitles: bool = False,
        subtitle_text: str = None
    ) -> str:
        """섹션 비디오 생성 (이미지 + 오디오)"""
        output_path = os.path.join(self.temp_dir, output_name)

        # ffmpeg 명령어 구성
        # 이미지를 오디오 길이만큼 반복하여 비디오 생성
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", image_path,
            "-i", audio_path,
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            "-t", str(duration),
            output_path
        ]

        # ffmpeg 실행
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            error_msg = stderr.decode('utf-8')
            logger.error(f"ffmpeg 실패: {error_msg}")
            raise Exception(f"비디오 생성 실패: {error_msg}")

        logger.info(f"섹션 비디오 생성: {output_path}")
        return output_path

    async def _concatenate_videos(self, video_paths: List[str], output_name: str) -> str:
        """여러 비디오를 하나로 결합"""
        output_path = os.path.join(self.video_dir, output_name)

        # concat 파일 생성
        concat_file = os.path.join(self.temp_dir, f"{uuid.uuid4()}_concat.txt")
        async with aiofiles.open(concat_file, 'w') as f:
            for video_path in video_paths:
                await f.write(f"file '{video_path}'\n")

        # ffmpeg concat
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_file,
            "-c", "copy",
            output_path
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            error_msg = stderr.decode('utf-8')
            logger.error(f"비디오 결합 실패: {error_msg}")
            raise Exception(f"비디오 결합 실패: {error_msg}")

        # concat 파일 삭제
        os.remove(concat_file)

        logger.info(f"비디오 결합 완료: {output_path}")
        return output_path

    async def _cleanup_temp_files(self, file_paths: List[str]):
        """임시 파일 정리"""
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                logger.warning(f"임시 파일 삭제 실패: {file_path} - {str(e)}")

    async def get_status(self, content_id: str) -> Dict:
        """비디오 생성 상태 조회"""
        return self.generation_status.get(content_id, {
            "status": "not_found",
            "progress": 0,
            "message": "비디오 생성 작업을 찾을 수 없습니다"
        })
