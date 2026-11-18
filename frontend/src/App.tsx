import { useEffect, useState, type FormEvent } from 'react'
import { authApi, cropHistory, dashboardStats, predictDisease, recommendCrop } from './api'
import './App.css'

const cropFields = [
  ['nitrogen', 'Nitrogen (N)', 90], ['phosphorus', 'Phosphorus (P)', 42],
  ['potassium', 'Potassium (K)', 43], ['temperature', 'Temperature (°C)', 21],
  ['humidity', 'Humidity (%)', 82], ['ph', 'Soil pH', 6.5], ['rainfall', 'Rainfall (mm)', 203],
] as const

function App() {
  const [token, setToken] = useState(localStorage.getItem('agrismart_token') || '')
  const [user, setUser] = useState<any>(null)
  const [view, setView] = useState<'dashboard' | 'crop' | 'disease' | 'history'>('dashboard')
  const [authView, setAuthView] = useState<'login' | 'register'>('login')
  const [values, setValues] = useState<Record<string, number>>(Object.fromEntries(cropFields.map(([key, , value]) => [key, value])))
  const [cropResult, setCropResult] = useState<any>(null)
  const [diseaseResult, setDiseaseResult] = useState<any>(null)
  const [stats, setStats] = useState<any>(null)
  const [history, setHistory] = useState<any[]>([])
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    return (localStorage.getItem('agrismart_theme') as 'light' | 'dark') || 'light'
  })

  useEffect(() => {
    if (!token) return
    authApi.me(token).then(setUser).catch(() => logout())
  }, [token])

  useEffect(() => {
    if (!token || !user) return
    dashboardStats(token).then(setStats).catch(() => setStats(null))
    if (view === 'history') cropHistory(token).then(setHistory).catch(() => setHistory([]))
  }, [token, user, view])

  useEffect(() => {
    document.documentElement.dataset.theme = theme
    localStorage.setItem('agrismart_theme', theme)
  }, [theme])

  function logout() {
    localStorage.removeItem('agrismart_token')
    setToken(''); setUser(null); setView('dashboard')
  }

  async function submitAuth(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setLoading(true); setMessage('')
    const form = new FormData(event.currentTarget)
    const payload = Object.fromEntries(form.entries()) as Record<string, string>
    try {
      const data = authView === 'login'
        ? await authApi.login({ email: payload.email, password: payload.password })
        : await authApi.register(payload)
      localStorage.setItem('agrismart_token', data.access_token)
      setToken(data.access_token); setUser(data.user)
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Authentication failed')
    } finally { setLoading(false) }
  }

  async function submitCrop(event: FormEvent) {
    event.preventDefault(); setLoading(true); setMessage('')
    try { setCropResult(await recommendCrop(values, token)) }
    catch (error) { setMessage(error instanceof Error ? error.message : 'Recommendation failed') }
    finally { setLoading(false) }
  }

  async function submitDisease(file?: File) {
    if (!file) return
    setLoading(true); setMessage(''); setDiseaseResult(null)
    try {
      setDiseaseResult(await predictDisease(file, token))
    }
    catch (error) { setMessage(error instanceof Error ? error.message : 'Disease detection failed') }
    finally { setLoading(false) }
  }

  if (!token || !user) return (
    <main className="auth-page">
      <section className="auth-brand">
        <div className="brand-mark">🌿</div>
        <div><strong>AgriSmart</strong><span>AI</span></div>
        <div className="brand-copy"><p>AGRICULTURAL INTELLIGENCE</p><h1>Grow smarter.<br/>Farm with confidence.</h1><small>Crop insights and plant health guidance, built for every season.</small></div>
      </section>
      <section className="auth-panel">
        <button className="theme-toggle auth-theme" onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')} aria-label="Switch theme">{theme === 'light' ? '🌙 Dark' : '☀️ Light'}</button>
        <div className="auth-card">
          <p className="eyebrow">FARMER PORTAL</p><h2>{authView === 'login' ? 'Welcome back' : 'Create your account'}</h2>
          <p className="muted">{authView === 'login' ? 'Sign in to manage your farm insights.' : 'Start using smarter agricultural guidance.'}</p>
          <form onSubmit={submitAuth}>
            {authView === 'register' && <><label>Full name<input name="full_name" required /></label><label>Mobile number<input name="mobile_number" minLength={8} required /></label><div className="location-row"><label>State<input name="state" /></label><label>District<input name="district" /></label></div></>}
            <label>Email address<input name="email" type="email" required /></label>
            <label>Password<input name="password" type="password" minLength={8} required /></label>
            {authView === 'register' && <><label>Village<input name="village" /></label><label>Confirm password<input name="confirm_password" type="password" required /></label></>}
            {message && <p className="error">{message}</p>}
            <button className="primary" disabled={loading}>{loading ? 'Please wait…' : authView === 'login' ? 'Sign in' : 'Create account'}</button>
          </form>
          <button className="text-button" onClick={() => { setAuthView(authView === 'login' ? 'register' : 'login'); setMessage('') }}>{authView === 'login' ? 'New farmer? Create an account' : 'Already registered? Sign in'}</button>
        </div>
      </section>
    </main>
  )

  const nav = [
    ['dashboard', '▦', 'Overview'], ['crop', '🌱', 'Crop advisor'],
    ['disease', '◎', 'Disease scan'], ['history', '◷', 'History'],
  ] as const

  return (
    <main className="app-shell">
      <aside>
        <div className="side-brand"><div className="brand-mark">🌿</div><strong>AgriSmart <span>AI</span></strong></div>
        <nav>{nav.map(([key, icon, label]) => <button key={key} className={view === key ? 'active' : ''} onClick={() => setView(key)}><b>{icon}</b><span>{label}</span></button>)}</nav>
        <div className="farmer-card"><div className="avatar">👤</div><div><b>{user.full_name}</b><small>Farmer account</small></div><button onClick={logout} aria-label="Sign out">↪</button></div>
      </aside>

      <section className="workspace">
        <header><div><p>FARMER DASHBOARD</p><h1>{view === 'dashboard' ? `Good morning, ${user.full_name.split(' ')[0]}` : nav.find(item => item[0] === view)?.[2]}</h1></div><div className="header-actions"><button className="theme-toggle" onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')} aria-label="Switch theme">{theme === 'light' ? '🌙' : '☀️'}</button><div className="weather"><b>☀️ 24°C</b><small>Clear conditions</small></div></div></header>

        {view === 'dashboard' && <>
          <section className="welcome-banner"><div><p>TODAY'S FARM INSIGHT</p><h2>Plan confidently for the next season.</h2><button onClick={() => setView('crop')}>Open crop advisor →</button></div><div className="field-art">🌱</div></section>
          <section className="stats-grid"><article><div className="stat-icon green">🌱</div><div><small>Crop recommendations</small><strong>{stats?.crop_recommendations ?? 0}</strong></div></article><article><div className="stat-icon amber">◎</div><div><small>Disease scans</small><strong>{stats?.disease_scans ?? 0}</strong></div></article><article><div className="stat-icon blue">☀</div><div><small>Weather status</small><strong>Good</strong></div></article></section>
          <section className="quick-grid"><button onClick={() => setView('crop')}><b>🌱</b><span><b>Recommend a crop</b><small>Use soil and climate data</small></span><i>→</i></button><button onClick={() => setView('disease')}><b>◎</b><span><b>Scan a plant</b><small>Upload a clear leaf image</small></span><i>→</i></button></section>
        </>}

        {view === 'crop' && <section className="tool-layout"><article className="panel"><div className="panel-heading"><div><p>SOIL & CLIMATE</p><h2>Crop recommendation</h2></div><b>🌱</b></div><form onSubmit={submitCrop}><div className="form-grid">{cropFields.map(([key, label, defaultValue]) => <label key={key}>{label}<input type="number" step="0.1" value={values[key] ?? defaultValue} onChange={event => setValues({...values, [key]: Number(event.target.value)})} required /></label>)}</div>{message && <p className="error">{message}</p>}<button className="primary" disabled={loading}>{loading ? 'Analyzing…' : 'Generate recommendation'}</button></form></article>{cropResult && <article className="panel result-panel"><p>BEST MATCH</p><h2>{cropResult.recommended_crop}</h2><div className="match-ring" style={{'--score': `${Math.round(cropResult.alternatives[0].score * 100)}%`} as React.CSSProperties}><b>{Math.round(cropResult.alternatives[0].score * 100)}%</b><small>match</small></div><h3>Alternatives</h3>{cropResult.alternatives.slice(1).map((item: any) => <div className="alternative" key={item.crop}><span>{item.crop}</span><b>{Math.round(item.score * 100)}%</b></div>)}</article>}</section>}

        {view === 'disease' && <section className="disease-layout"><article className="panel disease-panel"><div className="panel-heading"><div><p>PLANT HEALTH</p><h2>Disease detection</h2></div><b>◎</b></div><label className="drop-zone"><b>◎</b><b>{loading ? 'Analyzing leaf…' : 'Upload a leaf photo'}</b><span>JPG or PNG, maximum 5 MB</span><input type="file" accept="image/jpeg,image/png" onChange={event => void submitDisease(event.target.files?.[0])}/></label>{message && <p className="error">{message}</p>}</article>{diseaseResult && <article className="panel disease-result"><p>MODEL RESULT</p><h2>{diseaseResult.predicted_disease.replaceAll('_', ' ')}</h2><div className="confidence-row"><span>Confidence</span><strong>{Math.round(diseaseResult.confidence * 100)}%</strong></div><div className="confidence-track"><span style={{width: `${Math.round(diseaseResult.confidence * 100)}%`}} /></div><p className="crop-result"><span>Crop</span><b>{diseaseResult.crop_name}</b></p>{diseaseResult.low_confidence && <p className="review-warning">Low confidence: retake the image in clear light or consult an agricultural expert.</p>}</article>}</section>}

        {view === 'history' && <section className="panel"><div className="panel-heading"><div><p>RECENT ACTIVITY</p><h2>Crop history</h2></div><b>◷</b></div>{history.length ? <div className="history-list">{history.map(row => <article key={row.id}><div><b>{row.recommended_crop}</b><small>{row.created_at}</small></div><div className="history-values"><span>N {row.nitrogen}</span><span>P {row.phosphorus}</span><span>K {row.potassium}</span></div></article>)}</div> : <div className="empty"><b>◷</b><h3>No recommendations yet</h3><p>Use the crop advisor to create your first result.</p></div>}</section>}
      </section>
    </main>
  )
}

export default App
