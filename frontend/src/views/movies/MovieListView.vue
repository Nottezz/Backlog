<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />

    <main class="flex-1 max-w-6xl mx-auto px-6 pt-24 pb-16 w-full">
      <!-- Page header -->
      <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-6 mb-10">
        <div>
          <p class="font-mono text-xs tracking-widest text-base-400 uppercase mb-2">Коллекция</p>
          <h1 class="font-display text-3xl font-bold text-base-900">Мои фильмы</h1>
        </div>
        <button @click="showAddModal = true" class="btn-primary shrink-0">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Добавить фильм
        </button>
      </div>

      <!-- Filters -->
      <div class="flex flex-wrap items-center gap-3 mb-8 pb-6 border-b border-surface-border">
        <button
          v-for="filter in filters"
          :key="filter.key"
          :class="[
            'px-4 py-1.5 font-body text-sm rounded-xl border transition-all',
            activeFilter === filter.key
              ? 'bg-base-900 text-surface-muted border-base-900'
              : 'bg-white text-base-600 border-surface-border hover:border-base-400',
          ]"
          @click="setFilter(filter.key)"
        >
          {{ filter.label }}
          <span v-if="filter.count !== undefined" class="ml-1.5 font-mono text-xs opacity-60">
            {{ filter.count }}
          </span>
        </button>

        <div class="ml-auto">
            <BaseToggle v-model="onlyMine" label="Только мои" @update:modelValue="loadMovies" />
          </div>
      </div>

      <!-- Stats bar -->
      <div v-if="!store.loading && store.movies.length > 0" class="flex items-center gap-6 mb-8 font-mono text-xs text-base-400">
        <span>Всего: <strong class="text-base-700">{{ store.movies.length }}</strong></span>
        <span>Просмотрено: <strong class="text-emerald-600">{{ watchedCount }}</strong></span>
        <span>Ожидает: <strong class="text-base-700">{{ pendingCount }}</strong></span>
      </div>

      <!-- Loading -->
      <div v-if="store.loading" class="flex items-center justify-center py-24">
        <svg class="w-8 h-8 text-base-300 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
      </div>

      <!-- Error -->
      <AlertMessage v-else-if="store.error" :show="true" variant="error" :message="store.error" class="my-8" />

      <!-- Empty state -->
      <div v-else-if="filteredMovies.length === 0" class="flex flex-col items-center justify-center py-24 text-center">
        <div class="text-5xl mb-6">🎬</div>
        <h3 class="font-display text-xl font-bold text-base-900 mb-2">
          {{ store.movies.length === 0 ? 'Список пуст' : 'Ничего не найдено' }}
        </h3>
        <p class="font-body text-sm text-base-400 mb-8 max-w-xs">
          {{ store.movies.length === 0
            ? 'Добавьте первый фильм, который хотите посмотреть'
            : 'Попробуйте другой фильтр' }}
        </p>
        <button v-if="store.movies.length === 0" @click="showAddModal = true" class="btn-primary">
          Добавить первый фильм
        </button>
      </div>

      <!-- Grid -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <MovieCard
          v-for="movie in filteredMovies"
          :key="movie.id"
          :movie="movie"
          @toggle-watched="handleToggleWatched"
          @delete="confirmDelete($event)"
        />
      </div>
    </main>

    <!-- Add / Edit Modal -->
    <AddMovieModal
      :show="showAddModal"
      :edit-movie="editingMovie"
      @close="closeModal"
      @submit="handleMovieSubmit"
    />

    <!-- Delete confirm -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="deletingMovie" class="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div class="absolute inset-0 bg-base-950/50 backdrop-blur-sm" @click="deletingMovie = null" />
          <div class="relative bg-white rounded-xl shadow-2xl border border-surface-border p-6 max-w-sm w-full">
            <h3 class="font-display text-lg font-bold text-base-900 mb-2">Удалить фильм?</h3>
            <p class="font-body text-sm text-base-500 mb-6">
              «{{ deletingMovie.title }}» будет удалён без возможности восстановления.
            </p>
            <div class="flex gap-3 justify-end">
              <button @click="deletingMovie = null" class="btn-secondary">Отмена</button>
              <button @click="handleDelete" class="btn-danger">Удалить</button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useMoviesStore } from '@/stores/movies'
import type { MovieRead } from '@/api/movies'
import AppHeader from '@/components/layout/AppHeader.vue'
import MovieCard from '@/components/ui/MovieCard.vue'
import AddMovieModal from '@/components/ui/AddMovieModal.vue'
import AlertMessage from '@/components/ui/AlertMessage.vue'
import BaseToggle from '@/components/ui/BaseToggle.vue'
import { useToast } from '@/composables/useToast'

const store = useMoviesStore()
const toast = useToast()
const showAddModal = ref(false)
const editingMovie = ref<MovieRead | null>(null)
const deletingMovie = ref<MovieRead | null>(null)
const activeFilter = ref<'all' | 'watched' | 'pending'>('all')
const onlyMine = ref(false)

const watchedCount = computed(() => store.movies.filter((m) => m.watched).length)
const pendingCount = computed(() => store.movies.filter((m) => !m.watched).length)

const filters = computed(() => [
  { key: 'all' as const, label: 'Все', count: store.movies.length },
  { key: 'pending' as const, label: 'К просмотру', count: pendingCount.value },
  { key: 'watched' as const, label: 'Просмотрено', count: watchedCount.value },
])

const filteredMovies = computed(() => {
  if (activeFilter.value === 'watched') return store.movies.filter((m) => m.watched)
  if (activeFilter.value === 'pending') return store.movies.filter((m) => !m.watched)
  return store.movies
})

function setFilter(key: typeof activeFilter.value) {
  activeFilter.value = key
}

async function loadMovies() {
  await store.fetchMovies(onlyMine.value)
}

onMounted(loadMovies)

function closeModal() {
  showAddModal.value = false
  editingMovie.value = null
}

async function handleMovieSubmit(data: Parameters<typeof store.addMovie>[0] & { watched?: boolean }) {
  try {
    if (editingMovie.value) {
      await store.updateMovie(editingMovie.value.id, data)
    } else {
      await store.addMovie(data)
    }
    closeModal()
  } catch (e) {
    console.error(e)
  }
}

async function handleToggleWatched(movie: MovieRead) {
  try {
    await store.toggleWatched(movie)
  } catch (e: unknown) {
    const err = e as { response?: { status?: number } }
    if (err.response?.status === 403) {
      toast.error('Вы не можете изменять чужие записи')
    } else {
      toast.error('Не удалось обновить статус')
    }
  }
}

function confirmDelete(movie: MovieRead) {
  deletingMovie.value = movie
}

async function handleDelete() {
  if (!deletingMovie.value) return
  try {
    await store.deleteMovie(deletingMovie.value.id)
    deletingMovie.value = null
  } catch (e: unknown) {
    const err = e as { response?: { status?: number } }
    deletingMovie.value = null
    if (err.response?.status === 403) {
      toast.error('Вы не можете удалять чужие записи')
    } else {
      toast.error('Не удалось удалить фильм')
    }
  }
}
</script>
