from django.db import models
from django.contrib.auth.models import User

class Page(models.Model):
    parent = models.ForeignKey('Page', blank = True, null=True)
    author = models.ForeignKey(User)
    lastedited = models.DateTimeField(auto_now=True)
    illustration = models.ImageField(upload_to='illustrations/%Y/%m/%d')
    short_desc = models.CharField(max_length=30)
    long_desc = models.TextField()

    def __unicode__(self):
        return str(self.short_desc)

    def kill_branch(self):
        offspring = Page.objects.all().filter(parent=self)
        for page in offspring:
            page.kill_branch()
        self.delete()

class Properties(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='images/user_avatars/%Y/%m/%d') 
    already_approved_pages = models.ManyToManyField(Page)    
 
    def __unicode__(self):
        return str(self.user.username)

    def getPages(self):
        return Page.objects.all().filter(author=self.user)
        
