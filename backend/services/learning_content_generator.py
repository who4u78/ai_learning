"""
통합 학습 콘텐츠 생성 서비스
- 팟캐스트 스크립트
- 강의 슬라이드
- 읽기 자료
- 다양한 퀴즈
모두를 한 번의 Claude API 호출로 생성 (비용 최적화)
"""
import anthropic
import os
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
from models.schemas import (
    LearningContent,
    Podcast,
    PodcastScript,
    PodcastDialogue,
    VideoLecture,
    LectureSlide,
    ReadingMaterial,
    DeepThinkingQuestion,
    MultipleChoiceQuiz,
    ShortAnswerQuiz,
    EssayQuiz
)
import logging
import aiofiles

logger = logging.getLogger(__name__)


class LearningContentGenerator:
    """통합 학습 콘텐츠 생성기"""

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY가 설정되지 않았습니다")

        self.client = anthropic.Anthropic(api_key=api_key)
        # Claude 3 Opus 사용 (가장 안정적이고 호환성 좋음)
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
        self.content_dir = os.getenv("CONTENT_DIR", "../data/content")

        os.makedirs(self.content_dir, exist_ok=True)

    async def generate_all(
        self,
        source_content: Dict[str, Any],
        title: Optional[str] = None
    ) -> LearningContent:
        """
        소스로부터 모든 학습 자료 생성

        Args:
            source_content: 파싱된 소스 콘텐츠
            title: 콘텐츠 제목

        Returns:
            LearningContent: 완전한 학습 콘텐츠
        """
        try:
            logger.info(f"통합 학습 콘텐츠 생성 시작: {source_content.get('title')}")

            # 프롬프트 구성 (모든 자료를 한 번에 요청)
            prompt = self._build_comprehensive_prompt(source_content)

            # Claude API 호출 (단 1회로 모든 것 생성)
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,  # Claude 3 Opus 최대값
                temperature=0.7,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # 응답 파싱
            content_text = response.content[0].text
            parsed_data = self._parse_comprehensive_response(content_text)

            # LearningContent 객체 생성
            content_id = str(uuid.uuid4())
            now = datetime.now()

            learning_content = LearningContent(
                id=content_id,
                title=title or parsed_data.get("title", source_content.get("title")),
                description=parsed_data.get("description", ""),

                # 팟캐스트
                podcast=self._create_podcast(content_id, parsed_data.get("podcast"), now),

                # 강의 비디오
                video_lecture=self._create_video_lecture(content_id, parsed_data.get("video_lecture"), now),

                # 읽기 자료
                reading_material=self._create_reading_material(content_id, parsed_data.get("reading_material"), now),

                # 심화 질문
                deep_questions=self._create_deep_questions(parsed_data.get("deep_questions", [])),

                # 퀴즈들
                multiple_choice_quizzes=self._create_mc_quizzes(parsed_data.get("multiple_choice_quizzes", [])),
                short_answer_quizzes=self._create_sa_quizzes(parsed_data.get("short_answer_quizzes", [])),
                essay_quizzes=self._create_essay_quizzes(parsed_data.get("essay_quizzes", [])),

                source_url=source_content.get("url"),
                source_text=source_content.get("text_content", "")[:1000],  # 처음 1000자만 저장

                created_at=now,
                updated_at=now,
                metadata={
                    "source_word_count": source_content.get("word_count"),
                    "model": self.model
                }
            )

            # 저장
            await self._save_content(content_id, learning_content)

            logger.info(f"통합 학습 콘텐츠 생성 완료: {content_id}")
            return learning_content

        except Exception as e:
            logger.error(f"학습 콘텐츠 생성 실패: {str(e)}")
            raise Exception(f"콘텐츠 생성 실패: {str(e)}")

    def _build_comprehensive_prompt(self, source_content: Dict[str, Any]) -> str:
        """통합 프롬프트 구성"""
        source_text = source_content.get("text_content", "")[:15000]  # 토큰 제한
        source_title = source_content.get("title", "")

        prompt = f"""다음 콘텐츠를 분석하여 완전한 한글 학습 자료를 생성해주세요.

# 원본 콘텐츠
제목: {source_title}
내용:
{source_text}

# 요구사항 (간결하게 작성해주세요)

## 1. 팟캐스트 스크립트 (7-8분, 2인 대화)
- 진행자(host)와 게스트(guest)의 대화 **6-8개**
- 핵심 개념을 쉽게 설명

## 2. 강의 슬라이드 (**5-6장**)
- 각 슬라이드: 제목, 내용(불릿 3개), 나레이션(2-3문장)
- 간결하게 작성

## 3. 읽기 자료 (마크다운, **1500-2000자**)
- 핵심 내용만 간결하게

## 4. 심화 질문 (**2개**)
- 비판적 사고를 요구하는 질문

## 5. 4지선다형 퀴즈 (**5문제**)
- 난이도 다양화

## 6. 단답형 퀴즈 (**3문제**)
- 핵심 개념 확인

## 7. 서술형 문제 (**1개**)
- 종합적 이해 확인

# 출력 형식 (반드시 JSON으로 응답)
{{
  "title": "학습 자료 제목",
  "description": "학습 자료 설명 (2-3문장)",

  "podcast": {{
    "title": "팟캐스트 제목",
    "host_name": "진행자",
    "guest_name": "게스트",
    "dialogues": [
      {{"speaker": "host", "text": "안녕하세요! 오늘은..."}},
      {{"speaker": "guest", "text": "네, 반갑습니다..."}}
    ],
    "duration_minutes": 10
  }},

  "video_lecture": {{
    "title": "강의 제목",
    "slides": [
      {{
        "slide_number": 1,
        "title": "슬라이드 제목",
        "content": ["요점 1", "요점 2", "요점 3"],
        "narration": "이 슬라이드에서는..."
      }}
    ]
  }},

  "reading_material": {{
    "title": "읽기 자료 제목",
    "content": "마크다운 형식의 내용",
    "estimated_reading_time": 10
  }},

  "deep_questions": [
    {{
      "question": "질문 내용",
      "context": "질문의 맥락",
      "hints": ["힌트 1", "힌트 2"]
    }}
  ],

  "multiple_choice_quizzes": [
    {{
      "question": "문제",
      "options": ["선택지1", "선택지2", "선택지3", "선택지4"],
      "correct_answer": 0,
      "explanation": "해설",
      "difficulty": "easy"
    }}
  ],

  "short_answer_quizzes": [
    {{
      "question": "문제",
      "correct_answers": ["정답1", "정답2"],
      "explanation": "해설",
      "case_sensitive": false
    }}
  ],

  "essay_quizzes": [
    {{
      "question": "문제",
      "suggested_answer": "예시 답안",
      "grading_criteria": ["기준1", "기준2"],
      "min_words": 100
    }}
  ]
}}

**CRITICAL - 반드시 지켜주세요:**
- **모든 7가지 항목을 빠짐없이 생성** (podcast, video_lecture, reading_material, deep_questions, quizzes 전부)
- **간결하게 작성** - 지정된 개수/분량만 작성 (더 길게 쓰지 마세요)
- 모든 내용 한글로 작성
- JSON 형식 엄수 (순수 JSON만, 마크다운 코드 블록 없이)
- 응답이 잘리지 않도록 **모든 항목을 끝까지 완성**해주세요
"""

        return prompt

    def _parse_comprehensive_response(self, response_text: str) -> Dict[str, Any]:
        """통합 응답 파싱"""
        try:
            # JSON 추출
            response_text = response_text.strip()
            if response_text.startswith("```"):
                lines = response_text.split("\n")
                response_text = "\n".join(lines[1:-1])

            data = json.loads(response_text)
            return data

        except json.JSONDecodeError as e:
            logger.error(f"JSON 파싱 실패: {str(e)}")
            logger.error(f"응답: {response_text[:500]}")

            # 폴백: 기본 구조 반환
            return {
                "title": "생성된 학습 자료",
                "description": "콘텐츠가 생성되었습니다",
                "podcast": None,
                "video_lecture": None,
                "reading_material": {"title": "읽기 자료", "content": response_text, "estimated_reading_time": 10},
                "deep_questions": [],
                "multiple_choice_quizzes": [],
                "short_answer_quizzes": [],
                "essay_quizzes": []
            }

    def _create_podcast(self, content_id: str, data: Optional[Dict], created_at: datetime) -> Optional[Podcast]:
        """팟캐스트 객체 생성"""
        if not data:
            return None

        try:
            dialogues = [
                PodcastDialogue(
                    speaker=d.get("speaker", "host"),
                    text=d.get("text", "")
                )
                for d in data.get("dialogues", [])
            ]

            script = PodcastScript(
                title=data.get("title", "팟캐스트"),
                host_name=data.get("host_name", "진행자"),
                guest_name=data.get("guest_name", "게스트"),
                dialogues=dialogues,
                duration_minutes=data.get("duration_minutes", 10)
            )

            return Podcast(
                id=f"{content_id}_podcast",
                script=script,
                created_at=created_at
            )
        except Exception as e:
            logger.error(f"팟캐스트 생성 실패: {e}")
            return None

    def _create_video_lecture(self, content_id: str, data: Optional[Dict], created_at: datetime) -> Optional[VideoLecture]:
        """강의 비디오 객체 생성"""
        if not data:
            return None

        try:
            slides = [
                LectureSlide(
                    slide_number=s.get("slide_number", i+1),
                    title=s.get("title", f"슬라이드 {i+1}"),
                    content=s.get("content", []),
                    narration=s.get("narration", "")
                )
                for i, s in enumerate(data.get("slides", []))
            ]

            return VideoLecture(
                id=f"{content_id}_lecture",
                title=data.get("title", "강의"),
                slides=slides,
                created_at=created_at
            )
        except Exception as e:
            logger.error(f"강의 비디오 생성 실패: {e}")
            return None

    def _create_reading_material(self, content_id: str, data: Optional[Dict], created_at: datetime) -> Optional[ReadingMaterial]:
        """읽기 자료 객체 생성"""
        if not data:
            return None

        try:
            return ReadingMaterial(
                id=f"{content_id}_reading",
                title=data.get("title", "읽기 자료"),
                content=data.get("content", ""),
                estimated_reading_time=data.get("estimated_reading_time", 10),
                created_at=created_at
            )
        except Exception as e:
            logger.error(f"읽기 자료 생성 실패: {e}")
            return None

    def _create_deep_questions(self, data: List[Dict]) -> List[DeepThinkingQuestion]:
        """심화 질문 생성"""
        questions = []
        for q in data[:3]:  # 최대 3개
            try:
                questions.append(DeepThinkingQuestion(
                    question=q.get("question", ""),
                    context=q.get("context"),
                    hints=q.get("hints")
                ))
            except Exception as e:
                logger.error(f"심화 질문 생성 실패: {e}")
        return questions

    def _create_mc_quizzes(self, data: List[Dict]) -> List[MultipleChoiceQuiz]:
        """4지선다 퀴즈 생성"""
        quizzes = []
        for q in data[:10]:  # 최대 10개
            try:
                quizzes.append(MultipleChoiceQuiz(
                    question=q.get("question", ""),
                    options=q.get("options", [])[:4],  # 정확히 4개
                    correct_answer=q.get("correct_answer", 0),
                    explanation=q.get("explanation", ""),
                    difficulty=q.get("difficulty", "medium")
                ))
            except Exception as e:
                logger.error(f"4지선다 퀴즈 생성 실패: {e}")
        return quizzes

    def _create_sa_quizzes(self, data: List[Dict]) -> List[ShortAnswerQuiz]:
        """단답형 퀴즈 생성"""
        quizzes = []
        for q in data[:5]:  # 최대 5개
            try:
                quizzes.append(ShortAnswerQuiz(
                    question=q.get("question", ""),
                    correct_answers=q.get("correct_answers", []),
                    explanation=q.get("explanation", ""),
                    case_sensitive=q.get("case_sensitive", False)
                ))
            except Exception as e:
                logger.error(f"단답형 퀴즈 생성 실패: {e}")
        return quizzes

    def _create_essay_quizzes(self, data: List[Dict]) -> List[EssayQuiz]:
        """서술형 문제 생성"""
        quizzes = []
        for q in data[:2]:  # 최대 2개
            try:
                quizzes.append(EssayQuiz(
                    question=q.get("question", ""),
                    suggested_answer=q.get("suggested_answer", ""),
                    grading_criteria=q.get("grading_criteria", []),
                    min_words=q.get("min_words", 100)
                ))
            except Exception as e:
                logger.error(f"서술형 문제 생성 실패: {e}")
        return quizzes

    async def _save_content(self, content_id: str, content: LearningContent):
        """콘텐츠 저장"""
        file_path = os.path.join(self.content_dir, f"{content_id}.json")

        content_dict = content.model_dump(mode='json')

        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(content_dict, ensure_ascii=False, indent=2))

        logger.info(f"콘텐츠 저장 완료: {file_path}")

    async def get_content(self, content_id: str) -> Optional[LearningContent]:
        """콘텐츠 조회"""
        file_path = os.path.join(self.content_dir, f"{content_id}.json")

        if not os.path.exists(file_path):
            return None

        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content_str = await f.read()
                content_dict = json.loads(content_str)
                return LearningContent(**content_dict)
        except Exception as e:
            logger.error(f"콘텐츠 조회 실패: {str(e)}")
            return None

    # === 단계별 생성 메서드 ===

    async def generate_podcast(self, source_content: Dict[str, Any]) -> Dict[str, Any]:
        """팟캐스트만 생성"""
        source_text = source_content.get("text_content", "")[:8000]
        source_title = source_content.get("title", "")

        prompt = f"""다음 내용으로 **팟캐스트 스크립트**만 생성해주세요.

# 원본
제목: {source_title}
내용: {source_text}

# 요구사항
- 진행자(host)와 게스트(guest)의 대화 6-8개
- 핵심 내용을 쉽게 설명
- 7-8분 분량

# JSON 형식으로 응답
{{
  "title": "팟캐스트 제목",
  "host_name": "진행자 이름",
  "guest_name": "게스트 이름",
  "dialogues": [
    {{"speaker": "host", "text": "대화 내용"}},
    {{"speaker": "guest", "text": "대화 내용"}}
  ],
  "duration_minutes": 8
}}

순수 JSON만 반환하세요 (코드 블록 없이)."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text.strip())

    async def generate_video_lecture(self, source_content: Dict[str, Any]) -> Dict[str, Any]:
        """강의 슬라이드만 생성"""
        source_text = source_content.get("text_content", "")[:8000]
        source_title = source_content.get("title", "")

        prompt = f"""다음 내용으로 **강의 슬라이드**만 생성해주세요.

