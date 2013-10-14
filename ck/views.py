# -*- coding: utf-8 -*-

import os

from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render_to_response
import social_auth

from ck.models import *
from src.data.list import import_list
from src.data.group import create_group


def index(request):
    t = loader.get_template("index.html")
    if request.user.is_authenticated():
        return HttpResponseRedirect("/home/")
    c = RequestContext(request,
                       {"test": "hello!"})
    return HttpResponse(t.render(c))


@login_required
def home(request):
    ctx = RequestContext(request,
                         {"test": "hello! now login",
                          "user": request.user})
    return render_to_response("home.html", ctx)


@login_required
def checklist(request):
    #if request.GET.has_key("command"):
    #    if request.GET["command"] == "delete":
    #        print "Delete it!"

    if request.method == "POST":
        csv_file = request.FILES["csv"]
        import_list(csv_file ,request.user)
    c = RequestContext(request,
                       {"lists": request.user.list_set.all()})
    return render_to_response("checklist.html", c)


@login_required
def checklist_edit(request, list_id):
    if list_id is None:
        return HttpResponseRedirect("/checklist/")
    try:
        l = List.objects.get(id=list_id)
    except:
        raise Http404

    c = RequestContext(request,
                       {"list": l,
                       "circles": l.listcircle_set.all()})
    return render_to_response("checklist_edit.html", c)


@login_required
def group(request):
    if request.method == "POST":
        g = create_group(request.POST["group_name"], request.POST["group_id"])
        request.user.ck_groups.add(g)
    c = RequestContext(request, {"groups": request.user.ck_groups.all()})
    return render_to_response("group.html", c)


@login_required
def group_home(request, group_id):
    if group_id is None:
        return HttpResponseRedirect("/group/")
    # group_idがおかしい
    try:
        g = CKGroup.objects.get(group_id=group_id)
    except:
        raise Http404

    # ユーザーがグループに属していない
    if not request.user.ck_groups.filter(group_id=group_id):
        raise Http404

    members = g.ckuser_set.all()
    for member in members:
        member.lists = member.list_set.all()
    c = RequestContext(request,
                       {"group": g,
                        "members": members})
    return render_to_response("group_home.html", c)


def login(request):
    return HttpResponseRedirect("/login/twitter/")


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")