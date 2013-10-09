# -*- coding: utf-8 -*-
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout


def index(request):
    t = loader.get_template("index.html")
    if request.user.is_authenticated():
        c = RequestContext(request,
                           {"test": "hello! now login: " + request.user.username})
    else:
        c = RequestContext(request,
                           {"test": "hello!"})
    return HttpResponse(t.render(c))

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")