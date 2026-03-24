# Локальная разработка Backlog

## Клонирование репозитория

```bash
git clone https://github.com/Nottezz/Backlog.git
cd backend
```
Установка зависимостей
```bash
uv install
```

## Настройка переменных окружения

Скопируйте шаблон и заполните значения:
```bash
cp .env.template .env
```
Пропишите параметры БД, секреты, настройки SMTP и т.д.

## Применение миграций
```bash
alembic upgrade head
```
## Запуск приложения
### Режим разработки
```bash
fastapi dev
```
### Фронтенд (если есть отдельная папка frontend)
```bash
cd frontend
npm install
npm run dev
```
# Запуск Docker контейнеров
```bash
docker compose up --build -d
```
# Брокер сообщений

## Локальный запуск:
```bash
taskiq worker backlog_app.taskiq_broker:broker --fs-discover -tp "**/tasks" --no-configure-logging
```
# Тестирование

## Запуск тестов:
```
uv run pytest
```
## С покрытием:
```
uv run pytest --cov=backlog_app
```
