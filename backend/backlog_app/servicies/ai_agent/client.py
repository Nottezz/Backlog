import httpx

from backlog_app.config import settings


class AIClient:
    def __init__(self, model: str):
        self.model = model
        self.client = httpx.AsyncClient(timeout=settings.ai_agent.timeout)

    async def translate(self, text: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a translation engine. "
                        "Return ONLY the translated text in Russian. "
                        "Do NOT add explanations, comments, notes, or formatting. "
                        "Output must contain only the translation."
                    ),
                },
                {
                    "role": "user",
                    "content": f"{text}",
                },
            ],
            "temperature": 0.0,
        }

        response = await self.client.post(
            f"{settings.ai_agent.base_url}/api/v1/cloud-ai/agents/{settings.ai_agent.access_id}/v1/chat/completions",
            json=payload,
            headers={
                "Authorization": f"Bearer {settings.ai_agent.token}",
            },
        )

        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
