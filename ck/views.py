# -*- coding: utf-8 -*-

import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import loader, RequestContext
from social_auth.db.django_models import UserSocialAuth

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
    if request.method == "POST":
        csv_file = request.FILES["csv"]
        import_list(csv_file ,request.user)
    if request.GET.has_key("command"):
        if request.GET["command"] == "delete":
            delete_list(request.GET["id"])
            return HttpResponseRedirect("/checklist/")
        if request.GET["command"] == "save":
            response = HttpResponse(mimetype="text/comma-separated-values; charset=utf-8")
            response["Content-Disposition"] = "attachment; filename=%s.csv" % List.objects.get(list_id=request.GET["id"]).list_name
            return output_list(response, request.GET["id"], memo_template="{memo}({userid}) ")
    c = RequestContext(request,
                       {"lists": request.user.list_set.all()})
    return render_to_response("checklist.html", c)


@login_required
def checklist_edit(request, list_id):
    if list_id is None:
        return HttpResponseRedirect("/checklist/")
    if request.GET.has_key("command"):
        if request.GET["command"] == "delete":
            delete_circle(request.GET["id"])
            return HttpResponseRedirect("/checklist/" + list_id)
    try:
        l = List.objects.get(list_id=list_id)
    except:
        raise Http404

    c = RequestContext(request,
                       {"list": l,
                       "circles": l.listcircle_set.all()})
    return render_to_response("checklist_edit.html", c)


@login_required
def group(request):
    alert_code = 0
    created_group = None
    if request.method == "POST":
        try:
            g = create_group(request.POST["group_name"], request.POST["group_id"])
            add_member(g, request.user)
            alert_code = 1
            created_group = g
        except FormBlankError:
            alert_code = 2
        except FormDuplicateError:
            alert_code = 3

    if request.GET.has_key("command"):
        if request.GET["command"] == "join":
            verify_join(request.GET["id"], request.user.id)

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
                        "alert_code": alert_code,
                        "created_group": created_group})
    return render_to_response("group.html", c)


@login_required
def group_home(request, group_id):
    if group_id is None:
        return HttpResponseRedirect("/group/")
    try:
        g = CKGroup.objects.get(group_id=group_id)
    except:                                                             # group_idがおかしい
        raise Http404
    if not g.members.filter(id=request.user.id):                        # ユーザーがグループに属していない
        raise Http404
    r = Relation.objects.get(ckgroup=g, ckuser=request.user)            # ユーザーがまだグループに参加していない
    if r.verification == False:
        raise Http404

    if request.method == "POST":
        try:
            u = CKUser.objects.get(username=request.POST["name"])
            if request_join(g, u):
                print "Sent join request!"
            else:                                                       # リクエスト送信済み
                pass
        except CKUser.DoesNotExist:                                     # ユーザーがいない
            pass

    if request.GET.has_key("command"):
        if request.GET["command"] == "leave":
            pass

    members = []
    inviting_members = []
    for i in g.members.all():
        r = Relation.objects.get(ckgroup=g.id, ckuser=i.id)
        if r.verification == True:
            members.append(i)
        else:
            inviting_members.append(i)
    for member in members:
        member.lists = member.list_set.all()
    c = RequestContext(request,
                       {"group": g,
                        "members": members,
                        "inviting_members": inviting_members})
    return render_to_response("group_home.html", c)


@login_required
def group_checklist_create(request, group_id):
    if group_id is None:
        return HttpResponseRedirect("/group/")
    try:
        g = CKGroup.objects.get(group_id=group_id)
    except:                                                             # group_idがおかしい
        raise Http404
    if not g.members.filter(id=request.user.id):                        # ユーザーがグループに属していない
        raise Http404
    r = Relation.objects.get(ckgroup=g, ckuser=request.user)            # ユーザーがまだグループに参加していない
    if r.verification == False:
        raise Http404

    if request.method == "POST":
        lists = request.POST.getlist("list[]")
        first = request.POST["first"]
        if lists and first and first in lists:
            del lists[lists.index(first)]
            lists.insert(0, first)
            l = []
            for i in lists:
                l.append(List.objects.get(id=i))
            merge_list(l, request.user)

    members = []
    for i in g.members.all():
        r = Relation.objects.get(ckgroup=g.id, ckuser=i.id)
        if r.verification == True:
            members.append(i)
    for member in members:
        member.lists = member.list_set.all()
    c = RequestContext(request,
                       {"group": g,
                        "members": members})
    return render_to_response("group_checklist_create.html", c)


def login(request):
    return HttpResponseRedirect("/login/twitter/")


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")
