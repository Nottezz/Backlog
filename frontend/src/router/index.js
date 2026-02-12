import { createRouter, createWebHistory } from 'vue-router'
import authService from '../services/auth'

import HomeView from '../components/Home.vue'
import LoginView from '../components/Login.vue'
import RegisterView from '../components/Register.vue'
import ForgotPasswordView from '../components/ForgotPassword.vue'
import ResetPasswordView from '../components/ResetPassword.vue'

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
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: ForgotPasswordView,
    meta: { guest: true },
  },
  {
    path: '/reset-password',
    name: 'ResetPassword',
    component: ResetPasswordView,
    meta: { guest: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = authService.isAuthenticated()

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
    return
  }

  if (to.meta.guest && isAuthenticated) {
    next('/')
    return
  }

  next()
})

export default router
