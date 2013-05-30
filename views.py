from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from forms import NodeForm
from stories.models import *
from registrationviews import *
from django.http import HttpResponseRedirect
from helpers import *

def home(request):
    rootnodes = Node.objects.all().filter(parent=None)
    return render_to_response("home.html", {'rootnodes': rootnodes}, context_instance=RequestContext(request))

def node(request, nodeid):
    node = Node.objects.all().get(id=nodeid)
    nextnodes = Node.objects.all().filter(parent=node)
    return render_to_response("node.html", {'node': node, 'nextnodes':nextnodes}, context_instance=RequestContext(request))
 
def profile(request):
    return render_to_response("profile.html", context_instance=RequestContext(request))

def writenextnode(request, parentid):
    parentnode = findNode(parentid)
    form = NodeForm(request.POST)
    return render_to_response("writinganewnode.html", {'form': form, 'parentnode': parentnode}, context_instance=RequestContext(request))
