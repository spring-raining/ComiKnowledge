# -*- coding: utf-8 -*-

import csv
import json
from django.forms import ModelForm

from ck.models import *
from src.data.parser import parse_checklist_array
from src.translator import *
from src.container.list import *
from src.utils import generate_rand_str


def import_list(csv_file, parent_user):
    arr = parse_checklist_array(csv_file)

    l = List()
    l.list_name = csv_file.name
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
                continue
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
            try:
                lc.serial_number = int(line[1])
                lc.color_number = int(line[2])
                lc.page_number = int(line[3])
                lc.cut_index = int(line[4])
                lc.week = line[5]
                lc.area = line[6]
                lc.block = line[7]
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


def save_list(path, lists, members, color, profile=None):
    """
    :param path: 出力先パス
    :param lists: {id:ListContainer}の辞書
    :param members: {id:OriginalMemberContainer}の辞書
    :param color: {id:ColorContainer}の辞書
    :param profile: 出力OriginalProfileContainer(デフォルト:None)
    """
    out = ListContainer()
    f = open(path, mode="w")
    writer = csv.writer(f, delimiter=",", quotechar='"')
    out.header_name = "ComicMarket84"

    for key, li in lists.items():
        #li = ListContainer()
        for k, v in li.circle.items():
            if k in out.circle:
                #out.circle[k].memo += "\n" + v.memo + "(" + members[key].handle + ")"
                if out.circle[k].color_number > v.color_number and not v.color_number == 0:
                    out.circle[k].color_number = v.color_number
            else:
                out.circle[k] = v
                #out.circle[k].memo += "(" + members[key].handle + ")"
        for k, v in li.unknown.items():
            out.unknown[k] = v

    writer.writerow(("Header",
                     "ComicMarketCD-ROMCatalog",
                     out.header_name.encode("utf-8"),
                     "UTF-8"))
                     #APP_NAME + " " + str(VERSION)))

    for k, v in sorted(out.circle.items()):
        #v = CircleContainer()
        writer.writerow(("Circle",
                         v.number,
                         v.color_number,
                         v.page_number,
                         v.cut_index,
                         v.week.encode("utf-8")
                         if v.week else "",
                         v.area.encode("utf-8")
                         if v.area else "",
                         v.block.encode("utf-8")
                         if v.block else "",
                         v.space_number,
                         v.genre,
                         v.name.encode("utf-8")
                         if v.name else "",
                         v.name_yomigana.encode("utf-8")
                         if v.name_yomigana else "",
                         v.author.encode("utf-8")
                         if v.author else "",
                         v.issue.encode("utf-8")
                         if v.issue else "",
                         v.url.encode("utf-8")
                         if v.url else "",
                         v.mail.encode("utf-8")
                         if v.mail else "",
                         v.appendix.encode("utf-8")
                         if v.appendix else "",
                         v.memo.encode("utf-8")
                         if v.memo else "",
                         v.map_x
                         if not v.map_x is None else "",
                         v.map_y
                         if not v.map_y is None else "",
                         v.layout
                         if not v.layout is None else "",
                         v.space_position,
                         v.update.encode("utf-8")
                         if v.update else "",
                         v.circlems_url.encode("utf-8")
                         if v.circlems_url else "",
                         v.rss.encode("utf-8")
                         if v.rss else "",
                         v.rss_data.encode("utf-8")
                         if v.rss_data else ""))

    for k, v in out.unknown.items():
        #v =UnKnownContainer()
        writer.writerow(("UnKnown",
                         v.name.encode("utf-8")
                         if v.name else "",
                         v.name_yomigana.encode("utf-8")
                         if v.name_yomigana else "",
                         v.author.encode("utf-8")
                         if v.author else "",
                         v.memo.encode("utf-8")
                         if v.memo else "",
                         v.color.encode("utf-8")
                         if v.color else "",
                         v.issue.encode("utf-8")
                         if v.issue else "",
                         v.url.encode("utf-8")
                         if v.url else "",
                         v.mail.encode("utf-8")
                         if v.mail else "",
                         v.appendix.encode("utf-8")
                         if v.appendix else "",
                         v.update.encode("utf-8")
                         if v.update else "",
                         v.circlems_url.encode("utf-8")
                         if v.circlems_url else "",
                         v.rss.encode("utf-8")
                         if v.rss else ""))

    for k, v in sorted(color.items()):
        #v = ColorContainer()
        writer.writerow(("Color",
                         v.color_number,
                         to_bgr_color(v.check_color).encode("utf-8"),
                         to_bgr_color(v.print_color).encode("utf-8"),
                         v.description.encode("utf-8")
                         if v.description else ""))

    if out.last_select_page and out.last_select_circle:
        writer.writerow(("LastSelect",
                         out.last_select_page,
                         out.last_select_circle))

    if out.mac_print_info:
        writer.writerow(("MacPrintInfo", out.mac_print_info.encode("utf-8")))

    if profile:
        #profile = OriginalMemberContainer()
        writer.writerow(("Co-Navigator",
                         "Profile",
                         json.dumps(profile.__dict__)))

    f.close()


def merge_list(m_list, apply_color=0, apply_header=0):
    rtn = ListContainer()
    rtn.header_encoding = "UTF-8"
    rtn.header_name = m_list[apply_header].header_name
    rtn.header_id = "Co-Navigator"
    rtn.color = m_list[apply_color].color

    for i in m_list:
        if str(i) != "ListContainer":
            continue

        # i = ListContainer() # have to delete
        for j in i.circle:
            # j = CircleContainer() # have to delete
            if j in rtn.circle:
                if rtn.circle[j].color_number > i.circle[j].color_number:
                    rtn.circle[j].color_number = i.circle[j].color_number
                #TODO configで優先する色設定を変えられるようにする
                rtn.circle[j].memo += "\n" + i.circle[j].memo
            else:
                rtn.circle[j] = i.circle[j]
    return rtn


if __name__ == "__main__":
    # テストは書いちゃらめええええ
    pass
