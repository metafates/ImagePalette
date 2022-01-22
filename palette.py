from colorthief import ColorThief
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import os
import math
from argsparser import parser

args = parser.parse_args()

IMAGE_FULLNAME = args.image

IMAGE_NAME = ''.join(IMAGE_FULLNAME.split('.')[:-1])
IMAGE_EXTENSION = IMAGE_FULLNAME.split('.')[-1]
COLOR_COUNT = args.colors
BLOCK_GAP = .2  # %
BLUR = .004
FONT_NAME = "JetBrainsMono.ttf"
DIR = os.getcwd()
IMAGE_PATH = os.path.join(DIR, IMAGE_FULLNAME)
FONT_PATH = os.path.join(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'fonts'), FONT_NAME)

RGB = tuple[int, int, int]
HEX = str


def get_palette(image_path: str, count: int) -> list[RGB]:
    '''
    Generate a color pallette from the image
    '''
    color_thief = ColorThief(image_path)
    palette: list[RGB] = color_thief.get_palette(color_count=count, quality=6)
    return palette


def rgb_to_hex(rgb: RGB) -> HEX:
    '''
    Convert RGB tuple to HEX string
    '''
    return '#%02x%02x%02x' % rgb


def calculate_block_size(img_size: tuple[int, int]) -> tuple[int, int]:
    '''
    Calculate blocks width and height based on image size
    '''
    w, h = img_size
    block_h = h * .4
    block_w = w * .1
    return math.ceil(block_w), math.ceil(block_h)


def add_center_text(image: Image.Image, text: str):
    '''
    Add text to the image and align it
    '''
    w, h = image.size
    font = ImageFont.truetype(FONT_PATH, int(w * .15))
    draw = ImageDraw.Draw(image)
    draw.text((w/2, h/2), text, font=font, anchor='mm')


def make_block(color: RGB, size: tuple[int, int]) -> Image.Image:
    '''
    Make a color block
    '''
    block = Image.new(mode="RGB", size=size, color=color)
    add_center_text(block, rgb_to_hex(color))
    return block


# TODO: add shadows maybe
def add_blocks(image: Image.Image, blocks: list[Image.Image]):
    '''
    Add color blocks to the image
    '''
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
    '''
    Insert empty blocks to make them serve as gaps
    '''
    w = blocks[0].width
    gap = Image.new('RGBA', (int(w*BLOCK_GAP), 0), (0, 0, 0, 0))
    gap.putalpha(0)
    new = []
    for block in blocks:
        new.append(block)
        new.append(gap)
    return new[:-1]


def main():
    print("Opening image...")
    with Image.open(IMAGE_PATH) as im:
        print("Getting color palette...")
        palette = get_palette(IMAGE_PATH, COLOR_COUNT)[:COLOR_COUNT]
        block_size = calculate_block_size(im.size)
        blocks = [make_block(color, block_size) for color in palette]
        blocks = add_gaps(blocks)
        new_image = im.copy()
        print("Applying filters...")
        enhancer = ImageEnhance.Brightness(new_image)
        new_image = enhancer.enhance(.9)
        new_image = new_image.filter(
            ImageFilter.GaussianBlur(min(new_image.size) * BLUR))
        add_blocks(new_image, blocks)
        print("Saving...")
        new_image_name = f'{IMAGE_NAME}-palette.{IMAGE_EXTENSION}'
        new_image.save(
            new_image_name,
            quality=100,  # preserve original quality
            subsampling=0
        )
        print(f"Done! Image saved as '{new_image_name}'")


if __name__ == "__main__":
    main()
