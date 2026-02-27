# Backlog Frontend

Vue 3 + TypeScript фронтенд для Backlog API.

## Стек

- **Vue 3** (Composition API + `<script setup>`)
- **Vite** — сборщик
- **Vue Router 4** — маршрутизация с guards
- **Pinia** — state management
- **Axios** — HTTP-клиент с интерцепторами
- **Tailwind CSS** — стилизация
- **TypeScript** — типизация

## Установка и запуск

```bash
# Установить зависимости
npm install

# Запустить dev-сервер
npm run dev

# Собрать для продакшена
npm run build
```

По умолчанию dev-сервер запустится на http://localhost:5173

API-прокси: все запросы `/api/*` проксируются на `http://localhost:8000`
Это можно изменить в `vite.config.ts`.

## Структура проекта

```
src/
├── api/
│   ├── axios.ts          # настройка axios, токен + 401-редирект
│   ├── auth.ts           # методы: login, register, verify, reset
│   └── movies.ts         # CRUD фильмов
├── stores/
│   ├── auth.ts           # пользователь, токен (localStorage), isAuthenticated
│   └── movies.ts         # список фильмов, CRUD-методы
├── router/
│   └── index.ts          # маршруты + guards (requiresAuth, guestOnly)
├── views/
│   ├── LandingView.vue   # лэндинг
│   ├── auth/
│   │   ├── LoginView.vue
│   │   ├── RegisterView.vue
│   │   ├── ForgotPasswordView.vue
│   │   ├── ResetPasswordView.vue
│   │   ├── EmailSentView.vue       # "письмо отправлено"
│   │   └── EmailVerifiedView.vue   # "email подтверждён" (авто-верификация по токену)
│   └── movies/
│       ├── MovieListView.vue
│       └── MovieDetailView.vue
└── components/
    ├── layout/
    │   ├── AppHeader.vue
    │   ├── AppFooter.vue
    │   └── AuthLayout.vue
    └── ui/
        ├── BaseInput.vue      # input с label, error, password-toggle
        ├── AlertMessage.vue   # info/success/error алерт
        ├── MovieCard.vue      # карточка фильма
        └── AddMovieModal.vue  # модал добавления/редактирования
```

## Маршруты

| Путь | Страница | Доступ |
|------|----------|--------|
| `/` | Лэндинг | публичный |
| `/login` | Вход | только гости |
| `/register` | Регистрация | только гости |
| `/forgot-password` | Восстановление пароля | только гости |
| `/reset-password?token=...` | Новый пароль | только гости |
| `/email-sent?email=...` | Письмо отправлено | только гости |
| `/email-verified?token=...` | Подтверждение email | публичный |
| `/movies` | Список фильмов | авторизованный |
| `/movies/:id` | Детальная страница | авторизованный |

## Обработка ошибок API

### Auth
- `LOGIN_BAD_CREDENTIALS` → «Неверный email или пароль»
- `LOGIN_USER_NOT_VERIFIED` → предупреждение + кнопка повторной отправки
- `REGISTER_USER_ALREADY_EXISTS` → ошибка поля email
- `REGISTER_INVALID_PASSWORD` → ошибка поля пароля
- `RESET_PASSWORD_BAD_TOKEN` → страница с сообщением об ошибке
- `VERIFY_USER_ALREADY_VERIFIED` → отдельное состояние

### Token
Токен хранится в `localStorage` под ключом `access_token`.
Axios автоматически добавляет его в заголовок `Authorization: Bearer`.
При 401-ответе токен очищается и пользователь редиректится на `/login`.

## Конфигурация API

Измените `target` в `vite.config.ts` если ваш бэкенд работает на другом адресе:

```ts
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000', // ← ваш бэкенд
      changeOrigin: true,
    },
  },
},
```
