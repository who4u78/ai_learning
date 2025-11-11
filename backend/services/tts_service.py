"""
TTS 서비스
Fish Audio API를 사용하여 한글 음성 합성
"""
import httpx
import os
import uuid
import json
from typing import Optional, List, Dict
from models.schemas import TTSResponse
import logging
import aiofiles

logger = logging.getLogger(__name__)


class TTSService:
    """Fish Audio TTS 서비스"""

    def __init__(self):
        self.api_key = os.getenv("FISH_AUDIO_API_KEY")
        if not self.api_key:
            logger.warning("FISH_AUDIO_API_KEY가 설정되지 않았습니다")

        # Fish Audio API 엔드포인트
        self.base_url = "https://api.fish.audio/v1"
        self.audio_dir = os.getenv("AUDIO_DIR", "../data/audio")

        os.makedirs(self.audio_dir, exist_ok=True)

    async def generate(
        self,
        text: str,
        voice_id: Optional[str] = None,
        speed: float = 1.0,
        format: str = "mp3"
    ) -> TTSResponse:
        """
        텍스트를 음성으로 변환

        Args:
            text: 변환할 텍스트
            voice_id: Fish Audio 보이스 ID (선택사항)
            speed: 재생 속도 (0.5 ~ 2.0)
            format: 오디오 포맷 (mp3, wav)

        Returns:
            TTSResponse: 생성된 오디오 정보
        """
        try:
            logger.info(f"TTS 생성 시작: {len(text)} 글자")

            if not self.api_key:
                # API 키가 없으면 더미 파일 생성 (개발용)
                logger.warning("Fish Audio API 키가 없어 더미 파일 생성")
                return await self._create_dummy_audio(text, format)

            # Fish Audio API 호출
            audio_data = await self._call_fish_audio_api(text, voice_id, speed, format)

            # 파일 저장
            filename = f"{uuid.uuid4()}.{format}"
            file_path = os.path.join(self.audio_dir, filename)

            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(audio_data)

            # 오디오 길이 계산 (대략적으로)
            duration = self._estimate_duration(text, speed)

            audio_url = f"/api/audio/file/{filename}"

            logger.info(f"TTS 생성 완료: {file_path}")

            return TTSResponse(
                audio_url=audio_url,
                duration=duration,
                file_path=file_path
            )

        except Exception as e:
            logger.error(f"TTS 생성 실패: {str(e)}")
            raise Exception(f"음성 생성 실패: {str(e)}")

    async def _call_fish_audio_api(
        self,
        text: str,
        voice_id: Optional[str],
        speed: float,
        format: str
    ) -> bytes:
        """Fish Audio API 호출"""

        # Fish Audio API 요청
        # 문서: https://docs.fish.audio/
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # 기본 한국어 보이스 ID (실제로는 Fish Audio에서 제공하는 ID 사용)
        if not voice_id:
            voice_id = "korean-female-default"  # 실제 Fish Audio 보이스 ID로 교체 필요

        payload = {
            "text": text,
            "reference_id": voice_id,
            "format": format,
            "speed": speed,
            "normalize": True,
            "mp3_bitrate": 128  # kbps
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            # Fish Audio의 실제 TTS 엔드포인트
            # 주의: Fish Audio의 실제 API 엔드포인트와 파라미터는 공식 문서 참조
            response = await client.post(
                f"{self.base_url}/tts",
                headers=headers,
                json=payload
            )

            response.raise_for_status()

            # 응답이 JSON인 경우 (작업 ID 반환)
            if response.headers.get("content-type") == "application/json":
                result = response.json()
                # 작업 완료를 기다리거나 오디오 URL에서 다운로드
                if "audio_url" in result:
                    audio_response = await client.get(result["audio_url"])
                    return audio_response.content
                else:
                    raise Exception("Fish Audio API 응답에 오디오 URL이 없습니다")
            else:
                # 직접 오디오 데이터 반환
                return response.content

    async def _create_dummy_audio(self, text: str, format: str) -> TTSResponse:
        """더미 오디오 파일 생성 (개발용)"""
        filename = f"{uuid.uuid4()}.{format}"
        file_path = os.path.join(self.audio_dir, filename)

        # 빈 오디오 파일 생성 (실제로는 silence 생성 가능)
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(b'')  # 빈 파일

        duration = self._estimate_duration(text, 1.0)
        audio_url = f"/api/audio/file/{filename}"

        logger.info(f"더미 오디오 생성: {file_path}")

        return TTSResponse(
            audio_url=audio_url,
            duration=duration,
            file_path=file_path
        )

    def _estimate_duration(self, text: str, speed: float) -> float:
        """음성 길이 추정 (대략적)"""
        # 한국어: 평균 3자/초 (speed=1.0 기준)
        chars_per_second = 3.0 * speed
        duration = len(text) / chars_per_second
        return round(duration, 2)

    async def generate_for_content(
        self,
        content_id: str,
        section_ids: Optional[List[str]] = None,
        voice_id: Optional[str] = None
    ) -> List[Dict]:
        """
        [DEPRECATED] v1.0 API용 메서드. v2.0에서는 사용하지 않음.

        콘텐츠의 섹션들에 대해 음성 생성

        Args:
            content_id: 콘텐츠 ID
            section_ids: 특정 섹션만 생성 (None이면 전체)
            voice_id: 보이스 ID

        Returns:
            생성된 오디오 파일 정보 리스트
        """
        logger.warning("generate_for_content()는 deprecated되었습니다. v2.0 API를 사용하세요.")
        raise NotImplementedError("이 메서드는 v2.0에서 지원하지 않습니다.")

    async def _save_audio_metadata(self, content_id: str, audio_files: List[Dict]):
        """오디오 메타데이터 저장"""
        metadata_path = os.path.join(self.audio_dir, f"{content_id}_metadata.json")

        async with aiofiles.open(metadata_path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(audio_files, ensure_ascii=False, indent=2))

    async def get_audio_metadata(self, content_id: str) -> Optional[List[Dict]]:
        """오디오 메타데이터 조회"""
        metadata_path = os.path.join(self.audio_dir, f"{content_id}_metadata.json")

        if not os.path.exists(metadata_path):
            return None

        try:
            async with aiofiles.open(metadata_path, 'r', encoding='utf-8') as f:
                content = await f.read()
                return json.loads(content)
        except Exception as e:
            logger.error(f"메타데이터 조회 실패: {str(e)}")
            return None
