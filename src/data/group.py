# -*- coding: utf-8 -*-

import re
from django.forms import ValidationError

from ck.models import CKGroup, CKUser, Relation
from src.utils import check_unique_group_id

def create_group(group_name, group_id):
    g = CKGroup(group_id=group_id, name=group_name)
    #g.full_clean()
    g.save()
    return g

# グループにユーザーを強制的に追加(verification=True)
def add_member(ckgroup, ckuser):
    try:
        r = Relation.objects.get(ckgroup=ckgroup, ckuser=ckuser)
        r.verification = True
    except Relation.DoesNotExist:
        r = Relation(ckgroup=ckgroup, ckuser=ckuser, verification=True)
    r.save()

# グループにユーザーを招待(verification=False)
def request_join(ckgroup, ckuser):
    try:
        Relation.objects.get(ckgroup=ckgroup, ckuser=ckuser)
    except Relation.DoesNotExist:
        r = Relation(ckgroup=ckgroup, ckuser=ckuser, verification=False)
        r.save()
        return True
    return False

# 招待されたグループに参加(verificationをTrueに)
def verify_join(group_id, user_id):
    r = Relation.objects.get(ckgroup=group_id, ckuser=user_id)
    r.verification = True
    r.save()