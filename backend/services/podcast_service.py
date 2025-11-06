"""
팟캐스트 오디오 생성 서비스
2인 대화 형식의 팟캐스트를 Fish Audio TTS로 생성
"""
import httpx
import os
import uuid
from typing import Optional
from models.schemas import Podcast, TTSResponse
from pydub import AudioSegment
import logging
import aiofiles

logger = logging.getLogger(__name__)


class PodcastService:
    """팟캐스트 생성 서비스"""

    def __init__(self):
        self.api_key = os.getenv("FISH_AUDIO_API_KEY")
        self.base_url = "https://api.fish.audio/v1"
        self.audio_dir = os.getenv("AUDIO_DIR", "../data/audio")

        os.makedirs(self.audio_dir, exist_ok=True)

        # 기본 보이스 ID (실제로는 Fish Audio에서 제공하는 한국어 보이스 사용)
        self.host_voice_id = os.getenv("FISH_AUDIO_HOST_VOICE", "korean-male-1")
        self.guest_voice_id = os.getenv("FISH_AUDIO_GUEST_VOICE", "korean-female-1")

    async def generate_podcast_audio(self, podcast: Podcast) -> TTSResponse:
        """
        팟캐스트 오디오 생성

        Args:
            podcast: 팟캐스트 객체 (스크립트 포함)

        Returns:
            TTSResponse: 생성된 오디오 정보
        """
        try:
            logger.info(f"팟캐스트 오디오 생성 시작: {podcast.script.title}")

            audio_segments = []
            total_duration = 0.0

            # 각 대화를 개별적으로 TTS 생성
            for i, dialogue in enumerate(podcast.script.dialogues):
                logger.info(f"대화 {i+1}/{len(podcast.script.dialogues)} 생성 중...")

                # 화자에 따라 다른 보이스 사용
                voice_id = self.host_voice_id if dialogue.speaker == "host" else self.guest_voice_id

                # TTS 생성
                audio_data = await self._generate_single_tts(dialogue.text, voice_id)

                # 임시 파일로 저장
                temp_file = os.path.join(self.audio_dir, f"temp_{uuid.uuid4()}.mp3")
                async with aiofiles.open(temp_file, 'wb') as f:
                    await f.write(audio_data)

                # 오디오 세그먼트 로드
                segment = AudioSegment.from_mp3(temp_file)
                audio_segments.append(segment)

                # 짧은 정적(0.5초) 추가 (대화 사이 간격)
                silence = AudioSegment.silent(duration=500)
                audio_segments.append(silence)

                total_duration += len(segment) / 1000.0  # ms to seconds

                # 임시 파일 삭제
                os.remove(temp_file)

            # 모든 세그먼트 결합
            combined = sum(audio_segments)

            # 최종 파일 저장
            filename = f"{podcast.id}.mp3"
            file_path = os.path.join(self.audio_dir, filename)
            combined.export(file_path, format="mp3", bitrate="128k")

            audio_url = f"/api/audio/file/{filename}"

            logger.info(f"팟캐스트 오디오 생성 완료: {file_path}, {total_duration:.1f}초")

            return TTSResponse(
                audio_url=audio_url,
                duration=total_duration,
                file_path=file_path
            )

        except Exception as e:
            logger.error(f"팟캐스트 오디오 생성 실패: {str(e)}")
            raise Exception(f"팟캐스트 오디오 생성 실패: {str(e)}")

    async def _generate_single_tts(self, text: str, voice_id: str) -> bytes:
        """단일 TTS 생성"""

        if not self.api_key:
            logger.warning("Fish Audio API 키 없음, 더미 데이터 반환")
            # 짧은 무음 반환 (개발용)
            silence = AudioSegment.silent(duration=len(text) * 50)  # 대략적인 시간
            temp_file = f"/tmp/{uuid.uuid4()}.mp3"
            silence.export(temp_file, format="mp3")
            with open(temp_file, 'rb') as f:
                data = f.read()
            os.remove(temp_file)
            return data

        # Fish Audio API 호출
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "text": text,
            "reference_id": voice_id,
            "format": "mp3",
            "speed": 1.0,
            "normalize": True,
            "mp3_bitrate": 128
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                # Fish Audio의 실제 TTS 엔드포인트
                # 주의: 실제 API 문서에 따라 조정 필요
                response = await client.post(
                    f"{self.base_url}/tts",
                    headers=headers,
                    json=payload
                )

                response.raise_for_status()

                # 응답 타입에 따라 처리
                if response.headers.get("content-type") == "application/json":
                    result = response.json()
                    if "audio_url" in result:
                        # URL에서 오디오 다운로드
                        audio_response = await client.get(result["audio_url"])
                        return audio_response.content
                    else:
                        raise Exception("Fish Audio API 응답에 오디오 URL이 없습니다")
                else:
                    # 직접 오디오 데이터
                    return response.content

            except httpx.HTTPStatusError as e:
                logger.error(f"Fish Audio API 오류: {e}")
                raise Exception(f"TTS API 오류: {e.response.status_code}")
