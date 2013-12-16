# -*- coding: utf-8 -*-

import json
from django.contrib.auth.decorators import login_required
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form

from ck.views import *
from src.data.group import *
from src.data.list import *
from src.data.knowledge import *

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


@dajaxice_register
def ajax_reject_join(request, group_id):
    g = CKGroup.objects.get(group_id=group_id)
    leave_group(g, request.user)
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
def ajax_create_list(request, form):
    print "a"
    post = deserialize_form(form)
    response = {}
    if request.method != "POST":
        return
    if not post["list_name"]:
        alert_code = 2
    else:
        try:
            l = create_list(post["list_name"], request.user)
            response["list_name"] = l.list_name
            response["list_id"] = l.list_id
            alert_code = 1
        except:
            alert_code = 3
    response["alert_code"] = alert_code
    return json.dumps(response)

@dajaxice_register
def ajax_leave_group(request, group_id):
    g = CKGroup.objects.get(group_id=group_id)
    leave_group(g, request.user)
    return json.dumps({})

@dajaxice_register
def ajax_delete_listcircle(request, listcircle_id):
    l = ListCircle.objects.get(id=listcircle_id)
    l.delete()
    return json.dumps({"id": listcircle_id})

@dajaxice_register
def ajax_register_circleknowledgecomment(request, post):
    response = {}
    response["post"] = post
    try:
        ck = CircleKnowledge.objects.get(circle_knowledge_id = post["circle_knowledge_id"])
        if post["mode"] == 1:
            if post["start-hour"] < 10 or post["start-hour"] > 14 \
                or post["start-min"] < 0 or post["start-min"] > 59 \
                or post["finish-hour"] < 10 or post["finish-hour"] > 14 \
                or post["finish-min"] < 0 or post["finish-min"] > 59 \
                or (post["start-hour"]*60 + post["start-min"]) > (post["finish-hour"]*60 + post["finish-min"]):
                response["alert_code"] = 2
            else:
                try:
                    register_circleknowledgecomment(parent_circle_knowledge=ck, parent_user=request.user,
                                                    comiket_number=src.COMIKET_NUMBER, comment=post["comment"],
                                                    event_code=1, onymous=post["onymous"],
                                                    start_time_hour=post["start-hour"], start_time_min=post["start-min"],
                                                    finish_time_hour=post["finish-hour"], finish_time_min=post["finish-min"])
                    request.session["alert_code"] = 3
                    response["alert_code"] = 1
                except TooMuchCommentsError:
                    response["alert_code"] = 3
        elif post["mode"] == 2:
            if post["event-hour"] < 10 or post["event-hour"] > 14 \
                or post["event-min"] < 0 or post["event-min"] > 59:
                response["alert_code"] = 2
            else:
                try:
                    register_circleknowledgecomment(parent_circle_knowledge=ck, parent_user=request.user,
                                                    comiket_number=src.COMIKET_NUMBER, comment=post["comment"],
                                                    event_code=post["event"], onymous=post["onymous"],
                                                    event_time_hour=post["event-hour"], event_time_min=post["event-min"])
                    request.session["alert_code"] = 3
                    response["alert_code"] = 1
                except TooMuchCommentsError:
                    response["alert_code"] = 3
        else:
            response["alert_code"] = 4
    except:
        response["alert_code"] = 4
    return json.dumps(response)


@dajaxice_register
def ajax_delete_circleknowledgecomment(request, comment_id):
    if delete_circleknowledgecomment(comment_id):
        request.session["alert_code"] = 4
        return json.dumps({"alert_code": 1})
    else:
        return json.dumps({"alert_code": 2})