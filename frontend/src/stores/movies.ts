import { defineStore } from 'pinia'
import { ref } from 'vue'
import { moviesApi, type MovieRead, type MovieCreate, type MovieUpdate } from '@/api/movies'

export const useMoviesStore = defineStore('movies', () => {
  const movies = ref<MovieRead[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchMovies(onlyMine = false) {
    loading.value = true
    error.value = null
    try {
      const result = await moviesApi.getList(onlyMine)
      movies.value = result.movies
    } catch (e) {
      error.value = 'Не удалось загрузить список фильмов'
    } finally {
      loading.value = false
    }
  }

  async function addMovie(movie: MovieCreate): Promise<MovieRead> {
    const created = await moviesApi.create(movie)
    movies.value.unshift(created)
    return created
  }

  async function updateMovie(slug: string, movie: MovieUpdate): Promise<MovieRead> {
    const updated = await moviesApi.patch(slug, movie)
    const index = movies.value.findIndex((m) => m.slug === slug)
    if (index !== -1) movies.value[index] = updated
    return updated
  }

  async function deleteMovie(slug: string) {
    await moviesApi.delete(slug)
    movies.value = movies.value.filter((m) => m.slug !== slug)
  }

  async function toggleWatched(movie: MovieRead) {
    return updateMovie(movie.slug, { watched: !movie.watched })
  }

  return {
    movies,
    loading,
    error,
    fetchMovies,
    addMovie,
    updateMovie,
    deleteMovie,
    toggleWatched,
  }
})
