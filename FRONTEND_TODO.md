# Frontend 개발 가이드

Backend v2.0이 완성되었습니다. Frontend는 다음 컴포넌트들이 필요합니다:

## 필요한 컴포넌트

### 1. ContentGeneratorV2.tsx
```typescript
- URL/텍스트 입력
- 생성 시작
- 진행 상태 폴링 (progress bar)
- 완료 시 학습 대시보드로 이동
```

### 2. LearningDashboard.tsx
```typescript
- 7가지 학습 자료 섹션으로 구성
- 팟캐스트, 비디오, 읽기, 퀴즈 탭
- 항상 표시되는 챗봇 버튼
```

### 3. PodcastPlayer.tsx
```typescript
- 대화형 스크립트 표시
- 오디오 플레이어
- 진행자/게스트 구분
```

### 4. VideoLecturePlayer.tsx
```typescript
- 비디오 플레이어
- 슬라이드 목록
- 현재 슬라이드 표시
```

### 5. ReadingMaterialView.tsx
```typescript
- 마크다운 렌더링
- 읽기 시간 표시
- 목차 (헤딩 기반)
```

### 6. QuizComponents/
```typescript
- MultipleChoiceQuiz.tsx (4지선다)
- ShortAnswerQuiz.tsx (단답형)
- EssayQuiz.tsx (서술형)
- DeepQuestions.tsx (심화 질문)
```

### 7. ChatbotWidget.tsx
```typescript
- 우측 하단 고정
- 대화 인터페이스
- 대화 히스토리
- 학습 자료 컨텍스트
```

## 빠른 구현 가이드

### API 사용 예시

```typescript
// 1. 콘텐츠 생성
const handleGenerate = async () => {
  const status = await learningApi.generateContent({
    source_type: 'url',
    source_data: url
  })
  
  // 2. 상태 폴링
  const interval = setInterval(async () => {
    const s = await learningApi.getStatus(status.content_id)
    setProgress(s.progress)
    
    if (s.status === 'completed') {
      clearInterval(interval)
      onContentReady(status.content_id)
    }
  }, 3000)
}

// 3. 콘텐츠 로드
const content = await learningApi.getContent(contentId)

// 4. 챗봇
const response = await learningApi.chat({
  content_id: contentId,
  message: userMessage,
  conversation_history: history
})
```

### 스타일링

- Tailwind CSS 사용
- 다크 모드 지원
- 반응형 디자인
- 애니메이션 (진행 바, 로딩 등)

## 단계별 개발

1. ✅ API 클라이언트 (완료)
2. ⏳ ContentGeneratorV2 (기본 구조만)
3. ⏳ LearningDashboard (탭 구조)
4. ⏳ 개별 컴포넌트들
5. ⏳ 챗봇 위젯
6. ⏳ 스타일링 개선

## 현재 상태

Backend는 완전히 작동합니다:
- API Docs: http://localhost:8000/docs
- 모든 엔드포인트 테스트 가능

Frontend는 기본 구조만 작성되었습니다. 
위 가이드를 참고하여 컴포넌트를 구현하세요.

## 테스트 방법

1. Backend 실행: `./start-backend.sh`
2. Python으로 직접 테스트:

```python
import requests

# 콘텐츠 생성
r = requests.post("http://localhost:8000/api/learning/generate", json={
    "source_type": "text",
    "source_data": "인공지능은 컴퓨터가 인간처럼 생각하고 학습하는 기술입니다...",
    "title": "AI 기초"
})

content_id = r.json()["content_id"]

# 상태 확인
import time
while True:
    s = requests.get(f"http://localhost:8000/api/learning/status/{content_id}")
    print(s.json())
    if s.json()["status"] == "completed":
        break
    time.sleep(5)

# 완성된 콘텐츠 확인
c = requests.get(f"http://localhost:8000/api/learning/{content_id}")
print(c.json().keys())
```

## 추천 개발 순서

1. 먼저 Backend API를 Python으로 직접 테스트
2. 콘텐츠가 제대로 생성되는지 확인
3. 그 다음 Frontend 개발 시작
4. 간단한 컴포넌트부터 (생성 -> 표시)
5. 마지막에 챗봇 추가

