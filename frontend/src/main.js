import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import authService from './services/auth'
import './style.css'

// Настроить axios interceptor для автоматической авторизации
authService.setupAxiosInterceptor()

const app = createApp(App)

app.use(router)

app.mount('#app')
