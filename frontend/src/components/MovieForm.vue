<template>
  <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
    <h2 class="text-xl font-semibold mb-3 text-gray-700">
      {{ editingId ? 'Edit Movie' : 'Add New Movie' }}
    </h2>

    <div class="flex flex-col gap-3">
      <!-- Title (Required) -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Title <span class="text-red-500">*</span>
        </label>
        <input
            v-model="title"
            placeholder="Movie Title"
            class="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900 placeholder-gray-400"
            :class="{ 'border-red-500': errors.title }"
            @input="errors.title = ''"
        />
        <p v-if="errors.title" class="text-red-500 text-sm mt-1">{{ errors.title }}</p>
      </div>

      <!-- Description (Optional) -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Description <span class="text-gray-400 text-xs">(optional)</span>
        </label>
        <textarea
            v-model="description"
            placeholder="Movie description"
            rows="3"
            class="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none text-gray-900 placeholder-gray-400"
            :class="{ 'border-red-500': errors.description }"
            @input="errors.description = ''"
        ></textarea>
        <p v-if="errors.description" class="text-red-500 text-sm mt-1">{{ errors.description }}</p>
      </div>

      <!-- Year (Optional) -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Year <span class="text-gray-400 text-xs">(optional)</span>
        </label>
        <input
            v-model.number="year"
            placeholder="e.g. 2024"
            type="number"
            min="1888"
            :max="currentYear + 5"
            class="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900 placeholder-gray-400"
            :class="{ 'border-red-500': errors.year }"
            @input="errors.year = ''"
        />
        <p v-if="errors.year" class="text-red-500 text-sm mt-1">{{ errors.year }}</p>
      </div>

      <!-- Rating (Optional) -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Rating <span class="text-gray-400 text-xs">(optional, 1.0-10.0)</span>
        </label>
        <input
            v-model.number="rating"
            placeholder="e.g. 8.5"
            type="number"
            step="0.1"
            min="1.0"
            max="10.0"
            class="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900 placeholder-gray-400"
            :class="{ 'border-red-500': errors.rating }"
            @input="errors.rating = ''"
        />
        <p v-if="errors.rating" class="text-red-500 text-sm mt-1">{{ errors.rating }}</p>
      </div>

      <!-- Watch Link (Optional) -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Watch Link <span class="text-gray-400 text-xs">(optional)</span>
        </label>
        <input
            v-model="watch_link"
            placeholder="https://example.com/movie"
            type="url"
            class="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900 placeholder-gray-400"
            :class="{ 'border-red-500': errors.watch_link }"
            @input="errors.watch_link = ''"
        />
        <p v-if="errors.watch_link" class="text-red-500 text-sm mt-1">{{ errors.watch_link }}</p>
      </div>

      <!-- Kinopoisk ID (Optional) -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Kinopoisk ID <span class="text-gray-400 text-xs">(optional)</span>
        </label>
        <input
            v-model.number="kp_id"
            placeholder="e.g. 326"
            type="number"
            min="0"
            class="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900 placeholder-gray-400"
            :class="{ 'border-red-500': errors.kp_id }"
            @input="errors.kp_id = ''"
        />
        <p v-if="errors.kp_id" class="text-red-500 text-sm mt-1">{{ errors.kp_id }}</p>
      </div>

      <!-- IMDB ID (Optional) -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          IMDB ID <span class="text-gray-400 text-xs">(optional)</span>
        </label>
        <input
            v-model.number="imdb_id"
            placeholder="e.g. 326"
            type="number"
            min="0"
            class="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900 placeholder-gray-400"
            :class="{ 'border-red-500': errors.imdb_id }"
            @input="errors.imdb_id = ''"
        />
        <p v-if="errors.imdb_id" class="text-red-500 text-sm mt-1">{{ errors.imdb_id }}</p>
      </div>

      <!-- Watched (Optional) -->
      <div class="flex items-center gap-3 p-3 bg-white rounded border border-gray-300">
        <input
            v-model="watched"
            type="checkbox"
            id="watched-checkbox"
            class="w-5 h-5 text-indigo-600 border-gray-300 rounded focus:ring-2 focus:ring-indigo-500 cursor-pointer"
        />
        <label for="watched-checkbox" class="text-sm font-medium text-gray-700 cursor-pointer select-none">
          I've already watched this movie
        </label>
      </div>

      <!-- Publication Status -->
      <div class="bg-white p-3 rounded border border-gray-300">
        <div class="flex items-center justify-between mb-2">
          <div class="flex items-center gap-2">
            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span class="text-sm font-medium text-gray-700">Publication Status</span>
          </div>
          <span
              class="inline-flex items-center gap-1.5 px-2 py-1 rounded text-xs font-medium"
              :class="published
                ? 'bg-green-100 text-green-700'
                : 'bg-gray-100 text-gray-600'"
          >
            <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
              <circle v-if="published" cx="10" cy="10" r="3"></circle>
              <path v-else fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clip-rule="evenodd"></path>
            </svg>
            {{ published ? 'Public' : 'Private' }}
          </span>
        </div>

        <p class="text-xs text-gray-500 mb-3">
          <span v-if="published">👁️ This movie will be visible to everyone</span>
          <span v-else>🔒 This movie will be private and only visible to you</span>
        </p>

        <!-- Toggle Switch -->
        <label class="relative inline-flex items-center cursor-pointer">
          <input
              type="checkbox"
              v-model="published"
              class="sr-only peer"
          >
          <div
              class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-indigo-300 rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-500"></div>
          <span class="ms-2 text-sm text-gray-600">
            {{ published ? 'Published' : 'Unpublished' }}
          </span>
        </label>
      </div>

      <!-- Buttons -->
      <div class="flex gap-2 pt-2">
        <button
            v-if="!editingId"
            @click="addMovie"
            :disabled="loading"
            class="flex-1 bg-indigo-600 text-white px-4 py-3 rounded hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition font-medium"
        >
          {{ loading ? 'Adding...' : 'Add Movie' }}
        </button>

        <template v-else>
          <button
              @click="updateMovie"
              :disabled="loading"
              class="flex-1 bg-green-600 text-white px-4 py-3 rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition font-medium"
          >
            {{ loading ? 'Updating...' : 'Update Movie' }}
          </button>
          <button
              @click="clearForm"
              :disabled="loading"
              class="bg-gray-500 text-white px-4 py-3 rounded hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed transition font-medium"
          >
            Cancel
          </button>
        </template>
      </div>
    </div>

    <p v-if="successMessage" class="mt-3 text-green-600 text-sm font-medium">{{ successMessage }}</p>
    <p v-if="errorMessage" class="mt-3 text-red-600 text-sm font-medium">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      title: '',
      description: '',
      year: null,
      rating: null,
      watch_link: '',
      kp_id: null,
      imdb_id: null,
      watched: false,
      published: false,
      editingId: null,
      loading: false,
      errors: {
        title: '',
        description: '',
        year: '',
        rating: '',
        kp_id: '',
        imdb_id: ''
      },
      successMessage: '',
      errorMessage: ''
    }
  },
  computed: {
    currentYear() {
      return new Date().getFullYear()
    }
  },
  methods: {
    validate() {
      this.errors = {
        title: '',
        description: '',
        year: '',
        rating: '',
        watch_link: '',
        kp_id: '',
        imdb_id: '',
      }
      let isValid = true

      // Title is required
      if (!this.title || this.title.trim() === '') {
        this.errors.title = 'Title is required'
        isValid = false
      }

      // Year validation (optional, but if provided must be valid)
      if (this.year !== null && this.year !== '') {
        if (this.year < 1888) {
          this.errors.year = 'Year must be 1888 or later (first movie ever made)'
          isValid = false
        }
        if (this.year > this.currentYear + 5) {
          this.errors.year = `Year must be ${this.currentYear + 5} or earlier`
          isValid = false
        }
      }

      // Rating validation (optional, but if provided must be 1-10)
      if (this.rating !== null && this.rating !== '') {
        if (this.rating < 1 || this.rating > 10) {
          this.errors.rating = 'Rating must be between 1 and 10'
          isValid = false
        }
      }

      // URL validation (optional, but if provided must be valid)
      if (this.watch_link && this.watch_link.trim() !== '') {
        try {
          new URL(this.watch_link)
        } catch (e) {
          this.errors.watch_link = 'Please enter a valid URL (e.g., https://example.com)'
          isValid = false
        }
      }

      // KP ID validation (optional, but if provided must be positive)
      if (this.kp_id !== null && this.kp_id !== '' && this.kp_id < 0) {
        this.errors.kp_id = 'Kinopoisk ID must be a positive number'
        isValid = false
      }

      // IMDB ID validation (optional, but if provided must be positive)
      if (this.imdb_id !== null && this.imdb_id !== '' && this.imdb_id < 0) {
        this.errors.imdb_id = 'IMDB ID must be a positive number'
        isValid = false
      }

      return isValid
    },

    async addMovie() {
      if (!this.validate()) return

      this.loading = true
      this.errorMessage = ''
      this.successMessage = ''

      try {
        const payload = {
          title: this.title.trim(),
          description: this.description.trim() || null,
          year: this.year || null,
          rating: this.rating || null,
          watch_link: this.watch_link.trim() || null,
          kp_id: this.kp_id || null,
          imdb_id: this.imdb_id || null,
          watched: this.watched,
          published: this.published
        }

        await axios.post('/api/movies/', payload)
        this.successMessage = 'Movie added successfully!'
        this.clearForm()
        this.$emit('movie-updated')

        setTimeout(() => {
          this.successMessage = ''
        }, 3000)
      } catch (error) {
        console.error('Error adding movie:', error)
        this.errorMessage = error.response?.data?.detail || 'Failed to add movie'
      } finally {
        this.loading = false
      }
    },

    async updateMovie() {
      if (!this.validate()) return
      if (!this.editingId) return

      this.loading = true
      this.errorMessage = ''
      this.successMessage = ''

      try {
        const payload = {
          title: this.title.trim(),
          description: this.description.trim() || null,
          year: this.year || null,
          rating: this.rating || null,
          watch_link: this.watch_link.trim() || null,
          kp_id: this.kp_id || null,
          imdb_id: this.imdb_id || null,
          watched: this.watched,
          published: this.published
        }

        await axios.put(`/api/movies/${this.editingId}`, payload)
        this.successMessage = 'Movie updated successfully!'
        this.clearForm()
        this.$emit('movie-updated')

        setTimeout(() => {
          this.successMessage = ''
        }, 3000)
      } catch (error) {
        console.error('Error updating movie:', error)
        this.errorMessage = error.response?.data?.detail || 'Failed to update movie'
      } finally {
        this.loading = false
      }
    },

    clearForm() {
      this.title = ''
      this.description = ''
      this.year = null
      this.rating = null
      this.watch_link = ''
      this.kp_id = null
      this.imdb_id = null
      this.watched = false
      this.published = false
      this.editingId = null
      this.errors = {
        title: '',
        description: '',
        year: '',
        rating: '',
        watch_link: '',
        kp_id: '',
        imdb_id: ''
      }
      this.errorMessage = ''
    },

    editMovie(movie) {
      this.title = movie.title || ''
      this.description = movie.description || ''
      this.year = movie.year || null
      this.rating = movie.rating || null
      this.watch_link = movie.watch_link || ''
      this.kp_id = movie.kp_id || null
      this.imdb_id = movie.imdb_id || null
      this.watched = movie.watched || false
      this.published = movie.published || false
      this.editingId = movie.id
      this.errorMessage = ''
      this.successMessage = ''
    }
  }
}
</script>
