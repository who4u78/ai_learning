# Windows 설치 문제 해결 가이드

## 발생한 문제들과 해결 방법

### 1. Pillow 설치 오류

#### 문제
```
ERROR: Failed to build 'pillow' when getting requirements to build wheel
KeyError: '__version__'
```

#### 원인
- Pillow 10.2.0이 Windows에서 소스 빌드 시 문제 발생
- C 컴파일러가 없거나 빌드 도구가 부족

#### 해결 방법

**방법 1: requirements.txt 수정 (이미 적용됨)**
```bash
# requirements.txt에서 pillow 버전을 수정
pillow>=10.2.0  # 최신 버전 사용
```

**방법 2: pip 캐시 삭제 후 재설치**
```powershell
# PowerShell에서 실행
pip cache purge
pip install --no-cache-dir pillow
```

**방법 3: 사전 빌드된 휠 사용**
```powershell
pip install --only-binary :all: pillow
```

**방법 4: Microsoft Visual C++ 설치** (근본적 해결)
1. Visual Studio Build Tools 다운로드
   - https://visualstudio.microsoft.com/downloads/
   - "Build Tools for Visual Studio" 선택

2. 설치 시 "C++ 빌드 도구" 선택

3. 설치 후 재부팅

4. 다시 설치
   ```powershell
   pip install -r requirements.txt
   ```

### 2. Fish Audio 음성 모델 ID 설정

#### 문제
- `.env` 파일에 음성 모델 ID가 설정되지 않음
- 팟캐스트/강의 음성 생성이 불가능

#### 해결 방법

**1단계: Fish Audio 계정 생성**
```
1. https://fish.audio 접속
2. 회원가입 (Google 계정 연동 가능)
3. 로그인
```

**2단계: API 키 발급**
```
1. Dashboard → Settings → API Keys
2. "Create New Key" 클릭
3. API 키 복사
```

**3단계: 음성 모델 선택**
```
1. https://fish.audio/ko-KR/voices 접속
2. 한국어 음성 모델 찾기
3. 원하는 음성 2개 선택 (진행자용, 게스트용)
4. 각 음성의 "Model ID" 복사
```

**음성 모델 예시**:
- 진행자 (남성): `7d2a7894-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- 게스트 (여성): `a3b4c5d6-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

**4단계: .env 파일 설정**
```bash
# backend/.env 파일

# Fish Audio TTS
FISH_AUDIO_API_KEY=your-actual-api-key-here

# 진행자 음성 모델 ID (예: 남성 목소리)
FISH_AUDIO_HOST_VOICE_ID=7d2a7894-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# 게스트 음성 모델 ID (예: 여성 목소리)
FISH_AUDIO_GUEST_VOICE_ID=a3b4c5d6-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

**5단계: 설정 확인**
```powershell
# backend 디렉토리에서
python
>>> import os
>>> from dotenv import load_dotenv
>>> load_dotenv()
>>> os.getenv("FISH_AUDIO_HOST_VOICE_ID")
'7d2a7894-xxxx-xxxx-xxxx-xxxxxxxxxxxx'  # 값이 나와야 함
>>> exit()
```

#### TTS 없이 사용하기 (선택)

Fish Audio를 사용하지 않고 텍스트만으로 테스트하려면:

```bash
# .env 파일에서 주석 처리
# FISH_AUDIO_API_KEY=
# FISH_AUDIO_HOST_VOICE_ID=
# FISH_AUDIO_GUEST_VOICE_ID=
```

이 경우:
- 팟캐스트 스크립트는 생성되지만 음성은 생성 안 됨
- 강의 비디오는 슬라이드만 생성됨 (나레이션 없음)
- 읽기 자료, 퀴즈 등은 정상 작동

### 3. Frontend npm 경고

#### 문제
```
3 moderate severity vulnerabilities
npm warn deprecated...
```

#### 설명
- 대부분 **개발 의존성(dev dependencies)** 패키지의 경고
- 실제 프로덕션에는 영향 없음
- ESLint 등의 도구 버전 문제

#### 해결 방법

**무시해도 됨**: 개발에는 문제 없음

**업데이트하려면**:
```powershell
# 보안 취약점 자동 수정
npm audit fix

