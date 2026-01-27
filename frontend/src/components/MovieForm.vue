<template>
  <div class="flex gap-2 mb-4">
    <input v-model="title" placeholder="Title"
           class="flex-1 p-2 border border-gray-300 rounded" />
    <input v-model.number="rating" placeholder="Rating" type="number" step="0.1"
           class="w-24 p-2 border border-gray-300 rounded" />
    <button @click="addMovie"
            class="bg-indigo-600 text-white px-4 rounded hover:bg-indigo-700">
      Add
    </button>
    <button v-if="editingId" @click="updateMovie"
            class="bg-green-600 text-white px-4 rounded hover:bg-green-700">
      Update
    </button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      title: '',
      rating: null,
      editingId: null
    }
  },
  methods: {
    async addMovie() {
      if (!this.title) return
      await axios.post('http://127.0.0.1:8000/movies/', {
        title: this.title,
        rating: this.rating
      })
      this.clearForm()
      this.$emit('movie-updated')
    },
    async updateMovie() {
      if (!this.editingId) return
      await axios.patch(`http://127.0.0.1:8000/movies/${this.editingId}`, {
        title: this.title,
        rating: this.rating
      })
      this.clearForm()
      this.$emit('movie-updated')
    },
    clearForm() {
      this.title = ''
      this.rating = null
      this.editingId = null
    },
    editMovie(movie) {
      this.title = movie.title
      this.rating = movie.rating
      this.editingId = movie.id
    }
  }
}
</script>
