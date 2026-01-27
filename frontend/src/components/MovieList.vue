<template>
  <div class="space-y-2">
    <MovieItem
      v-for="movie in movies"
      :key="movie.id"
      :movie="movie"
      @movie-updated="fetchMovies"
      @edit="editMovie"
    />
  </div>
</template>

<script>
import axios from 'axios'
import MovieItem from './MovieItem.vue'
import MovieForm from './MovieForm.vue'

export default {
  components: { MovieItem },
  data() {
    return {
      movies: []
    }
  },
  mounted() {
    this.fetchMovies()
  },
  methods: {
    async fetchMovies() {
      const res = await axios.get('http://127.0.0.1:8000/movies/')
      this.movies = res.data
    },
    editMovie(movie) {
      // Передаём событие наверх, чтобы MovieForm открыл режим редактирования
      this.$emit('movie-updated')
      this.$root.$emit('edit-movie', movie)
    }
  }
}
</script>
