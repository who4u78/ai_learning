"""
소스 파싱 서비스
HTML, URL, 텍스트 파일 등을 파싱하여 학습 가능한 형태로 변환
"""
import requests
from bs4 import BeautifulSoup
import html2text
from typing import Dict, Any
from models.schemas import ContentSourceType
import logging

logger = logging.getLogger(__name__)


class SourceParser:
    """소스 파싱 클래스"""

    def __init__(self):
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = False
        self.html_converter.body_width = 0  # 줄바꿈 없음

    async def parse(self, source_type: ContentSourceType, source_data: str) -> Dict[str, Any]:
        """
        소스를 파싱하여 구조화된 데이터로 변환

        Args:
            source_type: 소스 타입 (url, html, text, file)
            source_data: 소스 데이터

        Returns:
            파싱된 콘텐츠 딕셔너리
        """
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

    async def _parse_url(self, url: str) -> Dict[str, Any]:
        """URL에서 콘텐츠 파싱"""
        try:
            logger.info(f"URL 파싱 시작: {url}")

            # User-Agent 헤더 추가
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
        """HTML 콘텐츠 파싱"""
        try:
            logger.info("HTML 파싱 시작")

            soup = BeautifulSoup(html_content, 'lxml')

            # 메타데이터 추출
            title = self._extract_title(soup)
            description = self._extract_description(soup)

            # 본문 추출 (스크립트, 스타일 제거)
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()

            # 주요 콘텐츠 영역 찾기
            main_content = (
                soup.find('main') or
                soup.find('article') or
                soup.find('div', class_=['content', 'main-content', 'post-content']) or
                soup.find('body')
            )

            if main_content:
                # HTML을 마크다운으로 변환
                markdown_content = self.html_converter.handle(str(main_content))

                # 텍스트만 추출
                text_content = main_content.get_text(separator='\n', strip=True)
            else:
                markdown_content = self.html_converter.handle(html_content)
                text_content = soup.get_text(separator='\n', strip=True)

            # 섹션 분할 (h1, h2, h3 기준)
            sections = self._extract_sections(soup)

            result = {
                "title": title,
                "description": description,
                "url": url,
                "text_content": text_content,
                "markdown_content": markdown_content,
                "sections": sections,
                "word_count": len(text_content.split())
            }

            logger.info(f"HTML 파싱 완료: {len(sections)} 섹션, {result['word_count']} 단어")
            return result

        except Exception as e:
            logger.error(f"HTML 파싱 실패: {str(e)}")
            raise Exception(f"HTML 파싱 실패: {str(e)}")

    async def _parse_text(self, text_content: str) -> Dict[str, Any]:
        """일반 텍스트 파싱"""
        logger.info("텍스트 파싱 시작")

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

    async def _parse_file(self, file_path: str) -> Dict[str, Any]:
        """파일 파싱"""
        logger.info(f"파일 파싱 시작: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 파일 확장자에 따라 처리
            if file_path.endswith('.html'):
                return await self._parse_html(content)
            else:
                return await self._parse_text(content)

        except Exception as e:
            logger.error(f"파일 파싱 실패: {str(e)}")
            raise Exception(f"파일을 읽을 수 없습니다: {str(e)}")

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """제목 추출"""
        # <title> 태그
        if soup.title:
            return soup.title.string.strip()

        # <h1> 태그
        h1 = soup.find('h1')
        if h1:
            return h1.get_text().strip()

        # og:title 메타태그
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            return og_title['content'].strip()

        return "제목 없음"

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """설명 추출"""
        # meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content'].strip()

        # og:description
        og_desc = soup.find('meta', property='og:description')
        if og_desc and og_desc.get('content'):
            return og_desc['content'].strip()

        # 첫 번째 문단
        first_p = soup.find('p')
        if first_p:
            text = first_p.get_text().strip()
            return text[:200] + '...' if len(text) > 200 else text

        return ""

    def _extract_sections(self, soup: BeautifulSoup) -> list:
        """섹션 추출 (제목 기준으로 분할)"""
        sections = []
        current_section = {"title": "", "content": ""}

        main_content = (
            soup.find('main') or
            soup.find('article') or
            soup.find('div', class_=['content', 'main-content']) or
            soup.find('body')
        )

        if not main_content:
            return sections

        for element in main_content.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol', 'pre']):
            if element.name in ['h1', 'h2', 'h3']:
                # 새로운 섹션 시작
                if current_section["content"]:
                    sections.append(current_section)

                current_section = {
                    "title": element.get_text().strip(),
                    "content": "",
                    "level": int(element.name[1])
                }
            else:
                # 콘텐츠 추가
                text = element.get_text().strip()
                if text:
                    current_section["content"] += text + "\n\n"

        # 마지막 섹션 추가
        if current_section["content"]:
            sections.append(current_section)

        return sections
