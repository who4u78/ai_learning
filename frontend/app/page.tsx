'use client'

import { useState } from 'react'
import ContentGenerator from '@/components/ContentGenerator'
import ContentViewer from '@/components/ContentViewer'
import Header from '@/components/Header'

export default function Home() {
  const [generatedContentId, setGeneratedContentId] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'generate' | 'view'>('generate')

  const handleContentGenerated = (contentId: string) => {
    setGeneratedContentId(contentId)
    setActiveTab('view')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <Header />

      <main className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          {/* 탭 네비게이션 */}
          <div className="flex space-x-4 mb-8 border-b border-gray-300 dark:border-gray-700">
            <button
              onClick={() => setActiveTab('generate')}
              className={`px-6 py-3 font-semibold transition-colors ${
                activeTab === 'generate'
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              콘텐츠 생성
            </button>
            <button
              onClick={() => setActiveTab('view')}
              className={`px-6 py-3 font-semibold transition-colors ${
                activeTab === 'view'
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
              disabled={!generatedContentId}
            >
              학습하기
            </button>
          </div>

          {/* 콘텐츠 영역 */}
          {activeTab === 'generate' && (
            <ContentGenerator onContentGenerated={handleContentGenerated} />
          )}

          {activeTab === 'view' && generatedContentId && (
            <ContentViewer contentId={generatedContentId} />
          )}
        </div>
      </main>

      {/* 푸터 */}
      <footer className="mt-16 py-8 bg-gray-900 text-gray-300 text-center">
        <p>한글 AI 학습 플랫폼 &copy; 2024</p>
        <p className="text-sm mt-2">Powered by Anthropic Claude & Fish Audio</p>
      </footer>
    </div>
  )
}
