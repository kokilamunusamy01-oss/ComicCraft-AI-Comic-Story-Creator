from PIL import Image, ImageDraw

from huggingface_hub import InferenceClient

from app.config import (
    settings,
    PANELS_DIR
)


def create_placeholder(
    prompt,
    panel_number
):

    path = PANELS_DIR / (
        f"panel_{panel_number}.png"
    )

    image = Image.new(
        "RGB",
        (1024, 768),
        "white"
    )

    draw = ImageDraw.Draw(image)

    draw.rectangle(
        (10, 10, 1014, 758),
        outline="black",
        width=5
    )

    draw.text(
        (40, 40),
        f"ComicCraft - Panel {panel_number}",
        fill="black"
    )

    short_prompt = prompt[:250]

    draw.text(
        (40, 100),
        short_prompt,
        fill="black"
    )

    image.save(path)

    return (
        f"/static/panels/{path.name}"
    )


def generate_image(
    prompt,
    panel_number
):

    path = PANELS_DIR / (
        f"panel_{panel_number}.png"
    )

    if not settings.hf_token:

        if settings.allow_placeholder_images:

            return create_placeholder(
                prompt,
                panel_number
            )

        raise RuntimeError(
            "HF_TOKEN is missing. "
            "Add your Hugging Face token to .env."
        )

    client = InferenceClient(

        provider=settings.hf_provider,

        api_key=settings.hf_token
    )

    image = client.text_to_image(

        prompt,

        model=settings.hf_image_model
    )

    image.save(path)

    return (
        f"/static/panels/{path.name}"
    )