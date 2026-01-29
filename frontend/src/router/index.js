import { createRouter, createWebHistory } from 'vue-router'
import authService from '../services/auth'

import HomeView from '../components/Home.vue'
import LoginView from '../components/Login.vue'
import RegisterView from '../components/Register.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
    meta: { requiresAuth: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { guest: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
    meta: { guest: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const isAuthenticated = authService.isAuthenticated()

  // Если маршрут требует авторизации
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
    return
  }

  // Если пользователь авторизован и пытается зайти на login/register
  if (to.meta.guest && isAuthenticated) {
    next('/')
    return
  }

  next()
})

export default router
