from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):

    gemini_api_key: str = ""

    hf_token: str = ""

    gemini_flash_model: str = "gemini-3.8-flash"

    gemini_pro_model: str = "gemini-2.5-pro"

    hf_image_model: str = "stabilityai/stable-diffusion-3.5-large"

    hf_provider: str = "hf-inference"

    allow_placeholder_images: bool = True

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()


TEMPLATES_DIR = BASE_DIR / "templates"

STATIC_DIR = BASE_DIR / "static"

PANELS_DIR = STATIC_DIR / "panels"

EXPORTS_DIR = STATIC_DIR / "exports"


PANELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

EXPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)