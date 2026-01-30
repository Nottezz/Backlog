<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-xl font-semibold text-gray-700">
        Your Movies ({{ movies.length }})
      </h2>

      <div class="flex items-center gap-3">
        <!-- Toggle Switch for "Only my movies" -->
        <div class="flex items-center gap-2">
          <span class="text-sm text-gray-700 font-medium">All movies</span>

          <!-- Toggle Switch -->
          <button
            @click="onlyMine = !onlyMine; fetchMovies()"
            type="button"
            :class="[
              'relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2',
              onlyMine ? 'bg-indigo-600' : 'bg-gray-300'
            ]"
          >
            <span
              :class="[
                'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                onlyMine ? 'translate-x-6' : 'translate-x-1'
              ]"
            ></span>
          </button>

          <span class="text-sm text-gray-700 font-medium">Only mine</span>
        </div>
      </div>

      <button
        @click="fetchMovies"
        :disabled="loading"
        class="bg-gray-200 text-gray-700 px-3 py-1 rounded hover:bg-gray-300 disabled:opacity-50 transition text-sm"
      >
        {{ loading ? 'Loading...' : 'Refresh' }}
      </button>
    </div>

    <div v-if="loading && movies.length === 0" class="text-center py-8">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
      <p class="mt-2 text-gray-600">Loading movies...</p>
    </div>

    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
      <p class="font-semibold">Error loading movies</p>
      <p class="text-sm mt-1">{{ error }}</p>
      <button
        @click="fetchMovies"
        class="mt-2 bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700 text-sm"
      >
        Try Again
      </button>
    </div>

    <div v-else-if="movies.length === 0" class="text-center py-12 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z" />
      </svg>
      <p class="mt-4 text-gray-600 font-medium">No movies in your backlog yet</p>
      <p class="mt-1 text-gray-500 text-sm">Add your first movie using the form above!</p>
    </div>

    <div v-else class="grid grid-cols-1 gap-3">
      <MovieItem
        v-for="movie in sortedMovies"
        :key="movie.id"
        :movie="movie"
        @movie-updated="fetchMovies"
        @edit="editMovie"
      />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import MovieItem from './MovieItem.vue'

export default {
  components: { MovieItem },
  data() {
    return {
      movies: [],
      loading: false,
      error: null,
      onlyMine: false
    }
  },
  computed: {
    sortedMovies() {
      return [...this.movies].sort((a, b) => {
        // Sort by rating (highest first), then by title
        if (b.rating !== a.rating) {
          return (b.rating || 0) - (a.rating || 0)
        }
        return a.title.localeCompare(b.title)
      })
    }
  },
  mounted() {
    this.fetchMovies()
  },
  methods: {
    async fetchMovies() {
      this.loading = true
      this.error = null

      try {
        const params = {
          only_mine: this.onlyMine
        }
        const res = await axios.get('http://127.0.0.1:8000/api/movies/', { params })
        this.movies = res.data
      } catch (error) {
        console.error('Error fetching movies:', error)
        this.error = error.response?.data?.detail || 'Failed to load movies. Please check your connection.'
      } finally {
        this.loading = false
      }
    },

    editMovie(movie) {
      this.$emit('edit-movie', movie)
    }
  }
}
</script>
