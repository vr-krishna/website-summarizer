from openai import AsyncOpenAI

from app.core.config import settings
from app.core.exceptions import SummarizationError
from app.core.prompts import (
    system_prompt,
    user_prompt_prefix,
)


class OpenAIService:
    """Service for generating summaries using the OpenAI API."""

    def __init__(
        self,
        client: AsyncOpenAI | None = None,
    ) -> None:
        self.client = client or AsyncOpenAI(
            api_key=settings.openai_api_key,
        )

    async def summarize(self, webpage: str) -> str:
        """Generate a summary for the given webpage content."""

        try:
            response = await self.client.chat.completions.create(
                model=settings.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": f"{user_prompt_prefix}{webpage}",
                    },
                ],
            )

            content = response.choices[0].message.content

            if not content:
                raise SummarizationError(
                    "OpenAI returned an empty response."
                )

            return content

        except SummarizationError:
            raise

        except Exception as exc:
            raise SummarizationError(
                "Failed to generate the summary."
            ) from exc