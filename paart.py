#!/usr/bin/env python3

from PIL import Image

LUM_CHARMAP = " `.-+x!|$*&%@#"
LUM_CALIBRATE = len(LUM_CHARMAP)

def luminance(pixel):
    return (min(pixel)/255 + max(pixel)/255) / 2

def calc_luminance_mean(pixels):
    rev_lums = [1 - luminance(pixel) for pixel in pixels]

    return sum(rev_lums) / (len(rev_lums)+1)

def pixels2char(pixels):
    luminance_mean = calc_luminance_mean(pixels)
    side = int(LUM_CALIBRATE * luminance_mean)

    return LUM_CHARMAP[side]

def sqrange(x1, y1, x2, y2):
    for y in range(y1, y2):
        for x in range(x1, x2):
            yield (x, y)

def pixels2string(pixels, w, h, cwidth=12):
    if not pixels:
        yield ''
        return

    if cwidth > w: cwidth = w

    ret = ""
    for sy in range(0, h-cwidth, cwidth):
        for sx in range(0, w-cwidth, cwidth):
            subpixels = map(
                lambda coord: pixels[coord],
                sqrange(sx, sy, sx+cwidth, sy+cwidth)
            )
            yield pixels2char(subpixels)

        yield '\n'

    return ret

if __name__ == "__main__":
    import sys

    if not 2 <= len(sys.argv) <= 3:
        print(f"Usage:\n\t{sys.argv[0]} <input> [cwidth]")
        sys.exit(1)

    img = Image.open(sys.argv[1])
    cwidth = int(sys.argv[2]) if len(sys.argv) == 3 else 12

    w, h = img.size
    for ch in pixels2string(img.load(), w, h, cwidth):
        sys.stdout.write(ch)
