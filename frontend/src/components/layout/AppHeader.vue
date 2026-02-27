<template>
  <header class="fixed top-0 inset-x-0 z-50 bg-surface/80 backdrop-blur-md border-b border-surface-border">
    <div class="max-w-6xl mx-auto px-6 h-15 flex items-center justify-between" style="height:60px">
      <!-- Logo -->
      <RouterLink to="/" class="flex items-center gap-2 group">
        <div class="w-7 h-7 rounded-lg bg-accent flex items-center justify-center shadow-sm">
          <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
            <path d="M19 3H5a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2V5a2 2 0 00-2-2zm-7 14l-5-5 1.41-1.41L12 14.17l7.59-7.59L21 8l-9 9z"/>
          </svg>
        </div>
        <span class="font-display font-bold text-base-900 text-lg tracking-tight group-hover:text-accent transition-colors">
          Backlog
        </span>
      </RouterLink>

      <!-- Nav -->
      <nav class="flex items-center gap-2">
        <template v-if="authStore.isAuthenticated">
          <RouterLink
            to="/movies"
            class="px-3 py-1.5 font-body text-sm text-base-600 hover:text-base-900 hover:bg-surface-muted rounded-lg transition-all"
          >
            Мои фильмы
          </RouterLink>
          <div class="w-px h-4 bg-surface-border mx-1" />
          <span class="text-xs text-base-400 font-mono hidden sm:block px-2">
            {{ authStore.user?.username || authStore.user?.email }}
          </span>
          <button
            @click="handleLogout"
            class="px-3 py-1.5 font-body text-sm text-base-500 hover:text-danger hover:bg-red-50 rounded-lg transition-all"
          >
            Выйти
          </button>
        </template>
        <template v-else>
          <RouterLink
            to="/login"
            class="px-3 py-1.5 font-body text-sm text-base-600 hover:text-base-900 hover:bg-surface-muted rounded-lg transition-all"
          >
            Войти
          </RouterLink>
          <RouterLink to="/register" class="btn-primary !py-2 !px-4">
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
