# 한글 AI 학습 플랫폼 v2.0 - 완전 설치 가이드

> 처음부터 끝까지 단계별로 따라하는 상세 설치 및 사용 가이드

## 📋 목차

1. [시스템 요구사항](#1-시스템-요구사항)
2. [필수 소프트웨어 설치](#2-필수-소프트웨어-설치)
3. [프로젝트 다운로드](#3-프로젝트-다운로드)
4. [API 키 발급 및 설정](#4-api-키-발급-및-설정)
5. [Backend 설정 및 실행](#5-backend-설정-및-실행)
6. [Frontend 설정 및 실행](#6-frontend-설정-및-실행)
7. [첫 번째 학습 자료 생성](#7-첫-번째-학습-자료-생성)
8. [다중 소스 사용하기](#8-다중-소스-사용하기)
9. [문제 해결](#9-문제-해결)
10. [고급 사용법](#10-고급-사용법)

---

## 1. 시스템 요구사항

### 최소 사양
- **OS**:
  - Ubuntu 20.04+ (권장)
  - macOS 11+
  - Windows 10+ (WSL2 권장)
- **RAM**: 4GB 이상
- **저장공간**: 10GB 이상
- **인터넷**: 안정적인 연결 (API 호출용)

### 권장 사양
- **RAM**: 8GB 이상
- **CPU**: 4코어 이상
- **저장공간**: 20GB 이상 (비디오/오디오 파일용)
- **GPU**: 선택사항 (비디오 생성 가속용)

---

## 2. 필수 소프트웨어 설치

### 2.1. Python 3.11+ 설치

#### Ubuntu/Debian
```bash
# Python 3.11 설치
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev python3-pip -y

# 버전 확인
python3.11 --version
```

#### macOS
```bash
# Homebrew로 설치 (Homebrew 없으면 먼저 설치)
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install python@3.11

# 버전 확인
python3.11 --version
```

#### Windows (WSL2)
```bash
# PowerShell을 관리자 권한으로 실행
wsl --install

# WSL2 Ubuntu에서
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev python3-pip -y
```

### 2.2. Node.js 18+ 설치

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

#### Windows (WSL2)
```bash
# WSL2 Ubuntu에서 위의 Ubuntu 명령어 사용
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 2.3. FFmpeg 설치 (비디오 생성용)

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

#### Windows (WSL2)
```bash
sudo apt update
sudo apt install ffmpeg -y
```

### 2.4. Git 설치

#### Ubuntu/Debian
```bash
sudo apt install git -y
git --version
```

#### macOS
```bash
brew install git
git --version
```

---

## 3. 프로젝트 다운로드

### 3.1. Git Clone

```bash
# 원하는 디렉토리로 이동
cd ~

# 프로젝트 클론 (실제 저장소 URL로 변경)
git clone https://github.com/yourusername/ai_learning.git

# 프로젝트 디렉토리로 이동
cd ai_learning

# 파일 구조 확인
ls -la
# backend/   frontend/   README.md   등이 보여야 함
```

### 3.2. ZIP 다운로드 방식 (Git 없는 경우)

1. GitHub에서 "Code" → "Download ZIP" 클릭
2. 압축 해제
3. 터미널에서 압축 해제된 폴더로 이동

---

## 4. API 키 발급 및 설정

### 4.1. Anthropic API 키 발급 (Claude)

**중요**: Claude API는 유료 서비스입니다. 신용카드 등록이 필요합니다.

#### 단계별 가이드

1. **Anthropic Console 접속**
   - https://console.anthropic.com 방문
   - "Sign Up" 클릭하여 계정 생성

2. **API 키 생성**
   - 로그인 후 "API Keys" 메뉴 클릭
   - "Create Key" 버튼 클릭
   - 키 이름 입력 (예: "ai-learning-platform")
   - **생성된 키를 반드시 복사하여 저장** (다시 볼 수 없음!)

3. **비용 확인**
   - Settings → Billing 에서 사용량 확인 가능
   - Claude 3.5 Sonnet: 입력 $3/MTok, 출력 $15/MTok
   - 학습 자료 1개당 약 $0.25 예상

#### API 키 형식
```
sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 4.2. Fish Audio API 키 발급 (TTS)

**선택사항**: TTS를 사용하려면 필요합니다.

1. **Fish Audio 접속**
   - https://fish.audio 방문
   - 계정 생성

2. **API 키 발급**
   - Dashboard → API Keys
   - "Create New Key" 클릭
   - 키 복사

### 4.3. 환경 변수 설정

```bash
# backend 디렉토리로 이동
cd ~/ai_learning/backend

# .env.example 파일 복사
cp .env.example .env

# .env 파일 편집
nano .env
# 또는 vi .env
# 또는 code .env (VS Code)
```

#### .env 파일 내용 (예시)

```bash
# Anthropic API (필수)
ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here

# Fish Audio API (선택 - TTS용)
FISH_AUDIO_API_KEY=your-fish-audio-key-here
FISH_AUDIO_HOST_VOICE_ID=your-host-voice-id
FISH_AUDIO_GUEST_VOICE_ID=your-guest-voice-id

# 서버 설정
API_HOST=0.0.0.0
API_PORT=8000

# 데이터 저장 경로
DATA_DIR=./data
OUTPUT_DIR=./output

# 로그 레벨
LOG_LEVEL=INFO
```

**저장 방법**:
- nano 사용 시: `Ctrl + O` (저장) → `Enter` → `Ctrl + X` (종료)
- vi 사용 시: `ESC` → `:wq` → `Enter`

---

## 5. Backend 설정 및 실행

### 5.1. Python 가상환경 생성

```bash
# backend 디렉토리에 있는지 확인
cd ~/ai_learning/backend

# 가상환경 생성
python3.11 -m venv venv

# 가상환경 활성화
# Linux/macOS:
source venv/bin/activate

# Windows (WSL2):
source venv/bin/activate

# (venv) 표시가 나타나야 함
```

### 5.2. Python 패키지 설치

```bash
# 가상환경이 활성화된 상태에서
pip install --upgrade pip

# 모든 의존성 설치 (5-10분 소요)
pip install -r requirements.txt

# 설치 확인
pip list | grep -E "(fastapi|anthropic|openpyxl|python-pptx)"
```

**설치되는 주요 패키지**:
- `fastapi` - 웹 API 프레임워크
- `anthropic` - Claude API 클라이언트
- `openpyxl` - Excel 파일 파싱
- `python-pptx` - PowerPoint 파일 파싱
- `pypdf` - PDF 파일 파싱
- `python-docx` - Word 파일 파싱
- `youtube-transcript-api` - YouTube 자막 추출
- `ffmpeg-python` - 비디오 생성
- `pillow` - 이미지 처리

### 5.3. Backend 서버 실행

```bash
# backend 디렉토리에서 실행
cd ~/ai_learning/backend

# 가상환경 활성화 (이미 활성화되어 있지 않다면)
source venv/bin/activate

# 서버 실행
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**성공 메시지**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 5.4. API 동작 확인

**새 터미널을 열어서 테스트**:

```bash
# Health check
curl http://localhost:8000/health

# 예상 응답: {"status":"ok"}

# API 문서 확인
# 브라우저에서 http://localhost:8000/docs 접속
```

---

## 6. Frontend 설정 및 실행

### 6.1. 새 터미널 열기

Backend는 계속 실행 중이어야 하므로, **새 터미널**을 엽니다.

```bash
# frontend 디렉토리로 이동
cd ~/ai_learning/frontend
```

### 6.2. Node 패키지 설치

```bash
# package.json 확인
cat package.json

# npm 패키지 설치 (3-5분 소요)
npm install

# 설치 확인
npm list react next axios
```

### 6.3. 환경 변수 설정 (선택)

```bash
# frontend/.env.local 파일 생성 (필요시)
cat > .env.local << 'EOF'
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF
```

### 6.4. Frontend 개발 서버 실행

```bash
# frontend 디렉토리에서
npm run dev
```

**성공 메시지**:
```
- ready started server on 0.0.0.0:3000, url: http://localhost:3000
- event compiled client and server successfully
```

### 6.5. 브라우저에서 접속

브라우저를 열고 다음 주소로 접속:

```
http://localhost:3000
```

**화면에 보여야 할 것**:
- "한글 AI 학습 플랫폼 v2.0" 제목
- 소스 입력 탭 (URL, YouTube, 파일, 텍스트)
- 생성되는 학습 자료 목록

---

## 7. 첫 번째 학습 자료 생성

### 7.1. 간단한 URL 테스트

1. **브라우저에서 http://localhost:3000 접속**

2. **"URL" 탭 선택** (기본값)

3. **테스트 URL 입력**:
   ```
   https://ko.wikipedia.org/wiki/인공지능
   ```

4. **"추가" 버튼 클릭**

5. **"1개 소스로 학습 자료 생성하기" 클릭**

6. **진행 상황 확인**:
   - 0% - 소스 파싱 중...
   - 20% - AI 콘텐츠 생성 중...
   - 50% - 팟캐스트 오디오 생성 중...
   - 70% - 강의 비디오 생성 중...
   - 100% - 완료!

7. **예상 시간**: 10-15분

8. **"학습 시작하기" 버튼 클릭**

9. **학습 대시보드 확인**:
   - 📖 읽기 자료 탭
   - 📻 팟캐스트 탭
   - 🎥 강의 비디오 탭
   - ✅ 퀴즈 탭
   - 💭 심화 질문 탭

### 7.2. 터미널에서 직접 테스트 (선택)

```bash
# 새 터미널 열기
cd ~/ai_learning

# 테스트 스크립트 생성
cat > test_simple.py << 'EOF'
import requests
import time

# 1. 학습 자료 생성 요청
response = requests.post('http://localhost:8000/api/learning/generate', json={
    "source_type": "url",
    "source_data": "https://ko.wikipedia.org/wiki/인공지능"
})

data = response.json()
content_id = data['content_id']
print(f"생성 시작! Content ID: {content_id}")

# 2. 상태 확인 (폴링)
while True:
    status_response = requests.get(f'http://localhost:8000/api/learning/status/{content_id}')
    status = status_response.json()

    print(f"{status['progress']}% - {status['current_task']}")

    if status['status'] == 'completed':
        print("\n✅ 생성 완료!")
        break
    elif status['status'] == 'failed':
        print(f"\n❌ 실패: {status.get('error')}")
        break

    time.sleep(3)

# 3. 학습 자료 조회
content_response = requests.get(f'http://localhost:8000/api/learning/{content_id}')
content = content_response.json()

print(f"\n제목: {content['title']}")
print(f"설명: {content['description']}")
print(f"팟캐스트: {content['podcast']['script']['title']}")
print(f"퀴즈 개수: {len(content['multiple_choice_quizzes'])}")
EOF

# 실행
python test_simple.py
```

---

## 8. 다중 소스 사용하기

### 8.1. 여러 파일 업로드

#### 예시 1: 여러 PDF 결합

1. **"파일" 탭 클릭**

2. **"파일 선택" 클릭**

3. **여러 PDF 파일 선택** (Ctrl+클릭으로 다중 선택)
   - paper1.pdf
   - paper2.pdf
   - paper3.pdf

4. **선택된 파일 목록 확인**

5. **"3개 소스로 학습 자료 생성하기" 클릭**

#### 예시 2: YouTube + PDF

1. **"YouTube" 탭 클릭**

2. **YouTube URL 입력**:
   ```
   https://www.youtube.com/watch?v=xxx
   ```

3. **"추가" 클릭**

4. **"파일" 탭 클릭**

5. **PDF 파일 선택**

6. **"2개 소스로 학습 자료 생성하기" 클릭**

#### 예시 3: 다양한 소스 믹스

1. URL 추가
2. PowerPoint 파일 추가
3. 텍스트 추가 (보충 설명)
4. 모두 결합하여 생성

### 8.2. 지원하는 파일 형식

| 형식 | 확장자 | 설명 |
|------|--------|------|
| PDF | `.pdf` | Adobe PDF 문서 |
| Word | `.docx`, `.doc` | Microsoft Word |
| Excel | `.xlsx`, `.xls` | Microsoft Excel |
| PowerPoint | `.pptx`, `.ppt` | Microsoft PowerPoint |
| Markdown | `.md`, `.markdown` | 마크다운 문서 |
| Quarto | `.qmd` | Quarto 마크다운 |
| Text | `.txt` | 일반 텍스트 |
| HTML | `.html`, `.htm` | HTML 문서 |
| YouTube | URL | 자막 추출 |
| 웹페이지 | URL | HTML 파싱 |

### 8.3. API로 다중 소스 사용

```python
# test_multi_source.py
import requests

# 방법 1: 파일 업로드
files = [
    ('files', open('document1.pdf', 'rb')),
    ('files', open('document2.pdf', 'rb')),
    ('files', open('slides.pptx', 'rb'))
]

response = requests.post(
    'http://localhost:8000/api/learning/upload',
    files=files
)

print(response.json())

# 방법 2: URL/텍스트 결합
response = requests.post(
    'http://localhost:8000/api/learning/generate',
    json={
        "sources": [
            {"type": "url", "data": "https://example.com/article"},
            {"type": "text", "data": "추가 설명 텍스트..."}
        ]
    }
)

print(response.json())
```

---

## 9. 문제 해결

### 9.1. Backend 오류

#### 오류: `ModuleNotFoundError: No module named 'xxx'`

**원인**: 패키지가 설치되지 않음

**해결**:
```bash
cd ~/ai_learning/backend
source venv/bin/activate
pip install -r requirements.txt
```

#### 오류: `anthropic.AuthenticationError`

**원인**: API 키가 잘못되었거나 설정되지 않음

**해결**:
```bash
# .env 파일 확인
cat backend/.env

# API 키가 올바른지 확인
# sk-ant-api03-로 시작해야 함
```

#### 오류: `Port 8000 already in use`

**원인**: 포트가 이미 사용 중

**해결**:
```bash
# 기존 프로세스 종료
sudo lsof -ti:8000 | xargs kill -9

# 또는 다른 포트 사용
python -m uvicorn main:app --port 8001
```

### 9.2. Frontend 오류

#### 오류: `ECONNREFUSED 127.0.0.1:8000`

**원인**: Backend 서버가 실행되지 않음

**해결**:
1. Backend 터미널 확인
2. Backend 서버 재시작

#### 오류: `npm ERR! code ENOENT`

**원인**: package.json이 없거나 경로가 잘못됨

**해결**:
```bash
cd ~/ai_learning/frontend
ls package.json  # 파일 존재 확인
npm install
```

### 9.3. 파일 파싱 오류

#### 오류: `openpyxl not installed`

**해결**:
```bash
cd ~/ai_learning/backend
source venv/bin/activate
pip install openpyxl python-pptx
```

#### 오류: YouTube 자막 추출 실패

**원인**:
- 자막이 없는 비디오
- 비공개 비디오
- 지역 제한

**해결**: 자막이 있는 공개 비디오 사용

### 9.4. 메모리 부족

**증상**:
- 비디오 생성 중 프로세스 종료
- "Killed" 메시지

**해결**:
```bash
# 스왑 메모리 확인
free -h

# 스왑 증가 (Ubuntu)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## 10. 고급 사용법

### 10.1. 백그라운드 실행

#### PM2 사용 (권장)

```bash
# PM2 설치
npm install -g pm2

# Backend 백그라운드 실행
cd ~/ai_learning/backend
source venv/bin/activate
pm2 start "uvicorn main:app --host 0.0.0.0 --port 8000" --name ai-backend

# Frontend 백그라운드 실행
cd ~/ai_learning/frontend
pm2 start npm --name ai-frontend -- start

# 상태 확인
pm2 status

# 로그 확인
pm2 logs

# 재시작
pm2 restart all

# 부팅 시 자동 시작
pm2 startup
pm2 save
```

### 10.2. 프로덕션 빌드

```bash
# Frontend 빌드
cd ~/ai_learning/frontend
npm run build
npm start  # 프로덕션 모드

# Backend (Gunicorn 사용)
cd ~/ai_learning/backend
source venv/bin/activate
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 10.3. 환경별 설정

#### 개발 환경
```bash
# backend/.env
LOG_LEVEL=DEBUG
DEBUG=true
```

#### 프로덕션 환경
```bash
# backend/.env
LOG_LEVEL=WARNING
DEBUG=false
```

### 10.4. 데이터 백업

```bash
# 생성된 학습 자료 백업
cd ~/ai_learning/backend
tar -czf backup_$(date +%Y%m%d).tar.gz data/ output/

# 복원
tar -xzf backup_20240315.tar.gz
```

---

## 📊 성능 최적화

### 비용 절감 팁

1. **캐싱 활용**: 동일 소스는 재사용
2. **소스 길이 제한**: 너무 긴 텍스트는 요약 후 사용
3. **TTS 선택적 사용**: 필요한 경우만 오디오 생성

### 속도 개선

1. **SSD 사용**: 비디오 생성 속도 향상
2. **RAM 증가**: 8GB 이상 권장
3. **멀티코어 CPU**: 병렬 처리

---

## 🎓 다음 단계

1. ✅ 기본 설치 완료
2. ✅ 첫 학습 자료 생성
3. ⬜ 다양한 소스 타입 테스트
4. ⬜ 커스터마이징 (프롬프트 수정 등)
5. ⬜ 프로덕션 배포

---

## 📞 도움말

### 문서
- [다중 소스 가이드](MULTI_SOURCE_GUIDE.md)
- [Frontend 가이드](FRONTEND_COMPLETE.md)
- [API 문서](http://localhost:8000/docs)

### 문제 발생 시
1. 로그 확인: `backend/logs/`
2. GitHub Issues 검색
3. API 키 재확인

---

## ✅ 설치 체크리스트

- [ ] Python 3.11+ 설치 완료
- [ ] Node.js 18+ 설치 완료
- [ ] FFmpeg 설치 완료
- [ ] 프로젝트 다운로드 완료
- [ ] Anthropic API 키 발급 완료
- [ ] .env 파일 설정 완료
- [ ] Backend 패키지 설치 완료
- [ ] Frontend 패키지 설치 완료
- [ ] Backend 서버 실행 성공
- [ ] Frontend 서버 실행 성공
- [ ] 브라우저 접속 성공
- [ ] 첫 학습 자료 생성 성공

**모든 항목 완료 시 설치 성공! 🎉**

---

**마지막 업데이트**: 2024-11
**버전**: v2.0
**지원**: 다중 소스, Excel, PowerPoint, Markdown, QMD
