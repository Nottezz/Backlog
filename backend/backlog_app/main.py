from datetime import datetime

import uvicorn
from api import router as api_router
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.backlog_app.app_lifespan import lifespan

app = FastAPI(title="Backlog API", lifespan=lifespan)
app_launch_time = datetime.now()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue dev
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def root(request: Request):
    uptime = (datetime.now() - app_launch_time).total_seconds()
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {
        "status": "OK",
        "current_time": datetime.now().isoformat(sep=" "),
        "app_launch_time": int(uptime),
        "docs_url": str(docs_url),
    }


app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
