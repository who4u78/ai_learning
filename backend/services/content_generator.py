"""
AI 콘텐츠 생성 서비스
Anthropic Claude API를 사용하여 학습 콘텐츠 생성
"""
import anthropic
import os
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from models.schemas import GeneratedContent, LearningSection, Quiz
import logging
import aiofiles

logger = logging.getLogger(__name__)


class ContentGenerator:
    """AI 콘텐츠 생성기"""

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY가 설정되지 않았습니다")

        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = os.getenv("AI_MODEL", "claude-3-5-sonnet-20241022")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "4096"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.content_dir = os.getenv("CONTENT_DIR", "../data/content")

        os.makedirs(self.content_dir, exist_ok=True)

    async def generate(
        self,
        source_content: Dict[str, Any],
        title: Optional[str] = None,
        language: str = "ko",
        include_quiz: bool = True,
        include_summary: bool = True,
        include_examples: bool = True
    ) -> GeneratedContent:
        """
        소스 콘텐츠로부터 학습 자료 생성

        Args:
            source_content: 파싱된 소스 콘텐츠
            title: 콘텐츠 제목 (선택사항)
            language: 출력 언어 (기본: 한글)
            include_quiz: 퀴즈 포함 여부
            include_summary: 요약 포함 여부
            include_examples: 예시 포함 여부

        Returns:
            생성된 학습 콘텐츠
        """
        try:
            logger.info(f"AI 콘텐츠 생성 시작: {source_content.get('title')}")

            # 프롬프트 구성
            prompt = self._build_prompt(
                source_content,
                language,
                include_quiz,
                include_summary,
                include_examples
            )

            # Claude API 호출
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # 응답 파싱
            content_text = response.content[0].text
            generated_data = self._parse_ai_response(content_text)

            # GeneratedContent 객체 생성
            content_id = str(uuid.uuid4())
            generated_content = GeneratedContent(
                id=content_id,
                title=title or generated_data.get("title", source_content.get("title", "제목 없음")),
                summary=generated_data.get("summary", ""),
                sections=generated_data.get("sections", []),
                quizzes=generated_data.get("quizzes") if include_quiz else None,
                created_at=datetime.now(),
                metadata={
                    "source_url": source_content.get("url"),
                    "source_word_count": source_content.get("word_count"),
                    "language": language,
                    "model": self.model
                }
            )

            # 파일로 저장
            await self._save_content(content_id, generated_content)

            logger.info(f"AI 콘텐츠 생성 완료: {content_id}")
            return generated_content

        except Exception as e:
            logger.error(f"AI 콘텐츠 생성 실패: {str(e)}")
            raise Exception(f"콘텐츠 생성 실패: {str(e)}")

    def _build_prompt(
        self,
        source_content: Dict[str, Any],
        language: str,
        include_quiz: bool,
        include_summary: bool,
        include_examples: bool
    ) -> str:
        """AI 프롬프트 구성"""

        source_text = source_content.get("text_content", "")
        source_title = source_content.get("title", "")

        prompt = f"""다음 콘텐츠를 분석하여 효과적인 학습 자료를 한글로 만들어주세요.

# 원본 콘텐츠
제목: {source_title}
내용:
{source_text[:10000]}  # 토큰 제한을 위해 일부만 사용

# 요구사항
1. 학습자가 이해하기 쉽도록 한글로 작성
2. 핵심 개념을 명확하게 설명
3. 논리적인 순서로 섹션 구성
4. 각 섹션은 5-10분 안에 학습 가능한 분량
{"5. 실제 예시와 사례 포함" if include_examples else ""}

# 출력 형식 (반드시 JSON으로 응답)
{{
  "title": "학습 자료 제목",
  {"\"summary\": \"전체 내용 요약 (3-5문장)\"," if include_summary else ""}
  "sections": [
    {{
      "id": "section-1",
      "title": "섹션 제목",
      "content": "섹션 내용 (한글, 마크다운 형식)",
      "order": 1,
      "estimated_time": 7  // 예상 학습 시간(분)
    }}
  ]
  {"," + '''
  "quizzes": [
    {
      "question": "퀴즈 질문",
      "options": ["선택지1", "선택지2", "선택지3", "선택지4"],
      "correct_answer": 0,  // 정답 인덱스 (0-3)
      "explanation": "정답 해설"
    }
  ]
  ''' if include_quiz else ""}
}}

반드시 유효한 JSON 형식으로 응답해주세요. 마크다운 코드 블록 없이 순수 JSON만 반환하세요."""

        return prompt

    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """AI 응답 파싱"""
        try:
            # JSON 추출 (마크다운 코드 블록 제거)
            response_text = response_text.strip()

            # ```json ... ``` 형식 제거
            if response_text.startswith("```"):
                lines = response_text.split("\n")
                response_text = "\n".join(lines[1:-1])

            # JSON 파싱
            data = json.loads(response_text)

            # LearningSection 객체로 변환
            sections = []
            for idx, section_data in enumerate(data.get("sections", [])):
                section = LearningSection(
                    id=section_data.get("id", f"section-{idx+1}"),
                    title=section_data.get("title", f"섹션 {idx+1}"),
                    content=section_data.get("content", ""),
                    order=section_data.get("order", idx + 1),
                    estimated_time=section_data.get("estimated_time")
                )
                sections.append(section)

            # Quiz 객체로 변환
            quizzes = []
            if "quizzes" in data:
                for quiz_data in data["quizzes"]:
                    quiz = Quiz(
                        question=quiz_data.get("question", ""),
                        options=quiz_data.get("options", []),
                        correct_answer=quiz_data.get("correct_answer", 0),
                        explanation=quiz_data.get("explanation", "")
                    )
                    quizzes.append(quiz)

            return {
                "title": data.get("title", "제목 없음"),
                "summary": data.get("summary", ""),
                "sections": sections,
                "quizzes": quizzes if quizzes else None
            }

        except json.JSONDecodeError as e:
            logger.error(f"JSON 파싱 실패: {str(e)}")
            logger.error(f"응답 텍스트: {response_text[:500]}")

            # 폴백: 간단한 섹션 생성
            return {
                "title": "생성된 콘텐츠",
                "summary": response_text[:200],
                "sections": [
                    LearningSection(
                        id="section-1",
                        title="학습 내용",
                        content=response_text,
                        order=1
                    )
                ],
                "quizzes": None
            }

    async def _save_content(self, content_id: str, content: GeneratedContent):
        """콘텐츠를 파일로 저장"""
        file_path = os.path.join(self.content_dir, f"{content_id}.json")

        # Pydantic 모델을 dict로 변환
        content_dict = content.model_dump(mode='json')

        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(content_dict, ensure_ascii=False, indent=2))

        logger.info(f"콘텐츠 저장 완료: {file_path}")

    async def get_content(self, content_id: str) -> Optional[GeneratedContent]:
        """저장된 콘텐츠 조회"""
        file_path = os.path.join(self.content_dir, f"{content_id}.json")

        if not os.path.exists(file_path):
            return None

        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content_str = await f.read()
                content_dict = json.loads(content_str)
                return GeneratedContent(**content_dict)
        except Exception as e:
            logger.error(f"콘텐츠 조회 실패: {str(e)}")
            return None

    async def delete_content(self, content_id: str) -> bool:
        """콘텐츠 삭제"""
        file_path = os.path.join(self.content_dir, f"{content_id}.json")

        if not os.path.exists(file_path):
            return False

        try:
            os.remove(file_path)
            return True
        except Exception as e:
            logger.error(f"콘텐츠 삭제 실패: {str(e)}")
            return False

    async def list_contents(self, skip: int = 0, limit: int = 10) -> List[GeneratedContent]:
        """콘텐츠 목록 조회"""
        contents = []

        try:
            files = sorted(
                [f for f in os.listdir(self.content_dir) if f.endswith('.json')],
                key=lambda x: os.path.getmtime(os.path.join(self.content_dir, x)),
                reverse=True
            )

            for filename in files[skip:skip + limit]:
                content_id = filename.replace('.json', '')
                content = await self.get_content(content_id)
                if content:
                    contents.append(content)

        except Exception as e:
            logger.error(f"콘텐츠 목록 조회 실패: {str(e)}")

        return contents
