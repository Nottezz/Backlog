<template>
  <AuthLayout>
    <div>
      <!-- Success state -->
      <template v-if="success">
        <div class="text-center py-4">
          <div class="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg class="w-8 h-8 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h1 class="font-display text-2xl font-bold text-ink-900 mb-3">Пароль изменён</h1>
          <p class="font-body text-ink-500 text-sm mb-8">Теперь вы можете войти с новым паролем</p>
          <RouterLink to="/login" class="btn-primary">
            Войти
          </RouterLink>
        </div>
      </template>

      <!-- Invalid token -->
      <template v-else-if="tokenError">
        <div class="text-center py-4">
          <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg class="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h1 class="font-display text-2xl font-bold text-ink-900 mb-3">Ссылка недействительна</h1>
          <p class="font-body text-ink-500 text-sm mb-8">
            Ссылка устарела или была использована ранее.<br />Запросите новую.
          </p>
          <RouterLink to="/forgot-password" class="btn-primary">
            Запросить снова
          </RouterLink>
        </div>
      </template>

      <!-- No token in URL -->
      <template v-else-if="!token">
        <div class="text-center py-4">
          <p class="font-body text-ink-500 mb-4">Ссылка для сброса пароля не найдена</p>
          <RouterLink to="/forgot-password" class="btn-secondary text-sm">
            Запросить ссылку
          </RouterLink>
        </div>
      </template>

      <!-- Form -->
      <template v-else>
        <h1 class="font-display text-2xl font-bold text-ink-900 mb-1">Новый пароль</h1>
        <p class="font-body text-ink-400 text-sm mb-8">Придумайте надёжный пароль</p>

        <AlertMessage
          :show="!!errorMessage"
          variant="error"
          :message="errorMessage"
          dismissible
          class="mb-6"
          @dismiss="errorMessage = ''"
        />

        <form @submit.prevent="handleSubmit" class="flex flex-col gap-5">
          <BaseInput
            v-model="form.password"
            label="Новый пароль"
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

          <button type="submit" class="btn-primary w-full" :disabled="loading">
            <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            {{ loading ? 'Сохраняем…' : 'Установить пароль' }}
          </button>
        </form>
      </template>
    </div>

    <template #footer>
      <RouterLink to="/login" class="font-body text-sm text-ink-400 hover:text-ink-700 transition-colors">
        ← Вернуться к входу
      </RouterLink>
    </template>
  </AuthLayout>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { authApi } from '@/api/auth'
import AuthLayout from '@/components/layout/AuthLayout.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import AlertMessage from '@/components/ui/AlertMessage.vue'

const route = useRoute()
const token = route.query.token as string | undefined

const loading = ref(false)
const success = ref(false)
const tokenError = ref(false)
const errorMessage = ref('')

const form = reactive({ password: '', confirmPassword: '' })
const fieldErrors = reactive({ password: '', confirmPassword: '' })

async function handleSubmit() {
  Object.assign(fieldErrors, { password: '', confirmPassword: '' })
  errorMessage.value = ''

  if (form.password.length < 8) {
    fieldErrors.password = 'Пароль должен содержать не менее 8 символов'
    return
  }
  if (form.password !== form.confirmPassword) {
    fieldErrors.confirmPassword = 'Пароли не совпадают'
    return
  }

  loading.value = true
  try {
    await authApi.resetPassword(token!, form.password)
    success.value = true
  } catch (e: unknown) {
    const err = e as { response?: { data?: { detail?: unknown } } }
    const detail = err.response?.data?.detail
    if (detail === 'RESET_PASSWORD_BAD_TOKEN') {
      tokenError.value = true
    } else if (typeof detail === 'object' && detail !== null) {
      const d = detail as { reason?: string }
      fieldErrors.password = d.reason || 'Недопустимый пароль'
    } else {
      errorMessage.value = 'Произошла ошибка. Попробуйте позже.'
    }
  } finally {
    loading.value = false
  }
}
</script>
