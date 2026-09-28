from pathlib import Path

from fpdf import FPDF

from app.config import (
    EXPORTS_DIR,
    STATIC_DIR
)


def get_local_image(url_path):
    relative_path = url_path.removeprefix("/static/")

    return str(
        STATIC_DIR / relative_path
    )


def save_pdf(title, layout):

    safe_title = ""

    for character in title:
        if character.isalnum() or character in "-_":
            safe_title += character
        else:
            safe_title += "_"

    safe_title = safe_title.strip("_") or "comic"

    pdf_path = EXPORTS_DIR / f"{safe_title}.pdf"

    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4"
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=12
    )

    for panel in layout:

        pdf.add_page()

        pdf.set_font(
            "Helvetica",
            "B",
            18
        )

        pdf.multi_cell(
            180,
            10,
            f"Panel {panel['panel_number']}: {panel['title']}"
        )

        image_file = get_local_image(
            panel["image_path"]
        )

        if Path(image_file).exists():
            pdf.image(
                image_file,
                x=15,
                y=32,
                w=180
            )

        pdf.set_y(145)

        pdf.set_font(
            "Helvetica",
            "I",
            10
        )

        pdf.multi_cell(
            180,
            6,
            panel.get(
                "scene_description",
                ""
            )
        )

        pdf.ln(2)

        if panel.get("caption"):
            pdf.set_font(
                "Helvetica",
                "B",
                11
            )

            pdf.multi_cell(
                180,
                6,
                "Caption: " + panel["caption"]
            )

        if panel.get("narration"):
            pdf.set_font(
                "Helvetica",
                "",
                11
            )

            pdf.multi_cell(
                180,
                6,
                "Narration: " + panel["narration"]
            )

        if panel.get("dialogue"):
            pdf.set_font(
                "Helvetica",
                "",
                11
            )

            pdf.multi_cell(
                180,
                6,
                "Dialogue: " + panel["dialogue"]
            )

    pdf.output(
        str(pdf_path)
    )

    return (
        f"/static/exports/"
        f"{pdf_path.name}"
    )