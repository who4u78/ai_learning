import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// ============= 타입 정의 =============

export interface ContentGenerationRequest {
  source_type: 'url' | 'html' | 'text' | 'file'
  source_data: string
  title?: string
  language?: string
}

export interface ContentGenerationStatus {
  content_id: string
  status: 'processing' | 'completed' | 'failed'
  progress: number
  current_task?: string
  error?: string
}

// 팟캐스트
export interface PodcastDialogue {
  speaker: 'host' | 'guest'
  text: string
  timestamp?: number
}

export interface PodcastScript {
  title: string
  host_name: string
  guest_name: string
  dialogues: PodcastDialogue[]
  duration_minutes: number
}

export interface Podcast {
  id: string
  script: PodcastScript
  audio_url?: string
  duration?: number
  created_at: string
}

// 강의 비디오
export interface LectureSlide {
  slide_number: number
  title: string
  content: string[]
  narration: string
  duration?: number
  image_path?: string
}

export interface VideoLecture {
  id: string
  title: string
  slides: LectureSlide[]
  video_url?: string
  total_duration?: number
  created_at: string
}

// 읽기 자료
export interface ReadingMaterial {
  id: string
  title: string
  content: string
  estimated_reading_time: number
  created_at: string
}

// 질문 및 퀴즈
export interface DeepThinkingQuestion {
  question: string
  context?: string
  hints?: string[]
}

export interface MultipleChoiceQuiz {
  question: string
  options: string[]
  correct_answer: number
  explanation: string
  difficulty?: string
}

export interface ShortAnswerQuiz {
  question: string
  correct_answers: string[]
  explanation: string
  case_sensitive: boolean
}

export interface EssayQuiz {
  question: string
  suggested_answer: string
  grading_criteria: string[]
  min_words?: number
}

// 통합 학습 콘텐츠
export interface LearningContent {
  id: string
  title: string
  description: string
  podcast?: Podcast
  video_lecture?: VideoLecture
  reading_material?: ReadingMaterial
  deep_questions: DeepThinkingQuestion[]
  multiple_choice_quizzes: MultipleChoiceQuiz[]
  short_answer_quizzes: ShortAnswerQuiz[]
  essay_quizzes: EssayQuiz[]
  source_url?: string
  source_text?: string
  created_at: string
  updated_at: string
  metadata?: any
}

// 챗봇
export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

export interface ChatRequest {
  content_id: string
  message: string
  conversation_history?: ChatMessage[]
}

export interface ChatResponse {
  message: string
  timestamp: string
}

// ============= API 함수들 =============

export const learningApi = {
  // 콘텐츠 생성 시작
  generateContent: async (request: ContentGenerationRequest): Promise<ContentGenerationStatus> => {
    const response = await api.post('/api/learning/generate', request)
    return response.data
  },

  // 생성 상태 확인
  getStatus: async (contentId: string): Promise<ContentGenerationStatus> => {
    const response = await api.get(`/api/learning/status/${contentId}`)
    return response.data
  },

  // 학습 콘텐츠 조회
  getContent: async (contentId: string): Promise<LearningContent> => {
    const response = await api.get(`/api/learning/${contentId}`)
    return response.data
  },

  // 챗봇 대화
  chat: async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await api.post('/api/learning/chat', request)
    return response.data
  },
}

export const healthApi = {
  check: async () => {
    const response = await api.get('/health')
    return response.data
  },
}

export default api
