# 한글 AI 학습 플랫폼 설치 가이드

## 시스템 요구사항

- Python 3.11+
- Node.js 18+
- FFmpeg (비디오 생성용)
- 최소 4GB RAM

## 1. 저장소 클론

```bash
git clone <repository-url>
cd ai_learning
```

## 2. API 키 설정

### Anthropic API 키 발급

1. [Anthropic Console](https://console.anthropic.com/) 방문
2. API Keys 메뉴에서 새 키 생성
3. 키 복사

### Fish Audio API 키 발급

1. [Fish Audio](https://fish.audio/) 방문
2. 계정 생성 및 로그인
3. API 키 발급

### 환경 변수 설정

```bash
cd backend
cp .env.example .env
```

`.env` 파일을 열어서 API 키 설정:

```env
ANTHROPIC_API_KEY=sk-ant-xxxxx  # 실제 키로 교체
FISH_AUDIO_API_KEY=xxxxx         # 실제 키로 교체
```

## 3. Backend 설정

### 의존성 설치

```bash
cd backend

# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate     # Windows

# 패키지 설치
pip install -r requirements.txt
```

### FFmpeg 설치 (비디오 생성용)

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# https://ffmpeg.org/download.html 에서 다운로드
```

### 한글 폰트 설치 (비디오 자막용)

```bash
# Ubuntu/Debian
sudo apt-get install fonts-nanum fonts-nanum-coding

# macOS
brew install --cask font-nanum-gothic
```

### Backend 서버 실행

```bash
# 개발 모드
uvicorn main:app --reload

# 또는 스크립트 사용
cd ..
./start-backend.sh
```

서버가 시작되면:
- API: http://localhost:8000
- API 문서: http://localhost:8000/docs

## 4. Frontend 설정

```bash
cd frontend

# 의존성 설치
npm install

# 환경 변수 설정
cp .env.local.example .env.local

# 개발 서버 실행
npm run dev

# 또는 스크립트 사용
cd ..
./start-frontend.sh
```

프론트엔드 접속: http://localhost:3000

## 5. 전체 실행 (권장)

모든 서비스를 한 번에 시작:

```bash
./start-all.sh
```

이 스크립트는 tmux를 사용하여 Backend와 Frontend를 동시에 실행합니다.

### tmux 명령어

- 로그 확인: `tmux attach -t ai_learning`
- 윈도우 전환: `Ctrl+B` 그리고 `0` (Backend) 또는 `1` (Frontend)
- 세션 나가기: `Ctrl+B` 그리고 `D`
- 종료: `tmux kill-session -t ai_learning`

## 6. 사용 방법

1. 브라우저에서 http://localhost:3000 접속
2. "콘텐츠 생성" 탭에서:
   - URL 입력 또는 텍스트 입력
   - 옵션 선택 (퀴즈, 요약, 예시)
   - "학습 콘텐츠 생성하기" 클릭
3. 생성 완료 후 "학습하기" 탭으로 자동 전환
4. 섹션별로 학습 콘텐츠 확인
5. "음성 생성" 버튼 클릭하여 TTS 생성
6. "비디오 생성" 버튼 클릭하여 학습 비디오 생성

## 7. 테스트

### Backend API 테스트

```bash
# 헬스 체크
curl http://localhost:8000/health

# API 문서 확인
# 브라우저에서 http://localhost:8000/docs
```

### 샘플 URL 테스트

다음 URL을 사용하여 테스트:
- Wikipedia 문서
- Medium 블로그 글
- 교육용 웹사이트

## 8. 문제 해결

### API 키 오류

```
⚠️  ANTHROPIC_API_KEY를 설정해주세요!
```

→ `backend/.env` 파일에 올바른 API 키를 설정했는지 확인

### 포트 충돌

```
Error: Port 8000 is already in use
```

→ 다른 프로세스가 포트를 사용 중. 종료하거나 `.env`에서 PORT 변경

### FFmpeg 오류

```
ffmpeg: command not found
```

→ FFmpeg 설치 필요 (위 설치 가이드 참조)

### 한글 폰트 오류 (비디오)

→ 한글 폰트 설치 필요 (위 설치 가이드 참조)

### Fish Audio API 오류

Fish Audio API 키가 없어도 개발 모드에서는 더미 오디오 파일이 생성됩니다.
실제 음성이 필요한 경우 Fish Audio 키를 설정하세요.

## 9. 비용 최적화 팁

### Anthropic Claude

- Claude Sonnet 사용 (Opus 대비 1/5 가격)
- `MAX_TOKENS` 설정으로 토큰 제한
- 긴 문서는 요약 후 처리

### Fish Audio

- 필요한 섹션만 음성 생성
- 캐싱 활용

## 10. 프로덕션 배포

### Backend

```bash
# Gunicorn 설치
pip install gunicorn

# 실행
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend

```bash
# 빌드
npm run build

# 실행
npm start
```

### 환경 변수

프로덕션 환경에서는:
- `DEBUG=False`
- `DATABASE_URL` PostgreSQL로 변경
- HTTPS 설정
- CORS 설정 조정

## 다음 단계

- 사용자 인증 추가
- 데이터베이스 연동 (PostgreSQL)
- 클라우드 배포 (AWS, GCP, Vercel)
- 캐싱 시스템 (Redis)
- 백그라운드 작업 큐 (Celery)
