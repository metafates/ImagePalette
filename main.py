from colorthief import ColorThief
from PIL import Image
import os
import math

IMAGE_NAME = "image.jpg"
COLOR_COUNT = 7
DIR = os.getcwd()
IMAGE_PATH = os.path.join(DIR, IMAGE_NAME)

RGB = tuple[int, int, int]
HEX = str


def get_palette(image_path: str, count: int) -> list[RGB]:
    color_thief = ColorThief(image_path)
    palette: list[RGB] = color_thief.get_palette(color_count=count, quality=6)
    return palette


def rgb_to_hex(rgb: RGB) -> HEX:
    return '#%02x%02x%02x' % rgb


def get_block_size(img_size: tuple[int, int]) -> tuple[int, int]:
    w, h = img_size
    block_h = h * .2
    block_w = w * .05
    return math.ceil(block_h), math.ceil(block_w)


with Image.open(IMAGE_PATH) as im:
    w, h = im.size
    palette = get_palette(IMAGE_PATH, COLOR_COUNT)
    print(w, h)
    print(palette)
    print(list(map(rgb_to_hex, palette)))
    print(get_block_size(im.size))
