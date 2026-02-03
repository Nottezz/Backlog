from datetime import datetime

from fastapi import APIRouter, Request

router = APIRouter()
app_launch_time = datetime.now()


@router.get("/", include_in_schema=False)
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
