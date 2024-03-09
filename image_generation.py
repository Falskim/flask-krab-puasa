import hashlib
import os
from PIL import Image, ImageFont, ImageDraw

import time

# Folder Relative Path
BASE_IMAGE_DIRECTORY_PATH = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "images/base")
RESULT_IMAGE_DIRECTORY_PATH = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "images/result")

# Asset Path
FONT_PATH = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "NotoSans-Bold.ttf")

# Base Images
BASE_IMAGE_PUASA_HARI_KE_FILENAME = "puasa_hari_ke.jpg"

# Total Cached Image
MAX_TOTAL_CACHED_IMAGE = 10


def generate_puasa_hari_ke_image(day) -> str:
    clear_cached_image()

    hash_id = hashlib.sha256(str(day).encode()).hexdigest()[:8]
    file_extension = 'jpg'
    filename = f"phk_{hash_id}.{file_extension}"
    result_filepath = os.path.join(RESULT_IMAGE_DIRECTORY_PATH, filename)

    # Image havent been generated yet
    if not os.path.exists(result_filepath):
        # Load Image
        img = Image.open(os.path.join(
            BASE_IMAGE_DIRECTORY_PATH, BASE_IMAGE_PUASA_HARI_KE_FILENAME))
        draw = ImageDraw.Draw(img)

        # Load Font
        font = ImageFont.truetype(FONT_PATH, 35, encoding="unic")

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

    return result_filepath


def clear_cached_image() -> None:
    # -1 for disabling
    if MAX_TOTAL_CACHED_IMAGE < 0:
        return

    EXCLUDED_FILES = ['.gitignore']

    files = os.listdir(RESULT_IMAGE_DIRECTORY_PATH)
    filtered_files = [f for f in files if f not in EXCLUDED_FILES]

    if len(filtered_files) >= MAX_TOTAL_CACHED_IMAGE:
        for img in filtered_files:
            img_path = os.path.join(RESULT_IMAGE_DIRECTORY_PATH, img)
            print("Removing", img_path)
            os.remove(img_path)
    return


# start = time.time()
# generate_puasa_hari_ke_image(5)
# generate_puasa_hari_ke_image(4)
# generate_puasa_hari_ke_image(2)
# generate_puasa_hari_ke_image(5)
# generate_puasa_hari_ke_image(2)
# generate_puasa_hari_ke_image(1)
# generate_puasa_hari_ke_image(5)
# generate_puasa_hari_ke_image(4)
# generate_puasa_hari_ke_image(2)
# generate_puasa_hari_ke_image(5)
# generate_puasa_hari_ke_image(2)
# generate_puasa_hari_ke_image(1)
# generate_puasa_hari_ke_image(5)
# generate_puasa_hari_ke_image("1")
# generate_puasa_hari_ke_image(11)
# generate_puasa_hari_ke_image(113)
# generate_puasa_hari_ke_image(115)
# generate_puasa_hari_ke_image(223)
# generate_puasa_hari_ke_image(5423)
# generate_puasa_hari_ke_image(5623)
# end = time.time()
# print("Time elapsed", (end - start))
