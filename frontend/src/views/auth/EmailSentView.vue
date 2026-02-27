<template>
  <AuthLayout>
    <div class="text-center py-4">
      <!-- Envelope illustration -->
      <div class="relative w-20 h-20 mx-auto mb-8">
        <div class="w-20 h-20 bg-ink-100 rounded-full flex items-center justify-center">
          <svg class="w-10 h-10 text-ink-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
        </div>
        <!-- Dot indicator -->
        <div class="absolute top-0 right-0 w-5 h-5 bg-accent rounded-full flex items-center justify-center">
          <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/>
          </svg>
        </div>
      </div>

      <h1 class="font-display text-2xl font-bold text-ink-900 mb-3">Подтвердите email</h1>

      <p class="font-body text-ink-500 text-sm mb-2">
        Мы отправили письмо с подтверждением на
      </p>
      <p class="font-mono text-sm text-ink-900 font-medium bg-parchment-100 px-3 py-1.5 rounded-sm inline-block mb-6">
        {{ email || 'ваш email' }}
      </p>

      <p class="font-body text-ink-400 text-xs mb-8 max-w-xs mx-auto leading-relaxed">
        Перейдите по ссылке в письме для активации аккаунта.
        Письмо может прийти в течение нескольких минут.
      </p>

      <!-- Resend -->
      <div class="border-t border-ink-100 pt-6">
        <p class="font-body text-sm text-ink-400 mb-3">Не получили письмо?</p>
        <button
          class="btn-secondary text-sm w-full"
          :disabled="resendCooldown > 0 || resending"
          @click="handleResend"
        >
          <svg v-if="resending" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          <template v-if="resendCooldown > 0">
            Отправить повторно ({{ resendCooldown }}с)
          </template>
          <template v-else>
            {{ resending ? 'Отправляем…' : 'Отправить повторно' }}
          </template>
        </button>

        <AlertMessage
          :show="resendSuccess"
          variant="success"
          message="Письмо отправлено повторно"
          class="mt-4"
        />
      </div>
    </div>

    <template #footer>
      <RouterLink to="/login" class="font-body text-sm text-ink-400 hover:text-ink-700 transition-colors">
        ← Вернуться к входу
      </RouterLink>
    </template>
  </AuthLayout>
</template>

<script setup lang="ts">
import { ref, onUnmounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { authApi } from '@/api/auth'
import AuthLayout from '@/components/layout/AuthLayout.vue'
import AlertMessage from '@/components/ui/AlertMessage.vue'

const route = useRoute()
const email = route.query.email as string | undefined

const resending = ref(false)
const resendSuccess = ref(false)
const resendCooldown = ref(0)
let cooldownTimer: ReturnType<typeof setInterval> | null = null

async function handleResend() {
  if (!email || resendCooldown.value > 0) return
  resending.value = true
  resendSuccess.value = false
  try {
    await authApi.requestVerifyToken(email)
    resendSuccess.value = true
    resendCooldown.value = 60
    cooldownTimer = setInterval(() => {
      resendCooldown.value--
      if (resendCooldown.value <= 0 && cooldownTimer) {
        clearInterval(cooldownTimer)
        cooldownTimer = null
      }
    }, 1000)
  } catch {
    // silently fail
  } finally {
    resending.value = false
  }
}

onUnmounted(() => {
  if (cooldownTimer) clearInterval(cooldownTimer)
})
</script>
