# -*- coding: utf-8 -*-

import csv
import os
import re
import dajaxice.finders

from ck.models import *
import src
from src.data.parser import parse_checklist_array
from src.translator import *
from src.utils import generate_rand_str, convert_to_hankaku
from src.error import *


LIST_LIMIT = 100

def import_list(csv_file, parent_user):
    ALLOWED_EVENT_NAME = (
        "ComicMarket" + str(src.COMIKET_NUMBER),
        "ComicMarketWeb" + str(src.COMIKET_NUMBER),
    )

    #parent_user = CKUser()
    ls = parent_user.list_set.all()
    if len(ls) >= LIST_LIMIT:
        raise TooMuchListsError

    try:
        arr = parse_checklist_array(csv_file)
    except:
        raise ChecklistInvalidError

    l = List()
    arr_lci = []
    arr_lun = []
    arr_lco = []
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
            if not line[2] in ALLOWED_EVENT_NAME:
                raise ChecklistVersionError
            l.header_name = line[2]
            l.header_encoding = line[3]
            l.header_id = line[4]
        elif line[0] == "LastSelect" and len(line) >= 3:
            l.last_select_page = int(line[1])
            l.last_select_circle = int(line[2])
        elif line[0] == "MacPrintInfo" and len(line) >=2:
            l.mac_print_info = line[1]
    for line in arr:
        if line[0] == "Circle":
            try:
                lc = prepare_circle_obj(line[1:], parent_user)
            except:
                raise ChecklistInvalidError
            if isinstance(lc, ListCircle):
                arr_lci.append(lc)
        elif line[0] == "UnKnown":
            try:
                lu = prepare_unknown_obj(line[1:])
            except:
                raise ChecklistInvalidError
            if isinstance(lu, ListUnKnown):
                arr_lun.append(lu)
        elif line[0] == "Color":
            try:
                lc = prepare_color_obj(line[1:])
            except:
                raise ChecklistInvalidError
            if isinstance(lc, ListColor):
                arr_lco.append(lc)
    try:
        l.save()
        for i in arr_lci:
            i.parent_list = l
            i.save()
        for i in arr_lun:
            i.parent_list = l
            i.save()
        for i in arr_lco:
            i.parent_list = l
            i.save()
    except:
        raise ChecklistInvalidError
    return l


def create_list(list_name, parent_user):
    l = List()
    l.list_name = list_name
    l.parent_user = parent_user
    while True:
        g = generate_rand_str(8)
        try:
            List.objects.get(list_id=g)
        except:
            break
    l.list_id = g
    l.header_name = src.HEADER_NAME
    l.header_id = "%s %s" % (src.APP_NAME, str(src.VERSION))
    l.save()
    return l


# 引数がリストの場合、CSVの順番で[serial_number, color_number,..., rss_data]
# 辞書の場合、{"serial_number": serial_number, ... }
def prepare_circle_obj(info, parent_user):
    sub = lambda x: "a" if x == "0" else ("b" if x == "1" else None)

    if isinstance(info, list):
        arr = info
    elif isinstance(info, dict):
        arr = [info.get("serial_number",""), info.get("color_number",""), info.get("page_number",""), info.get("cut_index",""),
               info.get("week",""), info.get("area",""), info.get("block",""), info.get("space_number",""), info.get("genre_code",""),
               info.get("circle_name",""), info.get("circle_name_yomigana",""), info.get("pen_name",""), info.get("book_name",""),
               info.get("url",""), info.get("mail",""), info.get("description",""), info.get("memo",""), info.get("map_x",""),
               info.get("map_y",""), info.get("layout",""), info.get("space_number_sub",""), info.get("update_data",""),
               info.get("circlems_url",""), info.get("rss",""), info.get("rss_data","")]
    else:
        return None
    lc = ListCircle()
    try:
        lc.added_by = parent_user
        lc.serial_number = int(arr[0])
        lc.color_number = int(arr[1])
        lc.page_number = int(arr[2]) if arr[2].isdigit() and int(arr[2]) else None
        lc.cut_index = int(arr[3]) if arr[3].isdigit() and int(arr[3]) else None
        lc.week = arr[4]
        lc.area = arr[5]
        lc.block = convert_to_hankaku(arr[6])
        lc.space_number = int(arr[7]) if arr[7].isdigit() and int(arr[7]) else None
        lc.genre_code = int(arr[8]) if arr[8].isdigit() and int(arr[8]) else None
        lc.circle_name = arr[9]
        lc.circle_name_yomigana = arr[10]
        lc.pen_name = arr[11]
        lc.book_name = arr[12]
        lc.url = arr[13]
        lc.mail = arr[14]
        lc.description = arr[15]
        lc.memo = arr[16]
        lc.map_x = int(arr[17]) if arr[17] else None
        lc.map_y = int(arr[18]) if arr[18] else None
        lc.layout = int(arr[19]) if arr[19] else None
        lc.space_number_sub = sub(arr[20])
        lc.update_data = arr[21]
        lc.circlems_url = arr[22]
        lc.rss = arr[23]
        lc.rss_data = arr[24]
    except IndexError:
        pass
    return lc


