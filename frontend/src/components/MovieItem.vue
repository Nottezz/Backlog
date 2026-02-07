<template>
  <div class="flex flex-col p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
    <div class="flex items-start justify-between gap-4 mb-3">
      <div class="flex-1 min-w-0">
        <!-- Title and Watched Badge -->
        <div class="flex items-center gap-2 mb-1">
          <h3 class="text-lg font-semibold text-gray-800">{{ movie.title }}</h3>
          <span v-if="movie.watched" class="px-2 py-0.5 bg-green-100 text-green-700 text-xs font-medium rounded-full">
            ✓ Watched
          </span>
        </div>

        <!-- Year -->
        <div v-if="movie.year" class="text-sm text-gray-600 mb-2">
          📅 {{ movie.year }}
        </div>

        <!-- Description -->
        <p v-if="movie.description" class="text-sm text-gray-600 mb-3 line-clamp-2">
          {{ movie.description }}
        </p>

        <!-- Metadata row -->
        <div class="flex flex-wrap gap-3 text-sm">

          <!-- User -->
          <div v-if="movie.user" class="flex items-center gap-1 text-gray-500">
            <span>👤</span>
            <span class="font-medium">{{ movie.user }}</span>
          </div>

          <!-- Rating -->
          <div v-if="movie.rating" class="flex items-center gap-1">
            <span class="text-yellow-500 font-medium">
              {{ movie.rating.toFixed(1) }} ★
            </span>
          </div>

          <!-- Kinopoisk ID -->
          <div v-if="movie.kp_id" class="flex items-center gap-1 text-gray-500">
            <span>🎬 KP:</span>
            <a
                :href="`https://www.kinopoisk.ru/film/${movie.kp_id}/`"
                target="_blank"
                class="text-indigo-600 hover:text-indigo-800 underline"
            >
              {{ movie.kp_id }}
            </a>
          </div>

          <!-- IMDB ID -->
          <div v-if="movie.imdb_id" class="flex items-center gap-1 text-gray-500">
            <span>IMDB:</span>
            <a
                :href="`https://www.imdb.com/title/tt${movie.imdb_id}/`"
                target="_blank"
                class="text-indigo-600 hover:text-indigo-800 underline"
            >
              {{ movie.imdb_id }}
            </a>
          </div>

          <!--  Watch Link -->
          <div v-if="movie.watch_link" class="flex items-center gap-1 text-gray-500">
            <span>🔗</span>
            <a
                :href="movie.watch_link"
                target="_blank"
                class="text-indigo-600 hover:text-indigo-800 underline truncate max-w-[200px]"
            >
              Watch link
            </a>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-2 flex-shrink-0">
        <button
            @click="$emit('edit', movie)"
            class="bg-blue-500 text-white px-3 py-1.5 rounded hover:bg-blue-600 transition text-sm font-medium"
        >
          Edit
        </button>
        <button
            @click="deleteMovie"
            class="bg-red-500 text-white px-3 py-1.5 rounded hover:bg-red-600 transition text-sm font-medium"
        >
          Delete
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  props: {
    movie: {
      type: Object,
      required: true
    }
  },
  methods: {
    async deleteMovie() {
      if (!confirm(`Delete "${this.movie.title}"?`)) return
      try {
        await axios.delete(`/api/movies/${this.movie.id}`)
        this.$emit('movie-updated')
      } catch (error) {
        console.error('Error deleting movie:', error)
        alert('Failed to delete movie')
      }
    }
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
