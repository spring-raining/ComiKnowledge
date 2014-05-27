# -*- coding: utf-8 -*-

import json
from django.contrib.auth.decorators import login_required
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form

#from ck.views import *

from ck.models import *
from src.data.group import *
from src.data.list import *
from src.data.knowledge import *

GROUP_LIMIT = 30

@dajaxice_register
def ajax_create_group(request, form):
    post = deserialize_form(form)
    response = {}
    if request.method != "POST":
        return
    rs = request.user.relation_set.all()
    count = 0
    for i in rs:
        if i.verification:
            count += 1
    if count >= GROUP_LIMIT:
        alert_code = 5
    else:
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
    response = {}
    rs = request.user.relation_set.all()
    count = 0
    for i in rs:
        if i.verification:
            count += 1
    if count >= GROUP_LIMIT:
        alert_code = 2
    else:
        g = CKGroup.objects.get(group_id=group_id)
        verify_join(g, request.user)
        alert_code = 1
        response["group_name"] = g.name
        response["group_id"] = g.group_id
    response["alert_code"] = alert_code
    return json.dumps(response)


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
    if delete_circleknowledgecomment(comment_id=comment_id, parent_user=request.user):
        request.session["alert_code"] = 4
        return json.dumps({"alert_code": 1})
    else:
        return json.dumps({"alert_code": 2})


@dajaxice_register
def ajax_register_companyknowledgecomment(request, post):
    response = {}
    response["post"] = post
    try:
        ck = CompanyKnowledge.objects.get(company_knowledge_id = post["company_knowledge_id"])
        if post["mode"] == 1:
            if post["start-hour"] < 10 or post["start-hour"] > 14 \
                or post["start-min"] < 0 or post["start-min"] > 59 \
                or post["finish-hour"] < 10 or post["finish-hour"] > 14 \
                or post["finish-min"] < 0 or post["finish-min"] > 59 \
                or (post["start-hour"]*60 + post["start-min"]) > (post["finish-hour"]*60 + post["finish-min"]):
                response["alert_code"] = 2
            else:
                try:
                    register_companyknowledgecomment(parent_company_knowledge=ck, parent_user=request.user,
                                                    comiket_number=src.COMIKET_NUMBER, comment=post["comment"],
                                                    event_code=1, onymous=post["onymous"], day=post["day"],
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
                    register_companyknowledgecomment(parent_company_knowledge=ck, parent_user=request.user,
                                                    comiket_number=src.COMIKET_NUMBER, comment=post["comment"],
                                                    event_code=post["event"], onymous=post["onymous"], day=post["day"],
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
def ajax_delete_companyknowledgecomment(request, comment_id):
    if delete_companyknowledgecomment(comment_id=comment_id, parent_user=request.user):
        request.session["alert_code"] = 4
        return json.dumps({"alert_code": 1})
    else:
        return json.dumps({"alert_code": 2})


@dajaxice_register
def ajax_get_circleknowledgecomments(request, circle_knowledge_id):
    comments = {}
    try:
        ck = CircleKnowledge.objects.get(circle_knowledge_id=circle_knowledge_id)
        for i in range(80, src.COMIKET_NUMBER+1):
            _ckc = ck.circleknowledgecomment_set.filter(comiket_number=i)
            comments[i] = sorted(_ckc, key=lambda x:
                x.start_time_hour * 60 + x.start_time_min if x.start_time_hour else x.event_time_hour * 60 + x.event_time_min)
    except:
        return

    response = {}
    for num, comments_ in comments.items():
        a = []
        for com in comments_:
            b = {}
            b["event_code"] = com.event_code
            b["start_time_hour"] = com.start_time_hour
            b["start_time_min"] = com.start_time_min
            b["finish_time_hour"] = com.finish_time_hour
            b["finish_time_min"] = com.finish_time_min
            b["event_time_hour"] = com.event_time_hour
            b["event_time_min"] = com.event_time_min
            b["id"] = com.id
            b["comment"] = com.comment
            b["onymous"] = com.onymous
            if com.onymous:
                #b["parent_user__thumbnail"] = c.parent_user.thumbnail
                b["parent_user__thumbnail__url"] = com.parent_user.thumbnail.url
                b["parent_user__username"] = com.parent_user.username
            b["is_my_comment"] = (request.user == com.parent_user)
            a.append(b)
        response[num] = a
    return json.dumps(response)


@dajaxice_register
def ajax_get_companyknowledgecomments(request, company_knowledge_id):
    comments = {}
    try:
        ck = CompanyKnowledge.objects.get(company_knowledge_id=company_knowledge_id)
        for i in range(80, src.COMIKET_NUMBER+1):
            _ckc = ck.companyknowledgecomment_set.filter(comiket_number=i)
            comments[i] = sorted(_ckc, key=lambda x:
                x.start_time_hour * 60 + x.start_time_min if x.start_time_hour else x.event_time_hour * 60 + x.event_time_min)
    except:
        return

    response = {}
    for num, comments_ in comments.items():
        a = {1: [], 2: [], 3: []}

        for com in comments_:
            b = {}
            day = com.day
            b["event_code"] = com.event_code
            b["start_time_hour"] = com.start_time_hour
            b["start_time_min"] = com.start_time_min
            b["finish_time_hour"] = com.finish_time_hour
            b["finish_time_min"] = com.finish_time_min
            b["event_time_hour"] = com.event_time_hour
            b["event_time_min"] = com.event_time_min
            b["id"] = com.id
            b["comment"] = com.comment
            b["day"] = day
            b["onymous"] = com.onymous
            if com.onymous:
                #b["parent_user__thumbnail"] = c.parent_user.thumbnail
                b["parent_user__thumbnail__url"] = com.parent_user.thumbnail.url
                b["parent_user__username"] = com.parent_user.username
            b["is_my_comment"] = (request.user == com.parent_user)
            a[day].append(b)
        response[num] = a
    return json.dumps(response)