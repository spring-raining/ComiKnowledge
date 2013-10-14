# -*- coding: utf-8 -*-

import re
from django.forms import ValidationError

from ck.models import CKGroup
from src.utils import check_unique_group_id

def create_group(group_name, group_id):
    #check_unique_group_id(group_id)     # code=1
    #check_group_id_regex(group_id)      # code=2
    g = CKGroup()
    g.name = group_name
    g.group_id = group_id
    g.full_clean()
    g.save()
    return g

_group_id_regex = re.compile('^\w+$')
def check_group_id_regex(group_id):
    if not _group_id_regex.match(group_id):
        raise ValidationError("Invalid group_id", code=2)
    return group_id