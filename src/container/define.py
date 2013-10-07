# -*- coding: utf-8 -*-

class DefineContainer:
    def __init__(self):
        """
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
        |   |   +-- small_map_key (unicode) data:(unicode)
        |   |   +-- fine_print_area (unicode) data:(int[X,X,X,X])
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
        |   |   +-- small_map_key (key=東123壁,東456壁,西1壁,西2壁を除く)(unicode) data:(unicode)
        |   |   +-- fine_print_area (key=東123壁,東456壁,西1壁,西2壁を除く)(unicode) data:(int[X,X,X,X])
        |   +-- 東1
        |   :
        |
        +-- ComiketGenre (unicode)
            +-- 100 (key=ジャンルコード(int) value=ジャンル名(unicode))
            +-- 110
            :
        """

        self.comiket_number = None
        self.comiket_name = None
        self.cut_info = DefineContainer.CutInfoContainer()
        self.map_table_info = DefineContainer.MapTableInfoContainer()
        self.comiket_date = {}
        self.comiket_map = {}
        self.comiket_area = {}
        self.comiket_genre = {}

    class CutInfoContainer:
        def __init__(self):
            self.width = None
            self.height = None
            self.origin_x = None
            self.origin_y = None
            self.offset_x = None
            self.offset_y = None

    class MapTableInfoContainer:
        def __init__(self):
            self.width = None
            self.height = None
            self.origin_x = None
            self.origin_y = None

    class ComiketDateContainer:
        def __init__(self):
            self.year = None
            self.month = None
            self.day = None
            self.week = None
            self.page = None

    class ComiketMapContainer:
        def __init__(self):
            self.name = None
            self.map_key = None
            self.print_area = None
            self.small_map_key = None
            self.fine_print_area = None
            self.reverse = None

    class ComiketAreaContainer:
        def __init__(self):
            self.name = None
            self.map = None
            self.block = None
            self.print_area = None
            self.small_map_key = None
            self.fine_print_area = None

if __name__ == "__main__":
    # テストは書いちゃダメ
    pass