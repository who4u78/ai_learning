import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 타입 정의
export interface ContentGenerationRequest {
  source_type: 'url' | 'html' | 'text' | 'file'
  source_data: string
  title?: string
  language?: string
  include_quiz?: boolean
  include_summary?: boolean
  include_examples?: boolean
}

export interface LearningSection {
  id: string
  title: string
  content: string
  order: number
  estimated_time?: number
}

export interface Quiz {
  question: string
  options: string[]
  correct_answer: number
  explanation: string
}

export interface GeneratedContent {
  id: string
  title: string
  summary: string
  sections: LearningSection[]
  quizzes?: Quiz[]
  created_at: string
  metadata?: any
}

export interface TTSRequest {
  text: string
  voice_id?: string
  speed?: number
  format?: string
}

export interface TTSResponse {
  audio_url: string
  duration: number
  file_path: string
}

export interface VideoGenerationRequest {
  content_id: string
  section_ids?: string[]
  include_subtitles?: boolean
  resolution?: string
  fps?: number
}

export interface VideoGenerationResponse {
  video_url: string
  file_path: string
  duration: number
  size_mb: number
}

// API 함수들
export const contentApi = {
  generate: async (request: ContentGenerationRequest): Promise<GeneratedContent> => {
    const response = await api.post('/api/content/generate', request)
    return response.data
  },

  get: async (contentId: string): Promise<GeneratedContent> => {
    const response = await api.get(`/api/content/${contentId}`)
    return response.data
  },

  list: async (skip: number = 0, limit: number = 10) => {
    const response = await api.get('/api/content/', { params: { skip, limit } })
    return response.data
  },

  delete: async (contentId: string) => {
    const response = await api.delete(`/api/content/${contentId}`)
    return response.data
  },
}

export const audioApi = {
  generate: async (request: TTSRequest): Promise<TTSResponse> => {
    const response = await api.post('/api/audio/generate', request)
    return response.data
  },

  generateForContent: async (
    contentId: string,
    sectionIds?: string[],
    voiceId?: string
  ) => {
    const response = await api.post(`/api/audio/generate-for-content/${contentId}`, {
      section_ids: sectionIds,
      voice_id: voiceId,
    })
    return response.data
  },

  getFile: (filename: string) => {
    return `${API_BASE_URL}/api/audio/file/${filename}`
  },
}

export const videoApi = {
  generate: async (request: VideoGenerationRequest): Promise<VideoGenerationResponse> => {
    const response = await api.post('/api/video/generate', request)
    return response.data
  },

  getStatus: async (contentId: string) => {
    const response = await api.get(`/api/video/status/${contentId}`)
    return response.data
  },

  getFile: (filename: string) => {
    return `${API_BASE_URL}/api/video/file/${filename}`
  },
}

export const healthApi = {
  check: async () => {
    const response = await api.get('/health')
    return response.data
  },
}

export default api
