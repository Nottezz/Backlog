from backlog_app.config import settings

from .client import AIClient


class TranslationService:
    def __init__(self):
        self.client = AIClient(settings.ai_agent.model)

    async def translate(self, text: str) -> str:
        result = await self.client.translate(text)
        return result
