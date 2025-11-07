'use client'

import { useState } from 'react'
import { ReadingMaterial } from '@/lib/api'

interface Props {
  material: ReadingMaterial
}

export default function ReadingMaterialView({ material }: Props) {
  const [fontSize, setFontSize] = useState(16)

  // Simple markdown-like rendering
  const renderContent = (content: string) => {
    const lines = content.split('\n')
    const elements: JSX.Element[] = []
    let listItems: string[] = []
    let key = 0

    const flushList = () => {
      if (listItems.length > 0) {
        elements.push(
          <ul key={`list-${key++}`} className="list-disc list-inside space-y-2 mb-4">
            {listItems.map((item, i) => (
              <li key={i} className="text-gray-700 leading-relaxed">{item}</li>
            ))}
          </ul>
        )
        listItems = []
      }
    }

    lines.forEach((line, index) => {
      // Headings
      if (line.startsWith('# ')) {
        flushList()
        elements.push(
          <h1 key={`h1-${key++}`} className="text-3xl font-bold text-gray-900 mb-4 mt-8">
            {line.substring(2)}
          </h1>
        )
      } else if (line.startsWith('## ')) {
        flushList()
        elements.push(
          <h2 key={`h2-${key++}`} className="text-2xl font-bold text-gray-900 mb-3 mt-6">
            {line.substring(3)}
          </h2>
        )
      } else if (line.startsWith('### ')) {
        flushList()
        elements.push(
          <h3 key={`h3-${key++}`} className="text-xl font-bold text-gray-900 mb-2 mt-4">
            {line.substring(4)}
          </h3>
        )
      }
      // List items
      else if (line.trim().startsWith('- ') || line.trim().startsWith('* ')) {
        listItems.push(line.trim().substring(2))
      }
      // Empty lines
      else if (line.trim() === '') {
        flushList()
        elements.push(<div key={`space-${key++}`} className="h-2" />)
      }
      // Regular paragraphs
      else if (line.trim()) {
        flushList()
        elements.push(
          <p key={`p-${key++}`} className="text-gray-700 leading-relaxed mb-4">
            {line}
          </p>
        )
      }
    })

    flushList()
    return elements
  }

  return (
    <div className="space-y-6">
      {/* Header with Controls */}
      <div className="flex items-center justify-between pb-4 border-b-2 border-gray-200">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">
            📖 {material.title}
          </h2>
          <p className="text-sm text-gray-500 mt-1">
            예상 읽기 시간: {material.estimated_reading_time}분
          </p>
        </div>

        {/* Font Size Controls */}
        <div className="flex items-center space-x-3 bg-gray-100 rounded-lg px-4 py-2">
          <span className="text-sm text-gray-600 font-medium">글자 크기:</span>
          <button
            onClick={() => setFontSize(Math.max(12, fontSize - 2))}
            className="w-8 h-8 flex items-center justify-center bg-white rounded-md hover:bg-gray-200 transition-colors"
            title="작게"
          >
            <span className="text-lg font-bold">-</span>
          </button>
          <span className="text-sm font-medium w-12 text-center">{fontSize}px</span>
          <button
            onClick={() => setFontSize(Math.min(24, fontSize + 2))}
            className="w-8 h-8 flex items-center justify-center bg-white rounded-md hover:bg-gray-200 transition-colors"
            title="크게"
          >
            <span className="text-lg font-bold">+</span>
          </button>
        </div>
      </div>

      {/* Reading Material Content */}
      <div
        className="prose prose-lg max-w-none bg-white p-8 rounded-lg shadow-sm border border-gray-100"
        style={{ fontSize: `${fontSize}px` }}
      >
        <div className="space-y-4">
          {renderContent(material.content)}
        </div>
      </div>

      {/* Reading Progress Indicator */}
      <div className="sticky bottom-0 bg-white border-t-2 border-gray-200 p-4 rounded-t-lg shadow-lg">
        <div className="flex items-center justify-between text-sm text-gray-600">
          <span>📚 읽기 자료</span>
          <span className="text-blue-600 font-medium">
            스크롤하여 계속 읽기
          </span>
        </div>
      </div>
    </div>
  )
}
