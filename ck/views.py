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
        usa = UserSocialAuth.objects.get(user_id=request.user.id)
        save_twitter_icon(request.user, usa.tokens["oauth_token"], usa.tokens["oauth_token_secret"])

    # recentクエリ
    _recent_ckc = []
    _recent_ckc.extend(CircleKnowledgeComment.objects.all().order_by("-write_at")[:5])
    _recent_ckc.extend(CompanyKnowledgeComment.objects.all().order_by("-write_at")[:5])
    s_recent_ckc = sorted(_recent_ckc, key=lambda x: x.write_at, reverse=True)
    recent_ckc = {}
    for i in range(min(5, len(s_recent_ckc))):
        if isinstance(s_recent_ckc[i], CircleKnowledgeComment):
            recent_ckc[s_recent_ckc[i]] = s_recent_ckc[i].parent_circle_knowledge.circleknowledgedata_set.get(comiket_number=src.COMIKET_NUMBER)
        else:
            recent_ckc[s_recent_ckc[i]] = s_recent_ckc[i].parent_company_knowledge.companyknowledgedata_set.get(comiket_number=src.COMIKET_NUMBER)
    response["recent_comments"] = recent_ckc
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
    response["circles"] = l.listcircle_set.all().order_by("page_number")
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
                merge_list(l, g, request.POST["list_name"])
                request.session["alert_code"] = 1
                request.session["list_name"] = request.POST["list_name"]
                return HttpResponseRedirect("/group/" + group_id)
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
    company_query = CompanyKnowledge.objects
    circle_query = CircleKnowledge.objects
    if len(keywords) == 0:
        keywords.append("")
    for k in keywords:
        company_query = company_query.filter(
            Q(companyknowledgedata__company_name__icontains=k) |
            Q(companyknowledgedata__description__icontains=k))
        circle_query = circle_query.filter(
            Q(circleknowledgedata__circle_name__icontains=k) |
            Q(circleknowledgedata__pen_name__icontains=k) |
            Q(circleknowledgedata__description__icontains=k))
    results = []
    for q in company_query:
        try:
            _q = q.companyknowledgedata_set.all()
            results.append(sorted(_q, key=lambda x: x.comiket_number, reverse=True)[0])
        except:
            pass
    for q in circle_query:
        try:
            _q = q.circleknowledgedata_set.all()
            results.append(sorted(_q, key=lambda x: x.comiket_number, reverse=True)[0])
        except:
            pass
    p_circles = Paginator(results, 20)
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
    response["p_results"] = p_circles
    response["results"] = p_circles.page(page)
    response["pages"] = pages
    ctx = RequestContext(request, response)
    return render_to_response("search.html", ctx)


def circle(request, circle_id):
    try:
        ck = CircleKnowledge.objects.get(circle_knowledge_id=circle_id)
    except:                                                             # circle_idがおかしい
        raise Http404
    try:
        ckd = ck.circleknowledgedata_set.filter(comiket_number=src.COMIKET_NUMBER)[0]
    except:                                                             # 最新のCircleKnowledgeDataがない
        raise Http404
        #_q = ck.circleknowledgedata_set.all()
        #ckd = sorted(_q, key=lambda x: x.comiket_number, reverse=True)[0]

    comments = {}
    for i in range(80, src.COMIKET_NUMBER+1):
        _ckc = ck.circleknowledgecomment_set.filter(comiket_number=i)
        comments[i] = sorted(_ckc, key=lambda x:
            x.start_time_hour * 60 + x.start_time_min if x.start_time_hour else x.event_time_hour * 60 + x.event_time_min)
    response = _base_response(request)
    if "alert_code" in request.session:
        response["alert_code"] = request.session["alert_code"]
        del request.session["alert_code"]
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
                request.session["alert_code"] = 2
                return HttpResponseRedirect("/circle/" + ckd_val.circle_knowledge_id)
            elif ckd_val is True:
                ckd.save()
                request.session["alert_code"] = 1
                return HttpResponseRedirect("/circle/" + ckd.parent_circle_knowledge.circle_knowledge_id)
    else:
        form = CircleRegisterForm()
    response["form"] = form
    response["alert_code"] = alert_code
    ctx = RequestContext(request, response)
    return render_to_response("circle_register.html", ctx)


