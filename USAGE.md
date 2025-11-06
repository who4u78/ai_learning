# 사용 가이드

## 기본 사용법

### 1. URL로 콘텐츠 생성

가장 간단한 방법입니다. 학습하고 싶은 웹페이지의 URL을 입력하면 자동으로 콘텐츠를 분석하고 한글 학습 자료를 생성합니다.

**예시 URL:**
```
https://en.wikipedia.org/wiki/Machine_learning
https://medium.com/@some-article
https://docs.python.org/3/tutorial/
```

**단계:**
1. 프론트엔드에서 "URL" 선택
2. URL 입력
3. 옵션 선택 (퀴즈, 요약, 예시)
4. "학습 콘텐츠 생성하기" 클릭
5. 1-2분 대기

### 2. 텍스트로 콘텐츠 생성

직접 학습 자료를 입력할 수 있습니다.

**예시:**
```
인공지능 개요

인공지능(Artificial Intelligence, AI)은 인간의 지능을 모방한
컴퓨터 시스템입니다. 주요 분야로는 기계학습, 자연어 처리,
컴퓨터 비전 등이 있습니다.

기계학습은 데이터로부터 패턴을 학습하는 기술입니다...
```

### 3. HTML로 콘텐츠 생성

HTML 문서를 직접 붙여넣을 수 있습니다.

## 고급 기능

### 음성 생성 (TTS)

생성된 학습 콘텐츠에 대해 한글 음성을 생성할 수 있습니다.

1. 콘텐츠 생성 완료 후
2. "🎤 음성 생성" 버튼 클릭
3. 각 섹션마다 음성 파일 생성
4. 오디오 플레이어로 재생

**특징:**
- Fish Audio TTS 사용
- 자연스러운 한글 발음
- 섹션별로 개별 생성

### 비디오 생성

텍스트 + 음성 + 시각자료를 결합한 학습 비디오를 생성합니다.

1. 음성 생성 완료 후
2. "🎥 비디오 생성" 버튼 클릭
3. 자막 포함 여부 선택 가능
4. 비디오 플레이어로 시청

**특징:**
- MP4 포맷
- 720p 해상도
- 자막 지원
- 섹션별 자동 결합

## API 사용 (개발자용)

### Python 예제

```python
import requests

API_URL = "http://localhost:8000"

# 1. 콘텐츠 생성
response = requests.post(f"{API_URL}/api/content/generate", json={
    "source_type": "url",
    "source_data": "https://example.com/article",
    "title": "예제 학습 자료",
    "include_quiz": True,
    "include_summary": True
})

content = response.json()
content_id = content["id"]

# 2. 음성 생성
audio_response = requests.post(
    f"{API_URL}/api/audio/generate-for-content/{content_id}"
)

# 3. 비디오 생성
video_response = requests.post(f"{API_URL}/api/video/generate", json={
    "content_id": content_id,
    "include_subtitles": True
})
```

### cURL 예제

```bash
# 콘텐츠 생성
curl -X POST http://localhost:8000/api/content/generate \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "text",
    "source_data": "학습할 내용...",
    "include_quiz": true
  }'

# 헬스 체크
curl http://localhost:8000/health
```

### JavaScript 예제

```javascript
const API_URL = 'http://localhost:8000'

async function generateContent(url) {
  const response = await fetch(`${API_URL}/api/content/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      source_type: 'url',
      source_data: url,
      include_quiz: true,
      include_summary: true,
    }),
  })

  return await response.json()
}

// 사용
const content = await generateContent('https://example.com')
console.log(content.id)
```

## 학습 워크플로우 예시

### 시나리오 1: 온라인 강의 자료 생성

1. 강의 노트 URL 입력
2. 콘텐츠 생성 (퀴즈, 요약 포함)
3. 음성 생성으로 오디오북 제작
4. 비디오 생성으로 학습 영상 제작
5. 학생들에게 공유

### 시나리오 2: 개인 학습

1. 학습하고 싶은 주제의 Wikipedia 페이지 URL 입력
2. 한글로 번역된 학습 자료 생성
3. 섹션별로 학습하며 퀴즈로 복습
4. 음성으로 들으며 출퇴근 시간 활용

### 시나리오 3: 연구 자료 정리

1. 여러 논문/기사를 텍스트로 입력
2. AI가 핵심 내용 요약 및 구조화
3. 한글로 정리된 자료 확보
4. 팀원들과 공유

## 팁과 요령

### 좋은 결과를 얻는 방법

1. **명확한 소스 제공**
   - 구조화된 웹페이지 선택
   - 너무 긴 문서는 분할

2. **적절한 옵션 선택**
   - 복습이 필요하면: 퀴즈 포함
   - 빠른 이해가 필요하면: 요약 포함
   - 실습이 필요하면: 예시 포함

3. **섹션 단위 학습**
   - 한 번에 하나씩 학습
   - 퀴즈로 이해도 확인
   - 음성으로 반복 청취

### 비용 절감 팁

1. **긴 문서는 분할**
   - 섹션별로 별도 생성
   - 필요한 부분만 처리

2. **음성/비디오는 선택적 생성**
   - 꼭 필요한 콘텐츠만
   - 재사용 고려

3. **캐싱 활용**
   - 같은 URL은 재사용
   - 이전 생성 콘텐츠 보관

## 문제 해결

### "콘텐츠 생성 실패" 오류

- URL이 접근 가능한지 확인
- 웹페이지가 로봇 차단하는지 확인
- 텍스트 길이가 너무 긴지 확인 (10,000자 이하 권장)

### "음성 생성 실패" 오류

- Fish Audio API 키 확인
- 텍스트가 너무 길지 않은지 확인
- 특수 문자나 이모지 제거

### "비디오 생성 실패" 오류

- FFmpeg 설치 확인
- 한글 폰트 설치 확인
- 충분한 디스크 공간 확인

## 추가 리소스

- API 문서: http://localhost:8000/docs
- GitHub Issues: 문제 보고 및 기능 요청
- 개발 가이드: DEVELOPMENT.md
