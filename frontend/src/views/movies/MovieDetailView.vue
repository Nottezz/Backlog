<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />

    <main class="flex-1 max-w-3xl mx-auto px-6 pt-24 pb-16 w-full">
      <!-- Back link -->
      <RouterLink to="/movies" class="inline-flex items-center gap-2 font-body text-sm text-ink-400 hover:text-ink-700 transition-colors mb-8">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        К списку фильмов
      </RouterLink>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-24">
        <svg class="w-8 h-8 text-ink-300 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
      </div>

      <!-- Error -->
      <AlertMessage v-else-if="error" :show="true" variant="error" :message="error" />

      <!-- Content -->
      <div v-else-if="movie">
        <!-- Header -->
        <div class="mb-10">
          <div class="flex flex-wrap items-center gap-3 mb-4">
            <span v-if="movie.year" class="font-mono text-sm text-ink-400 border border-ink-200 px-2 py-0.5 rounded-sm">
              {{ movie.year }}
            </span>
            <span
              :class="[
                'font-mono text-xs px-2 py-0.5 rounded-sm border',
                movie.watched
                  ? 'border-emerald-200 text-emerald-700 bg-emerald-50'
                  : 'border-ink-200 text-ink-400',
              ]"
            >
              {{ movie.watched ? '✓ Просмотрен' : 'Не просмотрен' }}
            </span>
            <span v-if="movie.published" class="font-mono text-xs text-ink-300 border border-ink-100 px-2 py-0.5 rounded-sm">
              публичный
            </span>
          </div>

          <h1 class="font-display text-4xl font-bold text-ink-900 mb-4 leading-tight">
            {{ movie.title }}
          </h1>

          <!-- Rating -->
          <div v-if="movie.rating" class="flex items-center gap-2 mb-6">
            <div class="flex">
              <span v-for="n in 10" :key="n"
                :class="n <= movie.rating ? 'text-amber-400' : 'text-ink-200'"
              >★</span>
            </div>
            <span class="font-mono text-sm text-ink-600 font-medium">{{ movie.rating }} / 10</span>
          </div>

          <!-- Description -->
          <p v-if="movie.description" class="font-body text-ink-600 leading-relaxed text-lg">
            {{ movie.description }}
          </p>
        </div>

        <!-- Meta info -->
        <div class="card p-5 mb-8 flex flex-wrap gap-6 text-sm font-body">
          <div>
            <p class="text-xs font-mono text-ink-400 mb-1">Добавил</p>
            <p class="text-ink-700 font-medium">{{ movie.user.username || movie.user.email }}</p>
          </div>
          <div>
            <p class="text-xs font-mono text-ink-400 mb-1">Добавлено</p>
            <p class="text-ink-700">{{ formatDate(movie.createdAt) }}</p>
          </div>
          <div v-if="movie.kpId">
            <p class="text-xs font-mono text-ink-400 mb-1">Кинопоиск ID</p>
            <p class="text-ink-700 font-mono">{{ movie.kpId }}</p>
          </div>
          <div v-if="movie.imdbId">
            <p class="text-xs font-mono text-ink-400 mb-1">IMDb ID</p>
            <p class="text-ink-700 font-mono">{{ movie.imdbId }}</p>
          </div>
        </div>

        <!-- Watch link -->
        <div v-if="movie.watchLink" class="mb-8">
          <a
            :href="movie.watchLink"
            target="_blank"
            rel="noopener noreferrer"
            class="btn-accent inline-flex"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Смотреть фильм
          </a>
        </div>

        <!-- Actions -->
        <div class="flex flex-wrap gap-3 pt-6 border-t border-ink-100">
          <button
            :class="[
              'btn-secondary text-sm py-2',
              movie.watched ? 'text-emerald-700 border-emerald-200 hover:bg-emerald-50' : '',
            ]"
            @click="handleToggleWatched"
          >
            {{ movie.watched ? '✓ Отметить как непросмотренный' : 'Отметить как просмотренный' }}
          </button>
          <button @click="showEditModal = true" class="btn-secondary text-sm py-2">
            Редактировать
          </button>
          <button @click="confirmDelete = true" class="btn-secondary text-sm py-2 text-accent border-red-100 hover:bg-red-50">
            Удалить
          </button>
        </div>
      </div>
    </main>

    <!-- Edit Modal -->
    <AddMovieModal
      :show="showEditModal"
      :edit-movie="movie"
      @close="showEditModal = false"
      @submit="handleEdit"
    />

    <!-- Delete confirm -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="confirmDelete" class="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div class="absolute inset-0 bg-ink-950/40 backdrop-blur-sm" @click="confirmDelete = false" />
          <div class="relative bg-white rounded-sm shadow-2xl border border-ink-100 p-6 max-w-sm w-full">
            <h3 class="font-display text-lg font-bold text-ink-900 mb-2">Удалить фильм?</h3>
            <p class="font-body text-sm text-ink-500 mb-6">
              «{{ movie?.title }}» будет удалён без возможности восстановления.
            </p>
            <div class="flex gap-3 justify-end">
              <button @click="confirmDelete = false" class="btn-secondary text-sm py-2">Отмена</button>
              <button @click="handleDelete" class="btn-accent text-sm py-2">Удалить</button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { moviesApi, type MovieRead } from '@/api/movies'
import { useMoviesStore } from '@/stores/movies'
import AppHeader from '@/components/layout/AppHeader.vue'
import AlertMessage from '@/components/ui/AlertMessage.vue'
import AddMovieModal from '@/components/ui/AddMovieModal.vue'

const route = useRoute()
const router = useRouter()
const store = useMoviesStore()

const movie = ref<MovieRead | null>(null)
const loading = ref(true)
const error = ref('')
const showEditModal = ref(false)
const confirmDelete = ref(false)

onMounted(async () => {
  try {
    movie.value = await moviesApi.getById(Number(route.params.id))
  } catch {
    error.value = 'Фильм не найден'
  } finally {
    loading.value = false
  }
})

async function handleToggleWatched() {
  if (!movie.value) return
  movie.value = await store.toggleWatched(movie.value)
}

async function handleEdit(data: Parameters<typeof store.updateMovie>[1]) {
  if (!movie.value) return
  movie.value = await store.updateMovie(movie.value.id, data)
  showEditModal.value = false
}

async function handleDelete() {
  if (!movie.value) return
  await store.deleteMovie(movie.value.id)
  router.push('/movies')
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })
}
</script>
