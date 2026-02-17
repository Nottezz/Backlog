<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-50 to-blue-50 flex items-center justify-center px-4">
    <div class="max-w-md w-full">
      <!-- Logo/Header -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-indigo-600 mb-2">🎬 Backlog Movies</h1>
        <p class="text-gray-600">Create your account</p>
      </div>

      <!-- Register Form -->
      <div class="bg-white shadow-2xl rounded-2xl p-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-6">Sign Up</h2>

        <form @submit.prevent="handleRegister" class="space-y-5">
          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Email
            </label>
            <input
                id="email"
                v-model="email"
                type="email"
                required
                placeholder="your@email.com"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
                :class="{ 'border-red-500': errors.email }"
                :disabled="loading"
                @input="errors.email = ''"
            />
            <p v-if="errors.email" class="text-red-500 text-sm mt-1">{{ errors.email }}</p>
          </div>

          <!-- Password -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <input
                id="password"
                v-model="password"
                type="password"
                required
                placeholder="••••••••"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
                :class="{ 'border-red-500': errors.password }"
                :disabled="loading"
                @input="errors.password = ''"
            />
            <p v-if="errors.password" class="text-red-500 text-sm mt-1">{{ errors.password }}</p>
            <p class="text-gray-500 text-xs mt-1">Minimum 8 characters</p>
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
                :class="{ 'border-red-500': errors.confirmPassword }"
                :disabled="loading"
                @input="errors.confirmPassword = ''"
            />
            <p v-if="errors.confirmPassword" class="text-red-500 text-sm mt-1">
              {{ errors.confirmPassword }}
            </p>
          </div>

          <!-- Success Message -->
          <div v-if="success" class="bg-green-50 border border-green-200 rounded-lg p-3">
            <p class="text-green-700 text-sm">
              ✓ Account created successfully! Redirecting to login...
            </p>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-3">
            <p class="text-red-700 text-sm">{{ error }}</p>
          </div>

          <!-- Submit Button -->
          <button
              type="submit"
              :disabled="loading"
              class="w-full bg-indigo-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {{ loading ? 'Creating account...' : 'Sign Up' }}
          </button>
        </form>

        <!-- Login Link -->
        <div class="mt-6 text-center">
          <p class="text-gray-600 text-sm">
            Already have an account?
            <router-link to="/login" class="text-indigo-600 hover:text-indigo-700 font-medium">
              Sign in
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import authService from '../services/auth'

export default {
  name: 'RegisterView',
  data() {
    return {
      email: '',
      password: '',
      confirmPassword: '',
      loading: false,
      success: false,
      error: null,
      errors: {
        email: '',
        password: '',
        confirmPassword: '',
      },
    }
  },
  methods: {
    validateForm() {
      this.errors = {
        email: '',
        password: '',
        confirmPassword: '',
      }

      let isValid = true

      // Email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(this.email)) {
        this.errors.email = 'Please enter a valid email'
        isValid = false
      }

      // Password validation
      if (this.password.length < 8) {
        this.errors.password = 'Password must be at least 8 characters'
        isValid = false
      }

      // Confirm password validation
      if (this.password !== this.confirmPassword) {
        this.errors.confirmPassword = 'Passwords do not match'
        isValid = false
      }

      return isValid
    },

    async handleRegister() {
      if (!this.validateForm()) return

      this.loading = true
      this.error = null
      this.success = false

      try {
        await authService.register(this.email, this.password)
        this.success = true

        this.$router.push({
          path: '/check-email',
          query: { email: this.email }
        })

      } catch (error) {
        console.error('Registration error:', error)
        this.error =
          error.response?.data?.detail ||
          'Registration failed. Please try again.'
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
