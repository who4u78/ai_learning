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

```bash
# 1. API 키 설정
cd backend
cp .env.example .env
nano .env  # ANTHROPIC_API_KEY, FISH_AUDIO_API_KEY 입력

# 2. 의존성 설치
pip install -r requirements.txt
cd ../frontend && npm install

# 3. 실행
cd ..
./start-all.sh

# 4. 접속
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

상세 가이드: [SETUP.md](SETUP.md)

## 📖 문서

- [설치 가이드](SETUP.md)
- [사용 방법](USAGE.md)
- [API 문서](http://localhost:8000/docs)
