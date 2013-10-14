# -*- coding: utf-8 -*-

import string
import random
from django.forms import ValidationError

from ck.models import *

def check_unique_group_id(group_id):
    try:
        CKGroup.objects.get(group_id=group_id)
        raise ValidationError("Group id is already used.", code=1)
    except CKGroup.DoesNotExist:
        return group_id

def generate_rand_str(length=6):
    alphabets = string.digits + string.letters
    return "".join(random.choice(alphabets) for i in xrange(length))

