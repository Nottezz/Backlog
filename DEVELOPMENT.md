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

## Production deployment and independent proxy Stack

`docker-compose.prod.yaml` runs the Backlog application services. A separately deployed proxy Stack
owns Nginx, Certbot, and host ports 80/443. Provision the external Docker network named `edge-proxy`
on the same Docker host before deploying Backlog, and attach the proxy to that network. Only Backlog's
`backend` and `frontend` join `edge-proxy`; all application services retain `app-network` for their
existing communication. The proxy reaches `backend:8000` and `frontend:80` through `edge-proxy`.
Keep virtual-host configuration, domains, IP addresses, and private access rules outside this public
repository. The proxy Stack is responsible for certificate renewal and reloading Nginx after renewal.

### Migrating an existing production deployment

Retain the existing `certbot-www` (ACME webroot) and `certbot-certs` (certificates and renewal state)
volumes for the proxy Stack. Removing their declarations from Backlog's Compose file does not migrate
their contents or establish ownership in another Stack. Do not delete these volumes, run a teardown
with volume removal, or prune them during migration, including while they are temporarily unused.

The old Compose file declares logical volume keys, so the actual existing names are normally
`<existing-compose-project>_certbot-www` and `<existing-compose-project>_certbot-certs`. Confirm the
actual names in the deployed environment; the Stack/project name or deployment tooling may change
the prefix. Configure the proxy Stack to use those exact existing volumes as external volumes,
mounting the webroot at `/var/www/certbot` and the certificate volume at `/etc/letsencrypt`.
Nginx can mount both read-only; Certbot needs write access.

Prepare the network, proxy configuration, and volume references before the cutover. Explicitly stop
and remove the old Backlog Nginx/Certbot containers while retaining their volumes; removing services
from Compose alone may leave those containers running as orphans. Release ports 80/443 before starting
the proxy Stack, and avoid running both Certbot instances against the same volumes. Coordinate this
cutover as a maintenance window: public access can be interrupted until the proxy is running and
Backlog's backend/frontend have joined `edge-proxy`. After deployment, confirm routing, TLS, ACME
challenge handling, and renewal/reload behavior through the independent proxy.

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
