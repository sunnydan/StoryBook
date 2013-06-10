from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from forms import pageForm
from stories.models import Page, Properties
from registrationviews import *
from django.http import HttpResponseRedirect
from helpers import *
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    rootpages = Page.objects.all().filter(parent=None)
    return render_to_response("home.html", {'rootpages': rootpages}, context_instance=RequestContext(request))

def page(request, pageid):
    page = findPage(pageid)
    if not page:
        return go404()
    page_is_users = False
    nextpages = Page.objects.all().filter(parent=page)
    nextpage1 = None
    nextpage2 = None
    if len(nextpages)>0:
        nextpage1 = nextpages[0]
    if len(nextpages)>1:
        nextpage2 = nextpages[1]
    context = {
        'page': page,
        'page_is_users': page_is_users,
        'nextpage1': nextpage1, 
        'nextpage2': nextpage2, 
        }
    return render_to_response("page.html", context, context_instance=RequestContext(request))
 
def profile(request):
    if request.user.is_authenticated():
        properties = findProperties(request.user)
        context = {
        'properties': properties,
        } 
        return render_to_response("profile.html", context, context_instance=RequestContext(request))

def editpage(request, pageid):
    page = findPage(pageid)
    if not page:
        return go404()
    if request.user.is_staff or page.author == findUser(request.user):
        already_written = {'short_desc': page.short_desc, 'long_desc': page.long_desc}
        form = pageForm(already_written)
        return render_to_response("editingapage.html", {'form': form, 'page': page}, context_instance=RequestContext(request))
    return goHome()

def submiteditedpage(request, pageid):
    if request.user.is_authenticated() and request.method == "POST":
        page = findPage(pageid)
        if not page:
            return go404()
        if request.user.is_staff or page.author == findUser(request.user):
            form = pageForm(request.POST, request.FILES)
            if form.is_valid():
                page.short_desc = form.cleaned_data['short_desc']
                page.illustration = request.FILES['illustration']
                page.long_desc = form.cleaned_data['long_desc']
                page.save()
                return HttpResponseRedirect("/page:"+str(page.id)+"/") 
            else:
                return render_to_response("editingapage.html", {'form': form, 'page': page}, context_instance=RequestContext(request))
    return goHome()

def writenextpage(request, parentid):
    if request.user.is_authenticated() and 'pageid' in request.GET and request.GET['pageid'] == parentid:
        if (not parentid and user.is_staff()) or parentid:
            form = pageForm
            return render_to_response("writinganewpage.html", {'form': form, 'parentid': parentid}, context_instance=RequestContext(request))
    return goHome()

def submitnewpage(request, parentid):
    if request.user.is_authenticated() and request.method == "POST":
        if (not parentid and user.is_staff()) or parentid:    
            form = pageForm(request.POST, request.FILES)
            if form.is_valid():
                page = Page()
                if int(parentid):
                    page.parent = Page.objects.all().get(id=parentid)
                else:
                    page.parent = None
                page.author = request.user
                page.short_desc = form.cleaned_data['short_desc']
                page.illustration = request.FILES['illustration']
                page.long_desc = form.cleaned_data['long_desc']            
                page.save()
                return HttpResponseRedirect("/page:"+str(page.id)+"/")
            else:
                return render_to_response("writinganewpage.html", {'form': form, 'parentid': parentid}, context_instance=RequestContext(request))
    return goHome() 

def deletebranch(request, pageid):
    if request.user.is_staff:
        page = findPage(pageid)
        if page.parent:
            parentpage = page.parent
            page.kill_branch()
            return HttpResponseRedirect("/page:"+str(parentpage.id)+"/")
        else:
            page.kill_branch()
            return HttpResponseRedirect("/")
    return goHome()

def page404(request):
    return render_to_response("404page.html", context_instance=RequestContext(request))
