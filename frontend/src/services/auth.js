import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/api'

class AuthService {
  constructor() {
    this.token = localStorage.getItem('token')
    this.user = JSON.parse(localStorage.getItem('user') || 'null')
  }

  // Регистрация
  async register(email, password) {
    const response = await axios.post(`${API_URL}/auth/register`, {
      email,
      password,
    })
    return response.data
  }

  // Вход
  async login(email, password) {
    const formData = new URLSearchParams()
    formData.append('username', email)
    formData.append('password', password)

    const response = await axios.post(`${API_URL}/auth/login`, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })

    const { access_token } = response.data
    this.token = access_token
    localStorage.setItem('token', access_token)

    await this.fetchUser()

    return response.data
  }

  async fetchUser() {
    if (!this.token) return null

    try {
      const response = await axios.get(`${API_URL}/users/me`, {
        headers: {
          Authorization: `Bearer ${this.token}`,
        },
      })
      this.user = response.data
      localStorage.setItem('user', JSON.stringify(response.data))
      return response.data
    } catch (error) {
      this.logout()
      throw error
    }
  }

  // Выход
  async logout() {
    try {
      if (this.token) {
        await axios.post(`${API_URL}/auth/logout`, null, {
          headers: {
            Authorization: `Bearer ${this.token}`,
          },
        })
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }

  // Проверка авторизации
  isAuthenticated() {
    return !!this.token
  }

  // Получить пользователя
  getUser() {
    return this.user
  }

  // Настроить axios interceptor для автоматической авторизации
  setupAxiosInterceptor() {
    axios.interceptors.request.use(
      config => {
        if (this.token) {
          config.headers.Authorization = `Bearer ${this.token}`
        }
        return config
      },
      error => Promise.reject(error)
    )

    axios.interceptors.response.use(
      response => response,
      error => {
        if (error.response?.status === 401) {
          this.logout()
          window.location.href = '/login'
        }
        return Promise.reject(error)
      }
    )
  }
}

export default new AuthService()
