from openai import AsyncOpenAI

from app.core.config import settings
from app.core.exceptions import SummarizationError
from app.core.prompts import (
    system_prompt,
    user_prompt_prefix,
)

client = AsyncOpenAI(
    api_key=settings.openai_api_key,
)


class OpenAIService:
    async def summarize(self, webpage: str) -> str:
        try:
            response = await client.chat.completions.create(
                model=settings.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt_prefix + webpage,
                    },
                ],
            )

            return response.choices[0].message.content

        except Exception as exc:
            raise SummarizationError(str(exc)) from exc