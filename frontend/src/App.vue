<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <div class="max-w-3xl mx-auto bg-white shadow-md rounded-lg p-6">
      <h1 class="text-3xl font-bold mb-4 text-center text-indigo-600">Backlog Movies</h1>

      <!-- MovieForm с ref, чтобы можно было вызывать editMovie -->
      <MovieForm ref="movieForm" @movie-updated="refreshMovies" class="mb-6" />

      <MovieList ref="movieList" @movie-updated="refreshMovies" />
    </div>
  </div>
</template>

<script>
import MovieForm from './components/MovieForm.vue'
import MovieList from './components/MovieList.vue'

export default {
  components: { MovieForm, MovieList },
  methods: {
    refreshMovies() {
      this.$refs.movieList.fetchMovies()
    }
  },
  mounted() {
    // Подписка на глобальное событие "edit-movie"
    this.$root.$on('edit-movie', movie => {
      // Вызываем метод editMovie у MovieForm через ref
      this.$refs.movieForm.editMovie(movie)
    })
  }
}
</script>
