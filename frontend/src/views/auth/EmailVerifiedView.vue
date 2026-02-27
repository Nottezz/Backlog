<template>
  <AuthLayout>
    <div class="text-center py-4">
      <!-- Loading -->
      <template v-if="status === 'loading'">
        <div class="w-16 h-16 bg-surface-muted rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-8 h-8 text-base-400 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
        </div>
        <p class="font-body text-base-500">Подтверждаем адрес…</p>
      </template>

      <!-- Success -->
      <template v-else-if="status === 'success'">
        <div class="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-8 h-8 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h1 class="font-display text-2xl font-bold text-base-900 mb-3">Email подтверждён!</h1>
        <p class="font-body text-base-500 text-sm mb-8">
          Ваш аккаунт активирован. Войдите, чтобы начать.
        </p>
        <RouterLink to="/login" class="btn-primary">
          Войти в аккаунт
        </RouterLink>
      </template>

      <!-- Already verified -->
      <template v-else-if="status === 'already-verified'">
        <div class="w-16 h-16 bg-amber-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-8 h-8 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h1 class="font-display text-2xl font-bold text-base-900 mb-3">Уже подтверждён</h1>
        <p class="font-body text-base-500 text-sm mb-8">
          Этот email уже был подтверждён ранее. Вы можете войти.
        </p>
        <RouterLink to="/login" class="btn-primary">
          Войти
        </RouterLink>
      </template>

      <!-- Error -->
      <template v-else-if="status === 'error'">
        <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </div>
        <h1 class="font-display text-2xl font-bold text-base-900 mb-3">Ссылка недействительна</h1>
        <p class="font-body text-base-500 text-sm mb-8">
          Ссылка устарела или была использована ранее.<br />Запросите новое письмо.
        </p>
        <RouterLink to="/login" class="btn-primary mb-3">
          Войти
        </RouterLink>
      </template>

      <!-- No token -->
      <template v-else>
        <p class="font-body text-base-500 mb-4">Токен подтверждения не найден</p>
        <RouterLink to="/" class="btn-secondary text-sm">На главную</RouterLink>
      </template>
    </div>
  </AuthLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { authApi } from '@/api/auth'
import AuthLayout from '@/components/layout/AuthLayout.vue'

type Status = 'loading' | 'success' | 'error' | 'already-verified' | 'no-token'

const route = useRoute()
const token = route.query.token as string | undefined
const status = ref<Status>(token ? 'loading' : 'no-token')

onMounted(async () => {
  if (!token) return

  try {
    await authApi.verify(token)
    status.value = 'success'
  } catch (e: unknown) {
    const err = e as { response?: { data?: { detail?: string } } }
    const detail = err.response?.data?.detail
    if (detail === 'VERIFY_USER_ALREADY_VERIFIED') {
      status.value = 'already-verified'
    } else {
      status.value = 'error'
    }
  }
})
</script>
