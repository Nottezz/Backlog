<template>
  <div class="flex justify-between items-center p-4 border-b border-gray-200 hover:bg-gray-50 rounded">
    <div>
      <h3 class="font-semibold text-lg">{{ movie.title }} ({{ movie.release_year }})</h3>
      <p class="text-gray-600">Rating: {{ movie.rating }}</p>
    </div>
    <div class="flex gap-2">
      <button @click="$emit('edit', movie)"
              class="bg-yellow-400 text-white px-3 py-1 rounded hover:bg-yellow-500">
        Edit
      </button>
      <button @click="deleteMovie"
              class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600">
        Delete
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  props: ['movie'],
  methods: {
    async deleteMovie() {
      await axios.delete(`http://127.0.0.1:8000/movies/${this.movie.id}`)
      this.$emit('movie-updated')
    }
  }
}
</script>
