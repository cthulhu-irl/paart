#!/usr/bin/env python3

from PIL import Image, ImageFilter

CHARMAP = " `'.,_-~+x:^%"
CHARMAP_LEN = len(CHARMAP)


def sqrange(x1, y1, x2, y2):
    for y in range(y1, y2):
        for x in range(x1, x2):
            yield (x, y)


def luminance(pixel):
    return (min(pixel)/255 + max(pixel)/255) / 2


def calc_luminance_mean(pixels):
    lums = [luminance(pixel) * 255 for pixel in pixels]
    high = max(lums) or 1

    lums = [lum/high for lum in lums]

    contrast = (max(lums) + min(lums)) / 2

    nums = [(n * n) * contrast for n in lums]

    return sum(nums) / len(nums)


def pixels2char_luminance(pixels):
    luminance_mean = calc_luminance_mean(pixels)
    side = int(CHARMAP_LEN * luminance_mean)

    return CHARMAP[side]


def pixels2char(pixels, w, h):
    return pixels2char_luminance(pixels)


def pixels2string(pixels, w, h, cwidth=12, cheight=12):
    if not pixels:
        yield ''
        return

    cwidth = w if cwidth > w else cwidth
    cheight = h if cheight > h else cheight

    ret = ""
    for sy in range(0, h-cheight, cheight):

        for sx in range(0, w-cwidth, cwidth):
            subpixels = map(
                lambda coord: pixels[coord],
                sqrange(sx, sy, sx+cwidth, sy+cheight)
            )

            yield pixels2char(subpixels, cwidth, cheight)

        yield '\n'

    return ret


if __name__ == "__main__":
    import sys

    if not 2 <= len(sys.argv) <= 3:
        print(f"Usage:\n\t{sys.argv[0]} <input> [column_count]")
        sys.exit(1)

    img = Image.open(sys.argv[1])
    w, h = img.size

    count = int(sys.argv[2]) if len(sys.argv) == 3 else 80

    cwidth = w // count
    cheight = int((cwidth / w) * h)

    cwidth, cheight = cheight, cwidth

    for ch in pixels2string(img.load(), w, h, cwidth, cheight):
        sys.stdout.write(ch)
