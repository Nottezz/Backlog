__all__ = ("templates",)

from fastapi.templating import Jinja2Templates

from backlog_app.config import BASE_DIR

templates = Jinja2Templates(directory=BASE_DIR / "templates")
