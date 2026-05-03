import json
from anthropic import AsyncAnthropic
from src.tools.tool_registry import get_tool_definitions


SYSTEM_PROMPT = """
Ты AI-контент менеджер. Анализируй намерение пользователя и вызывай tools.
Всегда сначала готовь контент и отправляй на preview перед публикацией.
"""


class ClaudeAgent:
    def __init__(self, api_key: str, model: str):
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = model

    async def plan(self, user_text: str) -> list[dict]:
        resp = await self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=get_tool_definitions(),
            messages=[{"role": "user", "content": user_text}],
        )

        actions = []
        for block in resp.content:
            if block.type == "tool_use":
                actions.append({"tool": block.name, "input": block.input})

        if not actions:
            actions = [{"tool": "create_post", "input": {"text": "Черновик: " + user_text}}]
        return actions
