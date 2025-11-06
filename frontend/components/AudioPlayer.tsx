'use client'

interface Props {
  audioUrl: string
}

export default function AudioPlayer({ audioUrl }: Props) {
  return (
    <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-gray-700 dark:to-gray-600 rounded-lg p-4">
      <div className="flex items-center space-x-4">
        <div className="text-2xl">🔊</div>
        <div className="flex-1">
          <p className="text-sm text-gray-600 dark:text-gray-300 mb-2">오디오 재생</p>
          <audio controls className="w-full" src={audioUrl}>
            오디오를 지원하지 않는 브라우저입니다.
          </audio>
        </div>
      </div>
    </div>
  )
}
