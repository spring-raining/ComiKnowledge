# -*- coding: utf-8 -*-

import csv
import json
import os
from django.forms import ModelForm

from ck.models import *
import src
from src.data.parser import parse_checklist_array
from src.translator import *
from src.container.list import *
from src.utils import generate_rand_str, convert_to_hankaku
from src.error import *


def import_list(csv_file, parent_user):
    try:
        arr = parse_checklist_array(csv_file)
    except:
        raise ChecklistInvalidError

    l = List()
    l.list_name = os.path.splitext(csv_file.name)[0]
    l.parent_user = parent_user
    while True:
        g = generate_rand_str(8)
        try:
            List.objects.get(list_id=g)
        except:
            break
    l.list_id = g
    sub = lambda x: "a" if x == "0" else ("b" if x == "1" else None)
    for line in arr:
        if line[0] == "Header" and len(line) >= 5:
            if line[1] != "ComicMarketCD-ROMCatalog":
                raise ChecklistInvalidError
            l.header_name = line[2]
            l.header_encoding = line[3]
            l.header_id = line[4]
        elif line[0] == "LastSelect" and len(line) >= 3:
            l.last_select_page = int(line[1])
            l.last_select_circle = int(line[2])
        elif line[0] == "MacPrintInfo" and len(line) >=2:
            l.mac_print_info = line[1]
    l.save()
    for line in arr:
        if line[0] == "Circle":
            lc = ListCircle()
            lc.parent_list = l
            lc.added_by = parent_user
            try:
                lc.serial_number = int(line[1])
                lc.color_number = int(line[2])
                lc.page_number = int(line[3])
                lc.cut_index = int(line[4])
                lc.week = line[5]
                lc.area = line[6]
                lc.block = convert_to_hankaku(line[7])
                lc.space_number = int(line[8])
                lc.genre_code = int(line[9])
                lc.circle_name = line[10]
                lc.circle_name_yomigana = line[11]
                lc.pen_name = line[12]
                lc.book_name = line[13]
                lc.url = line[14]
                lc.mail = line[15]
                lc.description = line[16]
                lc.memo = line[17]
                lc.map_x = int(line[18]) if line[18] else None
                lc.map_y = int(line[19]) if line[19] else None
                lc.layout = int(line[20]) if line[20] else None
                lc.space_number_sub = sub(line[21])
                lc.update_data = line[22]
                lc.circlems_url = line[23]
                lc.rss = line[24]
                lc.rss_data = line[25]
            except IndexError:
                pass
            lc.save()
        elif line[0] == "UnKnown":
            lu = ListUnKnown()
            lu.parent_list = l
            try:
                lu.circle_name = line[1]
                lu.circle_name_yomigana = line[2]
                lu.pen_name = line[3]
                lu.memo = line[4]
                lu.color_number = to_rgb_color(line[5])
                lu.book_name = line[6]
                lu.url = line[7]
                lu.mail = line[8]
                lu.description = line[9]
                lu.update_data = line[10]
                lu.circlems_url = line[11]
                lu.rss = line[12]
            except IndexError:
                pass
            lu.save()
        elif line[0] == "Color":
            lc = ListColor()
            lc.parent_list = l
            try:
                lc.color_number = int(line[1])
                lc.check_color = to_rgb_color(line[2])
                lc.print_color = to_rgb_color(line[3])
                lc.description = line[4]
            except IndexError:
                pass
            lc.save()
    return l


def delete_list(list_id):
    try:
        l = List.objects.get(list_id=list_id)
        l.delete()
        return True
    except:
        return False


def delete_circle(circle_id):
    try:
        c =ListCircle.objects.get(id=circle_id)
        c.delete()
        return True
    except:
        return False


