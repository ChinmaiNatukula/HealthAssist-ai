import { useState, useEffect } from 'react'
import axios from 'axios'

const API = 'http://localhost:5000/api'

const RANK_LABELS = ['1st', '2nd', '3rd']

export default function DiseaseResult({ predictions, predicting, token }) {
  const [expanded, setExpanded] = useState(null)
  const [diseaseInfo, setDiseaseInfo] = useState({})
  const [loadingInfo, setLoadingInfo] = useState(false)

  useEffect(() => {
    setExpanded(null)
    setDiseaseInfo({})
  }, [predictions])

  const toggleExpand = async (disease, idx) => {
    if (expanded === idx) { setExpanded(null); return }
    setExpanded(idx)
    if (diseaseInfo[disease]) return
    setLoadingInfo(true)
    try {
      const { data } = await axios.get(`${API}/disease/${encodeURIComponent(disease)}`)
      setDiseaseInfo(prev => ({ ...prev, [disease]: data }))
    } catch {
      setDiseaseInfo(prev => ({ ...prev, [disease]: null }))
    } finally {
      setLoadingInfo(false)
    }
  }

  return (
    <>
      <div className="panel-header">
        <div className="panel-icon panel-icon-purple">📊</div>
        <div>
          <div className="panel-title">Prediction Results</div>
          <div className="panel-subtitle">
            {predictions.length > 0 ? 'Click a condition for detailed info' : 'Run symptom checker to see results'}
          </div>
        </div>
        {predictions.length > 0 && (
          <span className="badge badge-purple" style={{ marginLeft: 'auto' }}>{predictions.length} conditions</span>
        )}
      </div>

      {predicting && (
        <div style={{ textAlign: 'center', padding: '32px 0' }}>
          <div className="spinner" />
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Analyzing symptoms with AI...</p>
        </div>
      )}

      {!predicting && predictions.length === 0 && (
        <div className="empty-state">
          <div className="empty-icon">🔬</div>
          <p>Enter your symptoms and click <strong>Predict</strong> to see possible conditions.</p>
        </div>
      )}

      {!predicting && predictions.map((pred, idx) => {
        const info = diseaseInfo[pred.disease]
        const isOpen = expanded === idx

        return (
          <div
            key={pred.disease}
            className={`result-card rank-${idx + 1}`}
            onClick={() => toggleExpand(pred.disease, idx)}
            style={{ cursor: 'pointer' }}
          >
            <div className="result-header">
              <div>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  {RANK_LABELS[idx]} most likely
                </span>
                <div className="result-disease">{pred.disease}</div>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <span className="result-prob">{pred.probability}%</span>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>{isOpen ? '▲' : '▼'}</span>
              </div>
            </div>

            <div className="prob-bar">
              <div className="prob-bar-fill" style={{ width: `${pred.probability}%` }} />
            </div>

            {/* Expanded detail */}
            {isOpen && (
              <div className="disease-detail" onClick={e => e.stopPropagation()}>
                {loadingInfo && !info && (
                  <div style={{ padding: '12px 0', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
                    Loading disease information...
                  </div>
                )}
                {info === null && (
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
                    Detailed information not available for this condition.
                  </p>
                )}
                {info && (
                  <>
                    <InfoSection title="🦠 Common Causes" items={info.causes} />
                    <InfoSection title="🤒 Key Symptoms" items={info.symptoms} />
                    <InfoSection title="🛡️ Precautions" items={info.precautions} />
                    <InfoSection title="💊 Basic Treatment" items={info.basic_treatment} />
                    {info.when_to_see_doctor && (
                      <div className="see-doctor">
                        <strong>⚠ When to see a doctor:</strong> {info.when_to_see_doctor}
                      </div>
                    )}
                  </>
                )}
              </div>
            )}
          </div>
        )
      })}

      {!predicting && predictions.length > 0 && (
        <div style={{ padding: '12px', background: 'rgba(252,129,129,0.06)', border: '1px solid rgba(252,129,129,0.15)', borderRadius: '10px', fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
          ⚠ <strong>Disclaimer:</strong> These predictions are AI-generated and for informational purposes only. Always consult a qualified healthcare professional for proper diagnosis.
        </div>
      )}
    </>
  )
}

function InfoSection({ title, items }) {
  if (!items?.length) return null
  return (
    <div style={{ marginBottom: '14px' }}>
      <h4>{title}</h4>
      <ul>
        {items.map((item, i) => <li key={i}>{item}</li>)}
      </ul>
    </div>
  )
}