# 원본
제목: {source_title}
내용: {source_text}

# 요구사항
- 슬라이드 5-6장
- 각 슬라이드: 제목, 내용(불릿 3개), 나레이션(2-3문장)

# JSON 형식
{{
  "title": "강의 제목",
  "slides": [
    {{
      "slide_number": 1,
      "title": "슬라이드 제목",
      "content": ["요점1", "요점2", "요점3"],
      "narration": "나레이션"
    }}
  ]
}}

순수 JSON만 반환하세요."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2500,
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text.strip())

    async def generate_reading_material(self, source_content: Dict[str, Any]) -> Dict[str, Any]:
        """읽기 자료만 생성"""
        source_text = source_content.get("text_content", "")[:8000]
        source_title = source_content.get("title", "")

        prompt = f"""다음 내용으로 **읽기 자료**만 생성해주세요.

# 원본
제목: {source_title}
내용: {source_text}

# 요구사항
- 마크다운 형식
- 1500-2000자
- 체계적으로 구조화
- 제목, 섹션, 설명 포함

# JSON 형식
{{
  "title": "읽기 자료 제목",
  "content": "# 제목\\n\\n## 섹션1\\n내용...\\n\\n## 섹션2\\n내용...",
  "estimated_reading_time": 10
}}

순수 JSON만 반환하세요."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text.strip())

    async def generate_quizzes(self, source_content: Dict[str, Any]) -> Dict[str, Any]:
        """퀴즈만 생성"""
        source_text = source_content.get("text_content", "")[:8000]

        prompt = f"""다음 내용으로 **퀴즈**만 생성해주세요.

