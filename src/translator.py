# -*- coding: utf-8 -*-

def to_bgr_color(rgb):
    return rgb[4:6] + rgb[2:4] + rgb[0:2]

def to_rgb_color(bgr):
    return bgr[4:6] + bgr[2:4] + bgr[0:2]


if __name__ == "__main__":
    # 何も書いてはいけない
    pass