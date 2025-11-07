'use client'

import { useState } from 'react'
import { MultipleChoiceQuiz, ShortAnswerQuiz, EssayQuiz } from '@/lib/api'

interface Props {
  multipleChoice: MultipleChoiceQuiz[]
  shortAnswer: ShortAnswerQuiz[]
  essay: EssayQuiz[]
}

type QuizType = 'multiple' | 'short' | 'essay'

export default function QuizSection({ multipleChoice, shortAnswer, essay }: Props) {
  const [quizType, setQuizType] = useState<QuizType>('multiple')

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">✅ 퀴즈</h2>
        <p className="text-gray-600">학습 내용을 확인해보세요</p>
      </div>

      {/* Quiz Type Selector */}
      <div className="flex justify-center space-x-3">
        <button
          onClick={() => setQuizType('multiple')}
          className={`
            px-6 py-3 rounded-lg font-medium transition-all
            ${quizType === 'multiple'
              ? 'bg-blue-600 text-white shadow-lg'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }
          `}
        >
          4지선다형 ({multipleChoice.length}문제)
        </button>
        <button
          onClick={() => setQuizType('short')}
          className={`
            px-6 py-3 rounded-lg font-medium transition-all
            ${quizType === 'short'
              ? 'bg-blue-600 text-white shadow-lg'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }
          `}
        >
          단답형 ({shortAnswer.length}문제)
        </button>
        <button
          onClick={() => setQuizType('essay')}
          className={`
            px-6 py-3 rounded-lg font-medium transition-all
            ${quizType === 'essay'
              ? 'bg-blue-600 text-white shadow-lg'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }
          `}
        >
          서술형 ({essay.length}문제)
        </button>
      </div>

      {/* Quiz Content */}
      <div>
        {quizType === 'multiple' && <MultipleChoiceSection quizzes={multipleChoice} />}
        {quizType === 'short' && <ShortAnswerSection quizzes={shortAnswer} />}
        {quizType === 'essay' && <EssaySection quizzes={essay} />}
      </div>
    </div>
  )
}

