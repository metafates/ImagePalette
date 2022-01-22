# Color palette generator

Generates a color palette from the image.

## Example

![original](examples/original.jpg 'Original')
![generated](examples/palette.jpg 'Generated')

[Artist](https://www.artstation.com/guweiz)

## Usage

Required dependencies

-   Pillow
-   ColorThief

`python palette.py <image> [--colors COLORS] [--no-blur]`

### TODO

-   [ ] Add vertical mode (for images with _Height_ > _Width_)

-   [ ] Add shadows to the color blocks _(optional)_

-   [ ] Make script executable, rather than calling `python palette.py` each time

-   [ ] Add blur radius as argument
