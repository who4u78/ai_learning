'use client'

import { useState, useRef, useEffect } from 'react'
import { Podcast, PodcastDialogue } from '@/lib/api'

interface Props {
  podcast: Podcast
}

export default function PodcastPlayer({ podcast }: Props) {
  const audioRef = useRef<HTMLAudioElement>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [currentDialogueIndex, setCurrentDialogueIndex] = useState(0)

  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return

    const handleTimeUpdate = () => {
      setCurrentTime(audio.currentTime)
    }

    const handleLoadedMetadata = () => {
      setDuration(audio.duration)
    }

    const handleEnded = () => {
      setIsPlaying(false)
    }

    audio.addEventListener('timeupdate', handleTimeUpdate)
    audio.addEventListener('loadedmetadata', handleLoadedMetadata)
    audio.addEventListener('ended', handleEnded)

    return () => {
      audio.removeEventListener('timeupdate', handleTimeUpdate)
      audio.removeEventListener('loadedmetadata', handleLoadedMetadata)
      audio.removeEventListener('ended', handleEnded)
    }
  }, [])

  const togglePlay = () => {
    const audio = audioRef.current
    if (!audio) return

    if (isPlaying) {
      audio.pause()
    } else {
      audio.play()
    }
    setIsPlaying(!isPlaying)
  }

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const audio = audioRef.current
    if (!audio) return

    const time = parseFloat(e.target.value)
    audio.currentTime = time
    setCurrentTime(time)
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          📻 {podcast.script.title}
        </h2>
        <p className="text-gray-600">
          진행자: {podcast.script.host_name} | 게스트: {podcast.script.guest_name}
        </p>
        <p className="text-sm text-gray-500 mt-1">
          예상 시간: {podcast.script.duration_minutes}분
        </p>
      </div>

      {/* Audio Player */}
      {podcast.audio_url ? (
        <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl p-6 shadow-lg">
          <audio ref={audioRef} src={podcast.audio_url} />

          {/* Waveform / Progress */}
          <div className="mb-4">
            <input
              type="range"
              min="0"
              max={duration || 0}
              value={currentTime}
              onChange={handleSeek}
              className="w-full h-2 bg-gray-300 rounded-lg appearance-none cursor-pointer accent-blue-600"
            />
            <div className="flex justify-between text-sm text-gray-600 mt-2">
              <span>{formatTime(currentTime)}</span>
              <span>{formatTime(duration)}</span>
            </div>
          </div>

          {/* Play Controls */}
          <div className="flex items-center justify-center space-x-4">
            <button
              onClick={togglePlay}
              className="w-16 h-16 flex items-center justify-center bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-all shadow-lg"
            >
              {isPlaying ? (
                <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              ) : (
                <svg className="w-8 h-8 ml-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
                </svg>
              )}
            </button>
          </div>
        </div>
      ) : (
        <div className="bg-yellow-50 border-2 border-yellow-200 rounded-lg p-4 text-center">
          <p className="text-yellow-800">
            ⏳ 오디오 생성 중... (몇 분 소요될 수 있습니다)
          </p>
        </div>
      )}

      {/* Transcript */}
      <div className="space-y-4">
        <h3 className="text-xl font-bold text-gray-900 flex items-center">
          <span className="mr-2">📝</span>
          대화 스크립트
        </h3>

        <div className="space-y-3 max-h-[600px] overflow-y-auto">
          {podcast.script.dialogues.map((dialogue, index) => (
            <div
              key={index}
              className={`
                p-4 rounded-lg transition-all
                ${dialogue.speaker === 'host'
                  ? 'bg-blue-50 border-l-4 border-blue-400'
                  : 'bg-green-50 border-l-4 border-green-400'
                }
                ${index === currentDialogueIndex ? 'ring-2 ring-offset-2 ring-blue-500' : ''}
              `}
            >
              <div className="flex items-start space-x-3">
                <div className={`
                  w-10 h-10 rounded-full flex items-center justify-center text-white font-bold
                  ${dialogue.speaker === 'host' ? 'bg-blue-500' : 'bg-green-500'}
                `}>
                  {dialogue.speaker === 'host' ? 'H' : 'G'}
                </div>
                <div className="flex-1">
                  <div className="font-semibold text-gray-900 mb-1">
                    {dialogue.speaker === 'host' ? podcast.script.host_name : podcast.script.guest_name}
                  </div>
                  <p className="text-gray-700 leading-relaxed">{dialogue.text}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
