from django.template import Context
from django.template import RequestContext
from django.contrib.auth.models import User
from stories.models import *
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

def findNode(nodeid):
    node = None
    node = Node.objects.all().get(id=nodeid)
    return node

'''def findProperties(User): 
1. See if the client is logged in; if not, return None.
2. If the user already has a corresponding properties object, return that.
3. If the user does not already have a corresponding properties object, make one, then return that.
'''
def findProperties(User):
    properties = None
    if User.is_authenticated(): 
        try:
            properties = Properties.objects.all().get(user = findUser(User))
        except ObjectDoesNotExist:
            properties = Properties()
            properties.user = findUser(user)
            properties.save()
    return properties

def findUser(requestuser):
    user = User.objects.all().get(username = str(requestuser.username))
    return user

def goHome():
    return HttpResponseRedirect('/')
