# -*- coding: utf-8 -*-
from django.template import loader, RequestContext
from django.http import HttpResponse

def index(request):
    t = loader.get_template("index.html")
    c = RequestContext(request,
                       {"test": "hello!"})
    return HttpResponse(t.render(c))