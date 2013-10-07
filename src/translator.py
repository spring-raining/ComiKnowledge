# -*- coding: utf-8 -*-

def to_bgr_color(rgb):
    return rgb[5:7] + rgb[3:5] + rgb[1:3]

def to_rgb_color(bgr):
    return "#" + bgr[4:6] + bgr[2:4] + bgr[0:2]


if __name__ == "__main__":
    # 何も書くな
    pass