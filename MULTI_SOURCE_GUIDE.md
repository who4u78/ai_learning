# 다중 소스 입력 가이드

## 🎯 지원하는 소스 타입

### 1. URL (웹페이지)
```python
{
    "source_type": "url",
    "source_data": "https://example.com/article"
}
```

### 2. YouTube (자막 추출)
```python
{
    "source_type": "url",  # 자동 감지됨
    "source_data": "https://www.youtube.com/watch?v=VIDEO_ID"
}
# 또는
{
    "source_type": "url",
    "source_data": "https://youtu.be/VIDEO_ID"
}
```

### 3. PDF 파일
```python
{
    "source_type": "file",
    "source_data": "/path/to/document.pdf"
}
```

### 4. Word 파일 (.docx)
```python
{
    "source_type": "file",
    "source_data": "/path/to/document.docx"
}
```

### 5. 텍스트 파일
```python
{
    "source_type": "file",
    "source_data": "/path/to/document.txt"
}
```

### 6. HTML 파일
```python
{
    "source_type": "file",
    "source_data": "/path/to/document.html"
}
```

### 7. 직접 텍스트 입력
```python
{
    "source_type": "text",
    "source_data": "여기에 학습할 텍스트를 직접 입력..."
}
```

## 💡 단일 소스 사용

### 예시 1: 웹페이지
```python
import requests

response = requests.post("http://localhost:8000/api/learning/generate", json={
    "source_type": "url",
    "source_data": "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "title": "인공지능 학습"
})
```

### 예시 2: YouTube
```python
response = requests.post("http://localhost:8000/api/learning/generate", json={
    "source_type": "url",
    "source_data": "https://www.youtube.com/watch?v=aircAruvnKk",
    "title": "신경망 기초"
})
```

### 예시 3: PDF
```python
response = requests.post("http://localhost:8000/api/learning/generate", json={
    "source_type": "file",
    "source_data": "/home/user/documents/machine_learning.pdf",
    "title": "기계학습 교재"
})
```

## 🔥 여러 소스 결합하기

하나의 학습 자료로 여러 소스를 결합할 수 있습니다!

### 예시 1: 웹페이지 + YouTube
```python
response = requests.post("http://localhost:8000/api/learning/generate", json={
    "sources": [
        {
            "type": "url",
            "data": "https://en.wikipedia.org/wiki/Machine_learning"
        },
        {
            "type": "url",
            "data": "https://www.youtube.com/watch?v=ukzFI9rgwfU"
        }
    ],
    "title": "기계학습 종합"
})
```

### 예시 2: PDF + Word + 웹페이지
```python
response = requests.post("http://localhost:8000/api/learning/generate", json={
    "sources": [
        {
            "type": "file",
            "data": "/home/user/lecture_notes.pdf"
        },
        {
            "type": "file",
            "data": "/home/user/assignment.docx"
        },
        {
            "type": "url",
            "data": "https://scikit-learn.org/stable/tutorial/index.html"
        }
    ],
    "title": "기계학습 전체 강의"
})
```

### 예시 3: 여러 YouTube 비디오 + 텍스트
```python
response = requests.post("http://localhost:8000/api/learning/generate", json={
    "sources": [
        {
            "type": "url",
            "data": "https://www.youtube.com/watch?v=VIDEO_1"
        },
        {
            "type": "url",
            "data": "https://www.youtube.com/watch?v=VIDEO_2"
        },
        {
            "type": "text",
            "data": "추가 설명: 이 비디오들은 딥러닝의 기초를 다룹니다..."
        }
    ],
    "title": "딥러닝 시리즈"
})
```

### 예시 4: 교재 전체 (여러 PDF 장)
```python
response = requests.post("http://localhost:8000/api/learning/generate", json={
    "sources": [
        {"type": "file", "data": "/textbook/chapter1.pdf"},
        {"type": "file", "data": "/textbook/chapter2.pdf"},
        {"type": "file", "data": "/textbook/chapter3.pdf"},
    ],
    "title": "교재 1-3장"
})
```

## 📊 결합된 소스 처리 방식

여러 소스를 입력하면:

1. **각 소스를 개별적으로 파싱**
   - PDF는 텍스트 추출
   - YouTube는 자막 추출
   - 웹페이지는 HTML 파싱

2. **모든 내용을 하나로 결합**
   ```
   [소스 1 내용]

   === 구분선 ===

   [소스 2 내용]

   === 구분선 ===

   [소스 3 내용]
   ```

3. **통합 학습 자료 생성**
   - 모든 소스의 내용을 고려한 팟캐스트
   - 종합적인 강의 슬라이드
   - 통합된 읽기 자료
   - 전체 내용을 아우르는 퀴즈

