<template>
  <Teleport to="body">
    <Transition name="roulette-modal">
      <div
        v-if="show"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        @keydown.esc="$emit('close')"
      >
        <!-- Backdrop -->
        <div
          class="absolute inset-0 bg-base-950/60 backdrop-blur-sm"
          @click="$emit('close')"
        />

        <!-- Panel -->
        <div class="relative w-full max-w-md bg-white rounded-2xl shadow-2xl border border-surface-border overflow-hidden">

          <!-- Header -->
          <div class="flex items-center justify-between px-6 py-4 border-b border-surface-border">
            <div class="flex items-center gap-2.5">
              <span class="text-xl">🎲</span>
              <div>
                <h2 class="font-display font-bold text-base-900 leading-tight">Что посмотреть?</h2>
                <p class="font-mono text-xs text-base-400 mt-0.5">
                  из публичных и ваших фильмов
                </p>
              </div>
            </div>
            <button
              @click="$emit('close')"
              class="p-1.5 text-base-400 hover:text-base-700 hover:bg-surface-muted rounded-lg transition-all"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Content -->
          <div class="px-6 py-6 min-h-[220px] flex flex-col items-center justify-center">

            <!-- Loading state -->
            <div v-if="loading" class="flex flex-col items-center gap-4 py-4">
              <div class="relative w-14 h-14">
                <div class="absolute inset-0 rounded-full border-4 border-surface-muted" />
                <div class="absolute inset-0 rounded-full border-4 border-accent border-t-transparent animate-spin" />
                <span class="absolute inset-0 flex items-center justify-center text-xl">🎬</span>
              </div>
              <p class="font-body text-sm text-base-400">Выбираем фильм...</p>
            </div>

            <!-- Exhausted state -->
            <div v-else-if="exhausted" class="flex flex-col items-center gap-3 py-4 text-center">
              <span class="text-4xl">😔</span>
              <div>
                <p class="font-display font-bold text-base-900 mb-1">Все фильмы перебраны</p>
                <p class="font-body text-sm text-base-400">
                  Вы отклонили все доступные непросмотренные фильмы.
                </p>
              </div>
              <button @click="$emit('restart')" class="btn-secondary mt-2">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Начать заново
              </button>
            </div>

            <!-- Movie card -->
            <div v-else-if="movie" class="w-full">
              <!-- Picked counter -->
              <div class="flex items-center justify-between mb-4">
                <span class="font-mono text-xs text-base-400">
                  Предложено: <strong class="text-base-600">{{ rejectedCount + 1 }}</strong>
                </span>
                <span v-if="rejectedCount > 0" class="font-mono text-xs text-base-300">
                  отклонено: {{ rejectedCount }}
                </span>
              </div>

              <!-- Film card body -->
              <div class="bg-surface-soft border border-surface-border rounded-xl p-5">
                <!-- Title row -->
                <div class="flex items-start justify-between gap-3 mb-2">
                  <h3 class="font-display font-bold text-base-900 text-lg leading-tight">
                    {{ movie.title }}
                  </h3>
                  <span v-if="movie.year" class="shrink-0 font-mono text-xs text-base-400 mt-1 bg-surface-muted px-2 py-0.5 rounded-lg">
                    {{ movie.year }}
                  </span>
                </div>

                <!-- Ratings row -->
                <div class="flex flex-wrap items-center gap-2 mb-3">
                  <!-- Personal rating stars -->
                  <div v-if="movie.rating" class="flex items-center gap-1">
                    <div class="flex">
                      <span
                        v-for="n in 5"
                        :key="n"
                        :class="n <= Math.round(movie.rating / 2) ? 'text-amber-400' : 'text-base-200'"
                        class="text-sm leading-none"
                      >★</span>
                    </div>
                    <span class="font-mono text-xs text-base-400">{{ movie.rating }}/10</span>
                  </div>

                  <!-- IMDb badge -->
                  <span
                    v-if="movie.imdbRating"
                    class="inline-flex items-center font-mono rounded px-1.5 py-0.5"
                    style="background: #fef3c7; color: #92400e; font-size: 11px;"
                  >IMDb {{ movie.imdbRating }}</span>

                  <!-- Metascore badge -->
                  <span
                    v-if="movie.metacriticScore"
                    :style="metacriticStyle(movie.metacriticScore)"
                    class="inline-flex items-center font-mono rounded px-1.5 py-0.5"
                    style="font-size: 11px;"
                  >MC {{ movie.metacriticScore }}</span>

                  <!-- Public badge -->
                  <span
                    v-if="movie.published"
                    class="font-mono text-xs text-base-300 border border-surface-border px-1.5 py-0.5 rounded-lg"
                  >публичный</span>
                </div>

                <!-- Description -->
                <p v-if="movie.description" class="font-body text-xs text-base-500 leading-relaxed line-clamp-3">
                  {{ movie.description }}
                </p>
              </div>
            </div>
          </div>

          <!-- Footer actions -->
          <div v-if="!loading && !exhausted && movie" class="px-6 pb-6 flex gap-3">
            <!-- Reject -->
            <button @click="$emit('reject')" class="btn-secondary flex-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
              Другой фильм
            </button>

            <!-- Accept: open watch link or go to detail page -->
            <a
              v-if="movie.watchLink"
              :href="movie.watchLink"
              target="_blank"
              rel="noopener noreferrer"
              class="btn-primary flex-1"
              @click="$emit('close')"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Смотреть
            </a>
            <RouterLink
              v-else
              :to="`/movies/${movie.id}`"
              class="btn-primary flex-1 text-center"
              @click="$emit('close')"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              Открыть
            </RouterLink>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type { MovieRead } from '@/api/movies.ts'

defineProps<{
  show: boolean
  movie: MovieRead | null
  loading: boolean
  exhausted: boolean
  rejectedCount: number
}>()

defineEmits<{
  close: []
  reject: []
  restart: []
}>()

function metacriticStyle(score: number) {
  const bg = score >= 61 ? '#dcfce7' : score >= 40 ? '#fef9c3' : '#fee2e2'
  const color = score >= 61 ? '#166534' : score >= 40 ? '#854d0e' : '#991b1b'
  return `background: ${bg}; color: ${color};`
}
</script>

<style scoped>
.roulette-modal-enter-active,
.roulette-modal-leave-active {
  transition: opacity 0.2s ease;
}
.roulette-modal-enter-active .relative,
.roulette-modal-leave-active .relative {
  transition: transform 0.2s ease, opacity 0.2s ease;
}
.roulette-modal-enter-from {
  opacity: 0;
}
.roulette-modal-enter-from .relative {
  transform: translateY(12px) scale(0.97);
  opacity: 0;
}
.roulette-modal-leave-to {
  opacity: 0;
}
.roulette-modal-leave-to .relative {
  transform: translateY(8px) scale(0.98);
  opacity: 0;
}
</style>
