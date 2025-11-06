'use client'

import { useState } from 'react'
import { contentApi, ContentGenerationRequest } from '@/lib/api'

interface Props {
  onContentGenerated: (contentId: string) => void
}

export default function ContentGenerator({ onContentGenerated }: Props) {
  const [sourceType, setSourceType] = useState<'url' | 'html' | 'text'>('url')
  const [sourceData, setSourceData] = useState('')
  const [title, setTitle] = useState('')
  const [includeQuiz, setIncludeQuiz] = useState(true)
  const [includeSummary, setIncludeSummary] = useState(true)
  const [includeExamples, setIncludeExamples] = useState(true)
  const [isGenerating, setIsGenerating] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleGenerate = async () => {
    if (!sourceData.trim()) {
      setError('소스 데이터를 입력해주세요')
      return
    }

    setIsGenerating(true)
    setError(null)

    try {
      const request: ContentGenerationRequest = {
        source_type: sourceType,
        source_data: sourceData,
        title: title || undefined,
        language: 'ko',
        include_quiz: includeQuiz,
        include_summary: includeSummary,
        include_examples: includeExamples,
      }

      const content = await contentApi.generate(request)
      onContentGenerated(content.id)
    } catch (err: any) {
      setError(err.response?.data?.detail || '콘텐츠 생성에 실패했습니다')
      console.error('Content generation error:', err)
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
      <h2 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">
        학습 콘텐츠 생성
      </h2>

      {/* 소스 타입 선택 */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          소스 타입
        </label>
        <div className="flex space-x-4">
          {(['url', 'html', 'text'] as const).map((type) => (
            <button
              key={type}
              onClick={() => setSourceType(type)}
              className={`px-4 py-2 rounded-md font-medium transition-colors ${
                sourceType === type
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              {type === 'url' ? 'URL' : type === 'html' ? 'HTML' : '텍스트'}
            </button>
          ))}
        </div>
      </div>

      {/* 소스 데이터 입력 */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          {sourceType === 'url' ? 'URL' : sourceType === 'html' ? 'HTML 코드' : '텍스트 내용'}
        </label>
        {sourceType === 'url' ? (
          <input
            type="url"
            value={sourceData}
            onChange={(e) => setSourceData(e.target.value)}
            placeholder="https://example.com/article"
            className="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-600 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          />
        ) : (
          <textarea
            value={sourceData}
            onChange={(e) => setSourceData(e.target.value)}
            placeholder={
              sourceType === 'html'
                ? '<html>...</html>'
                : '학습 자료로 만들고 싶은 내용을 입력하세요'
            }
            rows={10}
            className="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-600 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white font-mono text-sm"
          />
        )}
      </div>

      {/* 제목 입력 (선택사항) */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          제목 (선택사항)
        </label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="자동으로 생성됩니다"
          className="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-600 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white"
        />
      </div>

      {/* 옵션 */}
      <div className="mb-6 space-y-3">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
          포함 옵션
        </label>
        <div className="flex items-center">
          <input
            type="checkbox"
            id="include-quiz"
            checked={includeQuiz}
            onChange={(e) => setIncludeQuiz(e.target.checked)}
            className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
          <label htmlFor="include-quiz" className="ml-2 text-sm text-gray-700 dark:text-gray-300">
            퀴즈 포함
          </label>
        </div>
        <div className="flex items-center">
          <input
            type="checkbox"
            id="include-summary"
            checked={includeSummary}
            onChange={(e) => setIncludeSummary(e.target.checked)}
            className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
          <label htmlFor="include-summary" className="ml-2 text-sm text-gray-700 dark:text-gray-300">
            요약 포함
          </label>
        </div>
        <div className="flex items-center">
          <input
            type="checkbox"
            id="include-examples"
            checked={includeExamples}
            onChange={(e) => setIncludeExamples(e.target.checked)}
            className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
          <label htmlFor="include-examples" className="ml-2 text-sm text-gray-700 dark:text-gray-300">
            예시 포함
          </label>
        </div>
      </div>

      {/* 에러 메시지 */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-md">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      {/* 생성 버튼 */}
      <button
        onClick={handleGenerate}
        disabled={isGenerating}
        className={`w-full py-4 px-6 rounded-md font-semibold text-white transition-colors ${
          isGenerating
            ? 'bg-gray-400 cursor-not-allowed'
            : 'bg-blue-600 hover:bg-blue-700 active:bg-blue-800'
        }`}
      >
        {isGenerating ? (
          <div className="flex items-center justify-center">
            <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
                fill="none"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            생성 중... (1-2분 소요)
          </div>
        ) : (
          '학습 콘텐츠 생성하기'
        )}
      </button>

      {/* 안내 */}
      <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-md">
        <p className="text-sm text-blue-800 dark:text-blue-200">
          💡 <strong>팁:</strong> URL을 입력하면 해당 웹페이지의 내용을 자동으로 분석하여 한글 학습 자료를
          생성합니다. 텍스트나 HTML을 직접 입력할 수도 있습니다.
        </p>
      </div>
    </div>
  )
}
