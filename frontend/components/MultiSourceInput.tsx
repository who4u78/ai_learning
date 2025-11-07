'use client'

import { useState } from 'react'
import { learningApi } from '@/lib/api'
import axios from 'axios'

interface Source {
  id: string
  type: 'url' | 'file' | 'text' | 'youtube'
  data: string
  file?: File
  name: string
}

interface Props {
  onComplete: (contentId: string) => void
}

export default function MultiSourceInput({ onComplete }: Props) {
  const [sources, setSources] = useState<Source[]>([])
  const [currentInput, setCurrentInput] = useState('')
  const [currentType, setCurrentType] = useState<'url' | 'file' | 'text' | 'youtube'>('url')
  const [loading, setLoading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [message, setMessage] = useState('')

  // 소스 추가
  const addSource = () => {
    if (currentType === 'file') {
      // 파일은 별도 처리
      return
    }

    if (!currentInput.trim()) return

    const newSource: Source = {
      id: Math.random().toString(36).substring(7),
      type: currentType,
      data: currentInput,
      name: currentType === 'url' || currentType === 'youtube'
        ? currentInput.substring(0, 50) + '...'
        : `텍스트 (${currentInput.length}자)`
    }

    setSources([...sources, newSource])
    setCurrentInput('')
  }

  // 파일 추가
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (!files) return

    const newSources: Source[] = []
    for (let i = 0; i < files.length; i++) {
      const file = files[i]
      newSources.push({
        id: Math.random().toString(36).substring(7),
        type: 'file',
        data: file.name,
        file: file,
        name: file.name
      })
    }

    setSources([...sources, ...newSources])
  }

  // 소스 삭제
  const removeSource = (id: string) => {
    setSources(sources.filter(s => s.id !== id))
  }

  // 생성 시작
  const handleGenerate = async () => {
    if (sources.length === 0) return

    setLoading(true)
    setProgress(0)
    setMessage('생성 시작...')

    try {
      let contentId: string

      // 파일이 있는지 확인
      const hasFiles = sources.some(s => s.type === 'file')

      if (hasFiles) {
        // 파일 업로드 API 사용
        const formData = new FormData()
        sources.forEach(source => {
          if (source.file) {
            formData.append('files', source.file)
          }
        })

        const response = await axios.post(
          'http://localhost:8000/api/learning/upload',
          formData,
          {
            headers: { 'Content-Type': 'multipart/form-data' }
          }
        )

        contentId = response.data.content_id
      } else {
        // 일반 API 사용
        let request

        if (sources.length === 1) {
          // 단일 소스
          request = {
            source_type: sources[0].type,
            source_data: sources[0].data
          }
        } else {
          // 다중 소스
          request = {
            sources: sources.map(s => ({
              type: s.type,
              data: s.data
            }))
          }
        }

        const response = await learningApi.generateContent(request)
        contentId = response.content_id
      }

      // 진행 상태 폴링
      const interval = setInterval(async () => {
        const status = await learningApi.getStatus(contentId)
        setProgress(status.progress)
        setMessage(status.current_task || '')

        if (status.status === 'completed') {
          clearInterval(interval)
          setLoading(false)
          onComplete(contentId)
        } else if (status.status === 'failed') {
          clearInterval(interval)
          setLoading(false)
          setMessage('생성 실패: ' + (status.error || '알 수 없는 오류'))
        }
      }, 3000)
    } catch (error: any) {
      setLoading(false)
      setMessage('오류: ' + error.message)
    }
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'url': return '🌐'
      case 'youtube': return '📺'
      case 'file': return '📄'
      case 'text': return '📝'
      default: return '📋'
    }
  }

  const getTypeLabel = (type: string) => {
    switch (type) {
      case 'url': return 'URL'
      case 'youtube': return 'YouTube'
      case 'file': return '파일'
      case 'text': return '텍스트'
      default: return type
    }
  }

  return (
    <div className="space-y-6">
      {/* 소스 타입 선택 */}
      <div className="flex space-x-2">
        {['url', 'youtube', 'file', 'text'].map((type) => (
          <button
            key={type}
            onClick={() => setCurrentType(type as any)}
            disabled={loading}
            className={`
              px-4 py-2 rounded-lg font-medium transition-all
              ${currentType === type
                ? 'bg-blue-600 text-white shadow-md'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }
              ${loading ? 'opacity-50 cursor-not-allowed' : ''}
            `}
          >
            {getTypeIcon(type)} {getTypeLabel(type)}
          </button>
        ))}
      </div>

      {/* 입력 영역 */}
      <div className="bg-gray-50 rounded-xl p-6 border-2 border-gray-200">
        {currentType === 'file' ? (
          <div>
            <label className="block">
              <span className="text-sm font-medium text-gray-700 mb-2 block">
                파일 선택 (PDF, Word, Excel, PowerPoint, Markdown 등)
              </span>
              <input
                type="file"
                multiple
                onChange={handleFileSelect}
                disabled={loading}
                accept=".pdf,.docx,.doc,.xlsx,.xls,.pptx,.ppt,.md,.qmd,.txt"
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
              />
            </label>
            <p className="text-xs text-gray-500 mt-2">
              여러 파일을 동시에 선택할 수 있습니다. 모든 파일의 내용이 하나의 학습 자료로 결합됩니다.
            </p>
          </div>
        ) : currentType === 'text' ? (
          <div>
            <label className="block">
              <span className="text-sm font-medium text-gray-700 mb-2 block">
                학습할 텍스트 입력
              </span>
              <textarea
                value={currentInput}
                onChange={(e) => setCurrentInput(e.target.value)}
                disabled={loading}
                rows={6}
                placeholder="학습하고 싶은 텍스트를 직접 입력하세요..."
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none resize-none"
              />
            </label>
            <button
              onClick={addSource}
              disabled={!currentInput.trim() || loading}
              className="mt-3 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
            >
              텍스트 추가
            </button>
          </div>
        ) : (
          <div className="flex space-x-2">
            <input
              type="url"
              value={currentInput}
              onChange={(e) => setCurrentInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && addSource()}
              disabled={loading}
              placeholder={
                currentType === 'url'
                  ? 'https://example.com/article'
                  : 'https://youtube.com/watch?v=...'
              }
              className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
            />
            <button
              onClick={addSource}
              disabled={!currentInput.trim() || loading}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
            >
              추가
            </button>
          </div>
        )}
      </div>

      {/* 추가된 소스 목록 */}
      {sources.length > 0 && (
        <div className="bg-white rounded-xl p-6 border-2 border-blue-200">
          <h3 className="text-lg font-bold text-gray-900 mb-4">
            📚 추가된 소스 ({sources.length}개)
          </h3>

          <div className="space-y-2 mb-4">
            {sources.map((source) => (
              <div
                key={source.id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex items-center space-x-3 flex-1 min-w-0">
                  <span className="text-2xl">{getTypeIcon(source.type)}</span>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {source.name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {getTypeLabel(source.type)}
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => removeSource(source.id)}
                  disabled={loading}
                  className="ml-2 p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            ))}
          </div>

          <button
            onClick={handleGenerate}
            disabled={loading || sources.length === 0}
            className="w-full py-4 bg-green-600 text-white font-bold text-lg rounded-lg hover:bg-green-700 disabled:bg-gray-400 transition-colors"
          >
            {loading ? '생성 중...' : `🎓 ${sources.length}개 소스로 학습 자료 생성하기`}
          </button>

          {sources.length > 1 && (
            <p className="text-xs text-gray-600 text-center mt-2">
              모든 소스의 내용이 하나의 종합 학습 자료로 만들어집니다
            </p>
          )}
        </div>
      )}

      {/* 진행 상황 */}
      {loading && (
        <div className="bg-white rounded-xl p-6 border-2 border-blue-200">
          <div className="w-full bg-gray-200 rounded-full h-4 mb-2">
            <div
              className="bg-blue-600 h-4 rounded-full transition-all duration-500"
              style={{ width: `${progress}%` }}
            />
          </div>
          <p className="text-center text-gray-600">{progress}% - {message}</p>
        </div>
      )}
    </div>
  )
}
