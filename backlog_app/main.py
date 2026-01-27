import uvicorn
from fastapi import FastAPI
from backlog_app.api import movie

app = FastAPI(title="Backlog API")

app.include_router(movie.router)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
