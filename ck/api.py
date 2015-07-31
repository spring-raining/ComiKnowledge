# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound

from datetime import datetime
import json

from models import *

#
#   http methodに応じてディスパッチ
#
@login_required
def checklist(request, list_id):
    if request.method == "GET":
        return get_checklist(request, list_id)

@login_required
def checklist_list(request):
    if request.method == "GET":
        return get_checklist_list(request)

@login_required
def group(request, group_id):
    if request.method == "GET":
        return get_group(request, group_id)

@login_required
def group_list(request):
    if request.method == "GET":
        return get_group_list(request)

@login_required
def invited_group_list(request):
    if request.method == "GET":
        return get_invited_group_list(request)

#
#   get_checklist
#   GET     /api/v1/checklist/<list_id>/
#
def get_checklist(request, list_id):
    if list_id is None:
        return _base_json_response_404(request)
    try:
        list = List.objects.get(list_id=list_id)
    except:                                                             # list_idがおかしい
        return _base_json_response_404(request)
    if list.parent_user:
        if list.parent_user != request.user:                            # リストがログインしているユーザーのものでない
            return _base_json_response_404(request)
    elif list.parent_group:
        g = list.parent_group
        if not g.members.filter(id=request.user.id):                    # ユーザーがグループに属していない
            return _base_json_response_404(request)
        r = Relation.objects.get(ckgroup=g, ckuser=request.user)        # ユーザーがまだグループに参加していない
        if not r.verification:
            return _base_json_response_404(request)

    circles = list.listcircle_set.all().order_by("page_number", "cut_index")
    response = {}
    response["list_info"] = serializers.serialize("python", [list])[0]["fields"]
    response["circles"] = [d["fields"] for d in serializers.serialize("python", circles)]
    return _base_json_response(request, response)

#
#   get_checklist_list
#   GET     /api/v1/checklist/
#
def get_checklist_list(request):
    response ={}
    checklists = request.user.list_set.all()
    response["checklists"] = [d["fields"] for d in serializers.serialize("python", checklists)]
    return _base_json_response(request, response)

#
#   get_group
#   GET     /api/v1/group/<group_id>/
#
def get_group(request, group_id):
    if group_id is None:
        return _base_json_response_404(request)
    try:
        g = CKGroup.objects.get(group_id=group_id)
    except:                                                             # group_idがおかしい
        return _base_json_response_404(request)
    if not g.members.filter(id=request.user.id):                        # ユーザーがグループに属していない
        return _base_json_response_404(request)
    r = Relation.objects.get(ckgroup=g, ckuser=request.user)            # ユーザーがまだグループに参加していない
    if not r.verification:
        return _base_json_response_404(request)

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
    return _base_json_response(request, response)

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
    return _base_json_response(request, response)

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
    return _base_json_response(request, response)



def _base_json_response(request, data, status=None):
    return HttpResponse(json.dumps(data, ensure_ascii=False, default=_json_dumper_default),
                        content_type="application/json; charset=UTF-8",
                        status=status)

def _base_json_response_404(request, data=None, status=None):
    _data = {} if data is None else data
    return HttpResponseNotFound(json.dumps(_data, ensure_ascii=False, default=_json_dumper_default),
                                content_type="application/json; charset=UTF-8",
                                status=status)

def _json_dumper_default(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(repr(o) + "is not JSON serializable")