from xml.etree.ElementTree import PI
from colorthief import ColorThief
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os
import math

IMAGE_NAME = "image.jpg"
COLOR_COUNT = 7
BLOCK_GAP = .1  # percent
FONT_NAME = "JetBrainsMono.ttf"
DIR = os.getcwd()
IMAGE_PATH = os.path.join(DIR, IMAGE_NAME)
FONT_PATH = os.path.join(os.path.join(DIR, 'fonts'), FONT_NAME)

RGB = tuple[int, int, int]
HEX = str


def get_palette(image_path: str, count: int) -> list[RGB]:
    color_thief = ColorThief(image_path)
    palette: list[RGB] = color_thief.get_palette(color_count=count, quality=6)
    return palette


def rgb_to_hex(rgb: RGB) -> HEX:
    return '#%02x%02x%02x' % rgb


def make_block_size(img_size: tuple[int, int]) -> tuple[int, int]:
    w, h = img_size
    block_h = h * .4
    block_w = w * .1
    return math.ceil(block_w), math.ceil(block_h)


def add_center_text(image: Image.Image, text: str):
    w, h = image.size
    # TODO: adapt font size automatically
    font = ImageFont.truetype(FONT_PATH, 60)
    draw = ImageDraw.Draw(image)
    draw.text((w/2, h/2), text, font=font, anchor='mm')


def make_block(color: RGB, size: tuple[int, int]) -> Image.Image:
    block = Image.new(mode="RGB", size=size, color=color)
    add_center_text(block, rgb_to_hex(color))
    return block


def add_blocks(image: Image.Image, blocks: list[Image.Image]):
    w, h = image.size
    l = len(blocks)
    for i, block in enumerate(blocks):
        # Horizontal align
        w_ = int((w - (block.width * l)) / 2 + block.width * i)
        # Vertical align
        h_ = int((h - block.height) / 2)

        image.paste(block, (w_, h_))


with Image.open(IMAGE_PATH) as im:
    palette = get_palette(IMAGE_PATH, COLOR_COUNT)
    block_size = make_block_size(im.size)
    blocks = [make_block(color, block_size) for color in palette]
    new_image = im.copy()
    enhancer = ImageEnhance.Brightness(new_image)
    new_image = enhancer.enhance(0.8)
    add_blocks(new_image, blocks)
    new_image.save("new.jpg")
