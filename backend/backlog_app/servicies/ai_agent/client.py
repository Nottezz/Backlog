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
                    "role": "user",
                    "content": (
                        "Translate the following text from English into Russian, "
                        "preserve the meaning and naturalness of the language:\n\n"
                        f"{text}"
                    ),
                }
            ],
            "temperature": 0.3,
        }

        response = await self.client.post(
            f"{settings.ai_agent.base_url}/api/v1/cloud-ai/agents/{settings.ai_agent.access_id}/v1/chat/completions",
            json=payload,
            headers={
                "Authorization": f"Bearer {settings.ai_agent.token}",
            },
        )

        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
