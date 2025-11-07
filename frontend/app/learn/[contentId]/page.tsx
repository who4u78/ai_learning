'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { learningApi, LearningContent } from '@/lib/api'
import LearningDashboard from '@/components/LearningDashboard'

export default function LearnPage() {
  const params = useParams()
  const router = useRouter()
  const contentId = params.contentId as string

  const [content, setContent] = useState<LearningContent | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchContent = async () => {
      try {
        setLoading(true)
        const data = await learningApi.getContent(contentId)
        setContent(data)
      } catch (err: any) {
        setError(err.message || '콘텐츠를 불러올 수 없습니다.')
      } finally {
        setLoading(false)
      }
    }

    if (contentId) {
      fetchContent()
    }
  }, [contentId])

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-600 font-medium">학습 자료를 불러오는 중...</p>
        </div>
      </div>
    )
  }

  if (error || !content) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white rounded-xl shadow-lg p-8 max-w-md text-center">
          <div className="text-6xl mb-4">😞</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">오류가 발생했습니다</h2>
          <p className="text-gray-600 mb-6">{error || '콘텐츠를 찾을 수 없습니다.'}</p>
          <button
            onClick={() => router.push('/')}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            홈으로 돌아가기
          </button>
        </div>
      </div>
    )
  }

  return <LearningDashboard contentId={contentId} content={content} />
}
