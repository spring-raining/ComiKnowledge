# -*- coding: utf-8 -*-

import string
import random
from django.forms import ValidationError

from ck.models import *

def check_unique_group_id(group_id):
    try:
        CKGroup.objects.get(group_id=group_id)
        raise ValidationError("Group id is already used.", code=1)
    except CKGroup.DoesNotExist:
        return group_id

def generate_rand_str(length):
    alphabets = string.digits + string.letters
    return "".join(random.choice(alphabets) for i in xrange(length))


z_ascii = [u"ａ", u"ｂ", u"ｃ", u"ｄ", u"ｅ", u"ｆ", u"ｇ", u"ｈ", u"ｉ",
       u"ｊ", u"ｋ", u"ｌ", u"ｍ", u"ｎ", u"ｏ", u"ｐ", u"ｑ", u"ｒ",
       u"ｓ", u"ｔ", u"ｕ", u"ｖ", u"ｗ", u"ｘ", u"ｙ", u"ｚ",
       u"Ａ", u"Ｂ", u"Ｃ", u"Ｄ", u"Ｅ", u"Ｆ", u"Ｇ", u"Ｈ", u"Ｉ",
       u"Ｊ", u"Ｋ", u"Ｌ", u"Ｍ", u"Ｎ", u"Ｏ", u"Ｐ", u"Ｑ", u"Ｒ",
       u"Ｓ", u"Ｔ", u"Ｕ", u"Ｖ", u"Ｗ", u"Ｘ", u"Ｙ", u"Ｚ"]
h_ascii = [u"a", u"b", u"c", u"d", u"e", u"f", u"g", u"h", u"i",
       u"j", u"k", u"l", u"m", u"n", u"o", u"p", u"q", u"r",
       u"s", u"t", u"u", u"v", u"w", u"x", u"y", u"z",
       u"A", u"B", u"C", u"D", u"E", u"F", u"G", u"H", u"I",
       u"J", u"K", u"L", u"M", u"N", u"O", u"P", u"Q", u"R",
       u"S", u"T", u"U", u"V", u"W", u"X", u"Y", u"Z"]
zh_ascii = {}
hz_ascii = {}
for i in range(len(z_ascii)):
    zh_ascii[z_ascii[i]] = h_ascii[i]
del z_ascii, h_ascii
def convert_to_hankaku(text):
    converted = ""
    for c in text:
        if zh_ascii .has_key(c):
            converted += zh_ascii[c]
        else:
            converted += c
    return converted
