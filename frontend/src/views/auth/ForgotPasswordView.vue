<template>
  <AuthLayout>
    <div>
      <!-- Success state -->
      <template v-if="sent">
        <div class="text-center py-4">
          <div class="w-16 h-16 bg-surface-muted rounded-full flex items-center justify-center mx-auto mb-6">
            <svg class="w-8 h-8 text-base-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <h1 class="font-display text-2xl font-bold text-base-900 mb-3">Письмо отправлено</h1>
          <p class="font-body text-base-500 text-sm mb-2">
            Мы отправили инструкцию на
          </p>
          <p class="font-mono text-sm text-base-900 font-medium bg-surface-muted px-3 py-1.5 rounded-xl inline-block mb-6">
            {{ sentEmail }}
          </p>
          <p class="font-body text-base-400 text-xs mb-8">
            Не получили письмо? Проверьте папку «Спам» или
            <button
              class="underline hover:no-underline text-base-600 transition-colors"
              @click="sent = false"
            >
              попробуйте снова
            </button>
          </p>
          <RouterLink to="/login" class="btn-secondary text-sm">
            ← Вернуться к входу
          </RouterLink>
        </div>
      </template>

      <!-- Form state -->
      <template v-else>
        <h1 class="font-display text-2xl font-bold text-base-900 mb-1">Восстановление пароля</h1>
        <p class="font-body text-base-400 text-sm mb-8">
          Укажите email — мы пришлём ссылку для сброса пароля
        </p>

        <form @submit.prevent="handleSubmit" class="flex flex-col gap-5">
          <BaseInput
            v-model="email"
            label="Email"
            type="email"
            placeholder="you@example.com"
            required
            :error="emailError"
          />

          <button type="submit" class="btn-primary w-full" :disabled="loading">
            <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            {{ loading ? 'Отправляем…' : 'Отправить письмо' }}
          </button>
        </form>
      </template>
    </div>

    <template #footer>
      <RouterLink to="/login" class="font-body text-sm text-base-400 hover:text-base-700 transition-colors">
        ← Вернуться к входу
      </RouterLink>
    </template>
  </AuthLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { authApi } from '@/api/auth'
import AuthLayout from '@/components/layout/AuthLayout.vue'
import BaseInput from '@/components/ui/BaseInput.vue'

const email = ref('')
const emailError = ref('')
const loading = ref(false)
const sent = ref(false)
const sentEmail = ref('')

async function handleSubmit() {
  emailError.value = ''
  if (!email.value) { emailError.value = 'Введите email'; return }

  loading.value = true
  try {
    await authApi.forgotPassword(email.value)
    sentEmail.value = email.value
    sent.value = true
  } catch {
    // API возвращает 202 всегда — ошибка только при проблемах сети
    sentEmail.value = email.value
    sent.value = true
  } finally {
    loading.value = false
  }
}
</script>
