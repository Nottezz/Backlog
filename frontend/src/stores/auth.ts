import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, type UserRead } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<UserRead | null>(null)
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const loading = ref(false)

  const isAuthenticated = computed(() => !!token.value && !!user.value)

  function setToken(newToken: string) {
    token.value = newToken
    localStorage.setItem('access_token', newToken)
  }

  function clearAuth() {
    user.value = null
    token.value = null
    localStorage.removeItem('access_token')
  }

  async function login(email: string, password: string) {
    loading.value = true
    try {
      const response = await authApi.login(email, password)
      setToken(response.access_token)
      await fetchCurrentUser()
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      await authApi.logout()
    } catch {
      // Ignore errors on logout
    } finally {
      clearAuth()
    }
  }

  async function fetchCurrentUser() {
    try {
      user.value = await authApi.getCurrentUser()
    } catch {
      clearAuth()
    }
  }

  return {
    user,
    token,
    loading,
    isAuthenticated,
    login,
    logout,
    fetchCurrentUser,
    clearAuth,
  }
})
