# 한글 AI 학습 플랫폼 v2.0

> HTML/텍스트를 **완전한 한글 학습 과정**으로 자동 변환하는 AI 플랫폼
> 
> oboe.fyi 스타일의 종합 학습 경험 제공

## 🎯 주요 기능

### 📻 1. 2인 팟캐스트 (10분)
- 진행자와 게스트의 자연스러운 대화
- Fish Audio TTS로 2개의 다른 음성 생성
- 핵심 개념을 쉽게 설명
- 실생활 예시 포함

### 🎥 2. 강의 비디오 (20분 이상)
- 전문적인 강의 슬라이드 자동 생성 (8-12장)
- 슬라이드와 나레이션이 결합된 비디오
- 논리적 흐름과 시각적 구성
- MP4 포맷, 720p 해상도

### 📖 3. 읽기 자료 (10분 분량)
- 체계적으로 구조화된 텍스트
- 마크다운 형식
- 2500-3000자 분량

### 💭 4. 심화 사고 질문 (3개)
- 비판적 사고를 유도하는 열린 질문
- 맥락과 힌트 제공

### ✅ 5. 다양한 퀴즈
- **4지선다형** (10문제) - 난이도 다양
- **단답형** (5문제) - 핵심 개념 확인
- **서술형** (2문제) - 종합 이해 확인

### 🤖 6. 실시간 학습 챗봇
- Claude API 기반
- 학습 내용을 컨텍스트로 활용
- 즉시 질문하고 답변 받기

## 💰 비용 최적화

- **단일 API 호출**: 모든 자료를 1회의 Claude API 호출로 생성
- **Sonnet 모델**: GPT-4 대비 1/5 가격
- **예상 비용**: ~$0.25 per 학습 자료

## 🚀 빠른 시작

### Linux/macOS
```bash
# 1. API 키 설정
cd backend
cp .env.example .env
nano .env  # ANTHROPIC_API_KEY 입력 (필수), FISH_AUDIO 설정 (선택)

# 2. 의존성 설치
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd ../frontend && npm install

# 3. 실행
# Backend (터미널 1)
cd backend && source venv/bin/activate
python -m uvicorn main:app --reload

# Frontend (터미널 2)
cd frontend && npm run dev

# 4. 접속
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

### Windows
```powershell
# 1. API 키 설정
cd backend
copy .env.example .env
notepad .env  # ANTHROPIC_API_KEY 입력 (필수), FISH_AUDIO 설정 (선택)

# 2. 의존성 설치
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

cd ..\frontend
npm install

# 3. 실행
# Backend (PowerShell 1)
cd backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload

# Frontend (PowerShell 2)
cd frontend
npm run dev
```

**⚠️ Windows 사용자**: Pillow 설치 오류 발생 시 → **[WINDOWS_SETUP.md](WINDOWS_SETUP.md)** 참고

## 📖 문서

### 설치 가이드
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - 상세 설치 가이드 (모든 OS)
- **[WINDOWS_SETUP.md](WINDOWS_SETUP.md)** ⭐ - Windows 전용 가이드 (문제 해결 포함)
- [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) - 기본 설치 방법

### 사용 가이드
- [MULTI_SOURCE_GUIDE.md](MULTI_SOURCE_GUIDE.md) - 다중 소스 사용법
- [FRONTEND_COMPLETE.md](FRONTEND_COMPLETE.md) - 프론트엔드 기능
- [API 문서](http://localhost:8000/docs) - FastAPI 자동 문서

## ✨ 새로운 기능 (v2.0)

### 🎨 완전한 웹 UI
- **학습 대시보드**: 모든 자료를 탭으로 쉽게 전환
- **팟캐스트 플레이어**: 오디오 재생 + 대화 스크립트
- **비디오 플레이어**: 강의 영상 + 슬라이드 네비게이션
- **인터랙티브 퀴즈**: 자동 채점 + 즉시 피드백
- **플로팅 챗봇**: 언제든 질문 가능

### 📚 다양한 소스 지원 (v2.0 신규)
- 🌐 웹 URL (HTML 파싱)
- 📺 YouTube 비디오 (자막 추출)
- 📄 PDF 파일
- 📝 Word 문서 (.docx)
- 📊 **Excel 스프레드시트** (.xlsx, .xls) ⭐ 신규
- 📽️ **PowerPoint 프레젠테이션** (.pptx, .ppt) ⭐ 신규
- 📋 Markdown 문서 (.md, .qmd)
- 📃 일반 텍스트 (.txt)
- 🔗 **여러 소스 결합** (예: YouTube + PDF + PowerPoint)

### 💡 학습 경험
- 읽기 → 듣기 → 보기 → 퀴즈 → 심화 학습
- 각자의 속도로 학습
- 이해 안 되는 부분은 챗봇에 즉시 질문

## 🎯 사용 예시

```bash
# 1. 웹 기사로 학습 자료 생성
URL: https://ko.wikipedia.org/wiki/인공지능
→ 10분 팟캐스트 + 20분 강의 + 퀴즈 + 챗봇

# 2. YouTube + PDF 결합
- YouTube: https://youtube.com/watch?v=xxx
- PDF: lecture_notes.pdf
→ 비디오 자막 + 강의 노트 통합 학습 자료

# 3. 여러 논문 결합
- paper1.pdf + paper2.pdf + paper3.pdf
→ 종합 학습 과정 생성
```

## 🏗️ 아키텍처

```
┌─────────────┐
│  Frontend   │  Next.js 14 + TypeScript + Tailwind
│  (Port 3000)│  - 학습 대시보드
└──────┬──────┘  - 7가지 컴포넌트
       │
       ▼
┌─────────────┐
│   Backend   │  FastAPI + Python 3.11
│  (Port 8000)│  - 콘텐츠 생성
└──────┬──────┘  - 소스 파싱
       │         - TTS/비디오
       ▼
┌─────────────┐
│  AI APIs    │
├─────────────┤
│ Anthropic   │  Claude 3.5 Sonnet (콘텐츠 생성)
│ Fish Audio  │  한글 TTS (2개 음성)
└─────────────┘
```

## 📊 생성 시간

- **소스 파싱**: ~10초
- **AI 콘텐츠 생성**: 1-2분
- **팟캐스트 오디오**: 2-3분
- **강의 비디오**: 5-10분
- **총 소요 시간**: 약 10-15분

## 💵 비용 분석

### 학습 자료 1개당 예상 비용

**필수 비용**:
- **Claude API**: ~$0.25 (단일 API 호출)
  - 읽기 자료, 퀴즈, 질문, 스크립트 생성

**선택 비용** (TTS 사용 시):
- **Fish Audio TTS**: ~$0.10 (10분 팟캐스트)
- **Fish Audio TTS**: ~$0.20 (20분 강의)

**총 비용**:
- **텍스트만**: **$0.25** per 학습 자료
- **음성 포함**: **$0.55** per 학습 자료

### 비용 절감 전략
✅ 모든 텍스트 콘텐츠를 1회 API 호출로 생성 (80% 절감)
✅ Claude Sonnet 사용 (GPT-4 대비 1/5 가격)
✅ TTS 선택적 사용 (테스트 시에는 텍스트만)
✅ 캐싱 활용 (동일 소스 재사용)
