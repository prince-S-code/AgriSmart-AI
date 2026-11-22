import { useEffect, useState, type FormEvent } from 'react'
import { authApi, cropHistory, dashboardStats, predictDisease, recommendCrop } from './api'
import './App.css'

// ─── Season × Region climate presets ────────────────────────────────────────
// temperature (°C), humidity (%), rainfall (mm/season)
type ClimatePreset = { temperature: number; humidity: number; rainfall: number }

const SEASON_DEFAULTS: Record<string, ClimatePreset> = {
  kharif:  { temperature: 30, humidity: 82, rainfall: 210 },  // Jun–Oct
  rabi:    { temperature: 16, humidity: 55, rainfall:  40 },  // Nov–Mar
  zaid:    { temperature: 36, humidity: 42, rainfall:  18 },  // Mar–Jun
  spring:  { temperature: 22, humidity: 60, rainfall:  65 },
  summer:  { temperature: 34, humidity: 50, rainfall:  28 },
  autumn:  { temperature: 20, humidity: 65, rainfall:  80 },
  winter:  { temperature: 12, humidity: 58, rainfall:  35 },
  monsoon: { temperature: 29, humidity: 88, rainfall: 280 },
}

// Region adjustments applied ON TOP of season defaults (deltas)
const REGION_ADJUSTMENTS: Record<string, Partial<ClimatePreset>> = {
  // Indian regions
  'punjab':          { temperature: -3, humidity: -8,  rainfall: -20 },
  'haryana':         { temperature: -2, humidity: -10, rainfall: -25 },
  'uttar pradesh':   { temperature:  0, humidity:  0,  rainfall:   0 },
  'madhya pradesh':  { temperature:  1, humidity:  2,  rainfall:  15 },
  'rajasthan':       { temperature:  5, humidity: -20, rainfall: -60 },
  'gujarat':         { temperature:  3, humidity: -5,  rainfall: -40 },
  'maharashtra':     { temperature:  2, humidity:  5,  rainfall:  30 },
  'karnataka':       { temperature:  0, humidity:  8,  rainfall:  50 },
  'kerala':          { temperature: -1, humidity: 20,  rainfall: 160 },
  'tamil nadu':      { temperature:  2, humidity: 12,  rainfall:  70 },
  'andhra pradesh':  { temperature:  2, humidity: 10,  rainfall:  60 },
  'telangana':       { temperature:  3, humidity:  8,  rainfall:  45 },
  'west bengal':     { temperature:  1, humidity: 15,  rainfall: 100 },
  'odisha':          { temperature:  2, humidity: 14,  rainfall:  90 },
  'assam':           { temperature: -1, humidity: 20,  rainfall: 180 },
  'bihar':           { temperature:  0, humidity:  5,  rainfall:  20 },
  'jharkhand':       { temperature:  0, humidity:  8,  rainfall:  40 },
  'chhattisgarh':    { temperature:  1, humidity:  6,  rainfall:  50 },
  'himachal pradesh':{ temperature:-10, humidity:  5,  rainfall:  10 },
  'uttarakhand':     { temperature: -8, humidity:  5,  rainfall:  20 },
  'north east india':{ temperature: -2, humidity: 18,  rainfall: 150 },
  // Generic zones
  'tropical':        { temperature:  5, humidity: 15,  rainfall: 100 },
  'subtropical':     { temperature:  2, humidity:  8,  rainfall:  40 },
  'arid':            { temperature:  6, humidity:-18,  rainfall: -70 },
  'semi-arid':       { temperature:  4, humidity: -8,  rainfall: -40 },
  'humid':           { temperature:  0, humidity: 15,  rainfall:  80 },
  'temperate':       { temperature: -5, humidity:  2,  rainfall:   5 },
  'hilly':           { temperature:-12, humidity:  8,  rainfall:  30 },
  'coastal':         { temperature:  1, humidity: 18,  rainfall:  60 },
  'plains':          { temperature:  1, humidity:  0,  rainfall:   0 },
}

function clamp(val: number, min: number, max: number) {
  return Math.min(max, Math.max(min, Math.round(val * 10) / 10))
}

function getClimatePreset(season: string, region: string): ClimatePreset {
  const base = SEASON_DEFAULTS[season] ?? SEASON_DEFAULTS.kharif
  const key  = region.trim().toLowerCase()
  const adj  = REGION_ADJUSTMENTS[key] ?? {}
  return {
    temperature: clamp((base.temperature) + (adj.temperature ?? 0), -10, 60),
    humidity:    clamp((base.humidity)    + (adj.humidity    ?? 0),   0, 100),
    rainfall:    clamp((base.rainfall)    + (adj.rainfall    ?? 0),   0, 500),
  }
}

