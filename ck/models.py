# -*- coding: utf-8 -*-

import re
from django.core import validators
from django.db import models
from django.contrib.auth import models as auth_models

ENCODE_CHOICES = (
    ("S", "Shift_JIS"),
    ("I", "ISO-2022-JP"),
    ("E", "EUC-JP"),
    ("U", "UTF-8"),
)


#
# グループの拡張モデル
#
class CKGroup(auth_models.Group):
    group_id = models.CharField(max_length=30, unique=True,
                                validators=[validators.RegexValidator(re.compile('^\w+$'))])

#
# ユーザーの拡張モデル
#
class CKUser(auth_models.User):
    ck_groups = models.ManyToManyField(CKGroup, blank=True)
    circlems_access_token = models.CharField(max_length=50, null=True)
    circlems_refresh_token = models.CharField(max_length=50, null=True)

#
# CSVリストのモデル
#
class List(models.Model):
    parent_user = models.ForeignKey(CKUser)
    list_name = models.CharField(max_length=256)
    write_at = models.DateTimeField(auto_now=True)

    header_name = models.CharField(max_length=256)
    header_encoding = models.CharField(max_length=20)
    header_id = models.CharField(max_length=256, null=True)
    last_select_page = models.PositiveIntegerField(null=True)
    last_select_circle = models.IntegerField(null=True)
    mac_print_info = models.TextField(null=True)

    def __unicode__(self):
        return self.list_name

#
# CSVリストで記録されているサークルのモデル
#
class ListCircle(models.Model):
    parent_list = models.ForeignKey(List)

    serial_number = models.PositiveIntegerField()
    color_number = models.PositiveSmallIntegerField(default=0)
    page_number = models.PositiveIntegerField(null=True)
    cut_index = models.PositiveIntegerField(null=True)
    week = models.CharField(max_length=1, null=True)
    area = models.CharField(max_length=1, null=True)
    block = models.CharField(max_length=1, null=True)
    space_number = models.PositiveSmallIntegerField(null=True)
    genre_code = models.PositiveSmallIntegerField(null=True)
    circle_name = models.CharField(max_length=100)
    circle_name_yomigana = models.CharField(max_length=100, null=True)
    pen_name = models.CharField(max_length=100, null=True)
    book_name = models.CharField(max_length=100, null=True)
    url = models.URLField(max_length=100, null=True)
    mail = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=4000, null=True)
    memo = models.CharField(max_length=4000, null=True)
    map_x = models.IntegerField(null=True)
    map_y = models.IntegerField(null=True)
    layout = models.IntegerField(null=True)
    space_number_sub = models.CharField(max_length=1, choices=(("a","a"), ("b","b")), null=True)
    update_data = models.CharField(max_length=4000, null=True)
    circlems_url = models.URLField(max_length=100, null=True)
    rss = models.CharField(max_length=100, null=True)
    rss_data = models.CharField(max_length=4000, null=True)

    def __unicode__(self):
        return self.circle_name

    def get_long_space(self):
        if not self.area or not self.block or not self.space_number or not self.space_number_sub:
            return None
        else:
            return "%s%s-%d%s" % (self.area, self.block, self.space_number, self.space_number_sub)

#
# CSVリストで記録されている未登録サークルのモデル
#
class ListUnKnown(models.Model):
    parent_list = models.ForeignKey(List)

    circle_name = models.CharField(max_length=100)
    circle_name_yomigana = models.CharField(max_length=100, null=True)
    pen_name = models.CharField(max_length=100, null=True)
    memo = models.CharField(max_length=4000, null=True)
    color_number = models.PositiveSmallIntegerField(default=0)
    book_name = models.CharField(max_length=100, null=True)
    url = models.URLField(max_length=100, null=True)
    mail = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=4000, null=True)
    update_data = models.CharField(max_length=4000, null=True)
    circlems_url = models.URLField(max_length=100, null=True)
    rss = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return self.circle_name

#
# CSVリストで記録されている色のモデル
#
class ListColor(models.Model):
    parent_list = models.ForeignKey(List)

    color_number = models.PositiveSmallIntegerField()
    check_color = models.CharField(max_length=6)
    print_color = models.CharField(max_length=6)
    description = models.CharField(max_length=4000, null=True)

#
# Circle.Msデータベース形式で記録されるサークルのモデル
#
class ComiketCircle(models.Model):
                                                                        # ↓ Circle.Msデータベース作成時のSQL文
    comiket_number = models.PositiveSmallIntegerField()                 # comiketNo INTEGER not null, -- コミケ番号
    circle_id = models.IntegerField()                                   # id INTEGER not null,        -- サークルID
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
