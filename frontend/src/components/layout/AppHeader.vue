<template>
  <header class="fixed top-0 inset-x-0 z-50 border-b border-ink-100 bg-parchment-50/95 backdrop-blur-sm">
    <div class="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
      <!-- Logo -->
      <RouterLink to="/" class="flex items-center gap-2 group">
        <span class="font-display text-xl font-bold text-ink-900 group-hover:text-ink-700 transition-colors">
          Backlog
        </span>
        <span class="hidden sm:block font-mono text-xs text-ink-400 border border-ink-200 px-1.5 py-0.5 rounded-sm">
          β
        </span>
      </RouterLink>

      <!-- Nav -->
      <nav class="flex items-center gap-2">
        <template v-if="authStore.isAuthenticated">
          <RouterLink
            to="/movies"
            class="px-4 py-2 font-body text-sm text-ink-700 hover:text-ink-900 transition-colors"
          >
            Мои фильмы
          </RouterLink>
          <div class="w-px h-4 bg-ink-200 mx-1" />
          <span class="text-sm text-ink-400 font-mono hidden sm:block">
            {{ authStore.user?.username || authStore.user?.email }}
          </span>
          <button
            @click="handleLogout"
            class="px-4 py-2 font-body text-sm text-ink-500 hover:text-accent transition-colors"
          >
            Выйти
          </button>
        </template>
        <template v-else>
          <RouterLink
            to="/login"
            class="px-4 py-2 font-body text-sm text-ink-700 hover:text-ink-900 transition-colors"
          >
            Войти
          </RouterLink>
          <RouterLink to="/register" class="btn-primary text-sm py-2">
            Регистрация
          </RouterLink>
        </template>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

async function handleLogout() {
  await authStore.logout()
  router.push('/')
}
</script>