# 引数がリストの場合、CSVの順番で[circle_name, circle_name_yomigana,..., rss]
# 辞書の場合、{"circle_name": circle_name, ... }
def prepare_unknown_obj(info, csv_color_format=True):
    if isinstance(info, list):
        arr = info
    elif isinstance(info, dict):
        arr = [info.get("circle_name",""), info.get("circle_name_yomigana",""), info.get("pen_name",""), info.get("memo",""),
               info.get("color_number",""), info.get("book_name",""), info.get("url",""), info.get("mail",""),
               info.get("description",""), info.get("update_data",""), info.get("circlems_url",""), info.get("rss","")]
    else:
        return None
    lu = ListUnKnown()
    try:
        lu.circle_name = arr[0]
        lu.circle_name_yomigana = arr[1]
        lu.pen_name = arr[2]
        lu.memo = arr[3]
        lu.color_number = to_rgb_color(arr[4]) if csv_color_format else arr[4]
        lu.book_name = arr[5]
        lu.url = arr[6]
        lu.mail = arr[7]
        lu.description = arr[8]
        lu.update_data = arr[9]
        lu.circlems_url = arr[10]
        lu.rss = arr[11]
    except IndexError:
        pass
    return lu

# 引数がリストの場合、CSVの順番で[color_number, check_color, print_color, rss]
# 辞書の場合、{"color_number": color_number, ... }
def prepare_color_obj(info, csv_color_format=True):
    if isinstance(info, list):
        arr = info
    elif isinstance(info, dict):
        arr = [info.get("color_number",""), info.get("check_color",""), info.get("print_color",""), info.get("description","")]
    else:
        return None
    lc = ListColor()
    try:
        lc.color_number = int(arr[0])
        lc.check_color = to_rgb_color(arr[1]) if csv_color_format else arr[1]
        lc.print_color = to_rgb_color(arr[2]) if csv_color_format else arr[2]
        lc.description = arr[3]
    except IndexError:
        pass
    return lc


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
    l.header_name = src.HEADER_NAME
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


#
#   color_option=1  重複時color_orderで先頭に近い色を選ぶ
#   color_option=2  重複時select_colorの色にする
#
def output_list(response, list_id, memo_template, color_option=1, color_order=(1,2,3,4,5,6,7,8,9,), select_color=1):
    writer = csv.writer(response, delimiter=",", quotechar='"')
    sub = lambda x: "0" if x == "a" else ("1" if x == "b" else "")
    enc_utf8 = lambda x: x.encode("utf-8") if x else ""
    to_str = lambda x: str(x).encode("utf-8") if x is not None else ""
    out_list = List.objects.get(list_id=list_id)
    color_order = list(color_order)
    color_order.append(0)

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
                .replace("{userid}", i.added_by.username)\
                .replace("{username}", i.added_by.first_name)\
                .replace("{memo}", i.memo)\
                .replace("\\n", "\n")
            if color_option == 1:
                _c = i.color_number if color_order.index(i.color_number) < color_order.index(c) else c
            elif color_option == 2:
                _c = select_color
            else:
                _c = 0
            out_circles[i.serial_number] = (v, m, _c)
        else:
            m = memo_template\
                .replace("{userid}", i.added_by.username)\
                .replace("{username}", i.added_by.first_name)\
                .replace("{memo}", i.memo)\
                .replace("\\n", "\n")
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
    pass