## 🎓 실전 활용 시나리오

### 시나리오 1: 온라인 강의 수강
```python
# YouTube 강의 3개 + 강의 노트 PDF를 결합
{
    "sources": [
        {"type": "url", "data": "https://youtube.com/watch?v=lecture1"},
        {"type": "url", "data": "https://youtube.com/watch?v=lecture2"},
        {"type": "url", "data": "https://youtube.com/watch?v=lecture3"},
        {"type": "file", "data": "/downloads/lecture_notes.pdf"}
    ],
    "title": "머신러닝 입문 강의"
}
```

### 시나리오 2: 연구 논문 학습
```python
# 논문 PDF + 관련 위키피디아 + 저자 블로그
{
    "sources": [
        {"type": "file", "data": "/papers/transformer_paper.pdf"},
        {"type": "url", "data": "https://en.wikipedia.org/wiki/Transformer_(machine_learning_model)"},
        {"type": "url", "data": "https://jalammar.github.io/illustrated-transformer/"}
    ],
    "title": "Transformer 모델 이해하기"
}
```

### 시나리오 3: 시험 준비
```python
# 교재 PDF + 강의 노트 Word + 참고 웹사이트
{
    "sources": [
        {"type": "file", "data": "/study/textbook.pdf"},
        {"type": "file", "data": "/study/lecture_notes.docx"},
        {"type": "url", "data": "https://www.khanacademy.org/..."},
        {"type": "text", "data": "추가로 암기해야 할 공식들: ..."}
    ],
    "title": "선형대수 중간고사 대비"
}
```

## 🚀 API 완전한 예제

```python
import requests
import time

# 1. 여러 소스로 콘텐츠 생성
response = requests.post("http://localhost:8000/api/learning/generate", json={
    "sources": [
        {
            "type": "url",
            "data": "https://www.youtube.com/watch?v=aircAruvnKk"
        },
        {
            "type": "url",
            "data": "https://en.wikipedia.org/wiki/Neural_network"
        },
        {
            "type": "text",
            "data": """
            신경망 추가 설명:
            - 퍼셉트론: 가장 기본적인 신경망 단위
            - 활성화 함수: ReLU, Sigmoid, Tanh
            - 역전파: 가중치 업데이트 알고리즘
            """
        }
    ],
    "title": "신경망 종합 학습"
})

content_id = response.json()["content_id"]
print(f"생성 시작: {content_id}")

# 2. 진행 상태 확인
while True:
    status = requests.get(f"http://localhost:8000/api/learning/status/{content_id}")
    data = status.json()
    print(f"{data['progress']}% - {data['current_task']}")

    if data['status'] == 'completed':
        break
    time.sleep(5)

# 3. 완성된 콘텐츠 확인
content = requests.get(f"http://localhost:8000/api/learning/{content_id}").json()

print(f"\n✅ 생성 완료!")
print(f"- 팟캐스트: {content['podcast']['audio_url'] if content['podcast'] else 'N/A'}")
print(f"- 강의: {content['video_lecture']['video_url'] if content['video_lecture'] else 'N/A'}")
print(f"- 퀴즈: {len(content['multiple_choice_quizzes'])}개")
```

## ⚠️ 주의사항

### 파일 경로
- **절대 경로** 사용 권장: `/home/user/documents/file.pdf`
- 상대 경로는 Backend 실행 위치 기준

### YouTube 자막
- 한국어 자막 우선, 없으면 영어
- 자막이 없는 비디오는 실패
- 자동 생성 자막도 지원

### 파일 크기
- PDF: 100MB 이하 권장
- Word: 50MB 이하 권장
- 텍스트는 제한 없음

### 토큰 제한
- 너무 많은 소스를 결합하면 Claude API 토큰 제한 초과 가능
- 권장: 5개 이하의 소스
- 각 소스는 15,000자 이하 (자동으로 잘림)

## 💰 비용 고려

여러 소스를 결합해도 **비용은 거의 같습니다**:
- 단일 Claude API 호출로 처리
- 입력 토큰만 약간 증가
- ~$0.25 - $0.35 per 학습 자료 (소스 개수에 따라)

## 🔧 문제 해결

### "파일을 찾을 수 없습니다"
→ 파일 경로 확인, 절대 경로 사용

### "YouTube 자막을 가져올 수 없습니다"
→ 비디오에 자막이 있는지 확인

### "PDF 파싱 실패"
→ 암호화된 PDF는 지원 안 함

### "토큰 제한 초과"
→ 소스 개수 줄이거나, 각 소스의 길이 줄이기
