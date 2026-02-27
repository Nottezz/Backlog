<template>
  <footer class="bg-base-950 text-base-400 mt-auto">
    <div class="max-w-6xl mx-auto px-6 py-12">
      <!-- Top row -->
      <div class="flex flex-col md:flex-row justify-between gap-10 pb-10 border-b border-base-800">
        <!-- Brand -->
        <div class="max-w-xs">
          <div class="flex items-center gap-2 mb-3">
            <div class="w-7 h-7 rounded-lg bg-accent flex items-center justify-center">
              <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M19 3H5a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2V5a2 2 0 00-2-2zm-7 14l-5-5 1.41-1.41L12 14.17l7.59-7.59L21 8l-9 9z"/>
              </svg>
            </div>
            <span class="font-display font-bold text-white text-lg tracking-tight">Backlog</span>
          </div>
          <p class="text-sm leading-relaxed text-base-500">
            Личный трекер фильмов. Сохраняйте, оценивайте и отмечайте просмотренное.
          </p>
        </div>

        <!-- Links -->
        <div class="flex flex-wrap gap-12">
          <div>
            <p class="text-xs font-mono text-base-600 uppercase tracking-widest mb-4">Навигация</p>
            <div class="flex flex-col gap-2.5">
              <RouterLink to="/" class="text-sm text-base-400 hover:text-white transition-colors">Главная</RouterLink>
              <RouterLink to="/register" class="text-sm text-base-400 hover:text-white transition-colors">Регистрация</RouterLink>
              <RouterLink to="/login" class="text-sm text-base-400 hover:text-white transition-colors">Войти</RouterLink>
            </div>
          </div>

          <div>
            <p class="text-xs font-mono text-base-600 uppercase tracking-widest mb-4">Контакты</p>
            <div class="flex flex-col gap-2.5">
              <a
                href="mailto:admin@backlog-movie.ru"
                class="text-sm text-base-400 hover:text-white transition-colors flex items-center gap-1.5"
              >
                <svg class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                admin@backlog-movie.ru
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom row -->
      <div class="pt-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-base-600">
        <span>© {{ new Date().getFullYear() }} Backlog. Все права защищены.</span>
        <span class="flex items-center gap-1.5">
          Сделано
          <a
            href="https://nottezz.ru"
            target="_blank"
            rel="noopener noreferrer"
            class="text-base-400 hover:text-accent transition-colors font-medium"
          >
            nottezz.ru
          </a>
        </span>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>
