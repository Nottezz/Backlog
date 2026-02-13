<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-50 to-blue-50 flex items-center justify-center px-4">
    <div class="max-w-md w-full">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-indigo-600 mb-2">🎬 Backlog Movies</h1>
        <p class="text-gray-600">Email verification</p>
      </div>

      <!-- Card -->
      <div class="bg-white shadow-2xl rounded-2xl p-8 text-center">

        <!-- Loading -->
        <div v-if="status === 'loading'" class="space-y-4">
          <div class="text-5xl">⏳</div>
          <h2 class="text-2xl font-bold text-gray-800">
            Verifying your email...
          </h2>
          <p class="text-gray-600 text-sm">
            Please wait while we confirm your email address.
          </p>
        </div>

        <!-- Success -->
        <div v-else-if="status === 'success'" class="space-y-4">
          <div class="text-5xl">✅</div>
          <h2 class="text-2xl font-bold text-gray-800">
            Email verified!
          </h2>
          <p class="text-gray-600 text-sm">
            Your account has been successfully confirmed.
          </p>

          <router-link
            to="/login"
            class="inline-block mt-4 bg-indigo-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors"
          >
            Go to Login
          </router-link>
        </div>

        <!-- Error -->
        <div v-else class="space-y-4">
          <div class="text-5xl">❌</div>
          <h2 class="text-2xl font-bold text-gray-800">
            Verification failed
          </h2>
          <p class="text-red-600 text-sm">
            {{ error }}
          </p>

          <button
            @click="requestNewToken"
            :disabled="resending"
            class="mt-4 w-full bg-indigo-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {{ resending ? 'Sending...' : 'Request new verification link' }}
          </button>

          <router-link
            to="/login"
            class="block mt-3 text-indigo-600 hover:text-indigo-700 font-medium text-sm"
          >
            Back to Login
          </router-link>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import authService from '../services/auth'

export default {
  name: 'VerifyEmailView',

  data() {
    return {
      status: 'loading', // loading | success | error
      error: null,
      resending: false,
      token: null,
    }
  },

  async mounted() {
    this.token = this.$route.query.token

    if (!this.token) {
      this.status = 'error'
      this.error = 'Verification token is missing.'
      return
    }

    try {
      // ✅ Используем authService вместо прямого axios
      await authService.verifyEmail(this.token)

      this.status = 'success'

      // убрать токен из URL после использования
      this.$router.replace({ path: '/verify' })

    } catch (error) {
      console.error('Verification error:', error)
      this.status = 'error'
      this.error =
        error.response?.data?.detail ||
        'Invalid or expired verification token.'
    }
  },

  methods: {
    async requestNewToken() {
      try {
        this.resending = true

        // используем authService для повторной отправки токена
        await authService.requestVerifyToken(this.email) // или email, если есть

        this.error = 'A new verification link has been sent to your email.'
      } catch (error) {
        this.error =
          error.response?.data?.detail ||
          'Failed to send verification email.'
      } finally {
        this.resending = false
      }
    },
  },
}
</script>
