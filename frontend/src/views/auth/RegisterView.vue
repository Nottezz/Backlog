<template>
  <AuthLayout>
    <div>
      <h1 class="font-display text-2xl font-bold text-ink-900 mb-1">Создать аккаунт</h1>
      <p class="font-body text-ink-400 text-sm mb-8">Начните вести свой список фильмов</p>

      <AlertMessage
        :show="!!errorMessage"
        variant="error"
        :message="errorMessage"
        dismissible
        class="mb-6"
        @dismiss="errorMessage = ''"
      />

      <form @submit.prevent="handleRegister" class="flex flex-col gap-5">
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
          placeholder="Минимум 8 символов"
          required
          :error="fieldErrors.password"
          hint="Не менее 8 символов"
        />
        <BaseInput
          v-model="form.confirmPassword"
          label="Повторите пароль"
          type="password"
          placeholder="••••••••"
          required
          :error="fieldErrors.confirmPassword"
        />

        <button
          type="submit"
          class="btn-primary w-full mt-1"
          :disabled="loading"
        >
          <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          {{ loading ? 'Регистрируем…' : 'Зарегистрироваться' }}
        </button>
      </form>
    </div>

    <template #footer>
      <p class="font-body text-sm text-ink-400">
        Уже есть аккаунт?
        <RouterLink to="/login" class="text-ink-700 font-medium hover:text-ink-900 transition-colors">
          Войти
        </RouterLink>
      </p>
    </template>
  </AuthLayout>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { authApi } from '@/api/auth'
import AuthLayout from '@/components/layout/AuthLayout.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import AlertMessage from '@/components/ui/AlertMessage.vue'

const router = useRouter()

const loading = ref(false)
const errorMessage = ref('')

const form = reactive({ email: '', password: '', confirmPassword: '' })
const fieldErrors = reactive({ email: '', password: '', confirmPassword: '' })

function clearErrors() {
  errorMessage.value = ''
  Object.assign(fieldErrors, { email: '', password: '', confirmPassword: '' })
}

function validate(): boolean {
  clearErrors()
  let valid = true

  if (!form.email) { fieldErrors.email = 'Введите email'; valid = false }
  else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    fieldErrors.email = 'Некорректный email'; valid = false
  }

  if (!form.password) { fieldErrors.password = 'Введите пароль'; valid = false }
  else if (form.password.length < 8) {
    fieldErrors.password = 'Пароль должен содержать не менее 8 символов'; valid = false
  }

  if (!form.confirmPassword) { fieldErrors.confirmPassword = 'Повторите пароль'; valid = false }
  else if (form.password !== form.confirmPassword) {
    fieldErrors.confirmPassword = 'Пароли не совпадают'; valid = false
  }

  return valid
}

async function handleRegister() {
  if (!validate()) return

  loading.value = true
  try {
    await authApi.register(form.email, form.password)
    router.push({ name: 'email-sent', query: { email: form.email } })
  } catch (e: unknown) {
    const err = e as { response?: { data?: { detail?: unknown } } }
    const detail = err.response?.data?.detail
    if (detail === 'REGISTER_USER_ALREADY_EXISTS') {
      fieldErrors.email = 'Пользователь с таким email уже существует'
    } else if (typeof detail === 'object' && detail !== null) {
      const d = detail as { code?: string; reason?: string }
      if (d.code === 'REGISTER_INVALID_PASSWORD') {
        fieldErrors.password = d.reason || 'Недопустимый пароль'
      }
    } else {
      errorMessage.value = 'Произошла ошибка. Попробуйте позже.'
    }
  } finally {
    loading.value = false
  }
}
</script>
