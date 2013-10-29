# -*- coding: utf-8 -*-

import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import loader, RequestContext
from social_auth.db.django_models import UserSocialAuth
from dajaxice.decorators import dajaxice_register

from ComiKnowledge import settings
from ck.models import *
from src.api.twitter import *
from src.data.list import *
from src.data.group import *


def index(request):
    t = loader.get_template("index.html")
    if request.user.is_authenticated():
        return HttpResponseRedirect("/home/")
    c = RequestContext(request,
                       {"test": "hello!"})
    return HttpResponse(t.render(c))


@login_required
def home(request):
    # 招待されているグループがあるかチェック
    invited_groups = []
    for i in request.user.ckgroup_set.all():
        r = Relation.objects.get(ckgroup=i, ckuser=request.user)
        if r.verification == False:
            invited_groups.append(i)

    # サムネイル更新
    if not request.user.thumbnail or not os.path.exists(os.path.join(settings.MEDIA_ROOT, request.user.thumbnail.name)):
        usa = UserSocialAuth.objects.get(user_id=request.user.id)
        save_twitter_icon(request.user, usa.tokens["oauth_token"], usa.tokens["oauth_token_secret"])

    ctx = RequestContext(request,
                         {"test": "hello! now login",
                          "user": request.user,
                          "invited_groups": invited_groups})
    return render_to_response("home.html", ctx)


@login_required
def checklist(request):
    alert_code = 0
    response = {}

    # チェックリスト読み込み
    if request.method == "POST":
        if not "csv" in request.FILES:
            alert_code = 2
        else:
            csv_file = request.FILES["csv"]
            try:
                l = import_list(csv_file ,request.user)
                response["list_name"] = l.list_name
                alert_code = 1
            except ChecklistInvalidError:
                alert_code = 3

    response["alert_code"] = alert_code
    response["lists"] = request.user.list_set.all()
    c = RequestContext(request, response)
    return render_to_response("checklist.html", c)


@login_required
def checklist_download(request, list_id):
    if list_id is None:
        return HttpResponseRedirect("/")
    try:
        l = List.objects.get(list_id=list_id)
    except:                                                             # list_idがおかしい
        raise Http404
    if l.parent_user:
        if l.parent_user != request.user:                               # リストがログインしているユーザーのものでない
            raise Http404
        response = HttpResponse(mimetype="text/comma-separated-values; charset=utf-8")
        response["Content-Disposition"] = (u'attachment; filename="%s.csv"' % l.list_name).encode("utf-8")
        return output_list(response, l.list_id, memo_template=u"{memo}")
    elif l.parent_group:
        g = l.parent_group
        if not g.members.filter(id=request.user.id):                    # ユーザーがグループに属していない
            raise Http404
        r = Relation.objects.get(ckgroup=g, ckuser=request.user)        # ユーザーがまだグループに参加していない
        if r.verification == False:
            raise Http404
        response = HttpResponse(mimetype="text/comma-separated-values; charset=utf-8")
        response["Content-Disposition"] = (u'attachment; filename="%s.csv"' % l.list_name).encode("utf-8")
        return output_list(response, l.list_id, memo_template=u"{memo}({username}), ")
        #c = RequestContext(request)
        #return render_to_response("checklist_download.html", c)


@login_required
def checklist_edit(request, list_id):
    if list_id is None:
        raise Http404
    try:
        l = List.objects.get(list_id=list_id)
    except:                                                             # list_idがおかしい
        raise Http404
    if l.parent_user:
        if l.parent_user != request.user:                               # リストがログインしているユーザーのものでない
            raise Http404
    elif l.parent_group:
        g = l.parent_group
        if not g.members.filter(id=request.user.id):                    # ユーザーがグループに属していない
            raise Http404
        r = Relation.objects.get(ckgroup=g, ckuser=request.user)        # ユーザーがまだグループに参加していない
        if r.verification == False:
            raise Http404

    c = RequestContext(request,
                       {"list": l,
                       "circles": l.listcircle_set.all()})
    return render_to_response("checklist_edit.html", c)


@login_required
def group(request):
    alert_code = 0
    groups = []
    invited_groups = []
    for i in request.user.ckgroup_set.all():
        r = Relation.objects.get(ckgroup=i, ckuser=request.user)
        if r.verification == True:
            groups.append(i)
        else:
            invited_groups.append(i)
    c = RequestContext(request,
                       {"groups": groups,
                        "invited_groups": invited_groups,
                        "alert_code": alert_code})
    return render_to_response("group.html", c)


@login_required
def group_home(request, group_id):
    if group_id is None:
        raise Http404
    try:
        g = CKGroup.objects.get(group_id=group_id)
    except:                                                             # group_idがおかしい
        raise Http404
    if not g.members.filter(id=request.user.id):                        # ユーザーがグループに属していない
        raise Http404
    r = Relation.objects.get(ckgroup=g, ckuser=request.user)            # ユーザーがまだグループに参加していない
    if r.verification == False:
        raise Http404

    if request.GET.has_key("command"):
        if request.GET["command"] == "leave":
            pass

    members = []
    inviting_members = []
    response = {}
    for i in g.members.all():
        r = Relation.objects.get(ckgroup=g.id, ckuser=i.id)
        if r.verification == True:
            members.append(i)
        else:
            inviting_members.append(i)
    for member in members:
        member.lists = member.list_set.all()
    response["group"] = g
    response["members"] = members
    response["inviting_members"] = inviting_members
    response["lists"] = g.list_set.all()
    c = RequestContext(request, response)
    return render_to_response("group_home.html", c)


@login_required
def group_checklist_create(request, group_id):
    if group_id is None:
        raise Http404
    try:
        g = CKGroup.objects.get(group_id=group_id)
    except:                                                             # group_idがおかしい
        raise Http404
    if not g.members.filter(id=request.user.id):                        # ユーザーがグループに属していない
        raise Http404
    r = Relation.objects.get(ckgroup=g, ckuser=request.user)            # ユーザーがまだグループに参加していない
    if r.verification == False:
        raise Http404

    response = {}
    alert_code = 0
    if request.method == "POST":
        if not request.POST["list_name"]:
            alert_code = 2
        elif not request.POST.getlist("list[]"):
            alert_code = 3
        else:
            lists = request.POST.getlist("list[]")
            if "first" in request.POST:
                first = request.POST["first"]
                if first in lists:
                    del lists[lists.index(first)]
                    lists.insert(0, first)
            l = []
            for i in lists:
                l.append(List.objects.get(id=i))
            try:
                merge_list(l, g, request.POST["list_name"])
                response["list_name"] = request.POST["list_name"]
                alert_code = 1
            except:
                alert_code = 4

    members = []
    for i in g.members.all():
        r = Relation.objects.get(ckgroup=g.id, ckuser=i.id)
        if r.verification == True:
            members.append(i)
    for member in members:
        member.lists = member.list_set.all()
    response["group"] = g
    response["members"] = members
    response["alert_code"] = alert_code
    c = RequestContext(request, response)
    return render_to_response("group_checklist_create.html", c)


def login(request):
    return HttpResponseRedirect("/login/twitter/")


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")
