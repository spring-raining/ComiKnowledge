# -*- coding: utf-8 -*-

import re
from data.parser import parse_tab_array
from container.define import *

re_kind = re.compile("\*")
re_comment = re.compile("#")


def import_define(path, encoding):
    """
    CXXDEF.TXTファイルを読み、辞書形式で返します
    :param path:
    :param encoding:
    :return: dictionary

    dictionary
    +-- Comiket (unicode)
    |   +-- number (unicode) data:(int)
    |   +-- name (unicode) data:(unicode)
    |
    +-- cutInfo (unicode)
    |   +-- width (unicode) data:(int)
    |   +-- height (unicode) data:(int)
    |   +-- origin_x (unicode) data:(int)
    |   +-- origin_y (unicode) data:(int)
    |   +-- offset_x (unicode) data:(int)
    |   +-- offset_y (unicode) data:(int)
    |
    +-- mapTableInfo (unicode)
    |   +-- width (unicode) data:(int)
    |   +-- height (unicode) data:(int)
    |   +-- origin_x (unicode) data:(int)
    |   +-- origin_y (unicode) data:(int)
    |
    +-- ComiketDate (unicode)
    |   +-- 20XXXXXX (開催日付)(int)
    |   |   +-- year (unicode) data:(int)
    |   |   +-- month (unicode) data:(int)
    |   |   +-- day (unicode) data:(int)
    |   |   +-- week (unicode) data:(unicode)
    |   |   +-- page (unicode) data:(int)
    |   +-- 20XXXXXX
    |   :
    |
    +-- ComiketMap
    |   +-- 東123 (地図名)(unicode)
    |   |   +-- name (unicode) data:(unicode)
    |   |   +-- map_key (unicode) data:(unicode)
    |   |   +-- print_area (unicode) data:(int[X,X,X,X])
    |   |   +-- smallmap_key (unicode) data:(unicode)
    |   |   +-- fineprint_area (unicode) data:(int[X,X,X,X])
    |   |   +-- reverse (unicode) data:(bool)
    |   +-- 東456
    |   :
    |
    +-- ComiketArea
    |   +-- 東123壁 (地区名)(unicode)
    |   |   +-- name (unicode) data:(unicode)
    |   |   +-- map (unicode) data:(unicode)
    |   |   +-- block (unicode) data:(unicode)
    |   |   +-- print_area unicode) data:(int[X,X,X,X])
    |   |   +-- smallmap_key (key=東123壁,東456壁,西1壁,西2壁を除く)(unicode) data:(unicode)
    |   |   +-- fineprint_area (key=東123壁,東456壁,西1壁,西2壁を除く)(unicode) data:(int[X,X,X,X])
    |   +-- 東1
    |   :
    |
    +-- ComiketGenre (unicode)
        +-- 100 (key=ジャンルコード(int) value=ジャンル名(unicode))
        +-- 110
        :

    """
    text = parse_tab_array(path, encoding)
    rtn = DefineContainer()
    kind = ""

    for line in text:
        if re_comment.match(line[0]) != None:
            continue

        elif re_kind.match(line[0]) != None:
            kind = line[0]
            continue

        elif kind != "" and line[0] != "" and not line[0].isspace():
            # コミケット回数情報
            # 回数番号,コミケット名称
            if kind == "*Comiket":
                rtn.comiket_number = int(line[0])
                rtn.comiket_name = line[1]

            # サークルカット表示情報
            # 幅,高さ,原点X,原点Y,オフセットX,オフセットY
            elif kind == "*cutInfo":
                rtn.cut_info.width = int(line[0])
                rtn.cut_info.height = int(line[1])
                rtn.cut_info.origin_x = int(line[2])
                rtn.cut_info.origin_y = int(line[3])
                rtn.cut_info.offset_x = int(line[4])
                rtn.cut_info.offset_y = int(line[5])

            # マップ机表示情報
            # 幅,高さ,原点X,原点Y
            elif kind == "*mapTableInfo":
                rtn.map_table_info.width = int(line[0])
                rtn.map_table_info.height = int(line[1])
                rtn.map_table_info.origin_x = int(line[2])
                rtn.map_table_info.origin_y = int(line[3])

            # 開催日程 + ジャンプ情報
            # 年, 月, 日, 曜日,開始ページ  日順にならべる
            elif kind == "*ComiketDate":
                d = DefineContainer.ComiketDateContainer()
                k = int(line[0] + line[1] + line[2])
                d.year = int(line[0])
                d.month = int(line[1])
                d.day = int(line[2])
                d.week = line[3]
                d.page = int(line[4])
                rtn.comiket_date[k] = d

            # 地図情報
            # 地図名,地図ファイル名基幹部,印刷範囲,略地図ファイル名基幹部,ハイレゾ印刷範囲,レイアウト上下反転フラグ
            elif kind == "*ComiketMap":
                k = line[0]
                d = DefineContainer.ComiketMapContainer()
                d.name = line[0]
                d.map_key = line[1]
                d.print_area = [int(line[2]),
                                int(line[3]),
                                int(line[4]),
                                int(line[5])]
                d.small_map_key = line[6]
                d.fine_print_area = [int(line[7]),
                                     int(line[8]),
                                     int(line[9]),
                                     int(line[10])]
                d.reverse = True if 1 else False
                rtn.comiket_map[k] = d

            # 地区 + ブロック情報
            # 地区名,対応地図名,ブロック名s,印刷範囲,略地図ファイル名基幹部,ハイレゾ印刷範囲
            elif kind == "*ComiketArea":
                k = line[0]
                d = DefineContainer.ComiketAreaContainer()
                d.name = line[0]
                d.map = line[1]
                d.block = line[2]
                d.print_area = [int(line[3]),
                                int(line[4]),
                                int(line[5]),
                                int(line[6])]
                if len(line) >= 12:
                    d.small_map_key = line[7]
                    d.fine_print_area = [int(line[8]),
                                         int(line[9]),
                                         int(line[10]),
                                         int(line[11])]
                rtn.comiket_area[k] = d

            # ジャンル情報
            # ジャンルコード,ジャンル名
            elif kind == "*ComiketGenre":
                rtn.comiket_genre[int(line[0])] = line[1]

    return rtn

if __name__ == "__main__":
    c = import_define("C83DEF.TXT", "shift-jis")
    for i in c.comiket_genre.keys():
        print c.comiket_genre[i]
    for i in c.comiket_date.keys():
        j = c.comiket_date[i]
        print str(j.year) +"/"+ str(j.month) +"/"+ str(j.day) +"/"+ j.week
