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
    node_is_users = False
    nextnodes = Node.objects.all().filter(parent=node)
    nextnode1 = None
    nextnode2 = None
    if len(nextnodes)>0:
        nextnode1 = nextnodes[0]
    if len(nextnodes)>1:
        nextnode2 = nextnodes[1]
    approved_already = False
    if request.user.is_authenticated():
        properties = findProperties(request.user)
        if node.author == findUser(request.user):
            node_is_users = True
        if properties.already_approved_nodes.all().filter(id = nodeid):
            approved_already = True
    print(node.points)
    context = {
        'node': node,
        'node_is_users': node_is_users,
        'nextnode1': nextnode1, 
        'nextnode2': nextnode2, 
        'approved_already': approved_already,
        }
    return render_to_response("node.html", context, context_instance=RequestContext(request))
 
def profile(request):
    if request.user.is_authenticated():
        properties = findProperties(request.user)
        context = {
        'properties': properties,
        } 
        return render_to_response("profile.html", context, context_instance=RequestContext(request))

def editnode(request, nodeid):
    node = findNode(nodeid)
    if not node:
        return go404()
    if request.user.is_staff or node.author == findUser(request.user):
        already_written = {'action': node.action, 'text': node.text}
        form = NodeForm(already_written)
        return render_to_response("editinganode.html", {'form': form, 'node': node}, context_instance=RequestContext(request))
    return goHome()

def submiteditednode(request, nodeid):
    if request.user.is_authenticated() and request.method == "POST":
        if request.user.is_staff or node.author == findUser(request.user):
            node = findNode(nodeid)
            if not node:
                return go404()
            form = NodeForm(request.POST)
            if form.is_valid():
                node.action = form.cleaned_data['action']
                node.text = form.cleaned_data['text']
                node.save()
                return HttpResponseRedirect("/node:"+str(node.id)+"/") 
            else:
                return render_to_response("editinganode.html", {'form': form, 'node': node}, context_instance=RequestContext(request))
    return goHome()

def writenextnode(request, parentid):
    if request.user.is_authenticated() and 'nodeid' in request.GET and request.GET['nodeid'] == parentid:
        if (not parentid and user.is_staff()) or parentid:
            form = NodeForm
            return render_to_response("writinganewnode.html", {'form': form, 'parentid': parentid}, context_instance=RequestContext(request))
    return goHome()

def submitnewnode(request, parentid):
    if request.user.is_authenticated() and request.method == "POST":
        if (not parentid and user.is_staff()) or parentid:    
            form = NodeForm(request.POST)
            if form.is_valid():
                node = Node()
                if int(parentid):
                    node.parent = Node.objects.all().get(id=parentid)
                else:
                    node.parent = None
                node.author = request.user
                node.action = form.cleaned_data['action']
                node.text = form.cleaned_data['text']            
                node.points = 0
                node.save()
                return HttpResponseRedirect("/node:"+str(node.id)+"/")
            else:
                return render_to_response("writinganewnode.html", {'form': form, 'parentid': parentid}, context_instance=RequestContext(request))
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

def deletebranch(request, nodeid):
    if request.user.is_staff:
        node = findNode(nodeid)
        if node.parent:
            parentNode = node.parent
            node.kill_branch()
            return HttpResponseRedirect("/node:"+str(parentNode.id)+"/")
        else:
            node.kill_branch()
            return HttpResponseRedirect("/")
    return goHome()

def node404(request):
    return render_to_response("404node.html", context_instance=RequestContext(request))
