# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from datetime import datetime

from ck.models import *
from src.data.list import import_list, prepare_circle_obj
from src.error import *

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
@api_view(['POST'])
@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated,))
def obtain_token_by_session(request):
    if request.method == "POST":
        return post_obtain_token_by_session(request)

@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def checklist(request, list_id):
    if request.method == "GET":
        return get_checklist(request, list_id)
    if request.method == "POST":
        return post_checklist_circle(request, list_id)

@csrf_exempt
@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def checklist_on_delete(request, list_id):
    if request.method == "POST":
        return delete_checklist_circle(request, list_id)

@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def checklist_list(request):
    if request.method == "GET":
        return get_checklist_list(request)
    if request.method == "POST":
        return post_checklist(request)

@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def group(request, group_id):
    if request.method == "GET":
        return get_group(request, group_id)

@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def group_list(request):
    if request.method == "GET":
        return get_group_list(request)

@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def invited_group_list(request):
    if request.method == "GET":
        return get_invited_group_list(request)

#
#   obtain_token_by_session
#   POST    /api/v1/token
#
def post_obtain_token_by_session(request):
    (token, _) = Token.objects.get_or_create(user = request.user)
    return JSONResponse({"token": token.key}, status=201)

#
#   get_checklist
#   GET     /api/v1/checklist/<list_id>/
#
def get_checklist(request, list_id):
    list = _get_permitted_checklist_obj(request, list_id)
    if not list:
        return JSONResponse({}, status=404)

    circles = list.listcircle_set.all().order_by("page_number", "cut_index")
    response = {}
    response["list_info"] = serializers.serialize("python", [list])[0]["fields"]
    response["circles"] = [d["fields"] for d in serializers.serialize("python", circles)]
    return JSONResponse(response, status=200)

#
#   post_checklist_circle
#   POST    /api/v1/checklist/<list_id>/
#
def post_checklist_circle(request, list_id):
    list = _get_permitted_checklist_obj(request, list_id)
    if not list:
        return JSONResponse({}, status=404)
    try:
        circle = prepare_circle_obj(request.POST.dict(), request.user)
    except:
        return JSONResponse({"detail": "Invalid query."}, status=400)
    try:
        lc = list.listcircle_set.get(added_by=request.user, serial_number=circle.serial_number)
        lc.delete()
    except:
        pass
    finally:
        circle.parent_list = list
        circle.save()
    response = {}
    response["circle"] = serializers.serialize("python", [circle])[0]["fields"]
    return JSONResponse(response, status=200)


#
#   delete_checklist_circle
#   POST  /api/v1/checklist/<list_id>/delete/
#
def delete_checklist_circle(request, list_id):
    list = _get_permitted_checklist_obj(request, list_id)
    if not list:
        return JSONResponse({}, status=404)

    if not request.POST.get("serial_number") or not request.POST.get("serial_number").isdigit():
        return JSONResponse({"detail": "serial_number is required."}, status=400)
    try:
        serial_number = int(request.POST.get("serial_number"))
        lc = list.listcircle_set.get(added_by=request.user, serial_number=serial_number)
        lc.delete()
    except:
        return JSONResponse({"detail": "Circle not found."}, status=400)
    return JSONResponse({"detail": "Delete succeed."}, status=200)

#
#   get_checklist_list
#   GET     /api/v1/checklist/
#
def get_checklist_list(request):
    response = {}
    checklists = request.user.list_set.all()
    response["checklists"] = [d["fields"] for d in serializers.serialize("python", checklists)]
    return JSONResponse(response, status=200)

#
#   post_checklist
#   POST    /api/v1/checklist
#
def post_checklist(request):
    if not "csv" in request.data:
        return JSONResponse({"detail": "CSV file not found."}, status=400)
    csv_file = request.data.get("csv")
    try:
        l = import_list(csv_file, request.user)
        response = {
            "list_info": serializers.serialize("python", [l])[0]["fields"],
        }
        return JSONResponse(response, status=201)
    except (ChecklistInvalidError, ChecklistVersionError, TooMuchListsError) as err:
        return JSONResponse({"detail": str(err)}, status=400)

#
#   get_group
#   GET     /api/v1/group/<group_id>/
#
def get_group(request, group_id):
    g = _get_permitted_group_obj(request, group_id)
    if not g:
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



def _get_permitted_checklist_obj(request, list_id):
    if request is None or list_id is None:
        return None
    try:
        list = List.objects.get(list_id=list_id)
    except:                                                             # list_idがおかしい
        return None
    if list.parent_user:
        if list.parent_user != request.user:                            # リストがログインしているユーザーのものでない
            return None
    elif list.parent_group:
        g = list.parent_group
        if not g.members.filter(id=request.user.id):                    # ユーザーがグループに属していない
            return None
        r = Relation.objects.get(ckgroup=g, ckuser=request.user)        # ユーザーがまだグループに参加していない
        if not r.verification:
            return None
    return list

def _get_permitted_group_obj(request, group_id):
    if request is None or group_id is None:
        return None
    try:
        group = CKGroup.objects.get(group_id=group_id)
    except:                                                             # group_idがおかしい
        return None
    if not group.members.filter(id=request.user.id):                    # ユーザーがグループに属していない
        return None
    r = Relation.objects.get(ckgroup=group, ckuser=request.user)        # ユーザーがまだグループに参加していない
    if not r.verification:
        return None
    return group