import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior: () => ({ top: 0 }),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: () => import('@/views/LandingView.vue'),
      meta: { guestOnly: false, requiresAuth: false },
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/auth/LoginView.vue'),
      meta: { guestOnly: true },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/auth/RegisterView.vue'),
      meta: { guestOnly: true },
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: () => import('@/views/auth/ForgotPasswordView.vue'),
      meta: { guestOnly: true },
    },
    {
      path: '/reset-password',
      name: 'reset-password',
      component: () => import('@/views/auth/ResetPasswordView.vue'),
      meta: { guestOnly: true },
    },
    {
      path: '/email-sent',
      name: 'email-sent',
      component: () => import('@/views/auth/EmailSentView.vue'),
      meta: { guestOnly: true },
    },
    {
      path: '/email-verified',
      name: 'email-verified',
      component: () => import('@/views/auth/EmailVerifiedView.vue'),
    },
    {
      path: '/movies',
      name: 'movies',
      component: () => import('@/components/ui/MovieListView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/movies/:id',
      name: 'movie-detail',
      component: () => import('@/views/movies/MovieDetailView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      redirect: '/',
    },
  ],
})

router.beforeEach((to) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.token) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.meta.guestOnly && authStore.token) {
    return { name: 'movies' }
  }
})

export default router
