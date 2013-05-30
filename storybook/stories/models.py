from django.db import models
from django.contrib.auth.models import User

class Node(models.Model):
    parent = models.ForeignKey('Node', blank = True, null=True)
    author = models.ForeignKey(User)
    lastedited = models.DateTimeField(auto_now=True)
    action = models.CharField(max_length=30)
    text = models.TextField()
    points = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.action)

class Properties(models.Model):
    user = models.OneToOneField(User)
    #avatar = models.ImageField(upload_to='images/user_avatars/%Y/%m/%d') 