// Multiple Choice Quiz Component
function MultipleChoiceSection({ quizzes }: { quizzes: MultipleChoiceQuiz[] }) {
  const [answers, setAnswers] = useState<(number | null)[]>(Array(quizzes.length).fill(null))
  const [showResults, setShowResults] = useState(false)

  const handleAnswer = (quizIndex: number, optionIndex: number) => {
    const newAnswers = [...answers]
    newAnswers[quizIndex] = optionIndex
    setAnswers(newAnswers)
  }

  const checkAnswers = () => {
    setShowResults(true)
  }

  const resetQuiz = () => {
    setAnswers(Array(quizzes.length).fill(null))
    setShowResults(false)
  }

  const score = answers.reduce((acc, answer, index) => {
    return acc + (answer === quizzes[index].correct_answer ? 1 : 0)
  }, 0)

  return (
    <div className="space-y-6">
      {quizzes.map((quiz, quizIndex) => (
        <div key={quizIndex} className="bg-white border-2 border-gray-200 rounded-xl p-6 shadow-sm">
          {/* Question */}
          <div className="flex items-start space-x-3 mb-4">
            <span className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
              {quizIndex + 1}
            </span>
            <div className="flex-1">
              <p className="text-lg font-medium text-gray-900">{quiz.question}</p>
              {quiz.difficulty && (
                <span className={`
                  inline-block mt-2 px-3 py-1 rounded-full text-xs font-medium
                  ${quiz.difficulty === 'easy' ? 'bg-green-100 text-green-800' :
                    quiz.difficulty === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'}
                `}>
                  {quiz.difficulty === 'easy' ? '쉬움' : quiz.difficulty === 'medium' ? '보통' : '어려움'}
                </span>
              )}
            </div>
          </div>

          {/* Options */}
          <div className="space-y-2 ml-11">
            {quiz.options.map((option, optionIndex) => {
              const isSelected = answers[quizIndex] === optionIndex
              const isCorrect = optionIndex === quiz.correct_answer
              const showCorrectness = showResults && isSelected

              return (
                <button
                  key={optionIndex}
                  onClick={() => !showResults && handleAnswer(quizIndex, optionIndex)}
                  disabled={showResults}
                  className={`
                    w-full text-left p-4 rounded-lg border-2 transition-all
                    ${!showResults && isSelected ? 'border-blue-500 bg-blue-50' : ''}
                    ${!showResults && !isSelected ? 'border-gray-200 hover:border-blue-300 hover:bg-gray-50' : ''}
                    ${showResults && isCorrect ? 'border-green-500 bg-green-50' : ''}
                    ${showCorrectness && !isCorrect ? 'border-red-500 bg-red-50' : ''}
                    ${showResults ? 'cursor-default' : 'cursor-pointer'}
                  `}
                >
                  <div className="flex items-center space-x-3">
                    <span className="flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center font-medium text-sm">
                      {String.fromCharCode(65 + optionIndex)}
                    </span>
                    <span className="flex-1">{option}</span>
                    {showResults && isCorrect && <span className="text-green-600">✓</span>}
                    {showCorrectness && !isCorrect && <span className="text-red-600">✗</span>}
                  </div>
                </button>
              )
            })}
          </div>

          {/* Explanation */}
          {showResults && (
            <div className="mt-4 ml-11 p-4 bg-blue-50 border-l-4 border-blue-400 rounded">
              <p className="text-sm font-medium text-blue-900 mb-1">💡 설명:</p>
              <p className="text-sm text-blue-800">{quiz.explanation}</p>
            </div>
          )}
        </div>
      ))}

      {/* Action Buttons */}
      <div className="flex justify-center space-x-4">
        {!showResults ? (
          <button
            onClick={checkAnswers}
            disabled={answers.some(a => a === null)}
            className="px-8 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            답안 제출하기
          </button>
        ) : (
          <>
            <div className="px-8 py-3 bg-green-100 text-green-800 font-bold rounded-lg">
              점수: {score} / {quizzes.length} ({Math.round((score / quizzes.length) * 100)}%)
            </div>
            <button
              onClick={resetQuiz}
              className="px-8 py-3 bg-gray-600 text-white font-medium rounded-lg hover:bg-gray-700 transition-colors"
            >
              다시 풀기
            </button>
          </>
        )}
      </div>
    </div>
  )
}

// Short Answer Quiz Component
function ShortAnswerSection({ quizzes }: { quizzes: ShortAnswerQuiz[] }) {
  const [answers, setAnswers] = useState<string[]>(Array(quizzes.length).fill(''))
  const [showResults, setShowResults] = useState(false)

  const handleAnswer = (index: number, value: string) => {
    const newAnswers = [...answers]
    newAnswers[index] = value
    setAnswers(newAnswers)
  }

  const checkAnswer = (quizIndex: number) => {
    const quiz = quizzes[quizIndex]
    const userAnswer = answers[quizIndex].trim()

    return quiz.correct_answers.some(correct =>
      quiz.case_sensitive
        ? correct === userAnswer
        : correct.toLowerCase() === userAnswer.toLowerCase()
    )
  }

  return (
    <div className="space-y-6">
      {quizzes.map((quiz, index) => {
        const isCorrect = showResults ? checkAnswer(index) : false

        return (
          <div key={index} className="bg-white border-2 border-gray-200 rounded-xl p-6 shadow-sm">
            <div className="flex items-start space-x-3 mb-4">
              <span className="flex-shrink-0 w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center font-bold">
                {index + 1}
              </span>
              <p className="flex-1 text-lg font-medium text-gray-900">{quiz.question}</p>
            </div>

            <div className="ml-11 space-y-4">
              <input
                type="text"
                value={answers[index]}
                onChange={(e) => !showResults && handleAnswer(index, e.target.value)}
                disabled={showResults}
                placeholder="답을 입력하세요..."
                className={`
                  w-full px-4 py-3 border-2 rounded-lg
                  ${showResults
                    ? isCorrect
                      ? 'border-green-500 bg-green-50'
                      : 'border-red-500 bg-red-50'
                    : 'border-gray-300 focus:border-purple-500 focus:outline-none'
                  }
                `}
              />

              {showResults && (
                <div className={`p-4 rounded-lg border-l-4 ${isCorrect ? 'bg-green-50 border-green-400' : 'bg-red-50 border-red-400'}`}>
                  <p className="font-medium mb-2">
                    {isCorrect ? '✓ 정답입니다!' : '✗ 오답입니다.'}
                  </p>
                  <p className="text-sm mb-2">
                    <span className="font-medium">정답:</span> {quiz.correct_answers.join(' 또는 ')}
                  </p>
                  <p className="text-sm">
                    <span className="font-medium">설명:</span> {quiz.explanation}
                  </p>
                </div>
              )}
            </div>
          </div>
        )
      })}

      <div className="flex justify-center">
        {!showResults ? (
          <button
            onClick={() => setShowResults(true)}
            disabled={answers.some(a => !a.trim())}
            className="px-8 py-3 bg-purple-600 text-white font-medium rounded-lg hover:bg-purple-700 disabled:bg-gray-400 transition-colors"
          >
            답안 제출하기
          </button>
        ) : (
          <button
            onClick={() => {
              setAnswers(Array(quizzes.length).fill(''))
              setShowResults(false)
            }}
            className="px-8 py-3 bg-gray-600 text-white font-medium rounded-lg hover:bg-gray-700 transition-colors"
          >
            다시 풀기
          </button>
        )}
      </div>
    </div>
  )
}

