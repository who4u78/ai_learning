'use client'

import { useState } from 'react'
import { DeepThinkingQuestion } from '@/lib/api'

interface Props {
  questions: DeepThinkingQuestion[]
}

export default function DeepQuestionsView({ questions }: Props) {
  const [answers, setAnswers] = useState<string[]>(Array(questions.length).fill(''))
  const [expandedHints, setExpandedHints] = useState<boolean[]>(Array(questions.length).fill(false))

  const handleAnswer = (index: number, value: string) => {
    const newAnswers = [...answers]
    newAnswers[index] = value
    setAnswers(newAnswers)
  }

  const toggleHints = (index: number) => {
    const newExpanded = [...expandedHints]
    newExpanded[index] = !newExpanded[index]
    setExpandedHints(newExpanded)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">💭 심화 사고 질문</h2>
        <p className="text-gray-600">
          정답이 정해지지 않은 질문들입니다. 깊이 생각하고 자유롭게 답변해보세요.
        </p>
      </div>

      {/* Questions */}
      <div className="space-y-8">
        {questions.map((question, index) => (
          <div
            key={index}
            className="bg-gradient-to-br from-purple-50 to-pink-50 border-2 border-purple-200 rounded-2xl p-8 shadow-lg"
          >
            {/* Question Number Badge */}
            <div className="flex items-start space-x-4 mb-6">
              <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-purple-600 to-pink-600 text-white rounded-full flex items-center justify-center font-bold text-lg shadow-md">
                {index + 1}
              </div>
              <div className="flex-1">
                <h3 className="text-2xl font-bold text-gray-900 mb-3">
                  {question.question}
                </h3>

                {/* Context */}
                {question.context && (
                  <div className="bg-white bg-opacity-70 rounded-lg p-4 mb-4 border border-purple-200">
                    <p className="text-sm font-medium text-purple-900 mb-1">📖 배경:</p>
                    <p className="text-gray-700">{question.context}</p>
                  </div>
                )}

                {/* Hints */}
                {question.hints && question.hints.length > 0 && (
                  <div className="mb-4">
                    <button
                      onClick={() => toggleHints(index)}
                      className="text-purple-700 hover:text-purple-800 font-medium text-sm flex items-center space-x-1"
                    >
                      <span>{expandedHints[index] ? '▼' : '▶'}</span>
                      <span>힌트 {expandedHints[index] ? '숨기기' : '보기'}</span>
                    </button>

                    {expandedHints[index] && (
                      <div className="mt-3 space-y-2">
                        {question.hints.map((hint, hintIndex) => (
                          <div
                            key={hintIndex}
                            className="bg-yellow-50 border-l-4 border-yellow-400 rounded p-3"
                          >
                            <p className="text-sm text-yellow-900">
                              <span className="font-medium">💡 힌트 {hintIndex + 1}:</span> {hint}
                            </p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>

            {/* Answer Area */}
            <div className="space-y-3">
              <label className="block">
                <span className="text-sm font-medium text-gray-700 mb-2 block">
                  ✍️ 나의 생각:
                </span>
                <textarea
                  value={answers[index]}
                  onChange={(e) => handleAnswer(index, e.target.value)}
                  placeholder="자유롭게 생각을 작성해보세요. 정답은 없습니다!"
                  rows={6}
                  className="w-full px-4 py-3 border-2 border-purple-300 rounded-lg focus:border-purple-500 focus:ring-2 focus:ring-purple-200 focus:outline-none resize-none bg-white"
                />
              </label>

              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600">{answers[index].length}자</span>
                {answers[index].length > 0 && (
                  <span className="text-green-600 font-medium">
                    ✓ 좋습니다! 계속 생각을 발전시켜보세요
                  </span>
                )}
              </div>
            </div>

            {/* Thinking Tips */}
            <div className="mt-4 bg-purple-100 bg-opacity-50 rounded-lg p-4 border border-purple-300">
              <p className="text-sm font-medium text-purple-900 mb-2">🤔 생각을 발전시키는 방법:</p>
              <ul className="space-y-1 text-sm text-purple-800">
                <li className="flex items-start">
                  <span className="mr-2">•</span>
                  <span>왜 그렇게 생각하는지 근거를 들어보세요</span>
                </li>
                <li className="flex items-start">
                  <span className="mr-2">•</span>
                  <span>반대 의견은 어떤 것이 있을까요?</span>
                </li>
                <li className="flex items-start">
                  <span className="mr-2">•</span>
                  <span>실제 사례나 경험과 연결해보세요</span>
                </li>
                <li className="flex items-start">
                  <span className="mr-2">•</span>
                  <span>다른 관점에서는 어떻게 볼 수 있을까요?</span>
                </li>
              </ul>
            </div>
          </div>
        ))}
      </div>

      {/* Action Buttons */}
      <div className="flex justify-center space-x-4">
        <button
          onClick={() => {
            const answered = answers.filter(a => a.trim()).length
            alert(`${answered}개의 질문에 답변하셨습니다! 계속 생각을 발전시켜보세요.`)
          }}
          className="px-8 py-3 bg-purple-600 text-white font-medium rounded-lg hover:bg-purple-700 transition-colors shadow-md"
        >
          📝 답변 저장하기
        </button>
        <button
          onClick={() => {
            if (confirm('모든 답변을 초기화하시겠습니까?')) {
              setAnswers(Array(questions.length).fill(''))
            }
          }}
          className="px-8 py-3 bg-gray-500 text-white font-medium rounded-lg hover:bg-gray-600 transition-colors"
        >
          🔄 다시 작성하기
        </button>
      </div>

      {/* Encouragement Message */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6 text-center border-2 border-blue-200">
        <p className="text-lg font-medium text-gray-900 mb-2">
          💪 심화 질문은 비판적 사고력을 키우는 좋은 방법입니다
        </p>
        <p className="text-gray-600">
          궁금한 점이 있다면 챗봇에게 질문해보세요!
        </p>
      </div>
    </div>
  )
}
