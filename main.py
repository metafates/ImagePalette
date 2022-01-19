from xml.etree.ElementTree import PI
from colorthief import ColorThief
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import os
import math

IMAGE_NAME = "img"
IMAGE_EXTENSION = "jpg"
COLOR_COUNT = 7  # minimum 2
BLOCK_GAP = .2  # %
BLUR = .01  # %
FONT_NAME = "JetBrainsMono.ttf"
DIR = os.getcwd()
IMAGE_PATH = os.path.join(DIR, IMAGE_NAME + '.' + IMAGE_EXTENSION)
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
    font = ImageFont.truetype(FONT_PATH, int(w * .15))
    draw = ImageDraw.Draw(image)
    draw.text((w/2, h/2), text, font=font, anchor='mm')


def make_block(color: RGB, size: tuple[int, int]) -> Image.Image:
    block = Image.new(mode="RGB", size=size, color=color)
    add_center_text(block, rgb_to_hex(color))
    return block


# TODO: add shadows
def add_blocks(image: Image.Image, blocks: list[Image.Image]):
    image_w, image_h = image.size

    blocks_len = sum(block.width for block in blocks)
    prev_block_width = 0
    prev_w = int((image_w - blocks_len) / 2)
    for block in blocks:
        w = prev_w + prev_block_width
        prev_block_width = block.width
        prev_w = w

        h = int((image_h - block.height) / 2)

        image.paste(block, (w, h))


def add_gaps(blocks: list[Image.Image]) -> list[Image.Image]:
    w = blocks[0].width
    gap = Image.new('RGBA', (int(w*BLOCK_GAP), 0), (0, 0, 0, 0))
    gap.putalpha(0)
    new = []
    for block in blocks:
        new.append(block)
        new.append(gap)
    return new[:-1]


with Image.open(IMAGE_PATH) as im:
    palette = get_palette(IMAGE_PATH, COLOR_COUNT)
    block_size = make_block_size(im.size)
    blocks = [make_block(color, block_size) for color in palette]
    blocks = add_gaps(blocks)
    new_image = im.copy()
    enhancer = ImageEnhance.Brightness(new_image)
    new_image = enhancer.enhance(.9)
    new_image = new_image.filter(
        ImageFilter.BoxBlur(min(new_image.size) * BLUR))
    add_blocks(new_image, blocks)
    new_image.save(f'{IMAGE_NAME}-palette.{IMAGE_EXTENSION}')
