# Backlog

Backlog — сервис «списка хотелок» (backlog) для фильмов и сериалов. Позволяет сохранять фильмы и сериалы, добавлять
ссылку на источник просмотра, быстро выбирать, что смотреть прямо сейчас.

## Заметка от автора

> Идея создать такой сервис пришла тогда, когда накопившиеся хотелки на просмотр стали забываться в голове, слишком
> много мест где можно посмотреть тот или иной фильм/сериал, сидишь и мучаешься в попытках вспомнить.
> Добавляя ссылку на просмотр можно легко и быстро выбрать то, что подходит по настроению и перейти к просмотру. Если
> ссылка стала недоступна, то можно быстро найти по названию фильм и отредактировать.

## Технологии

### Backend

- Python 3.13+
- FastAPI
- SQLAlchemy
- Alembic (миграции)
- PostgreSQL
- taskiq (фоновые задачи)
- RabbitMQ
- Jinja2

### Frontend

- Vite + Vue
- NPM

Контейнеризация: Docker (+ docker-compose)

## Локальная развёртка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/Nottezz/Backlog.git
cd backend
```

2. Установите зависимости через uv:

```bash
uv install
```

3. Настройте переменные окружения:

- Скопируйте шаблон и заполните значения:

```bash
cp .env.template .env
```

- Пропишите параметры БД, секреты, настройки SMTP и т.д.

4. Примените миграции:

```bash
alembic upgrade head
```

5. Запустите приложение в режиме разработки:

```bash
fastapi dev
```

6. Запустите фронтенд (если есть отдельная папка frontend):

```bash
cd frontend
npm install
npm run dev
```

## Запуск Docker контейнеров

```bash
docker compose up --build -d
```

## API (общая информация)

- Базовый путь: `/`
- Документация OpenAPI:
    - Swagger UI: `/docs`
    - ReDoc: `/redoc`

Примеры endpoint-ов:

- GET /api/movies — получить список фильмов
- POST /api/movies — добавить фильм
- GET /api/movies/{id} — получить фильм по id
- PUT /api/movies/{id} — обновить фильм
- DELETE /api/movies/{id} — удалить фильм

Пример создания фильма (curl):

```bash
curl -X POST "http://localhost:8000/api/movies" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "title": "Inception",
    "rating": 8.7,
    "imdb_id": 1375666
  }'
```

## Авторизация

- Защищённые эндпоинты требуют заголовок:
  `Authorization: Bearer <access_token>`

## Брокер сообщений

- Локальный запуск:

```bash
taskiq worker backlog_app.taskiq_broker:broker --fs-discover -tp "**/tasks" --no-configure-logging
```

## Тестирование

- Запуск тестов:

```bash
uv run pytest
```

- Запуск тестов с покрытием:

```bash
uv run pytest --cov=backlog_app
```

## Вклад

1. Форкни репозиторий
2. Создай ветку: `feature/my-feature`
3. Сделай изменения и добавь тесты
4. Открой Pull Request: опиши цель изменений и план тестирования
