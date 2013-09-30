# -*- coding: utf-8 -*-

import sys
import os
import requests
from PIL import Image

from api.twitter import *

def save_thumbnail(url, path, size=(100, 100)):
    req = requests.get(url)
    f = open(path, "w")
    f.write(req.content)
    f.close()
    resize_thumbnail(path, size)

def resize_thumbnail(path, size):
    image = Image.open(path, "r")
    w = float(size[0]) / float(image.size[0])
    h = float(size[1]) / float(image.size[1])
    aspect = w if w > h else h
    image.thumbnail((image.size[0]*aspect, image.size[1]*aspect), Image.ANTIALIAS)
    canvas = Image.new("RGB", size, "#ffffff")
    canvas.paste(image, (((size[0] - image.size[0])/2),((size[1] - image.size[1])/2)))
    canvas.save(path, "PNG", quality=95)

if __name__ == "__main__":
    save_thumbnail(get_twitter_icon_url("spring_raining"), os.path.dirname(__file__)+"/test.png")