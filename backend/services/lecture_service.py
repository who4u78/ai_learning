"""
강의 비디오 생성 서비스
슬라이드 이미지 + 나레이션으로 강의 비디오 생성
"""
import os
import uuid
import asyncio
from typing import List
from PIL import Image, ImageDraw, ImageFont
import textwrap
from models.schemas import VideoLecture, LectureSlide, TTSResponse, VideoGenerationResponse
from services.tts_service import TTSService
import logging
import aiofiles

logger = logging.getLogger(__name__)


class LectureService:
    """강의 비디오 생성 서비스"""

    def __init__(self):
        self.video_dir = os.getenv("VIDEOS_DIR", "../data/videos")
        self.temp_dir = os.path.join(self.video_dir, "temp")
        self.slides_dir = os.path.join(self.video_dir, "slides")

        for dir_path in [self.video_dir, self.temp_dir, self.slides_dir]:
            os.makedirs(dir_path, exist_ok=True)

        self.tts_service = TTSService()

        # 슬라이드 설정
        self.width = 1280
        self.height = 720
        self.bg_color = (15, 23, 42)  # 다크 블루
        self.text_color = (255, 255, 255)
        self.accent_color = (59, 130, 246)  # 블루

    async def generate_lecture_video(self, video_lecture: VideoLecture) -> VideoGenerationResponse:
        """
        강의 비디오 생성

        Args:
            video_lecture: 강의 객체 (슬라이드 포함)

        Returns:
            VideoGenerationResponse: 생성된 비디오 정보
        """
        try:
            logger.info(f"강의 비디오 생성 시작: {video_lecture.title}")

            slide_videos = []
            total_duration = 0.0

            # 각 슬라이드별로 처리
            for i, slide in enumerate(video_lecture.slides):
                logger.info(f"슬라이드 {i+1}/{len(video_lecture.slides)} 처리 중...")

                # 1. 슬라이드 이미지 생성
                image_path = await self._create_slide_image(slide)

                # 2. 나레이션 음성 생성
                audio_response = await self.tts_service.generate(
                    text=slide.narration,
                    format="mp3"
                )

                # 슬라이드 지속 시간 = 나레이션 길이
                slide.duration = audio_response.duration

                # 3. 슬라이드 비디오 생성 (이미지 + 오디오)
                slide_video_path = await self._create_slide_video(
                    image_path=image_path,
                    audio_path=audio_response.file_path,
                    duration=audio_response.duration,
                    output_name=f"{video_lecture.id}_slide_{i+1}.mp4"
                )

                slide_videos.append(slide_video_path)
                total_duration += audio_response.duration

            # 4. 모든 슬라이드 비디오 결합
            final_video_path = await self._concatenate_videos(
                video_paths=slide_videos,
                output_name=f"{video_lecture.id}_final.mp4"
            )

            # 5. 파일 크기 계산
            file_size_mb = os.path.getsize(final_video_path) / (1024 * 1024)

            video_url = f"/api/video/file/{os.path.basename(final_video_path)}"

            # 6. 임시 파일 정리
            await self._cleanup_temp_files(slide_videos)

            logger.info(f"강의 비디오 생성 완료: {final_video_path}, {total_duration:.1f}초")

            return VideoGenerationResponse(
                video_url=video_url,
                file_path=final_video_path,
                duration=total_duration,
                size_mb=round(file_size_mb, 2)
            )

        except Exception as e:
            logger.error(f"강의 비디오 생성 실패: {str(e)}")
            raise Exception(f"강의 비디오 생성 실패: {str(e)}")

    async def _create_slide_image(self, slide: LectureSlide) -> str:
        """슬라이드 이미지 생성"""
        # 배경 이미지
        img = Image.new('RGB', (self.width, self.height), color=self.bg_color)
        draw = ImageDraw.Draw(img)

        try:
            # 한글 폰트 로드
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf", 64)
            content_font = ImageFont.truetype("/usr/share/fonts/truetype/nanum/NanumGothic.ttf", 36)
            number_font = ImageFont.truetype("/usr/share/fonts/truetype/nanum/NanumGothic.ttf", 24)
        except:
            logger.warning("한글 폰트 로드 실패, 기본 폰트 사용")
            title_font = ImageFont.load_default()
            content_font = ImageFont.load_default()
            number_font = ImageFont.load_default()

        # 상단 바
        draw.rectangle([(0, 0), (self.width, 10)], fill=self.accent_color)

        # 슬라이드 번호
        draw.text(
            (self.width - 50, 30),
            f"{slide.slide_number}",
            font=number_font,
            fill=(150, 150, 150),
            anchor="rm"
        )

        # 제목
        title_y = 120
        title_lines = textwrap.wrap(slide.title, width=20)
        for line in title_lines[:2]:
            draw.text(
                (self.width // 2, title_y),
                line,
                font=title_font,
                fill=self.text_color,
                anchor="mm"
            )
            title_y += 80

        # 구분선
        draw.line([(100, title_y + 30), (self.width - 100, title_y + 30)], fill=self.accent_color, width=3)

        # 내용 (불릿 포인트)
        content_y = title_y + 80
        for item in slide.content[:5]:  # 최대 5개
            # 불릿
            draw.ellipse([(140, content_y + 10), (155, content_y + 25)], fill=self.accent_color)

            # 텍스트
            item_lines = textwrap.wrap(item, width=40)
            for item_line in item_lines[:3]:  # 항목당 최대 3줄
                draw.text(
                    (180, content_y),
                    item_line,
                    font=content_font,
                    fill=self.text_color
                )
                content_y += 45

            content_y += 20  # 항목 간 간격

        # 이미지 저장
        image_filename = f"{uuid.uuid4()}.png"
        image_path = os.path.join(self.slides_dir, image_filename)
        img.save(image_path)

        slide.image_path = image_path
        logger.info(f"슬라이드 이미지 생성: {image_path}")

        return image_path

    async def _create_slide_video(
        self,
        image_path: str,
        audio_path: str,
        duration: float,
        output_name: str
    ) -> str:
        """슬라이드 비디오 생성 (이미지 + 오디오)"""
        output_path = os.path.join(self.temp_dir, output_name)

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

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            error_msg = stderr.decode('utf-8')
            logger.error(f"ffmpeg 실패: {error_msg}")
            raise Exception(f"슬라이드 비디오 생성 실패")

        return output_path

    async def _concatenate_videos(self, video_paths: List[str], output_name: str) -> str:
        """비디오 결합"""
        output_path = os.path.join(self.video_dir, output_name)

        # concat 파일 생성
        concat_file = os.path.join(self.temp_dir, f"{uuid.uuid4()}_concat.txt")
        async with aiofiles.open(concat_file, 'w') as f:
            for video_path in video_paths:
                await f.write(f"file '{video_path}'\n")

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
            raise Exception(f"비디오 결합 실패")

        os.remove(concat_file)
        return output_path

    async def _cleanup_temp_files(self, file_paths: List[str]):
        """임시 파일 정리"""
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                logger.warning(f"임시 파일 삭제 실패: {file_path}")
