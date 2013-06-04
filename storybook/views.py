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
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    rootnodes = Node.objects.all().filter(parent=None)
    return render_to_response("home.html", {'rootnodes': rootnodes}, context_instance=RequestContext(request))

def node(request, nodeid):
    node = findNode(nodeid)
    if not node:
        return go404()
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
    approved_already = False
    if request.user.is_authenticated():
        properties = findProperties(request.user)
        if properties.already_approved_nodes.all().filter(id = nodeid):
            approved_already = True
    print(node.points)
    context = {
        'node': node,
        'nextnode1': nextnode1, 
        'nextnode2': nextnode2, 
        'nextnode3': nextnode3,
        'approved_already': approved_already,
        }
    return render_to_response("node.html", context, context_instance=RequestContext(request))
 
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

def approvenode(request, nodeid):
    if request.user.is_authenticated() and request.method == "POST":
        node = findNode(nodeid)
        properties = findProperties(request.user)
        if not node in properties.already_approved_nodes.all():
            properties.already_approved_nodes.add(node)
            node.points += 1
            node.save()
            return HttpResponseRedirect("/node:"+str(node.id)+"/")
        else:
            return HttpResponseRedirect("/node:"+str(node.id)+"/")
    else:     
        return goHome()

def node404(request):
    return render_to_response("404node.html", context_instance=RequestContext(request))