# 또는 강제 업데이트 (주의: breaking changes 발생 가능)
npm audit fix --force
```

**권장사항**:
- 현재 상태로 개발 진행
- 안정화 후 업데이트

### 4. PowerShell 실행 정책 오류

#### 문제
```
venv\Scripts\activate : ... 이 시스템에서 스크립트를 실행할 수 없으므로
```

#### 해결
```powershell
# PowerShell을 관리자 권한으로 실행
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 가상환경 활성화
.\.venv\Scripts\Activate.ps1
```

### 5. FFmpeg 설치 (Windows)

#### Chocolatey 사용 (권장)
```powershell
# 1. Chocolatey 설치 (관리자 PowerShell)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 2. FFmpeg 설치
choco install ffmpeg
```

#### 수동 설치
```
1. https://www.gyan.dev/ffmpeg/builds/ 접속
2. "ffmpeg-release-essentials.zip" 다운로드
3. 압축 해제 (예: C:\ffmpeg)
4. 환경 변수 PATH에 추가: C:\ffmpeg\bin
5. PowerShell 재시작 후 확인:
   ffmpeg -version
```

---

## 완전한 Windows 설치 프로세스

### 1단계: 기본 도구 설치
```powershell
# PowerShell 관리자 권장으로 실행

# Python 3.11 (python.org에서 다운로드)
# 설치 시 "Add Python to PATH" 체크!

# Node.js 18+ (nodejs.org에서 다운로드)
# LTS 버전 권장

# Git (git-scm.com에서 다운로드)
```

### 2단계: 프로젝트 클론
```powershell
cd C:\Projects
git clone <repository-url> ai_learning
cd ai_learning
```

### 3단계: Backend 설정
```powershell
cd backend

# 가상환경 생성
python -m venv .venv

# 가상환경 활성화
.\.venv\Scripts\Activate.ps1

# pip 업그레이드
python -m pip install --upgrade pip

# 의존성 설치
pip install -r requirements.txt

# .env 파일 설정
copy .env.example .env
notepad .env  # API 키 입력
```

### 4단계: .env 파일 편집
```
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here

FISH_AUDIO_API_KEY=your-fish-audio-key
FISH_AUDIO_HOST_VOICE_ID=host-voice-model-id
FISH_AUDIO_GUEST_VOICE_ID=guest-voice-model-id
```

### 5단계: Backend 실행
```powershell
python -m uvicorn main:app --reload
```

성공 시:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 6단계: Frontend 설정 (새 PowerShell)
```powershell
cd C:\Projects\ai_learning\frontend

npm install

# 환경 변수 (선택)
echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local

npm run dev
```

성공 시:
```
- ready started server on 0.0.0.0:3000
```

### 7단계: 브라우저 접속
```
http://localhost:3000
```

---

## 자주 묻는 질문 (FAQ)

### Q1: "python: command not found"
**A**: Python이 PATH에 없습니다.
- Python 재설치 시 "Add Python to PATH" 체크
- 또는 수동으로 환경 변수 추가

### Q2: "ffmpeg: command not found"
**A**: FFmpeg가 설치되지 않았거나 PATH에 없습니다.
- 위의 FFmpeg 설치 방법 참고

### Q3: "Port 8000 already in use"
**A**: 다른 프로그램이 포트 사용 중
```powershell
# 사용 중인 프로세스 찾기
netstat -ano | findstr :8000

# 프로세스 종료
taskkill /PID <PID번호> /F

# 또는 다른 포트 사용
python -m uvicorn main:app --port 8001
```

### Q4: TTS 없이 테스트 가능한가?
**A**: 네, 가능합니다.
- Fish Audio 설정 없이도 텍스트 자료는 모두 생성됨
- 음성/비디오만 스킵됨

### Q5: 비용은 얼마나 드나요?
**A**:
- Anthropic API: 학습 자료 1개당 약 $0.25
- Fish Audio (선택): 학습 자료 1개당 약 $0.30
- 총: 약 $0.55 per 학습 자료

---

## 트러블슈팅 체크리스트

- [ ] Python 3.11+ 설치 확인: `python --version`
- [ ] Node.js 18+ 설치 확인: `node --version`
- [ ] FFmpeg 설치 확인: `ffmpeg -version`
- [ ] 가상환경 활성화: `(.venv)` 표시 확인
- [ ] .env 파일 존재: `backend\.env`
- [ ] Anthropic API 키 입력: 실제 값 확인
- [ ] Fish Audio API 키 입력 (선택)
- [ ] Fish Audio 음성 모델 ID 입력 (선택)
- [ ] Backend 실행: http://localhost:8000/docs 접속 가능
- [ ] Frontend 실행: http://localhost:3000 접속 가능

모든 항목 확인 후에도 문제가 있다면:
1. Backend 로그 확인
2. Frontend 콘솔 확인
3. GitHub Issues 검색

---

**최종 업데이트**: 2024-11
**테스트 환경**: Windows 10/11, Python 3.11, Node.js 18
