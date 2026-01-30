from datetime import datetime

import uvicorn
from backend.backlog_app.app_lifespan import lifespan
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from api import router as api_router
from api.main_view import router as main_router

app = FastAPI(title="Backlog API", lifespan=lifespan)
app_launch_time = datetime.now()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue dev
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(main_router)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
