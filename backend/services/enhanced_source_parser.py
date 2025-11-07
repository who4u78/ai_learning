"""
확장된 소스 파싱 서비스
PDF, Word, YouTube, 여러 소스 결합 지원
"""
import requests
from bs4 import BeautifulSoup
import html2text
from typing import Dict, Any, List
from models.schemas import ContentSourceType
import logging
import os
from pypdf import PdfReader
from docx import Document
from youtube_transcript_api import YouTubeTranscriptApi
import re

logger = logging.getLogger(__name__)


class EnhancedSourceParser:
    """확장된 소스 파싱 클래스"""

    def __init__(self):
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = False
        self.html_converter.body_width = 0

    async def parse_multiple(self, sources: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        여러 소스를 파싱하여 하나로 결합

        Args:
            sources: [{"type": "url", "data": "https://..."}, ...]

        Returns:
            결합된 콘텐츠
        """
        all_contents = []
        combined_title = []

        for i, source in enumerate(sources):
            logger.info(f"소스 {i+1}/{len(sources)} 파싱 중...")

            source_type = ContentSourceType(source["type"])
            source_data = source["data"]

            content = await self.parse(source_type, source_data)
            all_contents.append(content)
            combined_title.append(content.get("title", f"소스 {i+1}"))

        # 모든 텍스트 결합
        combined_text = "\n\n=== 구분선 ===\n\n".join(
            c.get("text_content", "") for c in all_contents
        )

        # 모든 섹션 결합
        combined_sections = []
        for content in all_contents:
            combined_sections.extend(content.get("sections", []))

        return {
            "title": " + ".join(combined_title[:3]),  # 처음 3개만
            "description": f"{len(sources)}개의 소스를 결합한 학습 자료",
            "url": None,
            "text_content": combined_text,
            "markdown_content": combined_text,
            "sections": combined_sections,
            "word_count": len(combined_text.split()),
            "source_count": len(sources)
        }

    async def parse(self, source_type: ContentSourceType, source_data: str) -> Dict[str, Any]:
        """
        소스를 파싱하여 구조화된 데이터로 변환

        지원 형식:
        - URL: 웹페이지 (HTML)
        - HTML: HTML 문자열
        - TEXT: 일반 텍스트
        - FILE: 파일 경로 (PDF, DOCX, TXT, HTML)
        - YOUTUBE: YouTube URL (자막 추출)
        """
        # YouTube URL 감지
        if source_type == ContentSourceType.URL and self._is_youtube_url(source_data):
            return await self._parse_youtube(source_data)

        if source_type == ContentSourceType.URL:
            return await self._parse_url(source_data)
        elif source_type == ContentSourceType.HTML:
            return await self._parse_html(source_data)
        elif source_type == ContentSourceType.TEXT:
            return await self._parse_text(source_data)
        elif source_type == ContentSourceType.FILE:
            return await self._parse_file(source_data)
        else:
            raise ValueError(f"지원하지 않는 소스 타입: {source_type}")

    def _is_youtube_url(self, url: str) -> bool:
        """YouTube URL 여부 확인"""
        youtube_patterns = [
            r'youtube\.com/watch\?v=',
            r'youtu\.be/',
            r'youtube\.com/embed/',
        ]
        return any(re.search(pattern, url) for pattern in youtube_patterns)

    async def _parse_youtube(self, url: str) -> Dict[str, Any]:
        """YouTube 비디오에서 자막 추출"""
        try:
            logger.info(f"YouTube 파싱 시작: {url}")

            # 비디오 ID 추출
            video_id = None
            if 'v=' in url:
                video_id = url.split('v=')[1].split('&')[0]
            elif 'youtu.be/' in url:
                video_id = url.split('youtu.be/')[1].split('?')[0]

            if not video_id:
                raise Exception("YouTube 비디오 ID를 추출할 수 없습니다")

            # 자막 가져오기 (한국어 우선, 없으면 영어)
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

                # 한국어 자막 시도
                try:
                    transcript = transcript_list.find_transcript(['ko'])
                except:
                    # 영어 자막 시도
                    try:
                        transcript = transcript_list.find_transcript(['en'])
                    except:
                        # 자동 생성 자막
                        transcript = transcript_list.find_generated_transcript(['ko', 'en'])

                transcript_data = transcript.fetch()

                # 텍스트 결합
                text_content = "\n\n".join(item['text'] for item in transcript_data)

                # 제목 가져오기 (간단한 방법)
                title = f"YouTube 비디오 (ID: {video_id})"

            except Exception as e:
                logger.error(f"자막 가져오기 실패: {str(e)}")
                raise Exception(f"YouTube 자막을 가져올 수 없습니다: {str(e)}")

            result = {
                "title": title,
                "description": f"YouTube 비디오 자막",
                "url": url,
                "text_content": text_content,
                "markdown_content": text_content,
                "sections": [{"title": title, "content": text_content}],
                "word_count": len(text_content.split()),
                "source_type": "youtube"
            }

            logger.info(f"YouTube 파싱 완료: {len(text_content)} 글자")
            return result

        except Exception as e:
            logger.error(f"YouTube 파싱 실패: {str(e)}")
            raise Exception(f"YouTube 파싱 실패: {str(e)}")

    async def _parse_pdf(self, file_path: str) -> Dict[str, Any]:
        """PDF 파일 파싱"""
        try:
            logger.info(f"PDF 파싱 시작: {file_path}")

            reader = PdfReader(file_path)

            # 메타데이터
            title = reader.metadata.get('/Title', os.path.basename(file_path))

            # 모든 페이지의 텍스트 추출
            text_content = ""
            for page in reader.pages:
                text_content += page.extract_text() + "\n\n"

            # 간단한 섹션 분할 (빈 줄 기준)
            sections = []
            paragraphs = text_content.split('\n\n')
            current_section = {"title": "섹션 1", "content": ""}
            section_num = 1

            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue

                # 새 섹션 시작 (대문자로 시작하고 짧은 경우)
                if len(para) < 100 and para[0].isupper():
                    if current_section["content"]:
                        sections.append(current_section)
                        section_num += 1
                    current_section = {"title": para, "content": ""}
                else:
                    current_section["content"] += para + "\n\n"

            if current_section["content"]:
                sections.append(current_section)

            result = {
                "title": title,
                "description": f"PDF 문서 ({len(reader.pages)} 페이지)",
                "url": None,
                "text_content": text_content,
                "markdown_content": text_content,
                "sections": sections,
                "word_count": len(text_content.split()),
                "page_count": len(reader.pages)
            }

            logger.info(f"PDF 파싱 완료: {len(reader.pages)} 페이지, {result['word_count']} 단어")
            return result

        except Exception as e:
            logger.error(f"PDF 파싱 실패: {str(e)}")
            raise Exception(f"PDF 파싱 실패: {str(e)}")

    async def _parse_docx(self, file_path: str) -> Dict[str, Any]:
        """Word 문서(.docx) 파싱"""
        try:
            logger.info(f"Word 파싱 시작: {file_path}")

            doc = Document(file_path)

            # 제목
            title = os.path.basename(file_path)

            # 텍스트 추출
            text_content = ""
            sections = []
            current_section = {"title": "시작", "content": ""}

            for para in doc.paragraphs:
                text = para.text.strip()
                if not text:
                    continue

                # 제목 스타일 확인 (Heading)
                if para.style.name.startswith('Heading'):
                    if current_section["content"]:
                        sections.append(current_section)
                    current_section = {"title": text, "content": ""}
                else:
                    current_section["content"] += text + "\n\n"
                    text_content += text + "\n\n"

            if current_section["content"]:
                sections.append(current_section)

            result = {
                "title": title,
                "description": f"Word 문서 ({len(doc.paragraphs)} 문단)",
                "url": None,
                "text_content": text_content,
                "markdown_content": text_content,
                "sections": sections,
                "word_count": len(text_content.split())
            }

            logger.info(f"Word 파싱 완료: {result['word_count']} 단어")
            return result

        except Exception as e:
            logger.error(f"Word 파싱 실패: {str(e)}")
            raise Exception(f"Word 파싱 실패: {str(e)}")

    async def _parse_file(self, file_path: str) -> Dict[str, Any]:
        """파일 파싱 (확장자에 따라 자동 선택)"""
        logger.info(f"파일 파싱: {file_path}")

        if not os.path.exists(file_path):
            raise Exception(f"파일을 찾을 수 없습니다: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()

        if ext == '.pdf':
            return await self._parse_pdf(file_path)
        elif ext in ['.docx', '.doc']:
            return await self._parse_docx(file_path)
        elif ext in ['.html', '.htm']:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            return await self._parse_html(html_content)
        elif ext in ['.txt', '.md']:
            with open(file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            return await self._parse_text(text_content)
        else:
            raise Exception(f"지원하지 않는 파일 형식: {ext}")

    async def _parse_url(self, url: str) -> Dict[str, Any]:
        """URL에서 콘텐츠 파싱 (기존 코드)"""
        try:
            logger.info(f"URL 파싱 시작: {url}")

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            response.encoding = response.apparent_encoding

            html_content = response.text
            return await self._parse_html(html_content, url=url)

        except requests.RequestException as e:
            logger.error(f"URL 파싱 실패: {str(e)}")
            raise Exception(f"URL을 가져올 수 없습니다: {str(e)}")

    async def _parse_html(self, html_content: str, url: str = None) -> Dict[str, Any]:
        """HTML 콘텐츠 파싱 (기존 코드 유지)"""
        try:
            logger.info("HTML 파싱 시작")

            soup = BeautifulSoup(html_content, 'lxml')

            # 제목
            title = soup.title.string.strip() if soup.title else "제목 없음"

            # 본문 추출
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()

            main_content = (
                soup.find('main') or
                soup.find('article') or
                soup.find('div', class_=['content', 'main-content']) or
                soup.find('body')
            )

            if main_content:
                text_content = main_content.get_text(separator='\n', strip=True)
            else:
                text_content = soup.get_text(separator='\n', strip=True)

            return {
                "title": title,
                "description": "",
                "url": url,
                "text_content": text_content,
                "markdown_content": text_content,
                "sections": [{"title": title, "content": text_content}],
                "word_count": len(text_content.split())
            }

        except Exception as e:
            logger.error(f"HTML 파싱 실패: {str(e)}")
            raise Exception(f"HTML 파싱 실패: {str(e)}")

    async def _parse_text(self, text_content: str) -> Dict[str, Any]:
        """일반 텍스트 파싱"""
        logger.info("텍스트 파싱")

        lines = text_content.strip().split('\n')
        title = lines[0] if lines else "제목 없음"

        return {
            "title": title,
            "description": "",
            "url": None,
            "text_content": text_content,
            "markdown_content": text_content,
            "sections": [{"title": title, "content": text_content}],
            "word_count": len(text_content.split())
        }
