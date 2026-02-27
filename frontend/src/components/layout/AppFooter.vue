<template>
  <footer class="border-t border-ink-100 py-10 mt-auto">
    <div class="max-w-6xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-4">
      <div class="flex items-center gap-2">
        <span class="font-display font-bold text-ink-900">Backlog</span>
        <span class="text-ink-300">·</span>
        <span class="font-body text-sm text-ink-400">Ваш личный список фильмов</span>
      </div>
      <div class="flex items-center gap-6">
        <RouterLink to="/" class="font-body text-sm text-ink-400 hover:text-ink-700 transition-colors">
          Главная
        </RouterLink>
        <RouterLink to="/register" class="font-body text-sm text-ink-400 hover:text-ink-700 transition-colors">
          Регистрация
        </RouterLink>
        <RouterLink to="/login" class="font-body text-sm text-ink-400 hover:text-ink-700 transition-colors">
          Войти
        </RouterLink>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>
