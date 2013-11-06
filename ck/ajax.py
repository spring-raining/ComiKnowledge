# -*- coding: utf-8 -*-

import json
from django.contrib.auth.decorators import login_required
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form

from src.data.group import *
from src.data.list import *

@dajaxice_register
def ajax_create_group(request, form):
    post = deserialize_form(form)
    response = {}
    if request.method != "POST":
        return
    try:
        g = create_group(post["group_name"], post["group_id"])
        add_member(g, request.user)
        alert_code = 1
        response["group_name"] = g.name
        response["group_id"] = g.group_id
    except FormBlankError:
        alert_code = 2
    except FormDuplicateError:
        alert_code = 3
    except FormInvalidError:
        alert_code = 4
    response["alert_code"] = alert_code
    return json.dumps(response)


@dajaxice_register
def ajax_update_group_description(request, form):
    post = deserialize_form(form)
    g = CKGroup.objects.get(group_id=post["group_id"])
    g.description = post["description"]
    g.save()
    return json.dumps({"description": g.description})


@dajaxice_register
def ajax_request_join(request, form):
    post = deserialize_form(form)
    response = {}
    if request.method != "POST":
        return

    response["user_id"] = post["user_id"]
    try:
        if request_join(post["group_id"], post["user_id"]):
            alert_code = 1
        else:
            alert_code = 4
    except FormBlankError:
        alert_code = 2
    except CKUser.DoesNotExist:
        alert_code = 3
    response["alert_code"] = alert_code
    return json.dumps(response)


@dajaxice_register
def ajax_verify_join(request, group_id):
    g = CKGroup.objects.get(group_id=group_id)
    verify_join(g, request.user)
    return json.dumps({"group_name": g.name, "group_id": g.group_id})


# 未実装
@dajaxice_register
def ajax_import_list(request, form):
    post = deserialize_form(form)
    response = {}
    if request.method != "POST":
        return
    try:
        l = import_list(post["csv"], request.user.username)
        response["list_name"] = l.list_name
        alert_code = 1
    except ChecklistInvalidError:
        alert_code = 2
    response["alert_code"] = alert_code
    return json.dumps(response)


@dajaxice_register
def ajax_delete_list(request, list_id):
    if delete_list(list_id):
        return json.dumps({"list_id": list_id})


@dajaxice_register
def ajax_leave_group(request, group_id):
    g = CKGroup.objects.get(group_id=group_id)
    leave_group(g, request.user)
    return json.dumps({})