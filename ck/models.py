# -*- coding: utf-8 -*-

import re
from django.core import validators
from django.db import models
from django.contrib.auth import models as auth_models

from ComiKnowledge.settings import THUMBNAILS_UPLOAD_TO
import src
from src.utils import generate_rand_str

ENCODE_CHOICES = (
    ("S", "Shift_JIS"),
    ("I", "ISO-2022-JP"),
    ("E", "EUC-JP"),
    ("U", "UTF-8"),
)


#
# ユーザーの拡張モデル
#
class CKUser(auth_models.User):
    thumbnail = models.ImageField(upload_to=THUMBNAILS_UPLOAD_TO, null=True)
    circlems_access_token = models.CharField(max_length=50, null=True)
    circlems_refresh_token = models.CharField(max_length=50, null=True)

#
# グループのモデル
#
class CKGroup(models.Model):
    name = models.CharField(max_length=30)
    group_id = models.SlugField(max_length=30, unique=True, blank=False)
    members = models.ManyToManyField(CKUser, through="Relation", null=True)
    description = models.CharField(max_length=4000, null=True)

#
# グループとユーザーの関係を示す中間モデル
#
class Relation(models.Model):
    ckuser = models.ForeignKey(CKUser)
    ckgroup = models.ForeignKey(CKGroup)
    verification = models.BooleanField(default=False)
    date_joined = models.DateTimeField(null=True)

#
# CSVリストのモデル
#
class List(models.Model):
    parent_user = models.ForeignKey(CKUser, null=True)
    parent_group = models.ForeignKey(CKGroup, null=True)
    list_id = models.SlugField(max_length=8, unique=True)
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
    added_by = models.ForeignKey(CKUser)

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
# Circle.Msデータベース形式で記録されるサークルの抽象モデル
#
class ComiketCircle(models.Model):
                                                                        # ↓ Circle.Msデータベース作成時のSQL文
    comiket_number = models.PositiveSmallIntegerField()                 # comiketNo INTEGER not null, -- コミケ番号
    circle_id = models.IntegerField(null=True)                          # id INTEGER not null,        -- サークルID
    page_number = models.PositiveIntegerField(null=True)                # pageNo      INTEGER,        -- ページ番号         漏れの場合は 0
    cut_index = models.PositiveIntegerField(null=True)                  # cutIndex    INTEGER,        -- カットインデックス 漏れの場合は 0
    day = models.PositiveSmallIntegerField(null=True,
                choices=((1, "1日目"), (2, "2日目"), (3, "3日目")))       # day         INTEGER,        -- 参加日             漏れの場合は 0
    block_id = models.PositiveIntegerField(null=True)                   # blockId     INTEGER,        -- ブロックID         漏れの場合は 0
    space_number = models.PositiveIntegerField(null=True)               # spaceNo     INTEGER,        -- スペース番号       漏れの場合は 0
    space_number_sub = models.CharField(max_length=1, null=True,
                choices=(("a","a"), ("b", "b")))                        # spaceNoSub  INTEGER,        -- スペース番号補助   0:a 1:b
    genre_id = models.PositiveIntegerField(null=True)                   # genreId     INTEGER,        -- ジャンルID
    circle_name = models.CharField(max_length=100)                      # circleName  VARCHAR(33),    -- サークル名
    pen_name = models.CharField(max_length=100, null=True)              # penName     VARCHAR(100),   -- 執筆者名
    book_name = models.CharField(max_length=100, null=True)             # bookName    VARCHAR(100),   -- 発行誌名
    url = models.URLField(max_length=100, null=True)                    # url         VARCHAR(100),   -- URL
    mail_address = models.CharField(max_length=100, null=True)          # mailAddr    VARCHAR(100),   -- メールアドレス
    description = models.CharField(max_length=4000, null=True)          # description VARCHAR(4000),  -- 補足説明
    memo = models.CharField(max_length=4000, null=True)                 # memo        VARCHAR(4000),  -- サークルメモ
    update_id = models.IntegerField(null=True)                          # updateId    INTEGER,        -- 更新用ID
    update_data = models.CharField(max_length=4000, null=True)          # updateData  VARCHAR(4000),  -- 更新情報
    circlems_url = models.URLField(max_length=100, null=True)           # circlems    VARCHAR(100),   -- Circle.ms URL
    rss = models.CharField(max_length=100, null=True)                   # rss         VARCHAR(100),   -- RSS
    update_flag = models.IntegerField(null=True)                        # updateFlag  INTEGER,        -- 更新フラグ
    # ↓ Extend                                                          # ↓ Extend
    wc_id = models.IntegerField(null=True)                              # WCId INTEGER not null,      -- 公開サークルID
    twitter_url = models.URLField(max_length=256, null=True)            # twitterURL  VARCHAR(256),   -- twitterURL
    pixiv_url = models.URLField(max_length=256, null=True)              # pixivURL    VARCHAR(256),   -- pixivURL

    class Meta:
        abstract = True

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

