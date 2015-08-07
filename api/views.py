# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from datetime import datetime

from ck.models import *

#
#   REST API用にHttpResponseをオーバーラップ
#
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json; charset=UTF-8'
        super(JSONResponse, self).__init__(content, **kwargs)

#
#   http methodに応じてディスパッチ
#
@csrf_exempt
def checklist(request, list_id):
    if request.method == "GET":
        return get_checklist(request, list_id)

def checklist_list(request):
    if request.method == "GET":
        return get_checklist_list(request)

def group(request, group_id):
    if request.method == "GET":
        return get_group(request, group_id)

def group_list(request):
    if request.method == "GET":
        return get_group_list(request)

def invited_group_list(request):
    if request.method == "GET":
        return get_invited_group_list(request)

#
#   get_checklist
#   GET     /api/v1/checklist/<list_id>/
#
def get_checklist(request, list_id):
    if list_id is None:
        return JSONResponse({}, status=404)
    try:
        list = List.objects.get(list_id=list_id)
    except:                                                             # list_idがおかしい
        return JSONResponse({}, status=404)
    if list.parent_user:
        if list.parent_user != request.user:                            # リストがログインしているユーザーのものでない
            return JSONResponse({}, status=404)
    elif list.parent_group:
        g = list.parent_group
        if not g.members.filter(id=request.user.id):                    # ユーザーがグループに属していない
            return JSONResponse({}, status=404)
        r = Relation.objects.get(ckgroup=g, ckuser=request.user)        # ユーザーがまだグループに参加していない
        if not r.verification:
            return JSONResponse({}, status=404)

    circles = list.listcircle_set.all().order_by("page_number", "cut_index")
    response = {}
    response["list_info"] = serializers.serialize("python", [list])[0]["fields"]
    response["circles"] = [d["fields"] for d in serializers.serialize("python", circles)]
    return JSONResponse(response, status=200)

#
#   get_checklist_list
#   GET     /api/v1/checklist/
#
def get_checklist_list(request):
    response ={}
    checklists = request.user.list_set.all()
    response["checklists"] = [d["fields"] for d in serializers.serialize("python", checklists)]
    return JSONResponse(response, status=200)

#
#   get_group
#   GET     /api/v1/group/<group_id>/
#
def get_group(request, group_id):
    if group_id is None:
        return JSONResponse({}, status=404)
    try:
        g = CKGroup.objects.get(group_id=group_id)
    except:                                                             # group_idがおかしい
        return JSONResponse({}, status=404)
    if not g.members.filter(id=request.user.id):                        # ユーザーがグループに属していない
        return JSONResponse({}, status=404)
    r = Relation.objects.get(ckgroup=g, ckuser=request.user)            # ユーザーがまだグループに参加していない
    if not r.verification:
        return JSONResponse({}, status=404)

    members = []
    inviting_members = []
    response = {}
    for i in g.members.all():
        r = Relation.objects.get(ckgroup=g.id, ckuser=i.id)
        if r.verification:
            members.append(i)
        else:
            inviting_members.append(i)
    for member in members:
        member.lists = member.list_set.all()
    response["group_info"] = serializers.serialize("python", [g])[0]["fields"]
    response["members"] = [d["fields"] for d in serializers.serialize("python", members)]
    response["inviting_members"] = [d["fields"] for d in serializers.serialize("python", inviting_members)]
    response["lists"] = [d["fields"] for d in serializers.serialize("python", g.list_set.all())]
    return JSONResponse(response, status=200)

#
#   get_group_list
#   GET     /api/v1/group/
#
def get_group_list(request):
    response = {}
    groups = []
    invited_groups = []
    for i in request.user.ckgroup_set.all():
        r = Relation.objects.get(ckgroup=i, ckuser=request.user)
        if r.verification:
            groups.append(i)
        else:
            invited_groups.append(i)
    response["groups"] = [d["fields"] for d in serializers.serialize("python", groups)]
    return JSONResponse(response, status=200)

#
#   get_invited_group_list
#   GET     /api/v1/invited_group/
#
def get_invited_group_list(request):
    response = {}
    groups = []
    invited_groups = []
    for i in request.user.ckgroup_set.all():
        r = Relation.objects.get(ckgroup=i, ckuser=request.user)
        if r.verification:
            groups.append(i)
        else:
            invited_groups.append(i)
    response["invited_groups"] = [d["fields"] for d in serializers.serialize("python", invited_groups)]
    return JSONResponse(response, status=200)
