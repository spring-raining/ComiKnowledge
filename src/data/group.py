# -*- coding: utf-8 -*-

import re
from django.db import IntegrityError

from ck.models import CKGroup, CKUser, Relation
from src.error import FormBlankError, FormDuplicateError, FormInvalidError

def create_group(group_name, group_id):
    if not group_name:
        raise FormBlankError("group_name")
    if not group_id:
        raise FormBlankError("group_id")
    if re.search("\W+", group_id) is not None:
        raise FormInvalidError("group_id")
    try:
        g = CKGroup(group_id=group_id, name=group_name)
        g.save()
        return g
    except IntegrityError:
        raise FormDuplicateError("group_id")

# グループにユーザーを強制的に追加(verification=True)
def add_member(ckgroup, ckuser):
    try:
        r = Relation.objects.get(ckgroup=ckgroup, ckuser=ckuser)
        r.verification = True
    except Relation.DoesNotExist:
        r = Relation(ckgroup=ckgroup, ckuser=ckuser, verification=True)
    r.save()

# グループにユーザーを招待(verification=False)
def request_join(group_id, username):
    if not username:
        raise FormBlankError("user_id")                                 # user_idが空
    try:
        g = CKGroup.objects.get(group_id=group_id)
        u = CKUser.objects.get(username=username)
        r = Relation.objects.get(ckgroup=g, ckuser=u)
        if r.verification:                                              # すでにグループに属している
            return False
        else:                                                           # リクエスト送信済み
            return True
    except CKUser.DoesNotExist:                                         # ユーザーがいない
        raise
    except Relation.DoesNotExist:
        r = Relation(ckgroup=g, ckuser=u, verification=False)
        r.save()
        return True

# 招待されたグループに参加(verificationをTrueに)
def verify_join(group, user):
    r = Relation.objects.get(ckgroup=group, ckuser=user)
    r.verification = True
    r.save()

# グループから抜ける(招待を拒否)
def leave_group(group, user):
    r = Relation.objects.get(ckgroup=group, ckuser=user)
    r.delete()
    if len(group.members.all()) == 0:
        group.delete()
