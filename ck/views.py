# -*- coding: utf-8 -*-

import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.core.paginator import Paginator
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotModified, Http404, QueryDict
from django.shortcuts import render_to_response
from django.template import loader, RequestContext
from social_auth.db.django_models import UserSocialAuth
from allauth.socialaccount.models import SocialToken, SocialAccount
import urllib

from ComiKnowledge import settings
from ck.models import *
import src
from src.api.twitter import *
from src.data.list import *
from src.utils import *


def index(request):
    t = loader.get_template("index.html")
    if request.user.is_authenticated():
        return HttpResponseRedirect("/home/")
    response = _base_response(request)
    ctx = RequestContext(request, response)
    return HttpResponse(t.render(ctx))


def tutorial(request):
    response = _base_response(request)
    ctx = RequestContext(request, response)
    return render_to_response("tutorial.html", ctx)


@login_required
def home(request):
    response = _base_response(request)
    # 招待されているグループがあるかチェック
    invited_groups = []
    for i in request.user.ckgroup_set.all():
        r = Relation.objects.get(ckgroup=i, ckuser=request.user)
        if not r.verification:
            invited_groups.append(i)
    response["invited_groups"] = invited_groups

    # サムネイル更新
    if not request.user.thumbnail or not os.path.exists(os.path.join(settings.MEDIA_ROOT, request.user.thumbnail.name)):
        st = SocialToken.objects.get(account_id=SocialAccount.objects.get(user_id=request.user.id))
        save_twitter_icon(request.user, st.token, st.token_secret)

    ctx = RequestContext(request, response)
    return render_to_response("home.html", ctx)


@login_required
def checklist(request):
    alert_code = 0
    response = _base_response(request)

    # チェックリスト読み込み
    if request.method == "POST":
        if not "csv" in request.FILES:
            alert_code = 2
        else:
            csv_file = request.FILES["csv"]
            try:
                l = import_list(csv_file, request.user)
                response["list_name"] = l.list_name
                alert_code = 1
            except ChecklistInvalidError:
                alert_code = 3
            except ChecklistVersionError:
                alert_code = 4
            except TooMuchListsError:
                alert_code = 5

    response["alert_code"] = alert_code
    response["lists"] = request.user.list_set.all()
    ctx = RequestContext(request, response)
    return render_to_response("checklist.html", ctx)


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
        if not r.verification:
            raise Http404

        option = l.extra["group_list_option"]
        response = HttpResponse(mimetype="text/comma-separated-values; charset=utf-8")
        response["Content-Disposition"] = (u'attachment; filename="%s.csv"' % l.list_name).encode("utf-8")
        return output_list(response, l.list_id,
                           memo_template=option["memo"],
                           color_option=option["color_option"],
                           color_order=tuple(option["color_order"]),
                           select_color=option["select_color"])


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
        if not r.verification:
            raise Http404

    if request.GET.has_key("sort"):
        if request.GET["sort"] == "color":
            l_all = l.listcircle_set.all().order_by("color_number")
        elif request.GET["sort"] == "space":
            l_all = l.listcircle_set.all().order_by("page_number", "cut_index")
        elif request.GET["sort"] == "circle":
            l_all = l.listcircle_set.all().order_by("circle_name")
        elif request.GET["sort"] == "check":
            l_all = l.listcircle_set.all().order_by("added_by")
        elif request.GET["sort"] == "memo":
            l_all = l.listcircle_set.all().order_by("memo")
        else:
            l_all = l.listcircle_set.all().order_by("page_number", "cut_index")
    else:
        l_all = l.listcircle_set.all().order_by("page_number", "cut_index")

    response = _base_response(request)
    color = {}
    for i in l.listcolor_set.all():
        if i.check_color:
            color[i.color_number] = "#" + i.check_color

    response["list"] = l
    response["circles"] = l_all
    response["color"] = color
    ctx = RequestContext(request, response)
    return render_to_response("checklist_edit.html", ctx)


@login_required
def group(request):
    alert_code = 0
    groups = []
    invited_groups = []
    response = _base_response(request)
    for i in request.user.ckgroup_set.all():
        r = Relation.objects.get(ckgroup=i, ckuser=request.user)
        if r.verification:
            groups.append(i)
        else:
            invited_groups.append(i)
    response["groups"] = groups
    response["invited_groups"] = invited_groups
    response["alert_code"] = alert_code
    ctx = RequestContext(request, response)
    return render_to_response("group.html", ctx)


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
    if not r.verification:
        raise Http404

    members = []
    inviting_members = []
    response = _base_response(request)
    if "alert_code" in request.session:
        response["alert_code"] = request.session["alert_code"]
        response["list_name"] = request.session["list_name"]
        del request.session["alert_code"]
        del request.session["list_name"]
    for i in g.members.all():
        r = Relation.objects.get(ckgroup=g.id, ckuser=i.id)
        if r.verification:
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
    if not r.verification:
        raise Http404

    response = _base_response(request)
    alert_code = 0
    if request.method == "POST":
        response["list_name"] = request.POST["list_name"]
        response["lists"] = request.POST.getlist("list[]")
        if "first" in request.POST:
            response["first"] = request.POST["first"]
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
                l = merge_list(l, g, request.POST["list_name"])
                l.extra = {"group_list_option":{"memo": request.POST["memo"],
                                                "color_option": int(request.POST["color_option"]),
                                                "color_order": map(int, request.POST["color_order"].split(",")),
                                                "select_color": int(request.POST["select_color"])}}
                l.save()
                request.session["alert_code"] = 1
                request.session["list_name"] = request.POST["list_name"]
                return HttpResponseRedirect("/group/" + group_id)
            except:
                alert_code = 4

    members = []
    color_sets = {}
    for i in g.members.all():
        r = Relation.objects.get(ckgroup=g.id, ckuser=i.id)
        if r.verification:
            members.append(i)
    for member in members:
        member.lists = member.list_set.all()
        for l in member.lists:
            color = {}
            for i in l.listcolor_set.all():
                if i.check_color:
                    color[i.color_number] = "#" + i.check_color
            color_sets[l.id] = color
    response["group"] = g
    response["members"] = members
    response["color_sets"] = color_sets
    response["alert_code"] = alert_code
    c = RequestContext(request, response)
    return render_to_response("group_checklist_create.html", c)


def login(request):
    response = _base_response(request)
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    ctx = RequestContext(request, response)
    return render_to_response("login.html", ctx)


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")


def _base_response(request):
    return {"user": request.user,
            "version": "%s %s" % (src.APP_NAME, src.VERSION),
            "default_color": src.DEFAULT_COLOR,
            "block_id": src.BLOCK_ID}
