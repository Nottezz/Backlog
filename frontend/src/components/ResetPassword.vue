<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-50 to-blue-50 flex items-center justify-center px-4">
    <div class="max-w-md w-full">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-indigo-600 mb-2">🎬 Backlog Movies</h1>
        <p class="text-gray-600">Set a new password</p>
      </div>

      <!-- Card -->
      <div class="bg-white shadow-2xl rounded-2xl p-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-6">Reset Password</h2>

        <form @submit.prevent="handleSubmit" class="space-y-5">
          <!-- New Password -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              New Password
            </label>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              placeholder="••••••••"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
              :class="{ 'border-red-500': error }"
              :disabled="loading"
            />
          </div>

          <!-- Confirm Password -->
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-2">
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              v-model="confirmPassword"
              type="password"
              required
              placeholder="••••••••"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
              :class="{ 'border-red-500': error }"
              :disabled="loading"
            />
          </div>

          <!-- Error -->
          <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-3">
            <p class="text-red-700 text-sm">{{ error }}</p>
          </div>

          <!-- Success -->
          <div v-if="success" class="bg-green-50 border border-green-200 rounded-lg p-3">
            <p class="text-green-700 text-sm">
              Password successfully reset. Redirecting to login...
            </p>
          </div>

          <!-- Submit -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-indigo-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {{ loading ? 'Resetting...' : 'Reset password' }}
          </button>
        </form>

        <!-- Back to login -->
        <div class="mt-6 text-center">
          <router-link
            to="/login"
            class="text-indigo-600 hover:text-indigo-700 text-sm font-medium"
          >
            ← Back to login
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import authService from '../services/auth'

export default {
  name: 'ResetPasswordView',
  data() {
    return {
      token: this.$route.query.token || '',
      password: '',
      confirmPassword: '',
      loading: false,
      error: null,
      success: false,
    }
  },
  methods: {
    async handleSubmit() {
      this.error = null

      if (!this.token) {
        this.error = 'Invalid or missing token.'
        return
      }

      if (this.password !== this.confirmPassword) {
        this.error = 'Passwords do not match.'
        return
      }

      this.loading = true

      try {
        await authService.resetPassword(this.token, this.password)
        this.success = true

        setTimeout(() => {
          this.$router.push('/login')
        }, 1500)
      } catch (error) {
        this.error =
          error.response?.data?.detail || 'Reset failed. The token may be invalid.'
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
