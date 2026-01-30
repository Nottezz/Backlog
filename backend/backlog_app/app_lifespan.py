from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.database import engine

from .taskiq_broker import broker


@asynccontextmanager
async def lifespan(
    app: FastAPI,  # noqa: ARG001
) -> AsyncIterator[None]:
    if not broker.is_worker_process:
        await broker.startup()
    yield
    await engine.dispose()
    if not broker.is_worker_process:
        await broker.shutdown()
