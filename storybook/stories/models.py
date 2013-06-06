from django.db import models
from django.contrib.auth.models import User

class Node(models.Model):
    parent = models.ForeignKey('Node', blank = True, null=True)
    author = models.ForeignKey(User)
    lastedited = models.DateTimeField(auto_now=True)
    action = models.CharField(max_length=30)
    illustration = models.ImageField(upload_to='illustrations/%Y/%m/%d')
    text = models.TextField()
    points = models.IntegerField()

    def __unicode__(self):
        return str(self.action)

    def kill_branch(self):
        offspring = Node.objects.all().filter(parent=self)
        for node in offspring:
            node.kill_branch()
        self.delete()

class Properties(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='images/user_avatars/%Y/%m/%d') 
    already_approved_nodes = models.ManyToManyField(Node)    
 
    def __unicode__(self):
        return str(self.user.username)

    def getPoints(self):
        points = 0
        nodes = Node.objects.all().filter(author=self.user)
        for node in nodes:
            points = points + node.points
        return points

    def getNodes(self):
        return Node.objects.all().filter(author=self.user)
        
