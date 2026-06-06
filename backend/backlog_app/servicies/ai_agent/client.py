from openai import OpenAI

from backlog_app.config import settings


class AIClient:
    def __init__(self, model: str):
        self.model = model
        self.client = OpenAI(
            base_url=settings.ai_agent.base_url, api_key=settings.ai_agent.token
        )

    async def translate(self, text: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=2500,
            temperature=0.5,
            presence_penalty=0,
            top_p=0.95,
            messages=[
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
        )

        return response.choices[0].message.content
