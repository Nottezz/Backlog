<template>
  <AuthLayout>
    <div>
      <h1 class="font-display text-2xl font-bold text-base-900 mb-1">Добро пожаловать</h1>
      <p class="font-body text-base-400 text-sm mb-8">Войдите, чтобы продолжить</p>

      <AlertMessage
        :show="!!errorMessage"
        variant="error"
        :message="errorMessage"
        dismissible
        class="mb-6"
        @dismiss="errorMessage = ''"
      />

      <!-- Unverified email warning -->
      <AlertMessage
        :show="showVerifyAlert"
        variant="info"
        class="mb-6"
        dismissible
        @dismiss="showVerifyAlert = false"
      >
        Ваш email не подтверждён.
        <button
          class="underline hover:no-underline ml-1 font-medium"
          @click="resendVerification"
        >
          Отправить письмо повторно
        </button>
      </AlertMessage>

      <form @submit.prevent="handleLogin" class="flex flex-col gap-5">
        <BaseInput
          v-model="form.email"
          label="Email"
          type="email"
          placeholder="you@example.com"
          required
          :error="fieldErrors.email"
        />
        <BaseInput
          v-model="form.password"
          label="Пароль"
          type="password"
          placeholder="••••••••"
          required
          :error="fieldErrors.password"
        />

        <div class="flex items-center justify-end">
          <RouterLink
            to="/forgot-password"
            class="font-body text-sm text-base-400 hover:text-base-700 transition-colors"
          >
            Забыли пароль?
          </RouterLink>
        </div>

        <button
          type="submit"
          class="btn-primary w-full"
          :disabled="loading"
        >
          <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          {{ loading ? 'Входим…' : 'Войти' }}
        </button>
      </form>
    </div>

    <template #footer>
      <p class="font-body text-sm text-base-400">
        Нет аккаунта?
        <RouterLink to="/register" class="text-base-700 font-medium hover:text-base-900 transition-colors">
          Зарегистрироваться
        </RouterLink>
      </p>
    </template>
  </AuthLayout>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, useRoute, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { authApi } from '@/api/auth'
import AuthLayout from '@/components/layout/AuthLayout.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import AlertMessage from '@/components/ui/AlertMessage.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const loading = ref(false)
const errorMessage = ref('')
const showVerifyAlert = ref(false)
const lastEmail = ref('')

const form = reactive({ email: '', password: '' })
const fieldErrors = reactive({ email: '', password: '' })

function clearErrors() {
  errorMessage.value = ''
  fieldErrors.email = ''
  fieldErrors.password = ''
}

async function handleLogin() {
  clearErrors()

  if (!form.email) { fieldErrors.email = 'Введите email'; return }
  if (!form.password) { fieldErrors.password = 'Введите пароль'; return }

  loading.value = true
  try {
    await authStore.login(form.email, form.password)
    const redirect = route.query.redirect as string | undefined
    router.push(redirect || '/movies')
  } catch (e: unknown) {
    const err = e as { response?: { data?: { detail?: string } } }
    const detail = err.response?.data?.detail
    if (detail === 'LOGIN_BAD_CREDENTIALS') {
      errorMessage.value = 'Неверный email или пароль'
    } else if (detail === 'LOGIN_USER_NOT_VERIFIED') {
      lastEmail.value = form.email
      showVerifyAlert.value = true
    } else {
      errorMessage.value = 'Произошла ошибка. Попробуйте позже.'
    }
  } finally {
    loading.value = false
  }
}

async function resendVerification() {
  if (!lastEmail.value) return
  try {
    await authApi.requestVerifyToken(lastEmail.value)
    showVerifyAlert.value = false
    router.push({ name: 'email-sent', query: { email: lastEmail.value } })
  } catch {
    errorMessage.value = 'Не удалось отправить письмо'
  }
}
</script>
