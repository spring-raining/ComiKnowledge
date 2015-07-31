# -*- coding: utf- -*-

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse

import json

from models import *

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

def get_checklist(request, list_id):
    response ={}
    checklists = request.user.list_set.all()
    response["checklists"] = [d["fields"] for d in serializers.serialize("python", checklists)]
    return _base_json_response(request, response)

def get_checklist_list(request):
    return _base_json_response(request, {})

def get_group(request, group_id):
    return _base_json_response(request, {})

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
    response["invited_groups"] = [d["fields"] for d in serializers.serialize("python", invited_groups)]

    return _base_json_response(request, response)

def _base_json_response(request, data, status=None):
    return HttpResponse(json.dumps(data, ensure_ascii=False),
                        content_type="application/json; charset=UTF-8",
                        status=status)