const SEASONS = [
  { value: 'kharif',  label: 'Kharif (Jun–Oct)'  },
  { value: 'rabi',    label: 'Rabi (Nov–Mar)'     },
  { value: 'zaid',    label: 'Zaid (Mar–Jun)'     },
  { value: 'spring',  label: 'Spring'              },
  { value: 'summer',  label: 'Summer'              },
  { value: 'monsoon', label: 'Monsoon'             },
  { value: 'autumn',  label: 'Autumn'              },
  { value: 'winter',  label: 'Winter'              },
]

const cropFields = [
  ['nitrogen',    'Nitrogen (N)',      90  ],
  ['phosphorus',  'Phosphorus (P)',    42  ],
  ['potassium',   'Potassium (K)',     43  ],
  ['temperature', 'Temperature (°C)', 21  ],
  ['humidity',    'Humidity (%)',      82  ],
  ['ph',          'Soil pH',           6.5],
  ['rainfall',    'Rainfall (mm)',    203  ],
] as const

function greeting() {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning'
  if (h < 17) return 'Good afternoon'
  return 'Good evening'
}

function App() {
  const [token, setToken] = useState(localStorage.getItem('agrismart_token') || '')
  const [user, setUser] = useState<any>(null)
  const [view, setView] = useState<'dashboard' | 'crop' | 'disease' | 'history'>('dashboard')
  const [authView, setAuthView] = useState<'login' | 'register'>('login')
  const [authEmail, setAuthEmail] = useState('')
  const [authPassword, setAuthPassword] = useState('')
  const [values, setValues] = useState<Record<string, number>>(Object.fromEntries(cropFields.map(([key, , value]) => [key, value])))
  const [season, setSeason] = useState('kharif')
  const [location, setLocation] = useState('')
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

  // Pre-fill user's registered state as default location
  useEffect(() => {
    if (user?.state && !location) setLocation(user.state)
  }, [user])

  function applyClimate(newSeason: string, newLocation: string) {
    const preset = getClimatePreset(newSeason, newLocation)
    setValues(prev => ({ ...prev, ...preset }))
  }

  function handleSeasonChange(s: string) {
    setSeason(s)
    applyClimate(s, location)
  }

  function handleLocationChange(loc: string) {
    setLocation(loc)
  }

  function handleLocationBlur() {
    if (location.trim()) applyClimate(season, location)
  }

  function logout() {
    localStorage.removeItem('agrismart_token')
    setToken(''); setUser(null); setView('dashboard')
  }

  async function submitAuth(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setLoading(true); setMessage('')
    const form = new FormData(event.currentTarget)
    const payload = Object.fromEntries(form.entries()) as Record<string, string>
    if (authView === 'register') {
      if (payload.password !== payload.confirm_password) {
        setMessage('Passwords do not match')
        setLoading(false)
        return
      }
    }
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
        <div className="auth-brand-top"><div className="brand-mark">🌿</div><div><strong>AgriSmart</strong><span>AI</span></div></div>
        <div className="brand-copy"><p>INTELLIGENT FARMING</p><h1>Smarter decisions.<br/><em>Better harvests.</em></h1><small>Personal crop guidance and plant health insights for every field.</small></div>
        <div className="auth-proof"><div><strong>38</strong><span>Plant classes</span></div><div><strong>7</strong><span>Crop inputs</span></div><div><strong>24/7</strong><span>Access</span></div></div>
      </section>
      <section className="auth-panel">
        <button className="theme-toggle auth-theme" onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')} aria-label="Switch theme">{theme === 'light' ? '◐' : '☀'}</button>
          <div className="auth-card">
            <div className="auth-tabs">
              <button
                type="button"
                className={`auth-tab ${authView === 'login' ? 'active' : ''}`}
                onClick={() => { setAuthView('login'); setMessage('') }}
              >
                Sign In
              </button>
              <button
                type="button"
                className={`auth-tab ${authView === 'register' ? 'active' : ''}`}
                onClick={() => { setAuthView('register'); setMessage('') }}
              >
                Register
              </button>
            </div>
            <p className="eyebrow">FARMER ACCESS</p>
            <h2>{authView === 'login' ? 'Welcome back' : 'Create account'}</h2>
            <p className="muted">{authView === 'login' ? 'Continue to your farm workspace.' : 'Join AgriSmart with your name and email to start.'}</p>
            {import.meta.env.DEV && authView === 'login' && (
              <div className="demo-hint-box">
                <span className="demo-hint-text">Demo login:</span>
                <button
                  type="button"
                  className="demo-pill-btn"
                  onClick={() => {
                    setAuthEmail('farmer@example.com')
                    setAuthPassword('password123')
                    setMessage('')
                  }}
                >
                  ⚡ Use demo credentials
                </button>
              </div>
            )}
            <form onSubmit={submitAuth}>
              {authView === 'register' && (
                <label>
                  Full name
                  <input name="full_name" required placeholder="e.g. Rahul Sharma" />
                </label>
              )}
              <label>
                Email address
                <input
                  name="email"
                  type="email"
                  placeholder="you@example.com"
                  value={authEmail}
                  onChange={e => setAuthEmail(e.target.value)}
                  required
                />
              </label>
              <label>
                Password
                <input
                  name="password"
                  type="password"
                  placeholder="At least 6 characters"
                  minLength={6}
                  value={authPassword}
                  onChange={e => setAuthPassword(e.target.value)}
                  required
                />
              </label>
              {authView === 'register' && (
                <label>
                  Confirm password
                  <input
                    name="confirm_password"
                    type="password"
                    placeholder="Repeat password"
                    minLength={6}
                    required
                  />
                </label>
              )}
              {message && <p className="error">{message}</p>}
              <button className="primary" disabled={loading}>{loading ? 'Please wait…' : authView === 'login' ? 'Sign in' : 'Create account'}<span>→</span></button>
            </form>
            <button className="text-button" onClick={() => { setAuthView(authView === 'login' ? 'register' : 'login'); setMessage('') }}>{authView === 'login' ? 'New here? Create an account' : 'Already registered? Sign in'}</button>
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
        <header><div><p>FARMER DASHBOARD</p><h1>{view === 'dashboard' ? `${greeting()}, ${user.full_name.split(' ')[0]}` : nav.find(item => item[0] === view)?.[2]}</h1></div><div className="header-actions"><button className="theme-toggle" onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')} aria-label="Switch theme">{theme === 'light' ? '🌙' : '☀️'}</button><div className="weather"><b>☀️ 24°C</b><small>Clear conditions</small></div></div></header>

        {view === 'dashboard' && <>
          <section className="welcome-banner"><div><p>TODAY'S FARM INSIGHT</p><h2>Plan confidently for the next season.</h2><button onClick={() => setView('crop')}>Open crop advisor →</button></div><div className="field-art">🌱</div></section>
          <section className="stats-grid"><article><div className="stat-icon green">🌱</div><div><small>Crop recommendations</small><strong>{stats?.crop_recommendations ?? 0}</strong></div></article><article><div className="stat-icon amber">◎</div><div><small>Disease scans</small><strong>{stats?.disease_scans ?? 0}</strong></div></article><article><div className="stat-icon blue">☀</div><div><small>Weather status</small><strong>Good</strong></div></article></section>
          <section className="quick-grid"><button onClick={() => setView('crop')}><b>🌱</b><span><b>Recommend a crop</b><small>Use soil and climate data</small></span><i>→</i></button><button onClick={() => setView('disease')}><b>◎</b><span><b>Scan a plant</b><small>Upload a clear leaf image</small></span><i>→</i></button></section>
        </>}

        {view === 'crop' && <section className="tool-layout">
          <article className="panel">
            <div className="panel-heading"><div><p>SOIL &amp; CLIMATE</p><h2>Crop recommendation</h2></div><b>🌱</b></div>

            {/* ── Context strip: season + location ── */}
            <div className="context-strip">
              <label className="context-label">
                <span>🗓 Season</span>
                <select value={season} onChange={e => handleSeasonChange(e.target.value)}>
                  {SEASONS.map(s => <option key={s.value} value={s.value}>{s.label}</option>)}
                </select>
              </label>
              <label className="context-label">
                <span>📍 Location / Region</span>
                <input
                  type="text"
                  placeholder="e.g. Punjab, Kerala, Coastal…"
                  value={location}
                  onChange={e => handleLocationChange(e.target.value)}
                  onBlur={handleLocationBlur}
                />
              </label>
              <button type="button" className="autofill-btn" onClick={() => applyClimate(season, location)} title="Auto-fill climate from season &amp; location">
                ⟳ Auto-fill climate
              </button>
            </div>

            <form onSubmit={submitCrop}>
              <div className="form-grid">
                {cropFields.map(([key, label, defaultValue]) => (
                  <label key={key} className={['temperature','humidity','rainfall'].includes(key) ? 'field-climate' : ''}>
                    {label}
                    <input type="number" step="0.1" value={values[key] ?? defaultValue}
                      onChange={event => setValues({...values, [key]: Number(event.target.value)})} required />
                  </label>
                ))}
              </div>
              {message && <p className="error">{message}</p>}
              <button className="primary" disabled={loading}>{loading ? 'Analyzing…' : 'Generate recommendation'}</button>
            </form>
          </article>

          {cropResult && <article className="panel result-panel">
            <p>BEST MATCH</p>
            <h2>{cropResult.recommended_crop}</h2>
            <div className="match-ring" style={{'--score': `${Math.round(cropResult.alternatives[0].score * 100)}%`} as React.CSSProperties}>
              <b>{Math.round(cropResult.alternatives[0].score * 100)}%</b><small>match</small>
            </div>
            {(season || location) && (
              <div className="result-context">
                {season && <span>🗓 {SEASONS.find(s => s.value === season)?.label}</span>}
                {location && <span>📍 {location}</span>}
              </div>
            )}
            <h3>Alternatives</h3>
            {cropResult.alternatives.slice(1).map((item: any) => (
              <div className="alternative" key={item.crop}><span>{item.crop}</span><b>{Math.round(item.score * 100)}%</b></div>
            ))}
          </article>}
        </section>}

        {view === 'disease' && <section className="disease-layout">
          <article className="panel disease-panel">
            <div className="panel-heading"><div><p>PLANT HEALTH</p><h2>Disease detection</h2></div><b>◎</b></div>
            <label className="drop-zone"><b>◎</b><b>{loading ? 'Analyzing leaf with both models…' : 'Upload a leaf photo'}</b><span>JPG or PNG, maximum 5 MB</span><input type="file" accept="image/jpeg,image/png" onChange={event => void submitDisease(event.target.files?.[0])}/></label>
            {message && <p className="error">{message}</p>}
          </article>
          {diseaseResult && <article className="panel disease-result">
            <p>MODEL COMPARISON</p>
            <h2>{diseaseResult.crop_name}</h2>
            <p className="model-metric-note">Confidence is per-image certainty; test accuracy is measured on a separate labeled dataset.</p>
            <div className="model-results">
              {diseaseResult.model_results.map((model: any) => <section className="model-result" key={model.model}>
                <h3>{model.model}</h3>
                <p className="model-prediction">{model.predicted_disease.replaceAll('_', ' ')}</p>
                <div className="confidence-row"><span>Prediction confidence</span><strong>{Math.round(model.confidence * 100)}%</strong></div>
                <div className="confidence-track"><span style={{width: `${Math.round(model.confidence * 100)}%`}} /></div>
                <p className="model-accuracy"><span>Held-out test accuracy</span><strong>{model.test_accuracy == null ? 'Not reported' : `${(model.test_accuracy * 100).toFixed(2)}%`}</strong></p>
                {model.detections.length > 0 && <ul className="model-detections">{model.detections.map((detection: any, index: number) => <li key={`${detection.class_name}-${index}`}><span>{detection.class_name.replaceAll('_', ' ')}</span><b>{Math.round(detection.confidence * 100)}%</b></li>)}</ul>}
              </section>)}
            </div>
            {diseaseResult.severity && <p className={`severity-badge severity-${diseaseResult.severity}`}>{diseaseResult.severity === 'low' ? '✔ Low severity' : diseaseResult.severity === 'medium' ? '⚠ Medium severity' : '✕ High severity'}</p>}
            {diseaseResult.description && <p className="disease-desc">{diseaseResult.description}</p>}
            {diseaseResult.low_confidence && <p className="review-warning">Low confidence: retake the image in clear light or consult an agricultural expert.</p>}
            {diseaseResult.treatment_steps?.length > 0 && <div className="treatment-steps"><p>TREATMENT STEPS</p><ol>{diseaseResult.treatment_steps.map((step: string, i: number) => <li key={i}>{step}</li>)}</ol></div>}
          </article>}
        </section>}

        {view === 'history' && <section className="panel"><div className="panel-heading"><div><p>RECENT ACTIVITY</p><h2>Crop history</h2></div><b>◷</b></div>{history.length ? <div className="history-list">{history.map(row => <article key={row.id}><div><b>{row.recommended_crop}</b><small>{row.created_at}</small></div><div className="history-values"><span>N {row.nitrogen}</span><span>P {row.phosphorus}</span><span>K {row.potassium}</span></div></article>)}</div> : <div className="empty"><b>◷</b><h3>No recommendations yet</h3><p>Use the crop advisor to create your first result.</p></div>}</section>}
      </section>
    </main>
  )
}

export default App