# 統合時、色などのリスト共通情報はlists[0]のものを保存する
def merge_list(lists, group, list_name):
    l = List()
    if not list_name:
        raise FormBlankError("list_name")
    if not lists:
        raise FormBlankError("lists")
    l.list_name = list_name
    l.parent_group = group
    while True:
        g = generate_rand_str(8)
        try:
            List.objects.get(list_id=g)
        except:
            break
    l.list_id = g
    l.header_name = "ComicMarketCD-ROMCatalog"
    l.header_encoding = "UTF-8"
    l.header_id = "%s %s" % (src.APP_NAME, str(src.VERSION))
    l.last_select_page = None
    l.last_select_circle = None
    l.mac_print_info = None
    l.save()
    for lc in lists[0].listcolor_set.all():
        nlc = ListColor()
        nlc.parent_list = l
        nlc.color_number = lc.color_number
        nlc.check_color = lc.check_color
        nlc.print_color = lc.print_color
        nlc.description = lc.description
        nlc.save()
    for _list in lists:
        for lc in _list.listcircle_set.all():
            nlc = ListCircle()
            nlc.parent_list = l
            nlc.added_by = lc.added_by
            nlc.serial_number = lc.serial_number
            nlc.color_number = lc.color_number
            nlc.page_number = lc.page_number
            nlc.cut_index = lc.cut_index
            nlc.week = lc.week
            nlc.area = lc.area
            nlc.block = lc.block
            nlc.space_number = lc.space_number
            nlc.genre_code = lc.genre_code
            nlc.circle_name = lc.circle_name
            nlc.circle_name_yomigana = lc.circle_name_yomigana
            nlc.pen_name = lc.pen_name
            nlc.book_name = lc.book_name
            nlc.url = lc.url
            nlc.mail = lc.mail
            nlc.description = lc.description
            nlc.memo = lc.memo
            nlc.map_x = lc.map_x
            nlc.map_y = lc.map_y
            nlc.layout = lc.layout
            nlc.space_number_sub = lc.space_number_sub
            nlc.update_data = lc.update_data
            nlc.circlems_url = lc.circlems_url
            nlc.rss = lc.rss
            nlc.rss_data = lc.rss_data
            nlc.save()
        for lu in _list.listunknown_set.all():
            nlu = ListUnKnown()
            nlu.parent_list = l
            nlu.circle_name = lu.circle_name
            nlu.circle_name_yomigana = lu.circle_name_yomigana
            nlu.pen_name = lu.pen_name
            nlu.memo = lu.memo
            nlu.color_number = lu.color_number
            nlu.book_name = lu.book_name
            nlu.url = lu.url
            nlu.mail = lu.mail
            nlu.description = lu.description
            nlu.update_data = lu.update_data
            nlu.circlems_url = lu.circlems_url
            nlu.rss = lu.rss
            nlu.save()
    return l


def output_list(response, list_id, memo_template, color_order=(1,2,3,4,5,6,7,8,9,)):
    writer = csv.writer(response, delimiter=",", quotechar='"')
    sub = lambda x: "0" if x == "a" else ("1" if x == "b" else "")
    enc_utf8 = lambda x: x.encode("utf-8") if x else ""
    to_str = lambda x: str(x).encode("utf-8") if x is not None else ""
    out_list = List.objects.get(list_id=list_id)

    writer.writerow(["Header",
                     "ComicMarketCD-ROMCatalog",
                     src.HEADER_NAME,
                     "UTF-8",
                     "%s %s" % (src.APP_NAME, str(src.VERSION))])
    for i in out_list.listcolor_set.all():
        writer.writerow(["Color",
                         to_str(i.color_number),
                         enc_utf8(to_bgr_color(i.check_color)),
                         enc_utf8(to_bgr_color(i.print_color)),
                         enc_utf8(i.description)])
    out_circles = {}
    for i in out_list.listcircle_set.all():
        if i.serial_number in out_circles:
            v, m, c = out_circles[i.serial_number]
            m += memo_template\
                .replace("{memo}", i.memo)\
                .replace("{username}", i.added_by.first_name)\
                .replace("{userid}", i.added_by.username)
            _c = i.color_number if color_order.index(i.color_number) < color_order.index(c) else c
            out_circles[i.serial_number] = (v, m, _c)
        else:
            m = memo_template\
                .replace("{memo}", i.memo)\
                .replace("{username}", i.added_by.first_name)\
                .replace("{userid}", i.added_by.username)
            out_circles[i.serial_number] = (i, m, i.color_number)
    for key, value in out_circles.items():
        v, m, c = value
        writer.writerow(["Circle",
                         to_str(v.serial_number),
                         to_str(c),
                         to_str(v.page_number),
                         to_str(v.cut_index),
                         enc_utf8(v.week),
                         enc_utf8(v.area),
                         enc_utf8(v.block),
                         to_str(v.space_number),
                         to_str(v.genre_code),
                         enc_utf8(v.circle_name),
                         enc_utf8(v.circle_name_yomigana),
                         enc_utf8(v.pen_name),
                         enc_utf8(v.book_name),
                         enc_utf8(v.url),
                         enc_utf8(v.mail),
                         enc_utf8(v.description),
                         enc_utf8(m),
                         to_str(v.map_x),
                         to_str(v.map_y),
                         to_str(v.layout),
                         sub(v.space_number_sub),
                         enc_utf8(v.update_data),
                         enc_utf8(v.circlems_url),
                         enc_utf8(v.rss),
                         enc_utf8(v.rss_data)])
    return response

if __name__ == "__main__":
    # テストは書いちゃらめええええ
    pass