// Essay Quiz Component
function EssaySection({ quizzes }: { quizzes: EssayQuiz[] }) {
  const [answers, setAnswers] = useState<string[]>(Array(quizzes.length).fill(''))
  const [showSuggested, setShowSuggested] = useState<boolean[]>(Array(quizzes.length).fill(false))

  const handleAnswer = (index: number, value: string) => {
    const newAnswers = [...answers]
    newAnswers[index] = value
    setAnswers(newAnswers)
  }

  const toggleSuggested = (index: number) => {
    const newShow = [...showSuggested]
    newShow[index] = !newShow[index]
    setShowSuggested(newShow)
  }

  return (
    <div className="space-y-6">
      {quizzes.map((quiz, index) => (
        <div key={index} className="bg-white border-2 border-gray-200 rounded-xl p-6 shadow-sm">
          <div className="flex items-start space-x-3 mb-4">
            <span className="flex-shrink-0 w-8 h-8 bg-indigo-600 text-white rounded-full flex items-center justify-center font-bold">
              {index + 1}
            </span>
            <div className="flex-1">
              <p className="text-lg font-medium text-gray-900 mb-2">{quiz.question}</p>
              {quiz.min_words && (
                <p className="text-sm text-gray-500">최소 {quiz.min_words}자 이상</p>
              )}
            </div>
          </div>

          <div className="ml-11 space-y-4">
            <textarea
              value={answers[index]}
              onChange={(e) => handleAnswer(index, e.target.value)}
              placeholder="답변을 작성하세요..."
              rows={8}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:outline-none resize-none"
            />

            <div className="flex items-center justify-between text-sm text-gray-600">
              <span>{answers[index].length}자</span>
              {quiz.min_words && answers[index].length < quiz.min_words && (
                <span className="text-orange-600">
                  {quiz.min_words - answers[index].length}자 더 작성하세요
                </span>
              )}
            </div>

            {/* Grading Criteria */}
            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="font-medium text-gray-900 mb-2">📋 채점 기준:</p>
              <ul className="space-y-1">
                {quiz.grading_criteria.map((criteria, i) => (
                  <li key={i} className="text-sm text-gray-700 flex items-start">
                    <span className="mr-2">•</span>
                    <span>{criteria}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Suggested Answer */}
            <div>
              <button
                onClick={() => toggleSuggested(index)}
                className="text-blue-600 hover:text-blue-700 font-medium text-sm"
              >
                {showSuggested[index] ? '▼ 모범답안 숨기기' : '▶ 모범답안 보기'}
              </button>

              {showSuggested[index] && (
                <div className="mt-3 p-4 bg-blue-50 border-l-4 border-blue-400 rounded">
                  <p className="text-sm font-medium text-blue-900 mb-2">💡 모범답안:</p>
                  <p className="text-sm text-blue-800 whitespace-pre-wrap">{quiz.suggested_answer}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
