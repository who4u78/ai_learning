'use client'

import { useState } from 'react'
import axios from 'axios'
import PodcastPlayer from './PodcastPlayer'
import VideoLecturePlayer from './VideoLecturePlayer'
import ReadingMaterialView from './ReadingMaterialView'
import QuizSection from './QuizSection'
import DeepQuestionsView from './DeepQuestionsView'

const STEPS = [
  { id: 'podcast', name: '팟캐스트', icon: '🎙️' },
  { id: 'video_lecture', name: '강의', icon: '🎥' },
  { id: 'reading_material', name: '읽기자료', icon: '📖' },
  { id: 'quizzes', name: '퀴즈', icon: '✏️' },
  { id: 'deep_questions', name: '심화질문', icon: '🤔' },
]

interface Props {
  sessionId: string
  sourceTitle: string
  onComplete?: () => void
}

export default function StepByStepGenerator({ sessionId, sourceTitle, onComplete }: Props) {
  const [currentStepIndex, setCurrentStepIndex] = useState(0)
  const [generatedContent, setGeneratedContent] = useState<Record<string, any>>({})
  const [isGenerating, setIsGenerating] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const currentStep = STEPS[currentStepIndex]
  const isLastStep = currentStepIndex === STEPS.length - 1

  const generateStep = async () => {
    setIsGenerating(true)
    setError(null)

    try {
      const response = await axios.post(
        `http://localhost:8000/api/learning/generate-step/${sessionId}?step=${currentStep.id}`
      )

      setGeneratedContent({
        ...generatedContent,
        [currentStep.id]: response.data.data
      })

      // 다음 단계로 자동 이동 (마지막 단계가 아니면)
      if (!isLastStep) {
        setTimeout(() => {
          setCurrentStepIndex(currentStepIndex + 1)
          setIsGenerating(false)
        }, 500)
      } else {
        setIsGenerating(false)
        if (onComplete) {
          onComplete()
        }
      }
    } catch (err: any) {
      console.error('생성 실패:', err)
      setError(err.response?.data?.detail || '생성에 실패했습니다')
      setIsGenerating(false)
    }
  }

  const goToStep = (index: number) => {
    // 이미 생성된 단계로만 이동 가능
    if (generatedContent[STEPS[index].id]) {
      setCurrentStepIndex(index)
    }
  }

  const renderContent = () => {
    const stepData = generatedContent[currentStep.id]

    if (!stepData) {
      return (
        <div className="text-center py-20">
          <div className="text-6xl mb-4">{currentStep.icon}</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-4">
            {currentStep.name} 생성
          </h2>
          <p className="text-gray-600 mb-8">
            "{sourceTitle}"의 {currentStep.name}을(를) 생성합니다
          </p>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4 max-w-md mx-auto">
              {error}
            </div>
          )}

          <button
            onClick={generateStep}
            disabled={isGenerating}
            className="bg-blue-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {isGenerating ? (
              <span className="flex items-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                생성 중...
              </span>
            ) : (
              '생성 시작'
            )}
          </button>
        </div>
      )
    }

    // 생성된 콘텐츠 표시
    switch (currentStep.id) {
      case 'podcast':
        return <PodcastPlayer podcast={{ ...stepData, script: stepData }} />

      case 'video_lecture':
        return <VideoLecturePlayer lecture={stepData} />

      case 'reading_material':
        return <ReadingMaterialView material={stepData} />

      case 'quizzes':
        return (
          <QuizSection
            multipleChoice={stepData.multiple_choice || []}
            shortAnswer={stepData.short_answer || []}
            essay={stepData.essay || []}
          />
        )

      case 'deep_questions':
        return <DeepQuestionsView questions={stepData} />

      default:
        return <div>알 수 없는 단계</div>
    }
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* 상단: 진행 단계 표시 */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          {STEPS.map((step, index) => (
            <div key={step.id} className="flex items-center flex-1">
              <button
                onClick={() => goToStep(index)}
                disabled={!generatedContent[step.id]}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                  index === currentStepIndex
                    ? 'bg-blue-100 text-blue-700 font-bold'
                    : generatedContent[step.id]
                    ? 'bg-green-50 text-green-700 hover:bg-green-100 cursor-pointer'
                    : 'bg-gray-50 text-gray-400 cursor-not-allowed'
                }`}
              >
                <span className="text-2xl">{step.icon}</span>
                <span className="text-sm">{step.name}</span>
                {generatedContent[step.id] && (
                  <span className="text-green-600">✓</span>
                )}
              </button>

              {index < STEPS.length - 1 && (
                <div className={`flex-1 h-1 mx-2 rounded ${
                  generatedContent[STEPS[index + 1].id] ? 'bg-green-400' : 'bg-gray-200'
                }`} />
              )}
            </div>
          ))}
        </div>

        {/* 다음/완료 버튼 */}
        {generatedContent[currentStep.id] && (
          <div className="text-center mt-4">
            {!isLastStep ? (
              <button
                onClick={() => setCurrentStepIndex(currentStepIndex + 1)}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
              >
                다음 단계 →
              </button>
            ) : (
              <button
                onClick={onComplete}
                className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700"
              >
                ✓ 완료
              </button>
            )}
          </div>
        )}
      </div>

      {/* 하단: 생성된 콘텐츠 표시 */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        {renderContent()}
      </div>
    </div>
  )
}
