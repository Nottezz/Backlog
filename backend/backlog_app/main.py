import logging
from datetime import datetime

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backlog_app.api import router as api_router
from backlog_app.api.view.main_view import router as main_router
from backlog_app.app_lifespan import lifespan
from backlog_app.config import settings

logging.basicConfig(
    format=settings.logging.log_format,
    level=settings.logging.log_level,
    datefmt=settings.logging.log_date_format,
)
app = FastAPI(title="Backlog API", lifespan=lifespan)
app_launch_time = datetime.now()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(main_router)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
