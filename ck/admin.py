# -*- coding: utf-8 -*-

from django.contrib import admin
from ck.models import *

class Admin(admin.ModelAdmin):
    pass

admin.site.register(CKGroup, Admin)
admin.site.register(Relation, Admin)
admin.site.register(List, Admin)
admin.site.register(ListCircle, Admin)
admin.site.register(ListUnKnown, Admin)
admin.site.register(ListColor, Admin)
