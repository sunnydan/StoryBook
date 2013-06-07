from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from forms import PageForm
from stories.models import Page, Properties
from registrationviews import *
from django.http import HttpResponseRedirect
from helpers import *
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    rootPages = Page.objects.all().filter(parent=None)
    return render_to_response("home.html", {'rootPages': rootPages}, context_instance=RequestContext(request))

def page(request, Pageid):
    page = findPage(Pageid)
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
        'Page': page,
        'Page_is_users': page_is_users,
        'nextPage1': nextpage1, 
        'nextPage2': nextpage2, 
        }
    return render_to_response("page.html", context, context_instance=RequestContext(request))
 
def profile(request):
    if request.user.is_authenticated():
        properties = findProperties(request.user)
        context = {
        'properties': properties,
        } 
        return render_to_response("profile.html", context, context_instance=RequestContext(request))

def editpage(request, Pageid):
    Page = findPage(Pageid)
    if not Page:
        return go404()
    if request.user.is_staff or Page.author == findUser(request.user):
        already_written = {'short_desc': Page.short_desc, 'text': Page.text}
        form = PageForm(already_written)
        return render_to_response("editingapage.html", {'form': form, 'Page': Page}, context_instance=RequestContext(request))
    return goHome()

def submiteditedpage(request, Pageid):
    if request.user.is_authenticated() and request.method == "POST":
        if request.user.is_staff or Page.author == findUser(request.user):
            Page = findPage(Pageid)
            if not Page:
                return go404()
            form = PageForm(request.POST)
            if form.is_valid():
                Page.short_desc = form.cleaned_data['short_desc']
                Page.text = form.cleaned_data['text']
                Page.save()
                return HttpResponseRedirect("/page:"+str(Page.id)+"/") 
            else:
                return render_to_response("editingapage.html", {'form': form, 'Page': Page}, context_instance=RequestContext(request))
    return goHome()

def writenextpage(request, parentid):
    if request.user.is_authenticated() and 'Pageid' in request.GET and request.GET['Pageid'] == parentid:
        if (not parentid and user.is_staff()) or parentid:
            form = PageForm
            return render_to_response("writinganewpage.html", {'form': form, 'parentid': parentid}, context_instance=RequestContext(request))
    return goHome()

def submitnewpage(request, parentid):
    if request.user.is_authenticated() and request.method == "POST":
        if (not parentid and user.is_staff()) or parentid:    
            form = PageForm(request.POST)
            if form.is_valid():
                page = Page()
                if int(parentid):
                    page.parent = Page.objects.all().get(id=parentid)
                else:
                    page.parent = None
                page.author = request.user
                page.short_desc = form.cleaned_data['short_desc']
                page.text = form.cleaned_data['text']            
                page.points = 0
                page.save()
                return HttpResponseRedirect("/page:"+str(Page.id)+"/")
            else:
                return render_to_response("writinganewpage.html", {'form': form, 'parentid': parentid}, context_instance=RequestContext(request))
    return goHome() 

def approvepage(request, Pageid):
    if request.user.is_authenticated() and request.method == "POST":
        Page = findPage(Pageid)
        properties = findProperties(request.user)
        if not Page in properties.already_approved_Pages.all():
            properties.already_approved_Pages.add(Page)
            Page.points += 1
            Page.save()
            return HttpResponseRedirect("/page:"+str(Page.id)+"/")
        else:
            return HttpResponseRedirect("/page:"+str(Page.id)+"/")
    else:     
        return goHome()

def deletebranch(request, Pageid):
    if request.user.is_staff:
        Page = findPage(Pageid)
        if Page.parent:
            parentPage = Page.parent
            Page.kill_branch()
            return HttpResponseRedirect("/page:"+str(parentPage.id)+"/")
        else:
            Page.kill_branch()
            return HttpResponseRedirect("/")
    return goHome()

def page404(request):
    return render_to_response("404page.html", context_instance=RequestContext(request))
