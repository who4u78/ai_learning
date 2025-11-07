# 한글 AI 학습 플랫폼 - 완전 설치 가이드

> 처음부터 끝까지 단계별로 따라하는 상세 가이드

## 📋 목차

1. [시스템 요구사항](#시스템-요구사항)
2. [필수 소프트웨어 설치](#필수-소프트웨어-설치)
3. [프로젝트 설정](#프로젝트-설정)
4. [API 키 발급 및 설정](#api-키-발급-및-설정)
5. [Backend 실행](#backend-실행)
6. [Frontend 실행](#frontend-실행)
7. [첫 번째 테스트](#첫-번째-테스트)
8. [문제 해결](#문제-해결)

---

## 시스템 요구사항

### 최소 사양
- **OS**: Ubuntu 20.04+, macOS 11+, Windows 10+ (WSL2 권장)
- **RAM**: 4GB 이상
- **저장공간**: 10GB 이상
- **인터넷**: 안정적인 연결 (API 호출용)

### 권장 사양
- **RAM**: 8GB 이상
- **CPU**: 4코어 이상
- **저장공간**: 20GB 이상 (비디오 생성 시)

---

## 필수 소프트웨어 설치

### 1. Python 3.11+ 설치

#### Ubuntu/Debian
```bash
# Python 3.11 설치
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev -y

# 버전 확인
python3.11 --version
```

#### macOS
```bash
# Homebrew로 설치
brew install python@3.11

# 버전 확인
python3.11 --version
```

#### Windows (WSL2 사용 권장)
```bash
# WSL2 설치 후 Ubuntu에서
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev -y
```

### 2. Node.js 18+ 설치

#### Ubuntu/Debian
```bash
# NodeSource 저장소 추가
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -

# Node.js 설치
sudo apt-get install -y nodejs

# 버전 확인
node --version  # v18.x.x 이상
npm --version
```

#### macOS
```bash
# Homebrew로 설치
brew install node@18

# 버전 확인
node --version
npm --version
```

### 3. FFmpeg 설치 (비디오 생성용)

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg -y

# 버전 확인
ffmpeg -version
```

#### macOS
```bash
brew install ffmpeg

# 버전 확인
ffmpeg -version
```

### 4. 한글 폰트 설치 (슬라이드 생성용)

#### Ubuntu/Debian
```bash
sudo apt install fonts-nanum fonts-nanum-coding fonts-nanum-extra -y
```

#### macOS
```bash
brew install --cask font-nanum-gothic
```

### 5. Git 설치
```bash
# Ubuntu/Debian
sudo apt install git -y

# macOS
brew install git

# 확인
git --version
```

---

## 프로젝트 설정

### 1. 저장소 클론

```bash
# 원하는 디렉토리로 이동
cd ~

# 프로젝트 클론
git clone https://github.com/YOUR_USERNAME/ai_learning.git
cd ai_learning

# 브랜치 확인
git branch -a
git checkout claude/korean-ai-learning-platform-011CUrU7rAREurFto7CJW2ES
```

### 2. 디렉토리 구조 확인

```bash
ls -la
```

다음과 같은 구조가 보여야 합니다:
```
ai_learning/
├── backend/
├── frontend/
├── data/
├── README.md
├── SETUP.md
├── MULTI_SOURCE_GUIDE.md
└── start-*.sh
```

---

## API 키 발급 및 설정

### 1. Anthropic API 키 발급 (필수)

1. **Anthropic 웹사이트 방문**
   - https://console.anthropic.com/ 접속

2. **계정 생성**
   - 이메일로 가입 (무료)
   - 휴대폰 인증 필요

3. **API 키 생성**
   - 왼쪽 메뉴 "API Keys" 클릭
   - "Create Key" 버튼 클릭
   - 키 이름 입력 (예: "ai-learning")
   - 생성된 키 복사 (한 번만 표시됨!)
   - 형식: `sk-ant-api03-xxxxx...`

4. **크레딧 충전**
   - Settings > Billing
   - 최소 $5 충전 권장
   - 학습 자료 1개당 ~$0.25 소모

### 2. Fish Audio API 키 발급 (선택사항)

> Fish Audio가 없어도 개발 모드로 작동합니다 (더미 오디오 생성)

1. **Fish Audio 웹사이트**
   - https://fish.audio/ 접속

2. **계정 생성 및 키 발급**
   - 회원가입
   - Dashboard > API Keys
   - 키 복사

### 3. 환경 변수 파일 설정

```bash
cd backend

# .env.example을 .env로 복사
cp .env.example .env

# .env 파일 편집
nano .env
# 또는
vim .env
# 또는
code .env  # VS Code 사용 시
```

`.env` 파일 내용:
```env
# API Keys (필수)
ANTHROPIC_API_KEY=sk-ant-api03-여기에_실제_키_입력
FISH_AUDIO_API_KEY=여기에_Fish_Audio_키_입력_또는_비워두기

# Fish Audio 보이스 ID (선택사항)
FISH_AUDIO_HOST_VOICE=korean-male-1
FISH_AUDIO_GUEST_VOICE=korean-female-1

# Server Config
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Database
DATABASE_URL=sqlite:///./ai_learning.db

# File Storage
DATA_DIR=../data
SOURCES_DIR=../data/sources
CONTENT_DIR=../data/content
AUDIO_DIR=../data/audio
VIDEOS_DIR=../data/videos

# AI Settings
AI_MODEL=claude-3-5-sonnet-20241022
MAX_TOKENS=16000
TEMPERATURE=0.7

# CORS
FRONTEND_URL=http://localhost:3000
```

**중요**: `ANTHROPIC_API_KEY`는 반드시 실제 키로 교체!

---

## Backend 실행

### 1. 가상환경 생성 및 활성화

```bash
cd backend

# 가상환경 생성
python3.11 -m venv venv

# 가상환경 활성화
source venv/bin/activate  # Linux/macOS
# 또는
venv\Scripts\activate  # Windows

# 프롬프트가 (venv)로 바뀌면 성공
```

### 2. 의존성 설치

```bash
# requirements.txt의 모든 패키지 설치 (2-3분 소요)
pip install -r requirements.txt

# 설치 확인
pip list | grep anthropic
pip list | grep fastapi
pip list | grep pypdf
```

다음 패키지들이 설치되어야 합니다:
- `anthropic` - Claude API
- `fastapi` - 웹 프레임워크
- `pypdf` - PDF 파싱
- `python-docx` - Word 파싱
- `youtube-transcript-api` - YouTube 자막
- `pydub` - 오디오 처리
- `pillow` - 이미지 생성
- `ffmpeg-python` - 비디오 생성

### 3. 데이터 디렉토리 생성

```bash
# 프로젝트 루트로 이동
cd ..

# 데이터 디렉토리 생성
mkdir -p data/sources data/content data/audio data/videos
```

### 4. Backend 서버 실행

```bash
cd backend

# 개발 서버 실행
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**성공 메시지**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
🚀 AI Learning Platform Backend Started
```

### 5. API 동작 확인

새 터미널을 열어서:

```bash
# Health check
curl http://localhost:8000/health

# 결과:
# {"status":"healthy","anthropic_key_set":true,"fish_audio_key_set":false}
```

브라우저에서 접속:
- API 문서: http://localhost:8000/docs
- 루트: http://localhost:8000/

---

## Frontend 실행

### 1. 새 터미널 열기

Backend는 그대로 두고 **새 터미널**을 엽니다.

```bash
cd ~/ai_learning/frontend
```

### 2. 의존성 설치

```bash
# Node.js 패키지 설치 (2-3분 소요)
npm install

# 설치 확인
npm list react next axios
```

### 3. 환경 변수 설정

```bash
# .env.local.example을 .env.local로 복사
cp .env.local.example .env.local

# 내용 확인 (수정 불필요)
cat .env.local
# NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 4. Frontend 개발 서버 실행

```bash
npm run dev
```

**성공 메시지**:
```
- Local:        http://localhost:3000
- Network:      http://192.168.x.x:3000

✓ Ready in 2.3s
```

### 5. 브라우저에서 확인

- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

---

## 첫 번째 테스트

### 방법 1: Python 스크립트로 테스트 (권장)

새 터미널을 열어서:

```bash
cd ~/ai_learning

# 테스트 스크립트 생성
cat > test_api.py << 'EOF'
import requests
import time

print("=" * 60)
print("한글 AI 학습 플랫폼 테스트")
print("=" * 60)

# 1. Health check
print("\n1. 서버 상태 확인...")
health = requests.get("http://localhost:8000/health").json()
print(f"   - 상태: {health['status']}")
print(f"   - Anthropic 키: {'설정됨' if health['anthropic_key_set'] else '없음'}")
print(f"   - Fish Audio 키: {'설정됨' if health['fish_audio_key_set'] else '없음'}")

# 2. 콘텐츠 생성
print("\n2. 학습 자료 생성 시작...")
response = requests.post("http://localhost:8000/api/learning/generate", json={
    "source_type": "text",
    "source_data": """
    인공지능의 기초

    인공지능(AI)은 컴퓨터가 인간의 지능을 모방하는 기술입니다.

    주요 분야:
    1. 기계학습: 데이터로부터 패턴을 학습하는 기술
    2. 딥러닝: 신경망을 활용한 학습 방법
    3. 자연어 처리: 인간의 언어를 이해하고 생성

    인공지능은 의료, 금융, 교육 등 다양한 분야에서 활용되고 있습니다.
    특히 최근에는 ChatGPT와 같은 대화형 AI가 큰 주목을 받고 있습니다.
    """,
    "title": "인공지능 기초"
})

content_id = response.json()["content_id"]
print(f"   - 콘텐츠 ID: {content_id}")

# 3. 진행 상태 확인
print("\n3. 생성 진행 상황 모니터링...")
while True:
    status = requests.get(f"http://localhost:8000/api/learning/status/{content_id}")
    data = status.json()

    print(f"   [{data['progress']:3d}%] {data['current_task']}")

    if data['status'] == 'completed':
        print("\n✅ 생성 완료!")
        break
    elif data['status'] == 'failed':
        print(f"\n❌ 실패: {data.get('error')}")
        exit(1)

    time.sleep(5)

# 4. 생성된 콘텐츠 확인
print("\n4. 생성된 학습 자료 확인...")
content = requests.get(f"http://localhost:8000/api/learning/{content_id}").json()

print(f"\n📦 생성된 자료:")
print(f"   - 제목: {content['title']}")
print(f"   - 설명: {content['description']}")
print(f"   - 팟캐스트: {'✓' if content.get('podcast') else '✗'}")
if content.get('podcast'):
    print(f"     * 대화 수: {len(content['podcast']['script']['dialogues'])}개")
    print(f"     * 오디오 URL: {content['podcast'].get('audio_url', 'N/A')}")

print(f"   - 강의 비디오: {'✓' if content.get('video_lecture') else '✗'}")
if content.get('video_lecture'):
    print(f"     * 슬라이드 수: {len(content['video_lecture']['slides'])}장")
    print(f"     * 비디오 URL: {content['video_lecture'].get('video_url', 'N/A')}")

print(f"   - 읽기 자료: {'✓' if content.get('reading_material') else '✗'}")
if content.get('reading_material'):
    print(f"     * 읽기 시간: {content['reading_material']['estimated_reading_time']}분")

print(f"   - 심화 질문: {len(content['deep_questions'])}개")
print(f"   - 4지선다 퀴즈: {len(content['multiple_choice_quizzes'])}개")
print(f"   - 단답형 퀴즈: {len(content['short_answer_quizzes'])}개")
print(f"   - 서술형 문제: {len(content['essay_quizzes'])}개")

# 5. 챗봇 테스트
print("\n5. 챗봇 테스트...")
chat_response = requests.post("http://localhost:8000/api/learning/chat", json={
    "content_id": content_id,
    "message": "인공지능의 주요 분야를 간단히 설명해줘",
    "conversation_history": []
})

print(f"   질문: 인공지능의 주요 분야를 간단히 설명해줘")
print(f"   답변: {chat_response.json()['message'][:200]}...")

print("\n" + "=" * 60)
print("✅ 모든 테스트 완료!")
print("=" * 60)
print(f"\n콘텐츠 ID: {content_id}")
print(f"API 문서: http://localhost:8000/docs")
print(f"Frontend: http://localhost:3000")
EOF

# 실행
python3 test_api.py
```

### 방법 2: 웹 인터페이스로 테스트

1. **브라우저에서 접속**
   - http://localhost:3000

2. **URL 또는 텍스트 입력**
   - 예시 URL: `https://en.wikipedia.org/wiki/Machine_learning`
   - 또는 직접 텍스트 입력

3. **"학습 자료 생성하기" 클릭**

4. **진행 상황 확인** (5-10분 소요)
   - 소스 파싱 → AI 생성 → 팟캐스트 → 비디오

5. **완료 후 콘텐츠 ID 확인**

### 방법 3: API 문서에서 테스트

1. **API 문서 접속**
   - http://localhost:8000/docs

2. **POST /api/learning/generate 펼치기**

3. **"Try it out" 클릭**

4. **Request body 입력**:
   ```json
   {
     "source_type": "text",
     "source_data": "인공지능은 컴퓨터가 학습하는 기술입니다.",
     "title": "AI 테스트"
   }
   ```

5. **"Execute" 클릭**

6. **Response에서 `content_id` 복사**

7. **GET /api/learning/status/{content_id}로 상태 확인**

---

## 다중 소스 테스트

### YouTube + Wikipedia 결합

```python
import requests
import time

response = requests.post("http://localhost:8000/api/learning/generate", json={
    "sources": [
        {
            "type": "url",
            "data": "https://www.youtube.com/watch?v=aircAruvnKk"  # 3Blue1Brown
        },
        {
            "type": "url",
            "data": "https://en.wikipedia.org/wiki/Neural_network"
        }
    ],
    "title": "신경망 종합 학습"
})

content_id = response.json()["content_id"]
print(f"생성 시작: {content_id}")

# 진행 상황 확인
while True:
    status = requests.get(f"http://localhost:8000/api/learning/status/{content_id}")
    data = status.json()
    print(f"[{data['progress']}%] {data['current_task']}")

    if data['status'] == 'completed':
        break
    time.sleep(5)

print("✅ 완료!")
```

### PDF 파일 테스트

```python
import requests

# PDF 파일 경로 (절대 경로 사용)
response = requests.post("http://localhost:8000/api/learning/generate", json={
    "source_type": "file",
    "source_data": "/home/user/documents/paper.pdf",
    "title": "논문 학습"
})
```

---

## 문제 해결

### 1. "ModuleNotFoundError: No module named 'anthropic'"

**원인**: 가상환경이 활성화되지 않았거나 패키지 미설치

**해결**:
```bash
cd backend
source venv/bin/activate  # 가상환경 활성화
pip install -r requirements.txt
```

### 2. "ANTHROPIC_API_KEY가 설정되지 않았습니다"

**원인**: `.env` 파일에 API 키가 없음

**해결**:
```bash
cd backend
nano .env
# ANTHROPIC_API_KEY=sk-ant-... 실제 키 입력
```

### 3. "ffmpeg: command not found"

**원인**: FFmpeg 미설치

**해결**:
```bash
# Ubuntu
sudo apt install ffmpeg -y

# macOS
brew install ffmpeg
```

### 4. "한글 폰트를 찾을 수 없습니다"

**원인**: 한글 폰트 미설치

**해결**:
```bash
# Ubuntu
sudo apt install fonts-nanum -y

# macOS
brew install --cask font-nanum-gothic
```

### 5. "Port 8000 is already in use"

**원인**: 이미 다른 프로세스가 8000 포트 사용 중

**해결**:
```bash
# 포트 사용 프로세스 확인
lsof -i :8000

# 프로세스 종료
kill -9 <PID>

# 또는 다른 포트 사용
uvicorn main:app --port 8001
```

### 6. "YouTube 자막을 가져올 수 없습니다"

**원인**: 비디오에 자막이 없음

**해결**:
- 자막이 있는 비디오 사용
- 설정 → 자막 → 한국어/영어 확인

### 7. "콘텐츠 생성 실패: Timeout"

**원인**: Claude API 응답 시간 초과

**해결**:
- 소스 텍스트 길이 줄이기
- 인터넷 연결 확인
- 나중에 다시 시도

### 8. "npm install 실패"

**원인**: Node.js 버전 문제

**해결**:
```bash
# Node.js 버전 확인
node --version  # 18.x 이상이어야 함

# 버전이 낮으면 재설치
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

---

## 개발 워크플로우

### 일반적인 사용 순서

1. **Backend 실행** (터미널 1)
   ```bash
   cd backend
   source venv/bin/activate
   python -m uvicorn main:app --reload
   ```

2. **Frontend 실행** (터미널 2)
   ```bash
   cd frontend
   npm run dev
   ```

3. **테스트** (터미널 3)
   ```bash
   python test_api.py
   ```

### 편리한 스크립트 사용

```bash
# 전체 실행 (tmux 필요)
./start-all.sh

# Backend만
./start-backend.sh

# Frontend만
./start-frontend.sh
```

---

## 다음 단계

설치가 완료되었습니다! 이제:

1. **MULTI_SOURCE_GUIDE.md** - 다양한 소스 사용법
2. **USAGE.md** - API 활용 방법
3. **FRONTEND_TODO.md** - Frontend 개발 가이드

---

## 추가 도움말

### 로그 확인

Backend 로그:
```bash
cd backend
tail -f logs/app.log  # 로그 파일이 있다면
```

Frontend 로그:
- 터미널에서 바로 확인 가능

### 데이터 확인

생성된 파일 위치:
```bash
ls -la data/content/    # 생성된 콘텐츠 JSON
ls -la data/audio/      # 오디오 파일
ls -la data/videos/     # 비디오 파일
```

### API 키 확인

```bash
cd backend
cat .env | grep API_KEY
```

---

## 문의

- GitHub Issues: 문제 보고
- API 문서: http://localhost:8000/docs

---

**축하합니다! 설치 완료!** 🎉
