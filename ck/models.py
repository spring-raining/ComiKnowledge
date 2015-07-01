# -*- coding: utf-8 -*-

import json
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
# extraカラムを追加するときはBaseExtraClassを継承
#
class BaseExtraCrass(models.Model):
    extra_json = models.TextField(default="{}")

    class Meta:
        abstract = True

    def _get_extra(self):
        return json.loads(self.extra_json)
    def _set_extra(self, dic):
        self.extra_json = json.dumps(dic)
    extra = property(_get_extra, _set_extra)


#
# ユーザーの拡張モデル
#
class CKUser(auth_models.User, BaseExtraCrass):
    thumbnail = models.ImageField(upload_to=THUMBNAILS_UPLOAD_TO, null=True)
    circlems_access_token = models.CharField(max_length=50, null=True)
    circlems_refresh_token = models.CharField(max_length=50, null=True)

#
# グループのモデル
#
class CKGroup(BaseExtraCrass):
    name = models.CharField(max_length=30)
    group_id = models.SlugField(max_length=30, unique=True, blank=False)
    members = models.ManyToManyField(CKUser, through="Relation", null=True)
    description = models.CharField(max_length=4000, null=True)

#
# グループとユーザーの関係を示す中間モデル
#
class Relation(BaseExtraCrass):
    ckuser = models.ForeignKey(CKUser)
    ckgroup = models.ForeignKey(CKGroup)
    verification = models.BooleanField(default=False)
    date_joined = models.DateTimeField(null=True)

#
# CSVリストのモデル
#
class List(BaseExtraCrass):
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
class ListCircle(BaseExtraCrass):
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
            return "%s%s%d%s" % (self.area, self.block, self.space_number, self.space_number_sub)

#
# CSVリストで記録されている未登録サークルのモデル
#
class ListUnKnown(BaseExtraCrass):
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
class ListColor(BaseExtraCrass):
    parent_list = models.ForeignKey(List)

    color_number = models.PositiveSmallIntegerField()
    check_color = models.CharField(max_length=6)
    print_color = models.CharField(max_length=6)
    description = models.CharField(max_length=4000, null=True)