@login_required
def circle_edit(request, circle_id):
    response = _base_response(request)
    alert_code = 0
    try:
        ck = CircleKnowledge.objects.get(circle_knowledge_id=circle_id)
        ckd = ck.circleknowledgedata_set.filter(comiket_number=src.COMIKET_NUMBER)[0]
    except:                                                             # circle_idがおかしい
        raise Http404
    if request.method == "POST":
        form = CircleEditForm(request.POST, instance=ckd)
        if not form.is_valid():
            alert_code = 2
            response["invalid"] = form.errors
        else:
            _ckd = CircleKnowledgeData.objects.filter(comiket_number=src.COMIKET_NUMBER,
                                                       day=int(request.POST["day"]),
                                                       block_id=int(request.POST["block_id"]),
                                                       space_number=int(request.POST["space_number"]),
                                                       space_number_sub=request.POST["space_number_sub"])
            if len(_ckd) >=1 and _ckd[0].parent_circle_knowledge != ck: # すでに同じ位置に別のサークルが登録されている
                request.session["alert_code"] = 2
                return HttpResponseRedirect("/circle/" + _ckd[0].parent_circle_knowledge.circle_knowledge_id)
            form.save()
            request.session["alert_code"] = 5
            return HttpResponseRedirect("/circle/" + circle_id)
    else:
        if ckd.wc_id:
            form = CircleEditForm(instance=ckd, initial={"wc_id": "https://webcatalog.circle.ms/Circle/" + str(ckd.wc_id)})
        else:
            form = CircleEditForm(instance=ckd)
    response["form"] = form
    response["alert_code"] = alert_code
    response["circle_id"] = circle_id
    ctx = RequestContext(request, response)
    return render_to_response("circle_edit.html", ctx)


def company(request, company_id):
    try:
        ck = CompanyKnowledge.objects.get(company_knowledge_id=company_id)
    except:                                                             # company_idがおかしい
        raise Http404
    try:
        ckd = ck.companyknowledgedata_set.filter(comiket_number=src.COMIKET_NUMBER)[0]
    except:                                                             # 最新のCompanyKnowledgeDataがない
        raise Http404
        #_q = ck.companyknowledgedata_set.all()
        #ckd = sorted(_q, key=lambda x: x.comiket_number, reverse=True)[0]

    comments = {}
    for i in range(80, src.COMIKET_NUMBER+1):
        comments_value = {}
        for j in (1, 2, 3):
            _ckc = ck.companyknowledgecomment_set.filter(comiket_number=i, day=j)
            comments_value[j] = sorted(_ckc, key=lambda x:
                x.start_time_hour * 60 + x.start_time_min if x.start_time_hour else x.event_time_hour * 60 + x.event_time_min)
        comments[i] = comments_value
    response = _base_response(request)
    if "alert_code" in request.session:
        response["alert_code"] = request.session["alert_code"]
        del request.session["alert_code"]
    if request.GET.has_key("alert_code"):
        try:
            response["alert_code"] = int(request.GET["alert_code"])
            request.GET = QueryDict({})
            request.META["QUERY_STRING"] = ""
        except ValueError:
            response["alert_code"] = ""
    response["company_knowledge"] = ck
    response["companies"] = ck.companyknowledgedata_set.all()
    response["company_data"] = ckd
    response["comments"] = comments
    ctx = RequestContext(request, response)
    return render_to_response("company.html", ctx)


@login_required
def company_register(request):
    response = _base_response(request)
    alert_code = 0
    if request.method == "POST":
        form = CompanyRegisterForm(request.POST)
        if not form.is_valid():
            alert_code = 2
            response["invalid"] = form.errors
        else:
            ckd = form.save(commit=False)
            ckd_val = ckd.validate_company()
            if isinstance(ckd_val, CompanyKnowledge):
                request.session["alert_code"] = 2
                return HttpResponseRedirect("/company/" + ckd_val.company_knowledge_id)
            elif ckd_val is True:
                ckd.save()
                request.session["alert_code"] = 1
                return HttpResponseRedirect("/company/" + ckd.parent_company_knowledge.company_knowledge_id)
    else:
        form = CompanyRegisterForm()
    response["form"] = form
    response["alert_code"] = alert_code
    ctx = RequestContext(request, response)
    return render_to_response("company_register.html", ctx)


@login_required
def company_edit(request, company_id):
    response = _base_response(request)
    alert_code = 0
    try:
        ck = CompanyKnowledge.objects.get(company_knowledge_id=company_id)
        ckd = ck.companyknowledgedata_set.filter(comiket_number=src.COMIKET_NUMBER)[0]
    except:                                                             # company_idがおかしい
        raise Http404
    if request.method == "POST":
        form = CompanyEditForm(request.POST, instance=ckd)
        if not form.is_valid():
            alert_code = 2
            response["invalid"] = form.errors
        else:
            _ckd = CompanyKnowledgeData.objects.filter(comiket_number=src.COMIKET_NUMBER,
                                                       space_number=int(request.POST["space_number"]))
            if len(_ckd) >=1 and _ckd[0].parent_company_knowledge != ck: # すでに同じ位置に別のブースが登録されている
                request.session["alert_code"] = 2
                return HttpResponseRedirect("/company/" + _ckd[0].parent_company_knowledge.company_knowledge_id)
            form.save()
            request.session["alert_code"] = 5
            return HttpResponseRedirect("/company/" + company_id)
    else:
        form = CompanyEditForm(instance=ckd)
    response["form"] = form
    response["alert_code"] = alert_code
    response["company_id"] = company_id
    ctx = RequestContext(request, response)
    return render_to_response("company_edit.html", ctx)


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
