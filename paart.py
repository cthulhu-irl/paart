#!/usr/bin/env python3

from PIL import Image, ImageFilter

CHARMAP = "  .'-~+x:^%"
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

    return sum(nums) / (len(nums)+1)


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

    for sy in range(0, h-cheight, cheight):

        for sx in range(0, w-cwidth, cwidth):
            subpixels = map(
                lambda coord: pixels[coord],
                sqrange(sx, sy, sx+cwidth, sy+cheight)
            )

            yield pixels2char(subpixels, cwidth, cheight)

        yield '\n'


def negative_normalization(chars):
    half_len = CHARMAP_LEN // 2

    # NOTE rev_index_map is supposed to have index+1 numbers, so theres is no 0
    rev_index_map = {
        char: CHARMAP_LEN - idx for idx, char in enumerate(CHARMAP)
    }
    balance_map = {char: half_len - idx for idx, char in enumerate(CHARMAP)}

    distribution_mean = sum(balance_map.get(char, 0) for char in chars)

    # if it's already more dark than bright, then do nothing
    if distribution_mean > 0:
        return chars

    rev_idxs = (rev_index_map.get(char, 0) for char in chars)

    return ''.join(
        CHARMAP[idx-1] if idx else char for idx, char in zip(rev_idxs, chars)
    )


if __name__ == "__main__":
    import sys

    if not 2 <= len(sys.argv) <= 3:
        print(f"Usage:\n\t{sys.argv[0]} <input> [column_count]")
        sys.exit(1)

    img = Image.open(sys.argv[1])
    w, h = img.size

    ratio = w / h
    font_ratio = 3 / 12

    count = int(sys.argv[2]) if len(sys.argv) == 3 else 80

    cwidth = w // count
    cheight = int(h / (count / ratio) * (2 - font_ratio))

    out = ''
    for ch in pixels2string(img.load(), w, h, cwidth, cheight):
        out += ch

    print(negative_normalization(out))
