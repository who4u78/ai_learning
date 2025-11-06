import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: '한글 AI 학습 플랫폼',
  description: 'HTML/텍스트를 한글 학습 콘텐츠로 자동 변환하는 AI 플랫폼',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  )
}
