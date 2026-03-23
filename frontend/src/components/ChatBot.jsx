import { useState, useEffect, useRef } from 'react'
import axios from 'axios'

const API = 'http://localhost:5000/api'

const QUICK_CHIPS = [
  'I have a fever',
  'Tips for headache',
  'What causes diabetes?',
  'How to improve sleep?',
  'Chest pain advice',
  'Healthy diet tips',
]

const WELCOME_MSG = {
  role: 'bot',
  text: "Hello! 👋 I'm **HealthAssist AI**, your virtual health companion.\n\nI can answer health questions, provide guidance on symptoms, suggest remedies, and recommend when to see a doctor.\n\n_Tap a suggestion below or type your question!_"
}

export default function ChatBot({ token }) {
  const [messages, setMessages] = useState([WELCOME_MSG])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const sendMessage = async (text) => {
    const msg = text || input.trim()
    if (!msg) return
    setInput('')
    setMessages(prev => [...prev, { role: 'user', text: msg }])
    setLoading(true)
    try {
      const { data } = await axios.post(`${API}/chat`, { message: msg })
      setMessages(prev => [...prev, { role: 'bot', text: data.reply }])
    } catch {
      setMessages(prev => [...prev, { role: 'bot', text: '⚠ Sorry, I could not connect to the server. Please make sure the backend is running.' }])
    } finally {
      setLoading(false)
    }
  }

  const handleKey = e => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage() }
  }

  return (
    <>
      <div className="panel-header">
        <div className="panel-icon panel-icon-green">🤖</div>
        <div>
          <div className="panel-title">AI Health Assistant</div>
          <div className="panel-subtitle">Ask about symptoms, conditions, diet & more</div>
        </div>
        <span className="badge badge-green" style={{ marginLeft: 'auto' }}>● Online</span>
      </div>

      <div className="chat-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`chat-bubble ${msg.role}`}>
            <div className="bubble-label">{msg.role === 'bot' ? '🤖 HealthAssist AI' : '👤 You'}</div>
            <FormattedText text={msg.text} />
          </div>
        ))}
        {loading && (
          <div className="chat-bubble bot">
            <div className="bubble-label">🤖 HealthAssist AI</div>
            <div className="typing-dots">
              <span /><span /><span />
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Quick suggestions */}
      <div className="quick-chips">
        {QUICK_CHIPS.map(chip => (
          <button key={chip} className="quick-chip" onClick={() => sendMessage(chip)}>
            {chip}
          </button>
        ))}
      </div>

      <div className="chat-input-row">
        <div className="chat-input-wrap">
          <input
            className="input"
            placeholder="Ask a health question..."
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKey}
            disabled={loading}
          />
        </div>
        <button className="btn btn-primary" onClick={() => sendMessage()} disabled={loading || !input.trim()}>
          Send ➤
        </button>
      </div>
    </>
  )
}

// Simple markdown-like renderer
function FormattedText({ text }) {
  if (!text) return null
  // Split on newlines and render basic bold + bullets
  const lines = text.split('\n')
  return (
    <div>
      {lines.map((line, i) => {
        if (!line.trim()) return <br key={i} />
        // bold
        const parts = line.split(/(\*\*.*?\*\*)/g)
        return (
          <p key={i} style={{ marginBottom: 2 }}>
            {parts.map((part, j) => {
              if (part.startsWith('**') && part.endsWith('**')) {
                return <strong key={j}>{part.slice(2, -2)}</strong>
              }
              if (part.startsWith('_') && part.endsWith('_')) {
                return <em key={j}>{part.slice(1, -1)}</em>
              }
              return part
            })}
          </p>
        )
      })}
    </div>
  )
}
