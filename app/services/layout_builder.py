def build_comic_layout(
    story,
    image_paths
):

    if len(story) != len(image_paths):

        raise ValueError(
            "Number of story panels and "
            "images must be equal."
        )

    layout = []

    for panel, image_path in zip(
        story,
        image_paths
    ):

        item = dict(panel)

        item["image_path"] = image_path

        layout.append(item)

    return layout