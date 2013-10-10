# -*- coding: utf-8 -*-
from django.db import models

ENCODE_CHOICES = (
    ("S", "Shift_JIS"),
    ("I", "ISO-2022-JP"),
    ("E", "EUC-JP"),
    ("U", "UTF-8"),
)


#
# CSVリストで記録されているサークルのモデル
#
class ListCircle(models.Model):
    serial_number = models.PositiveIntegerField()
    color_number = models.PositiveSmallIntegerField()
    page_number = models.PositiveIntegerField()
    cut_index = models.PositiveIntegerField()
    week = models.CharField(max_length=1)
    area = models.CharField(max_length=1)
    block = models.CharField(max_length=1)
    space_number = models.PositiveSmallIntegerField()
    genre_code = models.PositiveSmallIntegerField()
    circle_name = models.CharField(max_length=100)
    circle_name_yomigana = models.CharField(max_length=100)
    pen_name = models.CharField(max_length=100)
    book_name = models.CharField(max_length=100)
    url = models.URLField(max_length=100)
    mail = models.CharField(max_length=100)
    description = models.CharField(max_length=4000)
    memo = models.CharField(max_length=4000)
    map_x = models.IntegerField()
    map_y = models.IntegerField()
    layout = models.IntegerField()
    space_number_sub = models.CharField(max_length=1, choices=(("a","a"), ("b","b")))
    update_data = models.CharField(max_length=4000)
    circlems_url = models.URLField(max_length=100)
    rss = models.CharField(max_length=100)
    rss_data = models.CharField(max_length=4000)

#
# CSVリストで記録されている未登録サークルのモデル
#
class ListUnKnown(models.Model):
    circle_name = models.CharField(max_length=100)
    circle_name_yomigana = models.CharField(max_length=100)
    pen_name = models.CharField(max_length=100)
    memo = models.CharField(max_length=4000)
    color_number = models.PositiveSmallIntegerField()
    book_name = models.CharField(max_length=100)
    url = models.URLField(max_length=100)
    mail = models.CharField(max_length=100)
    description = models.CharField(max_length=4000)
    update_data = models.CharField(max_length=4000)
    circlems_url = models.URLField(max_length=100)
    rss = models.CharField(max_length=100)

#
# CSVリストで記録されている色のモデル
#
class ListColor(models.Model):
    color_number = models.PositiveSmallIntegerField()
    check_color = models.CharField(max_length=6)
    print_color = models.CharField(max_length=6)
    description = models.CharField(max_length=4000)

#
# CSVリストのモデル
#
class List(models.Model):
    circle = models.ForeignKey(ListCircle)
    unknown = models.ForeignKey(ListUnKnown)
    color = models.ForeignKey(ListColor)
    header_name = models.CharField(max_length=256)
    header_encoding = models.CharField(max_length=1, choices=ENCODE_CHOICES)
    header_id = models.CharField(max_length=256)
    last_select_page = models.PositiveIntegerField()
    last_select_circle = models.IntegerField()
    mac_print_info = models.TextField()

#
# Circle.Msデータベース形式で記録されるサークルのモデル
#
class ComiketCircle(models.Model):
                                                                        # ↓ Circle.Msデータベース作成時のSQL文
    comiket_number = models.PositiveSmallIntegerField()                 # comiketNo INTEGER not null, -- コミケ番号
    number = models.IntegerField()                                      # id INTEGER not null,        -- サークルID
    page_number = models.PositiveIntegerField()                         # pageNo      INTEGER,        -- ページ番号         漏れの場合は 0
    cut_index = models.PositiveIntegerField()                           # cutIndex    INTEGER,        -- カットインデックス 漏れの場合は 0
    day = models.DateField()                                            # day         INTEGER,        -- 参加日             漏れの場合は 0
    block_id = models.PositiveIntegerField()                            # blockId     INTEGER,        -- ブロックID         漏れの場合は 0
    space_number = models.PositiveIntegerField()                        # spaceNo     INTEGER,        -- スペース番号       漏れの場合は 0
    space_number_sub = models.CharField(max_length=1,
                                  choices=(("a","a"), ("b", "b")))      # spaceNoSub  INTEGER,	      -- スペース番号補助   0:a 1:b
    genre_id = models.PositiveIntegerField()                            # genreId     INTEGER,        -- ジャンルID
    circle_name = models.CharField(max_length=100)                      # circleName  VARCHAR(33),    -- サークル名
    pen_name = models.CharField(max_length=100)                         # penName     VARCHAR(100),   -- 執筆者名
    book_name = models.CharField(max_length=100)                        # bookName    VARCHAR(100),   -- 発行誌名
    url = models.URLField(max_length=100)                               # url         VARCHAR(100),   -- URL
    mail_address = models.CharField(max_length=100)                     # mailAddr    VARCHAR(100),   -- メールアドレス
    description = models.CharField(max_length=4000)                     # description VARCHAR(4000),  -- 補足説明
    memo = models.CharField(max_length=4000)                            # memo        VARCHAR(4000),  -- サークルメモ
    update_id = models.IntegerField()                                   # updateId    INTEGER,        -- 更新用ID
    update_data = models.CharField(max_length=4000)                     # updateData  VARCHAR(4000),  -- 更新情報
    circlems_url = models.URLField(max_length=100)                      # circlems    VARCHAR(100),   -- Circle.ms URL
    rss = models.CharField(max_length=100)                              # rss         VARCHAR(100),   -- RSS
    update_flag = models.BooleanField()                                 # updateFlag  INTEGER,        -- 更新フラグ
    # ↓ Extend                                                          # ↓ Extend
    wc_id = models.IntegerField()                                       # WCId INTEGER not null,      -- 公開サークルID
    twitter_url = models.URLField(max_length=256)                       # twitterURL  VARCHAR(256),   -- twitterURL
    pixiv_url = models.URLField(max_length=256)                         # pixivURL    VARCHAR(256),   -- pixivURL

#
# Circle.Msデータベース形式で記録されるジャンルのモデル
#
class ComiketGenre(models.Model):
                                                                        # ↓ Circle.Msデータベース作成時のSQL文
    comiket_number = models.PositiveSmallIntegerField()                 # comiketNo INTEGER not null, -- コミケ番号
    genre_id = models.PositiveIntegerField()                            # id INTEGER not null,        -- ジャンルID
    name = models.CharField(max_length=10)                              # name VARCHAR(10),           -- ジャンル名
    code = models.PositiveSmallIntegerField()                           # code INTEGER,               -- ジャンルコード

#
# Circle.Msデータベース形式で記録される日程のモデル
#
class ComiketDate(models.Model):
                                                                        # ↓ Circle.Msデータベース作成時のSQL文
    comiket_number = models.PositiveSmallIntegerField()                 # comiketNo INTEGER not null, -- コミケ番号
    date_id = models.PositiveSmallIntegerField()                        # id      INTEGER not null,   -- 日程ID(初日が1)
    day = models.DateField()
                                                                        # year    INTEGER,            -- 年
                                                                        # month   INTEGER,            -- 月
                                                                        # day     INTEGER,            -- 日
    weekday = models.CharField(max_length=1)                            # weekday INTEGER,            -- 曜日 (1:日 ～ 7:土)

# define.py

class Define(models.Model):
    pass

# original.py

class OriginalCircle(models.Model):
    pass

class OriginalMember(models.Model):
    pass
