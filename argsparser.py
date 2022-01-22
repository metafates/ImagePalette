import argparse

parser = argparse.ArgumentParser(
    prog='palette',
    description="Generates color palette from image"
)

parser.add_argument(
    'image',
    help='image to work with',
    type=str
)

parser.add_argument(
    '--colors',
    help='how many colors to show',
    type=int,
    default=7
)

parser.add_argument(
    '--no-blur',
    help='do not apply blur to the image',
    action='store_true'
)
