'use client'

import { useState, useRef } from 'react'
import { VideoLecture, LectureSlide } from '@/lib/api'

interface Props {
  lecture: VideoLecture
}

export default function VideoLecturePlayer({ lecture }: Props) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const [selectedSlide, setSelectedSlide] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)

  const togglePlay = () => {
    const video = videoRef.current
    if (!video) return

    if (isPlaying) {
      video.pause()
    } else {
      video.play()
    }
    setIsPlaying(!isPlaying)
  }

  const formatDuration = (seconds?: number) => {
    if (!seconds) return '0:00'
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          🎥 {lecture.title}
        </h2>
        <p className="text-sm text-gray-500">
          총 {lecture.slides.length}개 슬라이드 |
          {lecture.total_duration ? ` ${formatDuration(lecture.total_duration)} 분량` : ' 생성 중...'}
        </p>
      </div>

      {/* Video Player */}
      {lecture.video_url ? (
        <div className="bg-black rounded-xl overflow-hidden shadow-2xl">
          <video
            ref={videoRef}
            src={lecture.video_url}
            controls
            className="w-full aspect-video"
            onPlay={() => setIsPlaying(true)}
            onPause={() => setIsPlaying(false)}
          >
            <p className="text-white p-4">
              Your browser does not support the video tag.
            </p>
          </video>
        </div>
      ) : (
        <div className="bg-gray-100 rounded-xl aspect-video flex items-center justify-center">
          <div className="text-center">
            <div className="text-6xl mb-4">⏳</div>
            <p className="text-gray-600 font-medium">
              비디오 생성 중... (10-15분 소요될 수 있습니다)
            </p>
          </div>
        </div>
      )}

      {/* Slides Navigation */}
      <div className="space-y-4">
        <h3 className="text-xl font-bold text-gray-900 flex items-center">
          <span className="mr-2">📊</span>
          강의 슬라이드 ({lecture.slides.length}개)
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {lecture.slides.map((slide, index) => (
            <div
              key={index}
              onClick={() => setSelectedSlide(index)}
              className={`
                p-5 rounded-lg border-2 cursor-pointer transition-all
                ${selectedSlide === index
                  ? 'border-blue-500 bg-blue-50 shadow-lg'
                  : 'border-gray-200 bg-white hover:border-blue-300 hover:shadow-md'
                }
              `}
            >
              <div className="flex items-start space-x-3">
                <div className={`
                  w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm
                  ${selectedSlide === index ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'}
                `}>
                  {slide.slide_number}
                </div>
                <div className="flex-1">
                  <h4 className="font-bold text-gray-900 mb-2">{slide.title}</h4>
                  <ul className="space-y-1 text-sm text-gray-700">
                    {slide.content.slice(0, 3).map((item, i) => (
                      <li key={i} className="flex items-start">
                        <span className="mr-2 text-blue-500">•</span>
                        <span>{item}</span>
                      </li>
                    ))}
                    {slide.content.length > 3 && (
                      <li className="text-gray-500 italic">
                        +{slide.content.length - 3}개 더...
                      </li>
                    )}
                  </ul>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Selected Slide Detail */}
      {selectedSlide !== null && (
        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-8 shadow-lg">
          <div className="flex items-start justify-between mb-4">
            <h3 className="text-2xl font-bold text-gray-900">
              {lecture.slides[selectedSlide].title}
            </h3>
            <span className="px-3 py-1 bg-blue-600 text-white rounded-full text-sm font-medium">
              슬라이드 {lecture.slides[selectedSlide].slide_number}
            </span>
          </div>

          <div className="space-y-6">
            {/* Content Points */}
            <div>
              <h4 className="font-semibold text-gray-900 mb-3">주요 내용:</h4>
              <ul className="space-y-2">
                {lecture.slides[selectedSlide].content.map((item, i) => (
                  <li key={i} className="flex items-start">
                    <span className="mr-3 text-blue-600 font-bold">✓</span>
                    <span className="text-gray-700">{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Narration */}
            <div>
              <h4 className="font-semibold text-gray-900 mb-3">나레이션:</h4>
              <p className="text-gray-700 leading-relaxed bg-white p-4 rounded-lg border border-blue-200">
                {lecture.slides[selectedSlide].narration}
              </p>
            </div>

            {lecture.slides[selectedSlide].duration && (
              <div className="text-sm text-gray-600">
                ⏱️ 예상 시간: {formatDuration(lecture.slides[selectedSlide].duration)}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
