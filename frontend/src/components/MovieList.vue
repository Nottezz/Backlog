<template>
  <div>
    <h2>Movies</h2>
    <MovieItem
      v-for="movie in movies"
      :key="movie.id"
      :movie="movie"
      @deleted="fetchMovies"
    />
  </div>
</template>

<script>
import axios from 'axios';
import MovieItem from './MovieItem.vue';

export default {
  components: { MovieItem },
  data() {
    return { movies: [] };
  },
  mounted() {
    this.fetchMovies();
  },
  methods: {
    async fetchMovies() {
      const res = await axios.get('http://127.0.0.1:8000/movies/');
      this.movies = res.data;
    }
  }
}
</script>
