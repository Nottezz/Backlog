<template>
  <div class="group bg-linear-to-br from-white to-gray-50 rounded-xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-100 hover:border-indigo-200 h-full flex flex-col">
    <!-- Movie Header -->
    <div class="p-5 flex-1 flex flex-col">
      <!-- Title and Year -->
      <div class="mb-3">
        <div class="flex items-start justify-between gap-2 mb-1">
          <h3 class="text-xl font-bold text-gray-800 line-clamp-2 group-hover:text-indigo-600 transition-colors flex-1">
            {{ movie.title }}
          </h3>
          <span v-if="movie.watched" class="shrink-0 px-2 py-1 bg-green-100 text-green-700 text-xs font-medium rounded-full">
            ✓ Watched
          </span>
        </div>
        <p v-if="movie.year" class="text-sm text-gray-500">
          📅 {{ movie.year }}
        </p>
      </div>

      <!-- Rating Badge -->
      <div class="flex items-center gap-2 mb-3">
        <div v-if="movie.rating" class="flex items-center bg-linear-to-r from-yellow-400 to-yellow-500 text-white px-3 py-1.5 rounded-full shadow-sm">
          <span class="font-bold text-lg mr-1">{{ movie.rating.toFixed(1) }}</span>
          <span class="text-sm">★</span>
        </div>
        <span v-else class="text-sm text-gray-400 italic">No rating</span>
      </div>

      <!-- Description -->
      <p v-if="movie.description" class="text-sm text-gray-600 mb-3 line-clamp-3 flex-1">
        {{ movie.description }}
      </p>

      <!-- Movie Icon/Placeholder -->
      <div class="w-full aspect-video bg-linear-to-br from-indigo-50 to-purple-50 rounded-lg flex items-center justify-center mb-3">
        <span class="text-6xl opacity-40">🎬</span>
      </div>

      <!-- Links -->
      <div class="flex gap-2 text-xs">
        <a
          v-if="movie.kp_id"
          :href="`https://www.kinopoisk.ru/film/${movie.kp_id}/`"
          target="_blank"
          class="flex items-center gap-1 text-indigo-600 hover:text-indigo-800 underline"
        >
          🎬 Kinopoisk
        </a>
        <a
          v-if="movie.original_link"
          :href="movie.original_link"
          target="_blank"
          class="flex items-center gap-1 text-indigo-600 hover:text-indigo-800 underline"
        >
          🔗 Link
        </a>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="p-4 bg-gray-50 border-t border-gray-100 flex gap-2">
      <button
        @click="$emit('edit', movie)"
        class="flex-1 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2.5 rounded-lg transition font-medium text-sm flex items-center justify-center gap-2 shadow-sm hover:shadow-md"
      >
        <span>✏️</span>
        Edit
      </button>
      <button
        @click="deleteMovie"
        class="flex-1 bg-red-500 hover:bg-red-600 text-white px-4 py-2.5 rounded-lg transition font-medium text-sm flex items-center justify-center gap-2 shadow-sm hover:shadow-md"
      >
        <span>🗑️</span>
        Delete
      </button>
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
        await axios.delete(`http://127.0.0.1:8000/movies/${this.movie.id}`)
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

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
