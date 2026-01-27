<template>
  <div>
    <h3>{{ movie.title }} ({{ movie.release_year }})</h3>
    <p>Rating: {{ movie.rating }}</p>
    <button @click="deleteMovie">Delete</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: ['movie'],
  methods: {
    async deleteMovie() {
      await axios.delete(`http://127.0.0.1:8000/movies/${this.movie.id}`);
      this.$emit('deleted');
    }
  }
}
</script>
