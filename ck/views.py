# -*- coding: utf-8 -*-

import os

from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import social_auth

from ck.models import *
from src.data.list import import_list

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
    l = List.objects.get(id=list_id)
    c = RequestContext(request,
                       {"list": l,
                       "circles": l.listcircle_set.all()})
    return render_to_response("checklist_edit.html", c)

def login(request):
    return HttpResponseRedirect("/login/twitter/")


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")