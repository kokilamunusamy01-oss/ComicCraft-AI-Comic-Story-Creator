from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.schemas import PromptRequest
from app.config import TEMPLATES_DIR

from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout
from app.services.exporters import save_pdf


router = APIRouter()

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)


def run_pipeline(req):
    outline = generate_outline(req)

    story = generate_story(
        req,
        outline
    )

    image_paths = []

    for panel in story:
        image_path = generate_image(
            panel["image_prompt"],
            panel["panel_number"]
        )

        image_paths.append(image_path)

    layout = build_comic_layout(
        story,
        image_paths
    )

    title = (
        f"{req.character_name}'s "
        f"Comic Adventure"
    )

    pdf_url = save_pdf(
        title,
        layout
    )

    return title, layout, pdf_url


# HOME PAGE
@router.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# REAL AI GENERATION
@router.post(
    "/generate",
    response_class=HTMLResponse
)
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
    panels: int = Form(5)
):

    try:

        request_data = PromptRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
            panels=panels
        )

        title, layout, pdf_url = run_pipeline(
            request_data
        )

        return templates.TemplateResponse(
            request=request,
            name="export_success.html",
            context={
                "title": title,
                "pdf_url": pdf_url
            }
        )

    except Exception as error:

        with open(
            "error_log.txt",
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                repr(error) + "\n"
            )

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": str(error)
            },
            status_code=500
        )


# JSON GENERATION
@router.post(
    "/generate-comic/json"
)
async def generate_json(
    request_data: PromptRequest
):

    try:

        title, layout, pdf_url = run_pipeline(
            request_data
        )

        return {
            "title": title,
            "panels": layout,
            "pdf_url": pdf_url
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# EXPORT SUCCESS
@router.get(
    "/export-success",
    response_class=HTMLResponse
)
async def export_success(
    request: Request,
    pdf_url: str = "/",
    title: str = "Your Comic"
):

    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={
            "pdf_url": pdf_url,
            "title": title
        }
    )


# TEST IMAGE
@router.post(
    "/test-image"
)
async def test_image(
    prompt: str = Form(...)
):

    try:

        image_url = generate_image(
            prompt,
            999
        )

        return {
            "image_url": image_url
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# DEMO MODE
@router.get(
    "/demo",
    response_class=HTMLResponse
)
async def demo(request: Request):

    demo_story = [

        {
            "panel_number": 1,
            "title": "The Magical Book",
            "scene_description":
                "Kokila discovers a mysterious magical book at school.",
            "image_prompt":
                "Anime style student discovering a magical book in a library",
            "caption":
                "A mysterious discovery!",
            "narration":
                "Kokila opens the strange book.",
            "dialogue":
                "Wow! What is this?"
        },

        {
            "panel_number": 2,
            "title": "A Secret Appears",
            "scene_description":
                "The magical book begins to glow with a bright light.",
            "image_prompt":
                "Anime magical glowing book inside a school classroom",
            "caption":
                "Something magical is happening!",
            "narration":
                "The pages begin to shine.",
            "dialogue":
                "Is this really magic?"
        },

        {
            "panel_number": 3,
            "title": "The Hidden Message",
            "scene_description":
                "Kokila finds a secret message inside the book.",
            "image_prompt":
                "Anime student reading a mysterious magical message",
            "caption":
                "A hidden message!",
            "narration":
                "A secret message appears.",
            "dialogue":
                "I need to find out what this means."
        },

        {
            "panel_number": 4,
            "title": "The Adventure Begins",
            "scene_description":
                "Kokila decides to follow the clues from the magical book.",
            "image_prompt":
                "Anime student following magical clues through a school hallway",
            "caption":
                "The adventure begins!",
            "narration":
                "Kokila follows the mysterious clues.",
            "dialogue":
                "Let's go!"
        },

        {
            "panel_number": 5,
            "title": "A New Discovery",
            "scene_description":
                "Kokila discovers that the magical book has chosen her for an adventure.",
            "image_prompt":
                "Anime student holding a magical book with a happy ending",
            "caption":
                "The beginning of a new journey!",
            "narration":
                "A new adventure is waiting.",
            "dialogue":
                "This is only the beginning!"
        }
    ]

    image_paths = [
        "/static/panels/panel_1.png",
        "/static/panels/panel_2.png",
        "/static/panels/panel_3.png",
        "/static/panels/panel_4.png",
        "/static/panels/panel_5.png"
    ]

    layout = build_comic_layout(
        demo_story,
        image_paths
    )

    title = "Kokila's Magical School Adventure"

    pdf_url = save_pdf(
        title,
        layout
    )

    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={
            "title": title,
            "pdf_url": pdf_url
        }
    )