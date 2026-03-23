import { useState, useEffect } from 'react'
import axios from 'axios'

const API = 'http://localhost:5000/api'

export default function ReportHistory({ token }) {
  const [reports, setReports] = useState([])
  const [loading, setLoading] = useState(true)
  const [deleting, setDeleting] = useState(null)

  const headers = { Authorization: `Bearer ${token}` }

  const fetchReports = async () => {
    setLoading(true)
    try {
      const { data } = await axios.get(`${API}/reports`, { headers })
      setReports(data.reports || [])
    } catch {
      setReports([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchReports() }, [])

  const deleteReport = async (id) => {
    setDeleting(id)
    try {
      await axios.delete(`${API}/reports/${id}`, { headers })
      setReports(prev => prev.filter(r => r.id !== id))
    } catch {
    } finally {
      setDeleting(null)
    }
  }

  const formatDate = (iso) => new Date(iso).toLocaleDateString('en-IN', {
    day: 'numeric', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })

  return (
    <div style={{ padding: '24px' }}>
      <div className="panel-header" style={{ marginBottom: '24px' }}>
        <div className="panel-icon panel-icon-purple">📋</div>
        <div>
          <div className="panel-title">My Health Reports</div>
          <div className="panel-subtitle">Previous symptom checker results</div>
        </div>
        <button
          className="btn btn-secondary btn-sm"
          style={{ marginLeft: 'auto' }}
          onClick={fetchReports}
          disabled={loading}
        >
          ↻ Refresh
        </button>
      </div>

      {loading && <div className="spinner" />}

      {!loading && reports.length === 0 && (
        <div className="empty-state">
          <div className="empty-icon">📄</div>
          <p>No reports yet. Use the Symptom Checker to generate your first report!</p>
        </div>
      )}

      {!loading && reports.length > 0 && (
        <table className="reports-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Date & Time</th>
              <th>Symptoms</th>
              <th>Top Prediction</th>
              <th>Confidence</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {reports.map((report, idx) => {
              let symptoms = []
              let predictions = []
              try { symptoms = JSON.parse(report.symptoms) } catch {}
              try { predictions = JSON.parse(report.predictions) } catch {}
              const top = predictions[0]
              return (
                <tr key={report.id}>
                  <td style={{ color: 'var(--text-muted)', fontWeight: 600, width: 40 }}>
                    #{reports.length - idx}
                  </td>
                  <td style={{ whiteSpace: 'nowrap', color: 'var(--text-secondary)' }}>
                    {formatDate(report.timestamp)}
                  </td>
                  <td>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                      {symptoms.slice(0, 4).map(s => (
                        <span key={s} className="badge badge-blue" style={{ fontSize: '0.7rem', padding: '2px 8px' }}>
                          {s.replace(/_/g, ' ')}
                        </span>
                      ))}
                      {symptoms.length > 4 && (
                        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>+{symptoms.length - 4}</span>
                      )}
                    </div>
                  </td>
                  <td style={{ fontWeight: 600 }}>{top?.disease || '—'}</td>
                  <td>
                    {top ? (
                      <span className="badge badge-purple">{top.probability}%</span>
                    ) : '—'}
                  </td>
                  <td>
                    <button
                      className="btn btn-danger btn-sm"
                      onClick={() => deleteReport(report.id)}
                      disabled={deleting === report.id}
                    >
                      {deleting === report.id ? '...' : '🗑 Delete'}
                    </button>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      )}
    </div>
  )
}
