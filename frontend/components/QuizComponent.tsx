'use client'

import { useState } from 'react'
import { Quiz } from '@/lib/api'

interface Props {
  quiz: Quiz
  index: number
}

export default function QuizComponent({ quiz, index }: Props) {
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null)
  const [showExplanation, setShowExplanation] = useState(false)

  const handleAnswerSelect = (answerIndex: number) => {
    setSelectedAnswer(answerIndex)
    setShowExplanation(true)
  }

  const isCorrect = selectedAnswer === quiz.correct_answer

  return (
    <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6">
      <h4 className="text-lg font-semibold mb-4">
        문제 {index + 1}. {quiz.question}
      </h4>

      <div className="space-y-3">
        {quiz.options.map((option, optionIndex) => {
          const isSelected = selectedAnswer === optionIndex
          const isCorrectAnswer = optionIndex === quiz.correct_answer
          const showAsCorrect = showExplanation && isCorrectAnswer
          const showAsWrong = showExplanation && isSelected && !isCorrect

          return (
            <button
              key={optionIndex}
              onClick={() => handleAnswerSelect(optionIndex)}
              disabled={showExplanation}
              className={`w-full text-left px-4 py-3 rounded-md border-2 transition-colors ${
                showAsCorrect
                  ? 'border-green-500 bg-green-50 dark:bg-green-900/20'
                  : showAsWrong
                  ? 'border-red-500 bg-red-50 dark:bg-red-900/20'
                  : isSelected
                  ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                  : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
              } ${showExplanation ? 'cursor-default' : 'cursor-pointer'}`}
            >
              <div className="flex items-center justify-between">
                <span>{option}</span>
                {showAsCorrect && <span className="text-green-600">✓ 정답</span>}
                {showAsWrong && <span className="text-red-600">✗ 오답</span>}
              </div>
            </button>
          )
        })}
      </div>

      {/* 해설 */}
      {showExplanation && (
        <div
          className={`mt-4 p-4 rounded-md ${
            isCorrect
              ? 'bg-green-50 border border-green-200 dark:bg-green-900/20 dark:border-green-800'
              : 'bg-red-50 border border-red-200 dark:bg-red-900/20 dark:border-red-800'
          }`}
        >
          <p className="font-semibold mb-2">
            {isCorrect ? '🎉 정답입니다!' : '❌ 틀렸습니다'}
          </p>
          <p className="text-sm">{quiz.explanation}</p>
        </div>
      )}
    </div>
  )
}
