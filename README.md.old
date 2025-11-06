# 한글 AI 학습 플랫폼

HTML/텍스트 소스를 한글 학습 콘텐츠로 자동 변환하는 AI 플랫폼

## 주요 기능

- 📝 **콘텐츠 생성**: 원본 소스를 분석해 한글 학습 자료 자동 생성
- 🎤 **음성 합성**: Fish Audio TTS로 자연스러운 한글 음성 생성
- 🎥 **비디오 생성**: 텍스트 + 음성 + 시각자료를 결합한 학습 비디오
- 🎓 **인터랙티브 학습**: 퀴즈, 요약, 상세 설명 제공

## 기술 스택

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: Next.js 14 (React)
- **AI**: Anthropic Claude API
- **TTS**: Fish Audio API
- **Video**: FFmpeg
- **Database**: SQLite (개발), PostgreSQL (배포)

## 프로젝트 구조

```
ai_learning/
├── backend/              # FastAPI 서버
│   ├── api/             # API 엔드포인트
│   ├── services/        # 비즈니스 로직
│   │   ├── content_generator.py  # AI 콘텐츠 생성
│   │   ├── tts_service.py        # Fish Audio TTS
│   │   └── video_service.py      # 비디오 생성
│   ├── models/          # 데이터 모델
│   └── utils/           # 유틸리티
├── frontend/            # Next.js 애플리케이션
│   ├── app/            # App Router
│   ├── components/     # React 컴포넌트
│   └── lib/            # 유틸리티
├── data/               # 학습 데이터 저장
│   ├── sources/        # 원본 소스
│   ├── content/        # 생성된 콘텐츠
│   ├── audio/          # 음성 파일
│   └── videos/         # 비디오 파일
└── docs/               # 문서

```

## 로컬 개발 시작

### 1. Backend 설정

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # API 키 설정
uvicorn main:app --reload
```

### 2. Frontend 설정

```bash
cd frontend
npm install
npm run dev
```

### 3. 환경 변수 설정

`.env` 파일에 필요한 API 키 설정:
- `ANTHROPIC_API_KEY`: Claude API 키
- `FISH_AUDIO_API_KEY`: Fish Audio API 키

## 사용 방법

1. 학습 소스 URL 또는 HTML 파일 업로드
2. AI가 콘텐츠 분석 및 한글 학습 자료 생성
3. 음성 합성 및 비디오 생성
4. 웹 인터페이스에서 학습

## 개발 로드맵

- [x] 프로젝트 구조 설계
- [ ] Backend API 구현
- [ ] AI 콘텐츠 생성 서비스
- [ ] Fish Audio TTS 통합
- [ ] 비디오 생성 파이프라인
- [ ] Frontend UI 구현
- [ ] 통합 테스트

## 라이선스

MIT
