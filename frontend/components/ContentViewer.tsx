'use client'

import { useState, useEffect } from 'react'
import { contentApi, audioApi, videoApi, GeneratedContent } from '@/lib/api'
import ReactMarkdown from 'react-markdown'
import QuizComponent from './QuizComponent'
import AudioPlayer from './AudioPlayer'

interface Props {
  contentId: string
}

export default function ContentViewer({ contentId }: Props) {
  const [content, setContent] = useState<GeneratedContent | null>(null)
  const [currentSectionIndex, setCurrentSectionIndex] = useState(0)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [audioFiles, setAudioFiles] = useState<any[]>([])
  const [isGeneratingAudio, setIsGeneratingAudio] = useState(false)
  const [isGeneratingVideo, setIsGeneratingVideo] = useState(false)
  const [videoUrl, setVideoUrl] = useState<string | null>(null)

  useEffect(() => {
    loadContent()
  }, [contentId])

  const loadContent = async () => {
    setIsLoading(true)
    setError(null)

    try {
      const data = await contentApi.get(contentId)
      setContent(data)
    } catch (err: any) {
      setError(err.response?.data?.detail || '콘텐츠를 불러오는데 실패했습니다')
    } finally {
      setIsLoading(false)
    }
  }

  const handleGenerateAudio = async () => {
    if (!content) return

    setIsGeneratingAudio(true)
    try {
      const response = await audioApi.generateForContent(content.id)
      setAudioFiles(response.audio_files)
    } catch (err: any) {
      alert('음성 생성 실패: ' + (err.response?.data?.detail || err.message))
    } finally {
      setIsGeneratingAudio(false)
    }
  }

  const handleGenerateVideo = async () => {
    if (!content) return

    setIsGeneratingVideo(true)
    try {
      const response = await videoApi.generate({
        content_id: content.id,
        include_subtitles: true,
      })
      setVideoUrl(response.video_url)
    } catch (err: any) {
      alert('비디오 생성 실패: ' + (err.response?.data?.detail || err.message))
    } finally {
      setIsGeneratingVideo(false)
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (error || !content) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <p className="text-red-600">{error || '콘텐츠를 찾을 수 없습니다'}</p>
      </div>
    )
  }

  const currentSection = content.sections[currentSectionIndex]
  const currentAudio = audioFiles.find((a) => a.section_id === currentSection.id)

  return (
    <div className="space-y-6">
      {/* 헤더 */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          {content.title}
        </h1>
        {content.summary && (
          <p className="text-gray-600 dark:text-gray-400 text-lg leading-relaxed">
            {content.summary}
          </p>
        )}

        {/* 액션 버튼들 */}
        <div className="mt-6 flex space-x-4">
          <button
            onClick={handleGenerateAudio}
            disabled={isGeneratingAudio || audioFiles.length > 0}
            className={`px-6 py-3 rounded-md font-medium transition-colors ${
              isGeneratingAudio || audioFiles.length > 0
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-green-600 hover:bg-green-700 text-white'
            }`}
          >
            {isGeneratingAudio ? '음성 생성 중...' : audioFiles.length > 0 ? '음성 생성됨' : '🎤 음성 생성'}
          </button>

          <button
            onClick={handleGenerateVideo}
            disabled={isGeneratingVideo || !audioFiles.length}
            className={`px-6 py-3 rounded-md font-medium transition-colors ${
              isGeneratingVideo || !audioFiles.length
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-purple-600 hover:bg-purple-700 text-white'
            }`}
          >
            {isGeneratingVideo ? '비디오 생성 중...' : videoUrl ? '비디오 생성됨' : '🎥 비디오 생성'}
          </button>
        </div>

        {!audioFiles.length && (
          <p className="mt-4 text-sm text-gray-500">
            💡 음성을 생성하면 각 섹션을 들으면서 학습할 수 있습니다
          </p>
        )}
      </div>

      {/* 비디오 플레이어 */}
      {videoUrl && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold mb-4">전체 비디오</h3>
          <video controls className="w-full rounded-lg" src={videoUrl}>
            비디오를 지원하지 않는 브라우저입니다.
          </video>
        </div>
      )}

      {/* 섹션 네비게이션 */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-bold">
            섹션 {currentSectionIndex + 1} / {content.sections.length}
          </h3>
          <div className="flex space-x-2">
            <button
              onClick={() => setCurrentSectionIndex(Math.max(0, currentSectionIndex - 1))}
              disabled={currentSectionIndex === 0}
              className="px-4 py-2 bg-gray-200 rounded-md disabled:opacity-50"
            >
              ← 이전
            </button>
            <button
              onClick={() =>
                setCurrentSectionIndex(Math.min(content.sections.length - 1, currentSectionIndex + 1))
              }
              disabled={currentSectionIndex === content.sections.length - 1}
              className="px-4 py-2 bg-gray-200 rounded-md disabled:opacity-50"
            >
              다음 →
            </button>
          </div>
        </div>

        {/* 섹션 제목 */}
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          {currentSection.title}
        </h2>

        {currentSection.estimated_time && (
          <p className="text-sm text-gray-500 mb-4">
            ⏱️ 예상 학습 시간: {currentSection.estimated_time}분
          </p>
        )}

        {/* 오디오 플레이어 */}
        {currentAudio && (
          <div className="mb-6">
            <AudioPlayer audioUrl={currentAudio.audio_url} />
          </div>
        )}

        {/* 섹션 내용 */}
        <div className="prose prose-lg max-w-none dark:prose-invert markdown-content">
          <ReactMarkdown>{currentSection.content}</ReactMarkdown>
        </div>
      </div>

      {/* 퀴즈 */}
      {content.quizzes && content.quizzes.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <h3 className="text-2xl font-bold mb-6">퀴즈</h3>
          <div className="space-y-6">
            {content.quizzes.map((quiz, index) => (
              <QuizComponent key={index} quiz={quiz} index={index} />
            ))}
          </div>
        </div>
      )}

      {/* 섹션 목록 */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold mb-4">전체 섹션</h3>
        <div className="space-y-2">
          {content.sections.map((section, index) => (
            <button
              key={section.id}
              onClick={() => setCurrentSectionIndex(index)}
              className={`w-full text-left px-4 py-3 rounded-md transition-colors ${
                index === currentSectionIndex
                  ? 'bg-blue-100 dark:bg-blue-900 border-2 border-blue-600'
                  : 'bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="font-medium">{section.title}</span>
                {section.estimated_time && (
                  <span className="text-sm text-gray-500">{section.estimated_time}분</span>
                )}
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
