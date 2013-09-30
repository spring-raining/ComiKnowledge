# -*- coding: utf-8 -*-

import csv
import json

from data.parser import parse_checklist_array
from translator import *
from container.list import *
from container.original import *


def import_list(path):
    """
    :param path: 読み込むcsvファイルパス
    :return: 読み込み結果のタプル(OriginalMemberContainer, ListContainer)
    """
    text = parse_checklist_array(path)
    pro = OriginalMemberContainer()
    rtn = ListContainer()

    for line in text:
        if line[0] == "Header":
            if line[1] != "ComicMarketCD-ROMCatalog":
                raise
            rtn.header_name = line[2]
            rtn.header_encoding = line[3]
            rtn.header_id = line[4]

        elif line[0] == "Circle":
            ci = CircleContainer()
            try:
                ci.number = int(line[1])
                ci.color_number = int(line[2])
                ci.page_number = int(line[3])
                ci.cut_index = int(line[4])
                ci.week = line[5]
                ci.area = line[6]
                ci.block = line[7]
                ci.space_number = int(line[8])
                ci.genre = int(line[9])
                ci.name = line[10]
                ci.name_yomigana = line[11]
                ci.author = line[12]
                ci.issue = line[13]
                ci.url = line[14]
                ci.mail = line[15]
                ci.appendix = line[16]
                ci.memo = line[17]
                ci.map_x = int(line[18]) if line[18] else None
                ci.map_y = int(line[19]) if line[19] else None
                ci.layout = int(line[20]) if line[20] else None
                ci.space_position = int(line[21])
                ci.update = line[22]
                ci.circlems_url = line[23]
                ci.rss = line[24]
                ci.rss_data = line[25]
            except IndexError:
                pass

            rtn.circle[int(line[1])] = ci

        elif line[0] == "UnKnown":
            u = UnKnownContainer()
            try:
                u.name = line[1]
                u.name_yomigana = line[2]
                u.author = line[3]
                u.memo = line[4]
                u.color = to_rgb_color(line[5])
                u.issue = line[6]
                u.url = line[7]
                u.mail = line[8]
                u.appendix = line[9]
                u.update = line[10]
                u.circlems_url = line[11]
                u.rss = line[12]
            except IndexError:
                pass
            rtn.unknown[line[1]] = u

        elif line[0] == "Color":
            co = ColorContainer()
            co.color_number = int(line[1])
            co.check_color = to_rgb_color(line[2])
            co.print_color = to_rgb_color(line[3])
            co.description = line[4]
            rtn.color[int(line[1])] = co
        elif line[0] == "LastSelect":
            rtn.last_select_page = int(line[1])
            rtn.last_select_circle = int(line[2])
        elif line[0] == "MacPrintInfo":
            rtn.mac_print_info = line[1]
        elif line[0] == "Co-Navigator":
            if line[1] == "Profile":
                pro.import_json(line[2])

    return (pro, rtn)


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


if __name__ == "__main__":
    (pro, lis) = import_list("csv_win.CSV")
    save_list("csv_win2.CSV", lis, OriginalMemberContainer())
