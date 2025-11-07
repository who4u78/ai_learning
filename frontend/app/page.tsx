'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Header from '@/components/Header'
import MultiSourceInput from '@/components/MultiSourceInput'

export default function Home() {
  const router = useRouter()
  const [completed, setCompleted] = useState(false)
  const [contentId, setContentId] = useState<string | null>(null)

  const handleComplete = (newContentId: string) => {
    setContentId(newContentId)
    setCompleted(true)
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
        <div className="max-w-5xl mx-auto">
          <div className="bg-white rounded-2xl shadow-2xl p-8">
            <h1 className="text-4xl font-bold text-center mb-2">
              한글 AI 학습 플랫폼 v2.0
            </h1>
            <p className="text-center text-gray-600 mb-2">
              다양한 소스로 완전한 학습 과정을 자동 생성합니다
            </p>
            <p className="text-center text-sm text-blue-600 font-medium mb-8">
              ✨ 여러 소스를 결합하여 하나의 학습 자료 생성 가능!
            </p>

            {/* Multi-Source Input Component */}
            {!completed && <MultiSourceInput onComplete={handleComplete} />}

            {/* Completion Message */}
            {completed && contentId && (
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

            {/* Info Box */}
            <div className="mt-8 p-6 bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl border-2 border-blue-200">
              <h3 className="font-bold text-blue-900 mb-3 text-lg">📦 생성되는 학습 자료:</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div className="flex items-start space-x-2">
                  <span>📻</span>
                  <span className="text-sm text-blue-800">10분 2인 팟캐스트</span>
                </div>
                <div className="flex items-start space-x-2">
                  <span>🎥</span>
                  <span className="text-sm text-blue-800">20분+ 강의 비디오</span>
                </div>
                <div className="flex items-start space-x-2">
                  <span>📖</span>
                  <span className="text-sm text-blue-800">10분 읽기 자료</span>
                </div>
                <div className="flex items-start space-x-2">
                  <span>💭</span>
                  <span className="text-sm text-blue-800">심화 사고 질문 3개</span>
                </div>
                <div className="flex items-start space-x-2">
                  <span>✅</span>
                  <span className="text-sm text-blue-800">4지선다 퀴즈 10문제</span>
                </div>
                <div className="flex items-start space-x-2">
                  <span>✏️</span>
                  <span className="text-sm text-blue-800">단답형 퀴즈 5문제</span>
                </div>
                <div className="flex items-start space-x-2">
                  <span>📝</span>
                  <span className="text-sm text-blue-800">서술형 문제 2개</span>
                </div>
                <div className="flex items-start space-x-2">
                  <span>🤖</span>
                  <span className="text-sm text-blue-800">실시간 학습 챗봇</span>
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
      </main>
    </div>
  )
}
