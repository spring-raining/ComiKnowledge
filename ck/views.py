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
import urllib

from ComiKnowledge import settings
from ck.models import *
from ck.forms import *
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
        usa = UserSocialAuth.objects.get(user_id=request.user.id)
        save_twitter_icon(request.user, usa.tokens["oauth_token"], usa.tokens["oauth_token_secret"])

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

        response = _base_response(request)
        if request.method == "POST":
            response = HttpResponse(mimetype="text/comma-separated-values; charset=utf-8")
            response["Content-Disposition"] = (u'attachment; filename="%s.csv"' % l.list_name).encode("utf-8")
            return output_list(response, l.list_id,
                               memo_template=request.POST["memo"],
                               color_option=int(request.POST["color_option"]),
                               color_order=tuple(map(int, request.POST["color_order"].split(","))),
                               select_color=int(request.POST["select_color"]))
        color = {}
        for i in l.listcolor_set.all():
            if i.check_color:
                color[i.color_number] = "#" + i.check_color
        response["list"] = l
        response["color"] = color
        ctx = RequestContext(request, response)
        return render_to_response("checklist_download.html", ctx)


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

    response = _base_response(request)
    response["list"] = l
    response["circles"] = l.listcircle_set.all()
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
def group_home(request, group_id, **redirect_response):
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
    if redirect_response:
        response.update(redirect_response)
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
                merge_list(l, g, request.POST["list_name"])
                return group_home(request, group_id, alert_code=1, list_name=request.POST["list_name"])
            except:
                alert_code = 4

    members = []
    for i in g.members.all():
        r = Relation.objects.get(ckgroup=g.id, ckuser=i.id)
        if r.verification:
            members.append(i)
    for member in members:
        member.lists = member.list_set.all()
    response["group"] = g
    response["members"] = members
    response["alert_code"] = alert_code
    c = RequestContext(request, response)
    return render_to_response("group_checklist_create.html", c)


def search(request):
    if request.method == "POST":                                        # 検索窓からのPOST
        if not request.POST["keyword"]:
            return HttpResponseNotModified()
        kw = request.POST["keyword"].encode("utf-8")
        query = urllib.urlencode({"keyword": kw})
        return HttpResponseRedirect("/search?" + query)
    if not request.GET.has_key("keyword"):                              # keywordがない
        return HttpResponseRedirect("/")

    response = _base_response(request)
    response["keyword"] = request.GET["keyword"]
    keywords = request.GET["keyword"].split()
    query = CircleKnowledge.objects
    if len(keywords) == 0:
        keywords.append("")
    for k in keywords:
        query = query.filter(
            Q(circleknowledgedata__circle_name__icontains=k) |
            Q(circleknowledgedata__pen_name__icontains=k) |
            Q(circleknowledgedata__description__icontains=k))
    circles = []
    for q in query:
        try:
            _q = q.circleknowledgedata_set.all()
            circles.append(sorted(_q, key=lambda x: x.comiket_number, reverse=True)[0])
        except:
            pass
    p_circles = Paginator(circles, 20)
    try:
        page = int(request.GET.get("page", "1"))
        if page > p_circles.num_pages or page < 1:
            page = 1
    except ValueError:
        page = 1
    pages = [page]
    while len(pages) < 5 and len(pages) < p_circles.num_pages:
        if pages[0] != 1:
            pages.insert(0, pages[0] - 1)
        if pages[-1] != p_circles.num_pages:
            pages.append(pages[-1] + 1)
    response["p_circles"] = p_circles
    response["circles"] = p_circles.page(page)
    response["pages"] = pages
    ctx = RequestContext(request, response)
    return render_to_response("search.html", ctx)


def circle(request, circle_id, **redirect_response):
    try:
        ck = CircleKnowledge.objects.get(circle_knowledge_id=circle_id)
    except:                                                             # circle_idがおかしい
        raise Http404
    try:
        ckd = ck.circleknowledgedata_set.filter(comiket_number=src.COMIKET_NUMBER)[0]
    except:                                                             # 最新のCircleKnowledgeDataがない
        _q = ck.circleknowledgedata_set.all()
        ckd = sorted(_q, key=lambda x: x.comiket_number, reverse=True)[0]

    comments = {}
    for i in range(80, src.COMIKET_NUMBER+1):
        _ckc = ck.circleknowledgecomment_set.filter(comiket_number=i)
        comments[i] = sorted(_ckc, key=lambda x:
            x.start_time_hour * 60 + x.start_time_min if x.start_time_hour else x.event_time_hour * 60 + x.event_time_min)
    response = _base_response(request)
    if redirect_response:
        response.update(redirect_response)
    if request.GET.has_key("alert_code"):
        try:
            response["alert_code"] = int(request.GET["alert_code"])
            request.GET = QueryDict({})
            request.META["QUERY_STRING"] = ""
        except ValueError:
            response["alert_code"] = ""
    response["circle_knowledge"] = ck
    response["circles"] = ck.circleknowledgedata_set.all()
    response["circle_data"] = ckd
    response["comments"] = comments
    response["space_character"] = space_character(ckd.comiket_number, ckd.day, ckd.block_id, ckd.space_number)
    ctx = RequestContext(request, response)
    return render_to_response("circle.html", ctx)


@login_required
def circle_register(request):
    response = _base_response(request)
    alert_code = 0
    if request.method == "POST":
        form = CircleRegisterForm(request.POST)
        if not form.is_valid():
            alert_code = 2
            response["invalid"] = form.errors
        else:
            ckd = form.save(commit=False)
            ckd_val = ckd.validate_circle()
            if isinstance(ckd_val, CircleKnowledge):
                return circle(request, ckd_val.circle_knowledge_id, alert_code=2)
            elif ckd_val is True:
                ckd.save()
                return circle(request, ckd.parent_circle_knowledge.circle_knowledge_id, alert_code=1)
    else:
        form = CircleRegisterForm()
    response["form"] = form
    response["alert_code"] = alert_code
    ctx = RequestContext(request, response)
    return render_to_response("circle_register.html", ctx)


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
