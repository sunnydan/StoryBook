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
    nextnode1 = None
    nextnode2 = None
    nextnode3 = None
    if len(nextnodes)>0:
        nextnode1 = nextnodes[0]
    if len(nextnodes)>1:
        nextnode2 = nextnodes[1]
    if len(nextnodes)>2:
        nextnode3 = nextnodes[2]
    return render_to_response("node.html", {'node': node, 'nextnode1':nextnode1, 'nextnode2':nextnode2, 'nextnode3':nextnode3}, context_instance=RequestContext(request))
 
def profile(request):
    if request.user.is_authenticated():
        return render_to_response("profile.html", context_instance=RequestContext(request))
    else:
        return goHome()

def writenextnode(request, parentid):
    if request.user.is_authenticated() and 'nodeid' in request.GET and request.GET['nodeid'] == parentid:
        form = NodeForm
        return render_to_response("writinganewnode.html", {'form': form, 'parentid': parentid}, context_instance=RequestContext(request))
    else:
        return goHome()

def submitnode(request, parentid):
    if request.user.is_authenticated() and request.method == "POST":
        form = NodeForm(request.POST)
        if form.is_valid():
            node = Node()
            node.parent = Node.objects.all().get(id=parentid)
            node.author = request.user
            node.action = form.cleaned_data['action']
            node.text = form.cleaned_data['text']            
            node.points = 0
            node.save()
            return HttpResponseRedirect("/node:"+str(node.id)+"/")
        else:
            return goHome()            
    else:
        return goHome() 
