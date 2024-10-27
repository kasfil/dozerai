from pathlib import Path

from telegram import PhotoSize

from config import GROUP_PATH, IMG_PATH


async def imgsaver(photo: PhotoSize, group_id: str | None = None) -> Path:
    """Save image if it's has media_group_id."""
    if group_id:
        # create folder if it doesn't exist
        dest_path = Path.joinpath(GROUP_PATH, group_id)
        if not Path.exists(dest_path):
            Path.mkdir(dest_path, parents=True)
    else:
        dest_path = IMG_PATH

    # save image
    img = await photo.get_file()
    img_ext = img.file_path.split(".")[-1] if img.file_path else "jpg"
    img_path = Path.joinpath(dest_path, f"{img.file_id}.{img_ext}")
    await img.download_to_drive(custom_path=img_path)

    return img_path
