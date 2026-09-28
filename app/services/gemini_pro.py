import json

from google import genai

from app.config import settings


def get_client():
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is missing.")

    return genai.Client(api_key=settings.gemini_api_key)


def generate_story(req, outline):
    client = get_client()

    prompt = f"""
Create a simple comic story with exactly {len(outline)} panels.

Character: {req.character_name}
Setting: {req.setting}
Tone: {req.tone}
Art style: {req.art_style}

Outline:
{json.dumps(outline, ensure_ascii=False)}

Return JSON array only.

Each panel must contain:
panel_number
title
scene_description
image_prompt
caption
narration
dialogue
"""

    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "panel_number": {"type": "integer"},
                "title": {"type": "string"},
                "scene_description": {"type": "string"},
                "image_prompt": {"type": "string"},
                "caption": {"type": "string"},
                "narration": {"type": "string"},
                "dialogue": {"type": "string"},
            },
            "required": [
                "panel_number",
                "title",
                "scene_description",
                "image_prompt",
                "caption",
                "narration",
                "dialogue",
            ],
        },
    }

    response = client.interactions.create(
        model=settings.gemini_flash_model,
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": schema,
        },
    )

    data = json.loads(response.output_text)

    if not isinstance(data, list):
        raise RuntimeError("Gemini returned an invalid story.")

    if len(data) != len(outline):
        raise RuntimeError("Gemini returned an incorrect number of panels.")

    return data