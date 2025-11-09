# 빠른 참조 가이드 (Quick Reference)

## 🚨 긴급 문제 해결

### Windows: Pillow 설치 오류
```powershell
pip cache purge
pip install --no-cache-dir pillow
```

### Fish Audio 설정 안 됨
**.env 파일 확인**:
```
FISH_AUDIO_HOST_VOICE_ID=음성모델ID
FISH_AUDIO_GUEST_VOICE_ID=음성모델ID
```

**음성 모델 ID 찾기**: https://fish.audio/ko-KR/voices

### Backend 서버 실행 안 됨
```bash
# 가상환경 확인
which python  # .venv/bin/python 또는 venv/bin/python이어야 함

# API 키 확인
cat backend/.env | grep ANTHROPIC

# 로그 확인
python -m uvicorn main:app --reload --log-level debug
```

## 📝 .env 파일 템플릿

```bash
# 필수
ANTHROPIC_API_KEY=sk-ant-api03-실제키입력

# 선택 (TTS 사용 시)
FISH_AUDIO_API_KEY=fk_실제키입력
FISH_AUDIO_HOST_VOICE_ID=7d2a7894-xxxx-xxxx-xxxx-xxxxxxxxxxxx
FISH_AUDIO_GUEST_VOICE_ID=a3b4c5d6-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# 기본 설정
HOST=0.0.0.0
PORT=8000
```

## ⚡ 빠른 시작 명령어

### Linux/macOS
```bash
# Backend
cd backend && python3.11 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload

# Frontend (새 터미널)
cd frontend && npm install && npm run dev
```

### Windows
```powershell
# Backend
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn main:app --reload

# Frontend (새 PowerShell)
cd frontend
npm install
npm run dev
```

## 🎯 첫 테스트

### 웹 UI로 테스트
1. http://localhost:3000 접속
2. URL 입력: `https://ko.wikipedia.org/wiki/인공지능`
3. "추가" → "학습 자료 생성하기"
4. 10-15분 대기

### API로 직접 테스트
```bash
curl -X POST http://localhost:8000/api/learning/generate \
  -H "Content-Type: application/json" \
  -d '{"source_type":"url","source_data":"https://ko.wikipedia.org/wiki/인공지능"}'
```

## 🔍 상태 확인

### Backend 동작 확인
```bash
curl http://localhost:8000/health
# 예상 응답: {"status":"ok"}
```

### Frontend 동작 확인
브라우저에서 http://localhost:3000 접속

### API 문서 확인
http://localhost:8000/docs

## 📚 지원하는 파일 형식

| 형식 | 확장자 | 업로드 방법 |
|------|--------|------------|
| PDF | .pdf | 파일 탭 |
| Word | .docx | 파일 탭 |
| Excel | .xlsx, .xls | 파일 탭 |
| PowerPoint | .pptx, .ppt | 파일 탭 |
| Markdown | .md, .qmd | 파일 탭 |
| 텍스트 | .txt | 파일 탭 또는 텍스트 탭 |
| 웹페이지 | URL | URL 탭 |
| YouTube | URL | YouTube 탭 |

## 💰 비용

- **텍스트만**: $0.25/학습자료 (Anthropic만)
- **음성 포함**: $0.55/학습자료 (Anthropic + Fish Audio)

## 🆘 도움말

- **Windows 문제**: [WINDOWS_SETUP.md](WINDOWS_SETUP.md)
- **상세 가이드**: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **다중 소스**: [MULTI_SOURCE_GUIDE.md](MULTI_SOURCE_GUIDE.md)

## 🎓 학습 자료 구성

1. 📖 읽기 자료 (10분)
2. 📻 팟캐스트 (10분, 2인 대화)
3. 🎥 강의 비디오 (20분+, 슬라이드)
4. 💭 심화 질문 (3개)
5. ✅ 4지선다 퀴즈 (10문제)
6. ✏️ 단답형 퀴즈 (5문제)
7. 📝 서술형 퀴즈 (2문제)
8. 🤖 챗봇 (실시간 질문)

## 🔧 자주 쓰는 명령어

```bash
# Backend 재시작
cd backend
source venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload

# Frontend 재시작
cd frontend
npm run dev

# 패키지 재설치
cd backend && pip install -r requirements.txt
cd frontend && npm install

# 로그 확인
# Backend: 터미널 출력
# Frontend: 브라우저 콘솔 (F12)
```

## 📞 긴급 연락

GitHub Issues: [프로젝트 저장소]

---

**마지막 업데이트**: 2024-11
**버전**: v2.0
