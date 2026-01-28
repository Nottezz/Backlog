import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from alembic import context

# Импорт настроек из FastAPI
from config import settings
from models.base import Base

# Этот объект конфигурации Alembic
config = context.config

# Настройка логирования через alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаинформация для autogenerate
target_metadata = Base.metadata

# Функция для синхронного режима (можно оставить для sync)
def run_migrations_offline():
    url = settings.db.connection.database_url_asyncpg
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# Основная функция для async миграций
async def run_migrations_online():
    connectable = create_async_engine(
        settings.db.connection.database_url_asyncpg,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def do_run_migrations(connection: AsyncConnection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()

# Запуск миграций
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
