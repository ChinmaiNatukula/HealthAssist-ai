import { createContext, useContext, useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Dashboard from './pages/Dashboard'

// ─── Auth Context ─────────────────────────────────────────────────────────────
export const AuthContext = createContext(null)
export function useAuth() { return useContext(AuthContext) }

// ─── Theme Context ────────────────────────────────────────────────────────────
export const ThemeContext = createContext(null)
export function useTheme() { return useContext(ThemeContext) }

function App() {
  const [user, setUser] = useState(() => {
    try { return JSON.parse(localStorage.getItem('ha_user')) } catch { return null }
  })
  const [token, setToken] = useState(() => localStorage.getItem('ha_token') || null)
  const [theme, setTheme] = useState(() => localStorage.getItem('ha_theme') || 'dark')

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('ha_theme', theme)
  }, [theme])

  const login = (userData, tokenStr) => {
    setUser(userData)
    setToken(tokenStr)
    localStorage.setItem('ha_user', JSON.stringify(userData))
    localStorage.setItem('ha_token', tokenStr)
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    localStorage.removeItem('ha_user')
    localStorage.removeItem('ha_token')
  }

  const toggleTheme = () => setTheme(t => t === 'dark' ? 'light' : 'dark')

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      <AuthContext.Provider value={{ user, token, login, logout }}>
        <div className="app-bg">
          <BrowserRouter>
            <Routes>
              <Route path="/login" element={!user ? <Login /> : <Navigate to="/" />} />
              <Route path="/signup" element={!user ? <Signup /> : <Navigate to="/" />} />
              <Route path="/*" element={user ? <Dashboard /> : <Navigate to="/login" />} />
            </Routes>
          </BrowserRouter>
        </div>
      </AuthContext.Provider>
    </ThemeContext.Provider>
  )
}

export default App
