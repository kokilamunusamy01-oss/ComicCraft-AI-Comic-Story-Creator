from pydantic import BaseModel, Field, field_validator


class PromptRequest(BaseModel):

    story_prompt: str = Field(
        min_length=3,
        max_length=2000
    )

    character_name: str = Field(
        min_length=1,
        max_length=80
    )

    setting: str = Field(
        min_length=1,
        max_length=120
    )

    tone: str = Field(
        min_length=1,
        max_length=50
    )

    art_style: str = Field(
        min_length=1,
        max_length=80
    )

    panels: int = Field(
        default=5,
        ge=3,
        le=8
    )

    @field_validator("*")
    @classmethod
    def strip_values(cls, value):

        if isinstance(value, str):
            return value.strip()

        return value


class Panel(BaseModel):

    panel_number: int

    title: str

    scene_description: str

    image_prompt: str

    caption: str = ""

    narration: str = ""

    dialogue: str = ""


class ComicResponse(BaseModel):

    title: str

    panels: list[Panel]

    pdf_url: str