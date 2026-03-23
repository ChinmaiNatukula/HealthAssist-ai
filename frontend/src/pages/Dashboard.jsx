import { useState, useEffect } from 'react'
import { Routes, Route, Link, useNavigate, useLocation } from 'react-router-dom'
import axios from 'axios'
import { useAuth, useTheme } from '../App'
import SymptomChecker from '../components/SymptomChecker'
import ChatBot from '../components/ChatBot'
import DiseaseResult from '../components/DiseaseResult'
import ReportHistory from '../components/ReportHistory'
import ImageChecker from '../components/ImageChecker'

const API = 'http://localhost:5000/api'

export default function Dashboard() {
  const { user, token, logout } = useAuth()
  const { theme, toggleTheme } = useTheme()
  const navigate = useNavigate()
  const location = useLocation()

  const [predictions, setPredictions] = useState([])
  const [selectedSymptoms, setSelectedSymptoms] = useState([])
  const [predicting, setPredicting] = useState(false)
  const [activeTab, setActiveTab] = useState('dashboard')

  const headers = { Authorization: `Bearer ${token}` }

  const handlePredict = async (symptoms) => {
    setPredicting(true)
    setPredictions([])
    try {
      const { data } = await axios.post(`${API}/predict`, { symptoms }, { headers })
      setPredictions(data.predictions || [])
      // Save report
      if (data.predictions?.length > 0) {
        await axios.post(`${API}/reports`, { symptoms, predictions: data.predictions }, { headers })
      }
    } catch (err) {
      console.error('Prediction error:', err)
    } finally {
      setPredicting(false)
    }
  }

  const isReports = activeTab === 'reports'

  return (
    <>
      {/* Navbar */}
      <nav className="navbar">
        <a className="navbar-logo" href="#">
          <span className="logo-icon">🏥</span>
          HealthAssist AI
        </a>
        <div className="navbar-right">
          <button
            className="btn btn-secondary btn-sm"
            onClick={() => setActiveTab(isReports ? 'dashboard' : 'reports')}
          >
            {isReports ? '⬅ Dashboard' : '📋 My Reports'}
          </button>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span style={{ width: 28, height: 28, background: 'var(--gradient)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.7rem', fontWeight: 700, color: 'white' }}>
              {user?.name?.charAt(0)?.toUpperCase()}
            </span>
            {user?.name}
          </span>
          <button className="dark-toggle" onClick={toggleTheme} title="Toggle theme">
            {theme === 'dark' ? '☀️' : '🌙'}
          </button>
          <button className="btn btn-secondary btn-sm" onClick={logout}>Sign Out</button>
        </div>
      </nav>

      {/* Main Content */}
      {isReports ? (
        <div style={{ maxWidth: 1400, margin: '0 auto', padding: '24px', position: 'relative', zIndex: 1 }}>
          <div className="glass-card">
            <ReportHistory token={token} />
          </div>
        </div>
      ) : (
        <div className="dashboard">
          {/* Welcome Header */}
          <div className="glass-card dashboard-header">
            <div>
              <h1 className="dashboard-title">
                Good {getGreeting()}, {user?.name?.split(' ')[0]} 👋
              </h1>
              <p className="dashboard-subtitle">
                Describe your symptoms to get AI-powered health insights. Remember: this is not a substitute for professional medical advice.
              </p>
            </div>
            <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
              <span className="badge badge-green">● AI Active</span>
              <span className="badge badge-blue">ML Model Ready</span>
            </div>
          </div>

          {/* Symptom Checker */}
          <div className="glass-card symptom-panel">
            <SymptomChecker
              token={token}
              selectedSymptoms={selectedSymptoms}
              setSelectedSymptoms={setSelectedSymptoms}
              onPredict={handlePredict}
              predicting={predicting}
            />
          </div>

          {/* Results Panel */}
          <div className="glass-card results-panel">
            <DiseaseResult
              predictions={predictions}
              predicting={predicting}
              token={token}
            />
          </div>

          {/* Image Disease Checker — full width */}
          <div className="glass-card" style={{ gridColumn: '1 / -1', padding: '24px' }}>
            <ImageChecker />
          </div>

          {/* Chatbot — full width */}
          <div className="glass-card chatbot-panel" style={{ gridColumn: '1 / -1' }}>
            <ChatBot token={token} />
          </div>
        </div>
      )}
    </>
  )
}

function getGreeting() {
  const h = new Date().getHours()
  if (h < 12) return 'Morning'
  if (h < 17) return 'Afternoon'
  return 'Evening'
}
