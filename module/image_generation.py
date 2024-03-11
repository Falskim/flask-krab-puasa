import hashlib
import os
from PIL import Image, ImageFont, ImageDraw

ASSET_BASE_PATH = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '..', 'assets')

# Asset Path
FONT_FILEPATH = os.path.join(ASSET_BASE_PATH, "NotoSans-Bold.ttf")
SAHUR_ASSET_FILEPATH = os.path.join(ASSET_BASE_PATH, "wakamo_sahur.mp4")
BASE_PUASA_HARI_KE_IMAGE_FILEPATH = os.path.join(
    ASSET_BASE_PATH, "puasa_hari_ke.jpg")


TARAWIH_IMAGE_DIRECTORY_PATH = os.path.join(ASSET_BASE_PATH, "tarawih")

CACHED_RESULT_IMAGE_DIRECTORY_PATH = os.path.join(ASSET_BASE_PATH, "result")

# Total Cached Image
MAX_TOTAL_CACHED_IMAGE = 10


def get_puasa_hari_ke_image(day) -> str:
    clear_cached_image()

    hash_id = hashlib.sha256(str(day).encode()).hexdigest()[:8]
    file_extension = 'jpg'
    filename = f"phk_{hash_id}.{file_extension}"
    result_filepath = os.path.join(
        CACHED_RESULT_IMAGE_DIRECTORY_PATH, filename)

    try:
        # Image havent been generated yet
        if not os.path.exists(result_filepath):
            generate_puasa_hari_ke_image(day, result_filepath)

        return result_filepath
    except:
        return None


def generate_puasa_hari_ke_image(day, result_filepath) -> None:
    # Load Image
    img = Image.open(BASE_PUASA_HARI_KE_IMAGE_FILEPATH)
    draw = ImageDraw.Draw(img)

    # Load Font
    font = ImageFont.truetype(FONT_FILEPATH, 35, encoding="unic")

    # Add Text
    top_text = "PUASA"
    bottom_text = f"HARI KE {day}"
    fill_color = (255, 255, 255)
    stroke_color = (0, 0, 0)

    offset = len(str(day)) * 8
    draw.text((175, 0), top_text, font=font, fill=fill_color,
              stroke_width=4, stroke_fill=stroke_color)
    draw.text((145 - offset, 310), bottom_text, font=font,
              fill=fill_color, stroke_width=4, stroke_fill=stroke_color)

    img.save(result_filepath)


def get_tarawih_hari_ke_image(day) -> str:
    file_extension = 'jpg'
    filename = f"{int(day)}.{file_extension}"
    result_filepath = os.path.join(
        TARAWIH_IMAGE_DIRECTORY_PATH, filename)

    # Image havent been generated yet
    if os.path.exists(result_filepath):
        return result_filepath
    else:
        return None


def get_sahur_assets() -> str:
    return SAHUR_ASSET_FILEPATH


def clear_cached_image() -> None:
    # -1 for disabling
    if MAX_TOTAL_CACHED_IMAGE < 0:
        return

    EXCLUDED_FILES = ['.gitignore']

    files = os.listdir(CACHED_RESULT_IMAGE_DIRECTORY_PATH)
    filtered_files = [f for f in files if f not in EXCLUDED_FILES]

    if len(filtered_files) >= MAX_TOTAL_CACHED_IMAGE:
        for img in filtered_files:
            img_path = os.path.join(CACHED_RESULT_IMAGE_DIRECTORY_PATH, img)
            print("Removing", img_path)
            os.remove(img_path)
    return
