from django.db import models
from django.contrib.auth.models import User

class Page(models.Model):
    parent = models.ForeignKey('Page', blank = True, null=True)
    author = models.ForeignKey(User)
    lastedited = models.DateTimeField(auto_now=True)
    illustration = models.ImageField(upload_to='illustrations/%Y/%m/%d')
    short_desc = models.CharField(max_length=30)
    long_desc = models.TextField()
    
    def child1(self):
        if Page.objects.all().filter(parent=self):
          return Page.objects.all().filter(parent=self)[0]
        return 0
    
    def child2(self):
        if len(Page.objects.all().filter(parent=self)) > 1: 
          return Page.objects.all().filter(parent=self)[1]
        return 0
    
    def get_root(self):
        if not self.parent:
          return self
        else:
          return self.parent.get_root()
        
    def tree_to_array(self):
        if self.parent:
            return self.get_root().tree_to_array()
        else:
            array = []
            array = self.tree_to_array_recursive(array)
            return array
            
    def tree_to_array_recursive(self, array):
        array.append(self.simple_json())
        if self.child1():
            array = self.child1().tree_to_array_recursive(array)
        if self.child2():
            array = self.child2().tree_to_array_recursive(array)
        return array 
        
    def simple_json(self):
        child1id = 0
        child2id = 0
        if self.child1():
            child1id = self.child1().id
        if self.child2():
            child2id = self.child2().id
        json_object = {
            "id": self.id,
            "short_desc": self.short_desc.encode('ascii', 'ignore'),
            "child1id": child1id,
            "child2id": child2id,
            "extra": {},
        }
        return json_object
        
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
 
    def __unicode__(self):
        return str(self.user.username)

    def getPages(self):
        return Page.objects.all().filter(author=self.user)
        
