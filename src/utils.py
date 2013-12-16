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

def space_character(comiket_number, day, block_id, space_number):
    """
    スペースに応じてその特徴を表す名前を返す
    >>> print space_character(85, 3, 1, 4)
    シャッター
    >>> print space_character(85, 2, 116, 34)
    シャッター
    >>> print space_character(85, 1, 14, 36)
    偽壁(お誕生日席)
    >>> print space_character(85, 3, 36, 31)
    内壁(お誕生日席)
    """
    if comiket_number == 85:
        if block_id in (1, 38,):
            if space_number in (4, 5, 6, 15, 16, 17, 28, 29, 44, 45, 60, 61, 72, 73, 74, 83, 84, 85,):
                return u"シャッター"
            elif space_number in (20, 21, 36, 37, 52, 53, 68, 69,):
                return u"外壁(非常口)"
            else:
                return u"外壁"
        elif block_id in (75, 116,):
            if space_number in (19, 20, 34, 35,):
                return u"シャッター"
            else:
                return u"西館壁"
        elif block_id in (13, 14, 25, 26, 50, 51, 62, 63,):
            if space_number in (1, 5, 6, 12, 13, 19, 20, 24, 25, 29, 30, 36, 37, 43, 44, 48,):
                return u"偽壁(お誕生日席)"
            else:
                return u"偽壁"
        else:
            text = ""
            if (day == 2 and block_id == 40 and space_number <= 30)\
            or (day == 3 and block_id == 3 and space_number <= 30)\
            or (day == 3 and block_id == 36 and space_number >= 31)\
            or (day == 3 and block_id == 40 and space_number <= 30):
                text = u"内壁"
            if block_id in (2, 37, 39, 74,)                                         and space_number in (1, 7, 8, 13, 14, 19, 20, 26, 27, 33, 34, 39, 40, 45, 46, 52,)\
            or block_id <= 74                                                       and space_number in (1, 7, 8, 15, 16, 23, 24, 30, 31, 37, 38, 45, 46, 53, 54, 60,)\
            or block_id in (76, 81, 110, 115,)                                      and space_number in (1, 7, 8, 16, 17, 25,)\
            or block_id in (77, 78, 79, 80, 111, 112, 113, 114,)                    and space_number in (1, 8, 9, 17, 18, 26,)\
            or block_id in (82, 83, 84, 85, 86, 87, 104, 105, 106, 107, 108, 109,)  and space_number in (1, 9, 10, 18, 19, 24,)\
            or block_id in (88, 89, 102, 103,)                                      and space_number in (1, 6, 7, 11,)\
            or block_id in (90, 91, 92, 93, 94, 97, 98, 99, 100, 101,)              and space_number in (1, 7, 8, 13)\
            or block_id in (95, 96,)                                                and space_number in (1, 7, 8, 12,):
                text += u"お誕生日席" if text == "" else u"(お誕生日席)"
            return text
