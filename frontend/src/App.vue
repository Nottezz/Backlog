<template>
  <div>
    <h1>Backlog Movies</h1>
    <MovieForm @movie-added="refreshMovies" />
    <MovieList ref="movieList" />
  </div>
</template>

<script>
import MovieList from './components/MovieList.vue';
import MovieForm from './components/MovieForm.vue';

export default {
  components: { MovieList, MovieForm },
  methods: {
    refreshMovies() {
      this.$refs.movieList.fetchMovies();
    }
  }
}
</script>
