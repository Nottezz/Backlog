<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-50 to-blue-50 flex items-center justify-center px-4">
    <div class="max-w-md w-full text-center">
      <h1 class="text-4xl font-bold text-indigo-600 mb-2">🎬 Backlog Movies</h1>
      <p class="text-gray-600 mb-6">Check your email to verify your account</p>

      <div class="bg-white shadow-2xl rounded-2xl p-8">
        <p class="text-gray-700 mb-4">
          We have sent a verification link to <strong>{{ email }}</strong>.
        </p>
        <p class="text-gray-500 text-sm mb-6">
          Click the link in the email to activate your account.
        </p>

        <button
          @click="resend"
          :disabled="loading"
          class="w-full bg-indigo-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {{ loading ? 'Resending...' : 'Resend verification email' }}
        </button>

        <router-link
          to="/login"
          class="block mt-4 text-indigo-600 hover:text-indigo-700 font-medium text-sm"
        >
          Back to login
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import authService from '../services/auth'

export default {
  name: 'CheckEmailView',
  data() {
    return {
      email: this.$route.query.email || '',
      loading: false,
      error: null,
    }
  },
  methods: {
    async resend() {
      if (!this.email) return
      this.loading = true
      this.error = null
      try {
        await authService.requestVerifyToken(this.email)
      } catch (err) {
        this.error =
          err.response?.data?.detail || 'Failed to resend verification email.'
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
