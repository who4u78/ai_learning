#!/usr/bin/env python3
"""
한글 AI 학습 플랫폼 사용 예제

이 스크립트는 API를 사용하여 콘텐츠를 생성하는 방법을 보여줍니다.
"""

import requests
import time
import json

API_URL = "http://localhost:8000"


def check_health():
    """서버 상태 확인"""
    print("🔍 서버 상태 확인 중...")
    try:
        response = requests.get(f"{API_URL}/health")
        data = response.json()
        print(f"✅ 서버 정상: {data}")
        return True
    except Exception as e:
        print(f"❌ 서버 연결 실패: {e}")
        return False


def generate_content_from_url(url: str):
    """URL로부터 콘텐츠 생성"""
    print(f"\n📝 콘텐츠 생성 시작: {url}")

    payload = {
        "source_type": "url",
        "source_data": url,
        "language": "ko",
        "include_quiz": True,
        "include_summary": True,
        "include_examples": True
    }

    try:
        response = requests.post(
            f"{API_URL}/api/content/generate",
            json=payload,
            timeout=300  # 5분 타임아웃
        )
        response.raise_for_status()
        content = response.json()

        print(f"✅ 콘텐츠 생성 완료!")
        print(f"   ID: {content['id']}")
        print(f"   제목: {content['title']}")
        print(f"   섹션 수: {len(content['sections'])}")
        print(f"   퀴즈 수: {len(content.get('quizzes', []))}")

        return content

    except requests.exceptions.Timeout:
        print("❌ 타임아웃: 서버 응답 시간 초과")
    except requests.exceptions.RequestException as e:
        print(f"❌ 요청 실패: {e}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

    return None


def generate_content_from_text(text: str, title: str = None):
    """텍스트로부터 콘텐츠 생성"""
    print(f"\n📝 텍스트 콘텐츠 생성 시작...")

    payload = {
        "source_type": "text",
        "source_data": text,
        "title": title,
        "language": "ko",
        "include_quiz": True,
        "include_summary": True
    }

    try:
        response = requests.post(
            f"{API_URL}/api/content/generate",
            json=payload,
            timeout=300
        )
        response.raise_for_status()
        content = response.json()

        print(f"✅ 콘텐츠 생성 완료!")
        print(f"   ID: {content['id']}")
        print(f"   제목: {content['title']}")

        return content

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return None


def generate_audio(content_id: str):
    """콘텐츠에 대한 음성 생성"""
    print(f"\n🎤 음성 생성 시작...")

    try:
        response = requests.post(
            f"{API_URL}/api/audio/generate-for-content/{content_id}",
            timeout=600  # 10분
        )
        response.raise_for_status()
        audio_data = response.json()

        print(f"✅ 음성 생성 완료!")
        print(f"   생성된 파일 수: {audio_data['total']}")

        for audio_file in audio_data['audio_files']:
            print(f"   - {audio_file['section_title']}: {audio_file['duration']}초")

        return audio_data

    except Exception as e:
        print(f"❌ 음성 생성 실패: {e}")
        return None


def generate_video(content_id: str):
    """콘텐츠에 대한 비디오 생성"""
    print(f"\n🎥 비디오 생성 시작...")

    payload = {
        "content_id": content_id,
        "include_subtitles": True,
        "resolution": "1280x720"
    }

    try:
        response = requests.post(
            f"{API_URL}/api/video/generate",
            json=payload,
            timeout=1800  # 30분
        )
        response.raise_for_status()
        video_data = response.json()

        print(f"✅ 비디오 생성 완료!")
        print(f"   URL: {video_data['video_url']}")
        print(f"   길이: {video_data['duration']}초")
        print(f"   크기: {video_data['size_mb']}MB")

        return video_data

    except Exception as e:
        print(f"❌ 비디오 생성 실패: {e}")
        return None


def main():
    """메인 함수"""
    print("=" * 60)
    print("한글 AI 학습 플랫폼 - 예제 스크립트")
    print("=" * 60)

    # 1. 서버 상태 확인
    if not check_health():
        print("\n서버가 실행되고 있지 않습니다. 먼저 서버를 시작하세요:")
        print("  ./start-backend.sh")
        return

    # 2. 예제 선택
    print("\n예제를 선택하세요:")
    print("1. URL로 콘텐츠 생성")
    print("2. 텍스트로 콘텐츠 생성")
    print("3. 전체 워크플로우 (콘텐츠 + 음성 + 비디오)")

    choice = input("\n선택 (1-3): ").strip()

    if choice == "1":
        url = input("URL을 입력하세요: ").strip()
        if url:
            content = generate_content_from_url(url)
            if content:
                print(f"\n생성된 콘텐츠 ID: {content['id']}")
                print("이 ID로 음성/비디오를 생성할 수 있습니다.")

    elif choice == "2":
        print("\n텍스트를 입력하세요 (Ctrl+D로 완료):")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass

        text = "\n".join(lines)
        title = input("\n제목 (선택사항): ").strip()

        if text:
            content = generate_content_from_text(text, title or None)
            if content:
                print(f"\n생성된 콘텐츠 ID: {content['id']}")

    elif choice == "3":
        # 샘플 텍스트
        sample_text = """
        인공지능의 기초

        인공지능(AI)은 컴퓨터 시스템이 인간의 지능을 모방하도록 만드는 기술입니다.

        주요 개념:
        1. 기계학습: 데이터로부터 패턴을 학습
        2. 딥러닝: 신경망을 활용한 학습
        3. 자연어 처리: 인간의 언어 이해

        인공지능은 의료, 금융, 교육 등 다양한 분야에서 활용되고 있습니다.
        """

        print("\n🚀 전체 워크플로우 시작...")

        # 1단계: 콘텐츠 생성
        content = generate_content_from_text(sample_text, "인공지능의 기초")
        if not content:
            return

        content_id = content['id']

        # 2단계: 음성 생성
        time.sleep(2)
        audio_data = generate_audio(content_id)

        # 3단계: 비디오 생성
        if audio_data:
            time.sleep(2)
            video_data = generate_video(content_id)

        print("\n" + "=" * 60)
        print("✅ 전체 워크플로우 완료!")
        print("=" * 60)
        print(f"콘텐츠 ID: {content_id}")
        print(f"웹에서 확인: http://localhost:3000")
        print("=" * 60)

    else:
        print("잘못된 선택입니다.")


if __name__ == "__main__":
    main()
