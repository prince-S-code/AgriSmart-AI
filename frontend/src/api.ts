const API_URL = import.meta.env.VITE_API_URL ?? ''

function headers(token?: string) {
  const result: Record<string, string> = { 'Content-Type': 'application/json' }
  if (token) result.Authorization = `Bearer ${token}`
  return result
}

async function request(path: string, options: RequestInit = {}) {
  const response = await fetch(`${API_URL}${path}`, options)
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    let msg = 'Request failed'
    if (typeof data.detail === 'string') {
      msg = data.detail
    } else if (Array.isArray(data.detail) && data.detail.length > 0) {
      msg = data.detail.map((e: any) => e.msg || e.message || JSON.stringify(e)).join(', ')
    }
    throw new Error(msg)
  }
  return data
}

export const authApi = {
  register: (payload: Record<string, string>) => request('/api/auth/register', { method: 'POST', headers: headers(), body: JSON.stringify(payload) }),
  login: (payload: Record<string, string>) => request('/api/auth/login', { method: 'POST', headers: headers(), body: JSON.stringify(payload) }),
  me: (token: string) => request('/api/auth/me', { headers: headers(token) }),
}

export function recommendCrop(values: Record<string, number>, token: string) {
  return request('/api/crop/recommend', { method: 'POST', headers: headers(token), body: JSON.stringify(values) })
}

export function cropHistory(token: string) {
  return request('/api/crop/history', { headers: headers(token) })
}

export function dashboardStats(token: string) {
  return request('/api/dashboard/stats', { headers: headers(token) })
}

export async function predictDisease(file: File, token: string) {
  const form = new FormData()
  form.append('image', file)
  const response = await fetch(`${API_URL}/api/disease/predict`, { method: 'POST', headers: { Authorization: `Bearer ${token}` }, body: form })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    let msg = 'Prediction failed'
    if (typeof data.detail === 'string') {
      msg = data.detail
    } else if (Array.isArray(data.detail) && data.detail.length > 0) {
      msg = data.detail.map((e: any) => e.msg || e.message || JSON.stringify(e)).join(', ')
    }
    throw new Error(msg)
  }
  return data
}
