import api from './axios'
import axios from 'axios'

export interface UserRead {
  id: string
  email: string
  username: string
}

export interface BearerResponse {
  access_token: string
  token_type: string
}

export const authApi = {
  async login(email: string, password: string): Promise<BearerResponse> {
    // Login requires form-urlencoded
    const params = new URLSearchParams()
    params.append('username', email)
    params.append('password', password)

    const { data } = await axios.post<BearerResponse>('/api/auth/login', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
    return data
  },

  async logout(): Promise<void> {
    await api.post('/auth/logout')
  },

  async register(email: string, password: string): Promise<UserRead> {
    const { data } = await api.post<UserRead>('/auth/register', { email, password })
    return data
  },

  async requestVerifyToken(email: string): Promise<void> {
    await api.post('/auth/request-verify-token', { email })
  },

  async verify(token: string): Promise<UserRead> {
    const { data } = await api.post<UserRead>('/auth/verify', { token })
    return data
  },

  async forgotPassword(email: string): Promise<void> {
    await api.post('/auth/forgot-password', { email })
  },

  async resetPassword(token: string, password: string): Promise<void> {
    await api.post('/auth/reset-password', { token, password })
  },

  async getCurrentUser(): Promise<UserRead> {
    const { data } = await api.get<UserRead>('/users/me')
    return data
  },
}
