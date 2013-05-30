from django.template import Context
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings

def home(request):
    return render_to_response("base.html", context_instance=RequestContext(request))
 