# 원본 내용
{source_text}

# 요구사항
- 4지선다형 5문제
- 단답형 3문제
- 서술형 1문제

# JSON 형식
{{
  "multiple_choice": [
    {{
      "question": "문제",
      "options": ["선택1", "선택2", "선택3", "선택4"],
      "correct_answer": 0,
      "explanation": "해설",
      "difficulty": "easy"
    }}
  ],
  "short_answer": [
    {{
      "question": "문제",
      "correct_answers": ["정답1", "정답2"],
      "explanation": "해설",
      "case_sensitive": false
    }}
  ],
  "essay": [
    {{
      "question": "문제",
      "suggested_answer": "예시 답안",
      "grading_criteria": ["기준1", "기준2"],
      "min_words": 100
    }}
  ]
}}

순수 JSON만 반환하세요."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text.strip())

    async def generate_deep_questions(self, source_content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """심화 질문만 생성"""
        source_text = source_content.get("text_content", "")[:8000]

        prompt = f"""다음 내용으로 **심화 사고 질문** 2개만 생성해주세요.

# 원본 내용
{source_text}

# 요구사항
- 비판적 사고를 요구하는 질문
- 정답이 정해지지 않은 열린 질문

# JSON 형식
[
  {{
    "question": "질문 내용",
    "context": "질문의 맥락",
    "hints": ["힌트1", "힌트2"]
  }}
]

순수 JSON만 반환하세요 (배열 형태)."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text.strip())
