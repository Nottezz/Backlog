__all__ = ("templates",)

from fastapi.templating import Jinja2Templates

from backlog_app.config import APP_DIR

templates = Jinja2Templates(directory=APP_DIR / "templates")
