'use client'

export default function Header() {
  return (
    <header className="bg-white dark:bg-gray-900 shadow-md">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="text-4xl">📚</div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                한글 AI 학습 플랫폼
              </h1>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                AI가 만드는 맞춤형 한글 학습 콘텐츠
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <a
              href="https://github.com/yourusername/ai-learning"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white"
            >
              GitHub
            </a>
          </div>
        </div>
      </div>
    </header>
  )
}
