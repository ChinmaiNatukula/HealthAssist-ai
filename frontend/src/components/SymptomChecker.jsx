import { useState, useEffect, useRef } from 'react'
import axios from 'axios'

const API = 'http://localhost:5000/api'

export default function SymptomChecker({ token, selectedSymptoms, setSelectedSymptoms, onPredict, predicting }) {
  const [search, setSearch] = useState('')
  const [allSymptoms, setAllSymptoms] = useState([])
  const [filtered, setFiltered] = useState([])
  const [showDropdown, setShowDropdown] = useState(false)
  const dropRef = useRef(null)

  useEffect(() => {
    axios.get(`${API}/predict/symptoms`).then(({ data }) => {
      setAllSymptoms(data.symptoms || [])
    }).catch(() => {
      // Fallback symptoms
      setAllSymptoms([
        'Fever', 'Headache', 'Cough', 'Fatigue', 'Nausea', 'Vomiting',
        'Diarrhea', 'Chest Pain', 'Shortness Of Breath', 'Itching',
        'Skin Rash', 'Joint Pain', 'Back Pain', 'Dizziness', 'Chills',
        'Sweating', 'Loss Of Appetite', 'Abdominal Pain', 'Yellowing Of Eyes',
        'High Fever', 'Muscle Pain', 'Runny Nose', 'Sore Throat', 'Sneezing',
      ])
    })
  }, [])

  useEffect(() => {
    if (search.trim().length === 0) { setFiltered([]); return }
    const q = search.toLowerCase()
    setFiltered(
      allSymptoms.filter(s =>
        s.toLowerCase().includes(q) &&
        !selectedSymptoms.includes(s)
      ).slice(0, 8)
    )
  }, [search, allSymptoms, selectedSymptoms])

  // Close dropdown on outside click
  useEffect(() => {
    const handler = (e) => { if (dropRef.current && !dropRef.current.contains(e.target)) setShowDropdown(false) }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  const addSymptom = (sym) => {
    if (!selectedSymptoms.includes(sym)) setSelectedSymptoms(prev => [...prev, sym])
    setSearch('')
    setShowDropdown(false)
  }

  const removeSymptom = (sym) => setSelectedSymptoms(prev => prev.filter(s => s !== sym))

  const handleSubmit = () => {
    if (selectedSymptoms.length === 0) return
    // Convert display names to raw snake_case
    const raw = selectedSymptoms.map(s => s.toLowerCase().replace(/ /g, '_'))
    onPredict(raw)
  }

  return (
    <>
      <div className="panel-header">
        <div className="panel-icon panel-icon-blue">🩺</div>
        <div>
          <div className="panel-title">Symptom Checker</div>
          <div className="panel-subtitle">Add your symptoms to get AI predictions</div>
        </div>
      </div>

      {/* Search */}
      <div className="symptom-search-wrap" ref={dropRef}>
        <span className="search-icon">🔍</span>
        <input
          className="input"
          placeholder="Search symptoms (e.g. fever, headache...)"
          value={search}
          onChange={e => { setSearch(e.target.value); setShowDropdown(true) }}
          onFocus={() => setShowDropdown(true)}
        />
        {showDropdown && filtered.length > 0 && (
          <div className="symptom-dropdown">
            {filtered.map(s => (
              <div key={s} className="symptom-option" onMouseDown={() => addSymptom(s)}>
                + {s}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Selected tags */}
      <div className="selected-symptoms">
        {selectedSymptoms.length === 0 && (
          <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem', alignSelf: 'center' }}>
            No symptoms selected yet
          </span>
        )}
        {selectedSymptoms.map(s => (
          <span key={s} className="symptom-tag">
            {s}
            <button onClick={() => removeSymptom(s)} title="Remove">✕</button>
          </span>
        ))}
      </div>

      {/* Common symptoms quick-add */}
      <div style={{ marginBottom: '16px' }}>
        <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '8px', fontWeight: 500, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          Common symptoms:
        </div>
        <div className="quick-chips">
          {['Fever', 'Headache', 'Cough', 'Fatigue', 'Nausea', 'Itching', 'Chest Pain', 'Dizziness'].map(s => (
            <button
              key={s}
              className="quick-chip"
              onClick={() => addSymptom(s)}
              disabled={selectedSymptoms.includes(s)}
              style={{ opacity: selectedSymptoms.includes(s) ? 0.4 : 1 }}
            >
              {s}
            </button>
          ))}
        </div>
      </div>

      <div className="divider" />

      <button
        className="btn btn-primary btn-full"
        onClick={handleSubmit}
        disabled={selectedSymptoms.length === 0 || predicting}
      >
        {predicting ? (
          <><span className="spinner" style={{ width: 16, height: 16, margin: 0, borderWidth: 2 }} /> Analyzing...</>
        ) : (
          <> Predict Possible Conditions ({selectedSymptoms.length} symptom{selectedSymptoms.length !== 1 ? 's' : ''})</>
        )}
      </button>

      {selectedSymptoms.length > 0 && (
        <button
          className="btn btn-secondary btn-full"
          style={{ marginTop: '8px' }}
          onClick={() => setSelectedSymptoms([])}
        >
          Clear All
        </button>
      )}
    </>
  )
}
