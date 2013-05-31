from django.contrib.auth.models import User
from stories.models import *
from django.http import HttpResponseRedirect

def findNode(nodeid):
    node = None
    node = Node.objects.all().get(id=nodeid)
    return node

def goHome():
    return HttpResponseRedirect('/')
