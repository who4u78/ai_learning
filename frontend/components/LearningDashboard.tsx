'use client'

import { useState, useEffect } from 'react'
import { LearningContent } from '@/lib/api'
import PodcastPlayer from './PodcastPlayer'
import VideoLecturePlayer from './VideoLecturePlayer'
import ReadingMaterialView from './ReadingMaterialView'
import DeepQuestionsView from './DeepQuestionsView'
import QuizSection from './QuizSection'
import ChatbotWidget from './ChatbotWidget'

interface Props {
  contentId: string
  content: LearningContent
}

type TabType = 'reading' | 'podcast' | 'video' | 'quiz' | 'deep'

export default function LearningDashboard({ contentId, content }: Props) {
  const [activeTab, setActiveTab] = useState<TabType>('reading')
  const [showChatbot, setShowChatbot] = useState(false)

  const tabs = [
    { id: 'reading' as TabType, label: '📖 읽기 자료', icon: '📖', available: !!content.reading_material },
    { id: 'podcast' as TabType, label: '📻 팟캐스트', icon: '📻', available: !!content.podcast },
    { id: 'video' as TabType, label: '🎥 강의 비디오', icon: '🎥', available: !!content.video_lecture },
    { id: 'quiz' as TabType, label: '✅ 퀴즈', icon: '✅', available: true },
    { id: 'deep' as TabType, label: '💭 심화 질문', icon: '💭', available: content.deep_questions.length > 0 },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-md sticky top-0 z-10">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{content.title}</h1>
              <p className="text-gray-600 mt-1">{content.description}</p>
            </div>
            <button
              onClick={() => setShowChatbot(!showChatbot)}
              className="flex items-center space-x-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <span>🤖</span>
              <span>챗봇 {showChatbot ? '닫기' : '열기'}</span>
            </button>
          </div>

          {/* Tabs */}
          <div className="flex space-x-2 mt-6 overflow-x-auto">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => tab.available && setActiveTab(tab.id)}
                disabled={!tab.available}
                className={`
                  px-6 py-3 rounded-lg font-medium whitespace-nowrap transition-all
                  ${activeTab === tab.id
                    ? 'bg-blue-600 text-white shadow-lg'
                    : tab.available
                      ? 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      : 'bg-gray-50 text-gray-400 cursor-not-allowed'
                  }
                `}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Content Area */}
      <div className="container mx-auto px-4 py-8">
        <div className="bg-white rounded-xl shadow-lg p-8">
          {activeTab === 'reading' && content.reading_material && (
            <ReadingMaterialView material={content.reading_material} />
          )}

          {activeTab === 'podcast' && content.podcast && (
            <PodcastPlayer podcast={content.podcast} />
          )}

          {activeTab === 'video' && content.video_lecture && (
            <VideoLecturePlayer lecture={content.video_lecture} />
          )}

          {activeTab === 'quiz' && (
            <QuizSection
              multipleChoice={content.multiple_choice_quizzes}
              shortAnswer={content.short_answer_quizzes}
              essay={content.essay_quizzes}
            />
          )}

          {activeTab === 'deep' && (
            <DeepQuestionsView questions={content.deep_questions} />
          )}
        </div>
      </div>

      {/* Chatbot Widget */}
      {showChatbot && (
        <ChatbotWidget
          contentId={contentId}
          onClose={() => setShowChatbot(false)}
        />
      )}
    </div>
  )
}
