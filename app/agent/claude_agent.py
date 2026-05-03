import json
import logging

from anthropic import AsyncAnthropic

logger = logging.getLogger(__name__)


TOOLS_SPEC = [
    {
        "name": "create_post",
        "description": "Create a content draft",
        "input_schema": {
            "type": "object",
            "properties": {"topic": {"type": "string"}},
            "required": ["topic"],
        },
    },
    {
        "name": "edit_image",
        "description": "Edit image: crop/remove bg/add text",
        "input_schema": {
            "type": "object",
            "properties": {"input_path": {"type": "string"}, "overlay_text": {"type": "string"}},
            "required": ["input_path"],
        },
    },
    {
        "name": "generate_images",
        "description": "Generate images by prompt",
        "input_schema": {
            "type": "object",
            "properties": {"prompt": {"type": "string"}, "count": {"type": "integer"}},
            "required": ["prompt"],
        },
    },
    {
        "name": "add_subtitles_to_video",
        "description": "Add subtitles to video",
        "input_schema": {
            "type": "object",
            "properties": {"input_path": {"type": "string"}, "subtitle_text": {"type": "string"}},
            "required": ["input_path", "subtitle_text"],
        },
    },
    {
        "name": "schedule_reminder",
        "description": "Schedule reminder by cron",
        "input_schema": {
            "type": "object",
            "properties": {"cron_expr": {"type": "string"}, "description": {"type": "string"}},
            "required": ["cron_expr", "description"],
        },
    },
]


class ClaudeAgent:
    def __init__(self, api_key: str, tools, user_id: int):
        self.client = AsyncAnthropic(api_key=api_key)
        self.tools = tools
        self.user_id = user_id

    async def run(self, user_text: str) -> dict:
        logger.info("Sending request to Claude for internal_user_id=%s", self.user_id)
        response = await self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=800,
            system="Ты AI контент-менеджер. Вызывай tools для выполнения действий.",
            messages=[{"role": "user", "content": user_text}],
            tools=TOOLS_SPEC,
        )

        results = []
        for block in response.content:
            if block.type == "tool_use":
                tool_name = block.name
                args = block.input
                logger.info("Claude selected tool=%s with args=%s", tool_name, args)
                fn = getattr(self.tools, tool_name)
                if "user_id" in fn.__code__.co_varnames:
                    args["user_id"] = self.user_id
                tool_result = await fn(**args)
                logger.info("Tool execution finished: tool=%s result=%s", tool_name, tool_result)
                results.append({"tool": tool_name, "result": tool_result})

        logger.info("Claude flow finished with %s tool calls", len(results))
        return {
            "tools_called": results,
            "raw": json.dumps([r for r in results], ensure_ascii=False),
        }
