# -*- coding: utf-8 -*-

from django.contrib import admin
from ck.models import *

class Admin(admin.ModelAdmin):
    pass

admin.site.register(List, Admin)