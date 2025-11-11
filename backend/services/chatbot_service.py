"""
학습 챗봇 서비스
학습 콘텐츠를 컨텍스트로 하여 사용자 질문에 답변
"""
import anthropic
import os
from typing import List, Optional
from models.schemas import ChatMessage, ChatRequest, ChatResponse, LearningContent
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ChatbotService:
    """학습 챗봇 서비스"""

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY가 설정되지 않았습니다")

        self.client = anthropic.Anthropic(api_key=api_key)
        # Claude 3 Opus 사용 (가장 안정적이고 호환성 좋음)
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")

    async def chat(
        self,
        content: LearningContent,
        user_message: str,
        conversation_history: Optional[List[ChatMessage]] = None
    ) -> ChatResponse:
        """
        사용자 질문에 답변

        Args:
            content: 학습 콘텐츠 (컨텍스트)
            user_message: 사용자 메시지
            conversation_history: 이전 대화 내역

        Returns:
            ChatResponse: 챗봇 응답
        """
        try:
            logger.info(f"챗봇 질문: {user_message[:50]}...")

            # 컨텍스트 구성
            context = self._build_context(content)

            # 대화 히스토리 구성
            messages = []

            # 이전 대화 추가
            if conversation_history:
                for msg in conversation_history[-10:]:  # 최근 10개만 (비용 절감)
                    messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })

            # 현재 사용자 메시지
            messages.append({
                "role": "user",
                "content": user_message
            })

            # Claude API 호출
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                temperature=0.7,
                system=f"""당신은 친절한 학습 도우미입니다. 학생이 학습 중에 궁금한 점을 질문하면 다음 학습 자료를 바탕으로 명확하고 이해하기 쉽게 답변해주세요.

# 학습 자료
{context}

# 답변 가이드라인
- 학습 자료의 내용을 기반으로 답변
- 쉽고 명확한 설명
- 필요시 예시 제공
- 학습 자료에 없는 내용이면 정직하게 말하기
- 추가 질문 유도
- 한글로 답변
""",
                messages=messages
            )

            assistant_message = response.content[0].text

            logger.info(f"챗봇 응답 생성 완료")

            return ChatResponse(
                message=assistant_message,
                timestamp=datetime.now()
            )

        except Exception as e:
            logger.error(f"챗봇 응답 생성 실패: {str(e)}")
            # 폴백 응답
            return ChatResponse(
                message="죄송합니다. 일시적인 오류가 발생했습니다. 다시 질문해주세요.",
                timestamp=datetime.now()
            )

    def _build_context(self, content: LearningContent) -> str:
        """학습 콘텐츠를 컨텍스트로 변환"""
        context_parts = []

        # 제목과 설명
        context_parts.append(f"제목: {content.title}")
        context_parts.append(f"설명: {content.description}")
        context_parts.append("")

        # 읽기 자료
        if content.reading_material:
            context_parts.append("## 학습 내용")
            context_parts.append(content.reading_material.content[:3000])  # 처음 3000자
            context_parts.append("")

        # 팟캐스트 스크립트 (요약)
        if content.podcast:
            context_parts.append("## 팟캐스트 주요 내용")
            for dialogue in content.podcast.script.dialogues[:10]:  # 처음 10개 대화
                speaker = "진행자" if dialogue.speaker == "host" else "게스트"
                context_parts.append(f"{speaker}: {dialogue.text}")
            context_parts.append("")

        # 강의 슬라이드 내용
        if content.video_lecture:
            context_parts.append("## 강의 내용")
            for slide in content.video_lecture.slides:
                context_parts.append(f"### {slide.title}")
                for item in slide.content:
                    context_parts.append(f"- {item}")
            context_parts.append("")

        # 심화 질문 (참고)
        if content.deep_questions:
            context_parts.append("## 생각해볼 질문들")
            for q in content.deep_questions:
                context_parts.append(f"- {q.question}")
            context_parts.append("")

        return "\n".join(context_parts)
