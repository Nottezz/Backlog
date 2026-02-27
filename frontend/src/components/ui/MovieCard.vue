<template>
  <div class="card group hover:shadow-md transition-all duration-200 flex flex-col">
    <!-- Top bar: watched status + published -->
    <div class="flex items-center justify-between px-5 pt-4 pb-3 border-b border-surface-border">
      <button
        :class="[
          'flex items-center gap-1.5 text-xs font-mono transition-all duration-150',
          movie.watched
            ? 'text-emerald-600'
            : isOwner
              ? 'text-base-300 hover:text-base-600 cursor-pointer'
              : 'text-base-200 cursor-not-allowed opacity-60',
        ]"
        :disabled="!isOwner"
        :title="!isOwner ? 'Только автор может изменять статус' : movie.watched ? 'Снять отметку' : 'Отметить как просмотренный'"
        @click.stop="handleToggleWatched"
      >
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path v-if="movie.watched" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
          <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        {{ movie.watched ? 'Просмотрен' : 'Добавить отметку' }}
      </button>

      <span v-if="movie.published" class="font-mono text-xs text-base-300 border border-surface-border px-1.5 py-0.5 rounded-xl">
        публичный
      </span>
    </div>

    <!-- Main content -->
    <div class="p-5 flex-1 flex flex-col">
      <RouterLink :to="`/movies/${movie.id}`" class="flex-1">
        <!-- Title + year -->
        <div class="flex items-start justify-between gap-3 mb-2">
          <h3 class="font-display font-bold text-base-900 group-hover:text-accent transition-colors leading-tight">
            {{ movie.title }}
          </h3>
          <span v-if="movie.year" class="shrink-0 font-mono text-xs text-base-400 mt-0.5">
            {{ movie.year }}
          </span>
        </div>

        <!-- Description -->
        <p v-if="movie.description" class="font-body text-xs text-base-400 leading-relaxed line-clamp-3 mb-4">
          {{ movie.description }}
        </p>

        <!-- Rating -->
        <div v-if="movie.rating" class="flex items-center gap-1.5 mb-4">
          <div class="flex">
            <span
              v-for="n in 5" :key="n"
              :class="n <= Math.round(movie.rating / 2) ? 'text-amber-400' : 'text-base-200'"
              class="text-sm"
            >★</span>
          </div>
          <span class="font-mono text-xs text-base-400">{{ movie.rating }}/10</span>
        </div>
      </RouterLink>

      <!-- Actions -->
      <div class="flex items-center justify-between pt-3 border-t border-surface-border mt-auto">
        <!-- Author label for foreign movies -->
        <span v-if="!isOwner" class="font-mono text-xs text-base-300 flex items-center gap-1">
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          {{ movie.user.username || movie.user.email }}
        </span>
        <span v-else class="font-mono text-xs text-base-300">
          {{ formatDate(movie.createdAt) }}
        </span>

        <!-- Owner-only action buttons -->
        <div
          v-if="isOwner"
          class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity"
        >
          <RouterLink
            :to="`/movies/${movie.id}`"
            class="p-1.5 text-base-400 hover:text-base-700 rounded-lg transition-colors"
            title="Открыть"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
          </RouterLink>
          <button
            class="p-1.5 text-base-400 hover:text-danger rounded-lg transition-colors"
            title="Удалить"
            @click.stop="$emit('delete', movie)"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>

        <!-- Non-owner: just open link -->
        <RouterLink
          v-else
          :to="`/movies/${movie.id}`"
          class="p-1.5 text-base-300 hover:text-base-600 rounded-lg transition-colors opacity-0 group-hover:opacity-100"
          title="Открыть"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import type { MovieRead } from '@/api/movies'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'

const props = defineProps<{ movie: MovieRead }>()
const emit = defineEmits<{
  'toggle-watched': [movie: MovieRead]
  delete: [movie: MovieRead]
}>()

const authStore = useAuthStore()
const toast = useToast()

// Check ownership by comparing user IDs
const isOwner = computed(() =>
  authStore.user?.id === props.movie.user.id
)

function handleToggleWatched() {
  if (!isOwner.value) {
    toast.error('Вы не можете изменять чужие записи')
    return
  }
  emit('toggle-watched', props.movie)
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  })
}
</script>
