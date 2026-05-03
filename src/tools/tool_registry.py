from typing import Any


def get_tool_definitions() -> list[dict[str, Any]]:
    return [
        {"name": "create_post", "description": "Create a draft post", "input_schema": {"type": "object", "properties": {"text": {"type": "string"}, "media_path": {"type": "string"}}}},
        {"name": "edit_image", "description": "Edit image: remove background/overlay text", "input_schema": {"type": "object", "properties": {"input_path": {"type": "string"}, "output_path": {"type": "string"}, "text": {"type": "string"}}}},
        {"name": "generate_images", "description": "Generate N images", "input_schema": {"type": "object", "properties": {"prompt": {"type": "string"}, "count": {"type": "integer"}}}},
        {"name": "add_subtitles_to_video", "description": "Add subtitles to video", "input_schema": {"type": "object", "properties": {"input_path": {"type": "string"}, "subtitles_srt": {"type": "string"}, "output_path": {"type": "string"}}}},
        {"name": "schedule_reminder", "description": "Schedule reminder/job using cron", "input_schema": {"type": "object", "properties": {"cron_expr": {"type": "string"}, "payload": {"type": "object"}}}},
        {"name": "publish_post", "description": "Publish a post by id", "input_schema": {"type": "object", "properties": {"post_id": {"type": "integer"}}}},
        {"name": "update_schedule", "description": "Update scheduled task", "input_schema": {"type": "object", "properties": {"task_id": {"type": "integer"}, "new_cron_expr": {"type": "string"}}}},
    ]
