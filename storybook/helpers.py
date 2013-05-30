from django.contrib.auth.models import User
from stories.models import *

def findNode(nodeid):
    node = None
    node = Node.objects.all().get(id=nodeid)
    return node
