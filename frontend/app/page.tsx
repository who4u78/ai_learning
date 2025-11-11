'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import axios from 'axios'
import Header from '@/components/Header'
import MultiSourceInput from '@/components/MultiSourceInput'
import StepByStepGenerator from '@/components/StepByStepGenerator'

export default function Home() {
  const router = useRouter()
  const [phase, setPhase] = useState<'input' | 'generating' | 'completed'>('input')
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [sourceTitle, setSourceTitle] = useState<string>('')

  const handleSourceSubmit = async (sources: any) => {
    try {
      // 세션 시작
      const response = await axios.post('http://localhost:8000/api/learning/start', sources)

      setSessionId(response.data.session_id)
      setSourceTitle(response.data.title)
      setPhase('generating')
    } catch (error) {
      console.error('세션 시작 실패:', error)
      alert('세션 시작에 실패했습니다')
    }
  }

  const handleComplete = () => {
    setPhase('completed')
  }

  const handleReset = () => {
    setPhase('input')
    setSessionId(null)
    setSourceTitle('')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Header />

      <main className="container mx-auto px-4 py-16">
        {phase === 'input' && (
          <div className="max-w-5xl mx-auto">
            <div className="bg-white rounded-2xl shadow-2xl p-8">
              <h1 className="text-4xl font-bold text-center mb-2">
                한글 AI 학습 플랫폼 v2.0
              </h1>
              <p className="text-center text-gray-600 mb-2">
                다양한 소스로 완전한 학습 과정을 단계별로 생성합니다
              </p>
              <p className="text-center text-sm text-blue-600 font-medium mb-8">
                ✨ 하나씩 생성하면서 바로 확인하세요!
              </p>

              {/* Multi-Source Input Component */}
              <MultiSourceInput onComplete={handleSourceSubmit} />

              {/* Info Box */}
              <div className="mt-8 p-6 bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl border-2 border-blue-200">
                <h3 className="font-bold text-blue-900 mb-3 text-lg">📦 단계별 생성:</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div className="flex items-start space-x-2">
                    <span>🎙️</span>
                    <span className="text-sm text-blue-800">1. 팟캐스트</span>
                  </div>
                  <div className="flex items-start space-x-2">
                    <span>🎥</span>
                    <span className="text-sm text-blue-800">2. 강의 슬라이드</span>
                  </div>
                  <div className="flex items-start space-x-2">
                    <span>📖</span>
                    <span className="text-sm text-blue-800">3. 읽기 자료</span>
                  </div>
                  <div className="flex items-start space-x-2">
                    <span>✏️</span>
                    <span className="text-sm text-blue-800">4. 퀴즈</span>
                  </div>
                  <div className="flex items-start space-x-2">
                    <span>🤔</span>
                    <span className="text-sm text-blue-800">5. 심화 질문</span>
                  </div>
                </div>
              </div>

              {/* Supported Sources */}
              <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                <p className="text-sm font-medium text-gray-700 mb-2">지원하는 소스:</p>
                <div className="flex flex-wrap gap-2">
                  {['URL', 'YouTube', 'PDF', 'Word', 'Excel', 'PowerPoint', 'Markdown', 'QMD', '텍스트'].map((format) => (
                    <span key={format} className="px-3 py-1 bg-white border border-gray-200 rounded-full text-xs text-gray-600">
                      {format}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 단계별 생성 화면 */}
        {phase === 'generating' && sessionId && (
          <StepByStepGenerator
            sessionId={sessionId}
            sourceTitle={sourceTitle}
            onComplete={handleComplete}
          />
        )}

        {/* 완료 화면 */}
        {phase === 'completed' && (
          <div className="max-w-3xl mx-auto">
            <div className="bg-white rounded-2xl shadow-2xl p-12 text-center">
              <div className="text-6xl mb-6">🎉</div>
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                모든 학습 자료 생성 완료!
              </h2>
              <p className="text-gray-600 mb-8">
                "{sourceTitle}"의 모든 학습 콘텐츠가 준비되었습니다
              </p>

              <button
                onClick={handleReset}
                className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 font-medium"
              >
                새로운 학습 자료 만들기
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
