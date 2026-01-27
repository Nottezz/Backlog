<template>
  <div>
    <input v-model="title" placeholder="Title" />
    <input v-model.number="rating" placeholder="Rating" type="number" step="0.1" />
    <button @click="addMovie">Add Movie</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return { title: '', rating: null };
  },
  methods: {
    async addMovie() {
      await axios.post('http://127.0.0.1:8000/movies/', {
        title: this.title,
        rating: this.rating
      });
      this.title = '';
      this.rating = null;
      this.$emit('movie-added');
    }
  }
}
</script>
