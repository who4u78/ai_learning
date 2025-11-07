'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Header from '@/components/Header'
import { learningApi, ContentGenerationRequest } from '@/lib/api'

export default function Home() {
  const router = useRouter()
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [contentId, setContentId] = useState<string | null>(null)
  const [progress, setProgress] = useState(0)
  const [message, setMessage] = useState('')
  const [completed, setCompleted] = useState(false)

  const handleGenerate = async () => {
    if (!url.trim()) return

    setLoading(true)
    setProgress(0)
    setMessage('생성 시작...')
    setCompleted(false)

    try {
      const request: ContentGenerationRequest = {
        source_type: 'url',
        source_data: url,
      }

      const status = await learningApi.generateContent(request)
      setContentId(status.content_id)

      // 진행 상태 폴링
      const interval = setInterval(async () => {
        const s = await learningApi.getStatus(status.content_id)
        setProgress(s.progress)
        setMessage(s.current_task || '')

        if (s.status === 'completed') {
          clearInterval(interval)
          setLoading(false)
          setCompleted(true)
          setMessage('완료! 학습 자료가 생성되었습니다.')
        } else if (s.status === 'failed') {
          clearInterval(interval)
          setLoading(false)
          setMessage('생성 실패: ' + (s.error || '알 수 없는 오류'))
        }
      }, 3000)
    } catch (error: any) {
      setLoading(false)
      setMessage('오류: ' + error.message)
    }
  }

  const handleViewContent = () => {
    if (contentId) {
      router.push(`/learn/${contentId}`)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Header />

      <main className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-2xl shadow-2xl p-8">
            <h1 className="text-4xl font-bold text-center mb-4">
              한글 AI 학습 플랫폼 v2.0
            </h1>
            <p className="text-center text-gray-600 mb-8">
              URL이나 텍스트를 입력하면 완전한 학습 자료를 생성합니다
            </p>

            <div className="space-y-4">
              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://example.com/article 또는 학습할 텍스트"
                className="w-full px-6 py-4 border-2 border-gray-300 rounded-lg text-lg focus:border-blue-500 focus:outline-none"
                disabled={loading}
              />

              <button
                onClick={handleGenerate}
                disabled={loading || !url.trim()}
                className="w-full py-4 bg-blue-600 text-white font-bold text-lg rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
              >
                {loading ? '생성 중...' : '학습 자료 생성하기'}
              </button>
            </div>

            {loading && (
              <div className="mt-8">
                <div className="w-full bg-gray-200 rounded-full h-4 mb-2">
                  <div
                    className="bg-blue-600 h-4 rounded-full transition-all duration-500"
                    style={{ width: `${progress}%` }}
                  />
                </div>
                <p className="text-center text-gray-600">{progress}% - {message}</p>
              </div>
            )}

            {contentId && !loading && completed && (
              <div className="mt-8 p-6 bg-green-50 border-2 border-green-200 rounded-lg">
                <h3 className="text-xl font-bold text-green-800 mb-4">✅ 생성 완료!</h3>
                <p className="text-green-700 mb-6">
                  모든 학습 자료가 준비되었습니다! 이제 학습을 시작해보세요.
                </p>
                <button
                  onClick={handleViewContent}
                  className="w-full py-4 bg-green-600 text-white font-bold text-lg rounded-lg hover:bg-green-700 transition-colors mb-3"
                >
                  🎓 학습 시작하기
                </button>
                <div className="text-xs text-gray-600 text-center">
                  콘텐츠 ID: {contentId}
                </div>
              </div>
            )}

            <div className="mt-8 p-6 bg-blue-50 rounded-lg">
              <h3 className="font-bold text-blue-900 mb-2">📦 생성되는 학습 자료:</h3>
              <ul className="space-y-2 text-sm text-blue-800">
                <li>📻 10분 2인 팟캐스트 (진행자 + 게스트)</li>
                <li>🎥 20분+ 강의 비디오 (슬라이드 포함)</li>
                <li>📖 10분 읽기 자료</li>
                <li>💭 심화 사고 질문 3개</li>
                <li>✅ 4지선다형 퀴즈 10문제</li>
                <li>✏️ 단답형 퀴즈 5문제</li>
                <li>📝 서술형 문제 2개</li>
                <li>🤖 실시간 학습 챗봇</li>
              </ul>
            </div>

          </div>
        </div>
      </main>
    </div>
  )
}
