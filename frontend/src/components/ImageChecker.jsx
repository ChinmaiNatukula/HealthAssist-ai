import { useState, useRef, useCallback } from 'react'
import axios from 'axios'

const API = 'http://localhost:5000/api'

const RANK_COLORS = [
  { card: 'rgba(79,172,254,0.08)', bar: 'linear-gradient(135deg,#4facfe,#00f2fe)', badge: 'badge-blue', accent: 'var(--accent)' },
  { card: 'rgba(167,139,250,0.08)', bar: 'linear-gradient(135deg,#a78bfa,#818cf8)', badge: 'badge-purple', accent: 'var(--accent-purple)' },
  { card: 'rgba(86,239,138,0.08)', bar: 'linear-gradient(135deg,#43e97b,#38f9d7)', badge: 'badge-green', accent: 'var(--accent-green)' },
]

export default function ImageChecker() {
  const [dragging, setDragging] = useState(false)
  const [preview, setPreview] = useState(null)       // local preview URL
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)         // API response
  const [error, setError] = useState('')
  const [expanded, setExpanded] = useState(null)
  const fileInput = useRef(null)

  /* ── File handling ─────────────────────────────── */
  const handleFile = (f) => {
    if (!f) return
    const allowed = ['image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/webp']
    if (!allowed.includes(f.type)) {
      setError('Please upload a valid image file (JPG, PNG, GIF, BMP, WEBP).')
      return
    }
    setError('')
    setResult(null)
    setExpanded(null)
    setFile(f)
    setPreview(URL.createObjectURL(f))
  }

  const onDrop = useCallback((e) => {
    e.preventDefault()
    setDragging(false)
    const f = e.dataTransfer?.files?.[0]
    if (f) handleFile(f)
  }, [])

  const onDragOver = (e) => { e.preventDefault(); setDragging(true) }
  const onDragLeave = () => setDragging(false)

  /* ── API call ──────────────────────────────────── */
  const analyzeImage = async () => {
    if (!file) return
    setLoading(true)
    setError('')
    setResult(null)
    setExpanded(null)
    try {
      const form = new FormData()
      form.append('image', file)
      const { data } = await axios.post(`${API}/image-predict`, form, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setResult(data)
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to analyze image. Please ensure the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const reset = () => {
    setFile(null)
    setPreview(null)
    setResult(null)
    setError('')
    setExpanded(null)
    if (fileInput.current) fileInput.current.value = ''
  }

  return (
    <>
      {/* Header */}
      <div className="panel-header">
        <div className="panel-icon" style={{ background: 'rgba(255,180,50,0.15)', fontSize: '1rem', width: 36, height: 36, borderRadius: 10, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          🔬
        </div>
        <div>
          <div className="panel-title">Image Disease Detector</div>
          <div className="panel-subtitle">Upload a skin photo for AI-powered condition analysis</div>
        </div>
        <span className="badge badge-blue" style={{ marginLeft: 'auto' }}>Computer Vision</span>
      </div>

      {/* Upload zone */}
      {!preview && (
        <div
          onDrop={onDrop}
          onDragOver={onDragOver}
          onDragLeave={onDragLeave}
          onClick={() => fileInput.current?.click()}
          style={{
            border: `2px dashed ${dragging ? 'var(--accent)' : 'var(--border)'}`,
            borderRadius: 'var(--radius)',
            padding: '48px 24px',
            textAlign: 'center',
            cursor: 'pointer',
            background: dragging ? 'rgba(79,172,254,0.06)' : 'var(--bg-input)',
            transition: 'all 0.25s',
            marginBottom: 16,
          }}
        >
          <div style={{ fontSize: '3rem', marginBottom: 12 }}>📷</div>
          <div style={{ fontWeight: 600, marginBottom: 6 }}>Drop your image here</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: 16 }}>
            or click to browse — JPG, PNG, GIF, WEBP supported
          </div>
          <button className="btn btn-secondary" style={{ pointerEvents: 'none' }}>
            Browse Files
          </button>
          <input
            ref={fileInput}
            type="file"
            accept="image/*"
            style={{ display: 'none' }}
            onChange={e => handleFile(e.target.files?.[0])}
          />
        </div>
      )}

      {/* Image preview + actions */}
      {preview && (
        <div style={{ display: 'flex', gap: 16, marginBottom: 16, flexWrap: 'wrap' }}>
          <div style={{ position: 'relative', flexShrink: 0 }}>
            <img
              src={preview}
              alt="Uploaded preview"
              style={{
                width: 140, height: 140,
                objectFit: 'cover',
                borderRadius: 'var(--radius-sm)',
                border: '2px solid var(--border)',
                display: 'block'
              }}
            />
            {result && (
              <div style={{
                position: 'absolute', inset: 0,
                background: 'rgba(0,0,0,0.45)',
                borderRadius: 'var(--radius-sm)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: '1.6rem'
              }}>✅</div>
            )}
          </div>
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 10 }}>
            <div>
              <div style={{ fontWeight: 600, fontSize: '0.9rem', marginBottom: 4 }}>{file?.name}</div>
              <div style={{ color: 'var(--text-secondary)', fontSize: '0.8rem' }}>
                {(file?.size / 1024).toFixed(1)} KB
                {result && ` · ${result.image_size?.[0]}×${result.image_size?.[1]}px`}
              </div>
            </div>

            {/* Feature summary badges */}
            {result?.features_summary && (
              <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                <span className="badge badge-blue">🔴 Redness: {result.features_summary.redness_level}</span>
                <span className="badge badge-purple">⬛ Darkness: {result.features_summary.darkness_level}</span>
                <span className="badge badge-green">📐 Contrast: {result.features_summary.contrast}</span>
              </div>
            )}

            <div style={{ display: 'flex', gap: 8 }}>
              {!loading && !result && (
                <button className="btn btn-primary btn-sm" onClick={analyzeImage}>
                  🔬 Analyze Image
                </button>
              )}
              {loading && (
                <button className="btn btn-primary btn-sm" disabled>
                  <span className="spinner" style={{ width: 14, height: 14, margin: 0, borderWidth: 2 }} />
                  Analyzing...
                </button>
              )}
              {result && (
                <button className="btn btn-primary btn-sm" onClick={analyzeImage}>
                  ↻ Re-analyze
                </button>
              )}
              <button className="btn btn-secondary btn-sm" onClick={reset}>
                ✕ Remove
              </button>
            </div>
          </div>
        </div>
      )}

      {error && <div className="error-msg">⚠ {error}</div>}

      {/* Results */}
      {result && !loading && (
        <>
          <div className="divider" />
          <div style={{ marginBottom: 14 }}>
            <div style={{ fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)', marginBottom: 12 }}>
              AI Analysis — Top 3 Possible Conditions
            </div>
            {result.predictions.map((pred, idx) => {
              const col = RANK_COLORS[idx]
              const isOpen = expanded === idx
              return (
                <div
                  key={pred.condition}
                  onClick={() => setExpanded(isOpen ? null : idx)}
                  style={{
                    padding: '16px',
                    background: col.card,
                    border: `1px solid ${isOpen ? 'var(--border-hover)' : 'var(--border)'}`,
                    borderRadius: 'var(--radius-sm)',
                    marginBottom: 10,
                    cursor: 'pointer',
                    transition: 'all 0.2s',
                    position: 'relative',
                    overflow: 'hidden',
                  }}
                >
                  {/* Left color bar */}
                  <div style={{ position: 'absolute', left: 0, top: 0, bottom: 0, width: 3, background: col.bar, borderRadius: '3px 0 0 3px' }} />

                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
                    <div>
                      <div style={{ fontSize: '0.72rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)', marginBottom: 2 }}>
                        #{idx + 1} Most Likely
                      </div>
                      <div style={{ fontWeight: 700, fontSize: '0.95rem' }}>{pred.condition}</div>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <span className={`badge ${col.badge}`} style={{ fontWeight: 700 }}>{pred.probability}%</span>
                      <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>{isOpen ? '▲' : '▼'}</span>
                    </div>
                  </div>

                  {/* Probability bar */}
                  <div style={{ height: 4, background: 'var(--border)', borderRadius: 2, overflow: 'hidden', marginBottom: 8 }}>
                    <div style={{ height: '100%', width: `${pred.probability}%`, background: col.bar, borderRadius: 2, transition: 'width 1s ease' }} />
                  </div>

                  <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>{pred.description}</div>

                  {/* Expanded Details */}
                  {isOpen && (
                    <div
                      className="disease-detail"
                      style={{ marginTop: 14, paddingTop: 14, borderTop: '1px solid var(--border)' }}
                      onClick={e => e.stopPropagation()}
                    >
                      <InfoBox title="👁️ Visual Clues" items={pred.visual_clues} />
                      <InfoBox title="🦠 Common Causes" items={pred.causes} />
                      <InfoBox title="🛡️ Precautions" items={pred.precautions} />
                      <InfoBox title="💊 Basic Treatment" items={pred.basic_treatment} />
                      {pred.when_to_see_doctor && (
                        <div className="see-doctor">
                          <strong>⚠ When to see a doctor:</strong> {pred.when_to_see_doctor}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )
            })}
          </div>

          {/* Disclaimer */}
          <div style={{ padding: '10px 14px', background: 'rgba(252,129,129,0.07)', border: '1px solid rgba(252,129,129,0.15)', borderRadius: 10, fontSize: '0.76rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
            ⚠ <strong>Disclaimer:</strong> This AI analysis is based on image color and texture features and is <strong>not a medical diagnosis</strong>. Always consult a qualified dermatologist for proper skin condition evaluation.
          </div>
        </>
      )}
    </>
  )
}

function InfoBox({ title, items }) {
  if (!items?.length) return null
  return (
    <div style={{ marginBottom: 12 }}>
      <h4 style={{ fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-secondary)', marginBottom: 6 }}>{title}</h4>
      <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: 3 }}>
        {items.map((item, i) => (
          <li key={i} style={{ fontSize: '0.83rem', color: 'var(--text-secondary)', paddingLeft: 14, position: 'relative' }}>
            <span style={{ position: 'absolute', left: 4, color: 'var(--accent)' }}>•</span>
            {item}
          </li>
        ))}
      </ul>
    </div>
  )
}