#
# CircleKnowledge, CompanyKnowledgeにひもづけされる個々の情報の抽象モデル
#
class AbstractKnowledgeComment(models.Model):
    parent_user = models.ForeignKey("CKUser")
    parent_group = models.ForeignKey("CKGroup", null=True)
    write_at = models.DateTimeField(auto_now=True)
    comiket_number = models.PositiveSmallIntegerField()
    comment = models.CharField(max_length=50, null=True)
    event_code = models.PositiveSmallIntegerField()
    event_time = models.TimeField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)

    class Meta:
        abstract = True

#
# ユーザーが入力するサークルの基本情報
#
class CircleKnowledge(models.Model):
    circle_knowledge_id = models.SlugField(max_length=8, unique=True)
    comment = models.CharField(max_length=200, null=True)

#
# その年のサークルの情報
#
re_twitter = re.compile('^https?://(www\.)?twitter.com/')
re_pixiv = re.compile('^http://(www\.)?pixiv\.net/member\.php\?id=\d+')
re_url = re.compile('^https?://')
class CircleKnowledgeData(ComiketCircle):
    parent_circle_knowledge = models.ForeignKey("CircleKnowledge")

    # save()前に実行する すでにサークルを登録している場合CircleKnowledgeオブジェクトを返す
    def validate_circle(self):
        try:
            c = list(CircleKnowledgeData.objects.filter
                (comiket_number=src.COMIKET_NUMBER,
                 day=self.day,
                 block_id=self.block_id,
                 space_number=self.space_number,
                 space_number_sub=self.space_number_sub))[0]
            return c.parent_circle_knowledge
        except IndexError:
            pass
        self.comiket_number = src.COMIKET_NUMBER
        try:
            self.parent_circle_knowledge
        except:
            while True:
                g = generate_rand_str(8)
                try:
                    CircleKnowledge.objects.get(circle_knowledge_id=g)
                except:
                    break
            ck = CircleKnowledge()
            ck.circle_knowledge_id = g
            ck.save()
            self.parent_circle_knowledge = ck
        return True

#
# CircleKnowledgeにひもづけされるKnowledgeDataの実装
#
class CircleKnowledgeComment(AbstractKnowledgeComment):
    parent_circle_knowledge = models.ForeignKey("CircleKnowledge")

#
# ユーザーが入力する企業の基本情報
#
class CompanyKnowledge(models.Model):
    company_knowledge_id = models.SlugField(max_length=8)
    comment = models.CharField(max_length=200, null=True)

#
# その年の企業の情報
#
class CompanyKnowledgeData(models.Model):
    parent_company_knowledge = models.ForeignKey("CompanyKnowledge")
    comiket_number = models.PositiveSmallIntegerField()
    space_number = models.PositiveSmallIntegerField(null=True)
    company_name = models.CharField(max_length=30)
    url = models.URLField(max_length=256, null=True)
    description = models.CharField(max_length=400, null=True)

#
# CircleKnowledgeにひもづけされるKnowledgeDataの実装
#
class CompanyKnowledgeData(AbstractKnowledgeComment):
    parent_company_knowledge = models.ForeignKey("CompanyKnowledge")
