<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-50 to-blue-50">
    <!-- Navigation Bar -->
    <nav class="bg-white shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo -->
          <div class="flex items-center">
            <h1 class="text-2xl font-bold text-indigo-600">🎬 Backlog Movies</h1>
          </div>

          <!-- User Menu -->
          <div class="flex items-center gap-4">
            <span class="text-gray-700 text-sm">{{ userEmail }}</span>
            <button
              @click="handleLogout"
              class="bg-red-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-red-700 transition-colors text-sm"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="w-full max-w-[95vw] sm:max-w-[90vw] lg:max-w-[1400px] xl:max-w-[1600px] 2xl:max-w-[1800px] mx-auto px-3 sm:px-4 md:px-6 lg:px-8 py-3 sm:py-4 md:py-6 lg:py-8">
      <!-- Header -->
      <header class="text-center mb-6 md:mb-8">
        <p class="text-sm sm:text-base md:text-lg text-gray-600">
          Keep track of movies you want to watch
        </p>
      </header>

      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 md:gap-6">
        <!-- Movie Form - Left Side on large screens, full width on mobile -->
        <div class="lg:col-span-4 xl:col-span-3">
          <div class="bg-white shadow-xl rounded-xl p-4 sm:p-5 md:p-6 lg:sticky lg:top-6">
            <MovieForm ref="movieForm" @movie-updated="refreshMovies" />
          </div>
        </div>

        <!-- Movie List - Right Side on large screens, full width on mobile -->
        <div class="lg:col-span-8 xl:col-span-9">
          <div class="bg-white shadow-xl rounded-xl p-4 sm:p-5 md:p-6 lg:p-8">
            <MovieList
              ref="movieList"
              @movie-updated="refreshMovies"
              @edit-movie="handleEdit"
            />
          </div>
        </div>
      </div>

      <!-- Footer -->
      <footer class="text-center mt-6 md:mt-8 text-gray-500 text-xs sm:text-sm">
        <p>Built with Vue 3 + Vite</p>
      </footer>
    </div>
  </div>
</template>

<script>
import MovieForm from '../components/MovieForm.vue'
import MovieList from '../components/MovieList.vue'
import authService from '../services/auth'

export default {
  name: 'HomeView',
  components: { MovieForm, MovieList },
  data() {
    return {
      userEmail: '',
    }
  },
  mounted() {
    const user = authService.getUser()
    this.userEmail = user?.email || 'User'
  },
  methods: {
    refreshMovies() {
      this.$refs.movieList.fetchMovies()
    },
    handleEdit(movie) {
      this.$refs.movieForm.editMovie(movie)
      // Scroll to form when editing on mobile
      if (window.innerWidth < 1024) {
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    },
    async handleLogout() {
      try {
        await authService.logout()
        this.$router.push('/login')
      } catch (error) {
        console.error('Logout error:', error)
      }
    },
  },
}
</script>
