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
    Page = findPage(Pageid)
    if not Page:
        return go404()
    Page_is_users = False
    nextPages = Page.objects.all().filter(parent=Page)
    nextPage1 = None
    nextPage2 = None
    if len(nextPages)>0:
        nextPage1 = nextPages[0]
    if len(nextPages)>1:
        nextPage2 = nextPages[1]
    approved_already = False
    if request.user.is_authenticated():
        properties = findProperties(request.user)
        if Page.author == findUser(request.user):
            Page_is_users = True
        if properties.already_approved_Pages.all().filter(id = Pageid):
            approved_already = True
    print(Page.points)
    context = {
        'Page': Page,
        'Page_is_users': Page_is_users,
        'nextPage1': nextPage1, 
        'nextPage2': nextPage2, 
        'approved_already': approved_already,
        }
    return render_to_response("Page.html", context, context_instance=RequestContext(request))
 
def profile(request):
    if request.user.is_authenticated():
        properties = findProperties(request.user)
        context = {
        'properties': properties,
        } 
        return render_to_response("profile.html", context, context_instance=RequestContext(request))

def editPage(request, Pageid):
    Page = findPage(Pageid)
    if not Page:
        return go404()
    if request.user.is_staff or Page.author == findUser(request.user):
        already_written = {'action': Page.action, 'text': Page.text}
        form = PageForm(already_written)
        return render_to_response("editingaPage.html", {'form': form, 'Page': Page}, context_instance=RequestContext(request))
    return goHome()

def submiteditedPage(request, Pageid):
    if request.user.is_authenticated() and request.method == "POST":
        if request.user.is_staff or Page.author == findUser(request.user):
            Page = findPage(Pageid)
            if not Page:
                return go404()
            form = PageForm(request.POST)
            if form.is_valid():
                Page.action = form.cleaned_data['action']
                Page.text = form.cleaned_data['text']
                Page.save()
                return HttpResponseRedirect("/Page:"+str(Page.id)+"/") 
            else:
                return render_to_response("editingaPage.html", {'form': form, 'Page': Page}, context_instance=RequestContext(request))
    return goHome()

def writenextPage(request, parentid):
    if request.user.is_authenticated() and 'Pageid' in request.GET and request.GET['Pageid'] == parentid:
        if (not parentid and user.is_staff()) or parentid:
            form = PageForm
            return render_to_response("writinganewPage.html", {'form': form, 'parentid': parentid}, context_instance=RequestContext(request))
    return goHome()

def submitnewPage(request, parentid):
    if request.user.is_authenticated() and request.method == "POST":
        if (not parentid and user.is_staff()) or parentid:    
            form = PageForm(request.POST)
            if form.is_valid():
                Page = Page()
                if int(parentid):
                    Page.parent = Page.objects.all().get(id=parentid)
                else:
                    Page.parent = None
                Page.author = request.user
                Page.action = form.cleaned_data['action']
                Page.text = form.cleaned_data['text']            
                Page.points = 0
                Page.save()
                return HttpResponseRedirect("/Page:"+str(Page.id)+"/")
            else:
                return render_to_response("writinganewPage.html", {'form': form, 'parentid': parentid}, context_instance=RequestContext(request))
    return goHome() 

def approvePage(request, Pageid):
    if request.user.is_authenticated() and request.method == "POST":
        Page = findPage(Pageid)
        properties = findProperties(request.user)
        if not Page in properties.already_approved_Pages.all():
            properties.already_approved_Pages.add(Page)
            Page.points += 1
            Page.save()
            return HttpResponseRedirect("/Page:"+str(Page.id)+"/")
        else:
            return HttpResponseRedirect("/Page:"+str(Page.id)+"/")
    else:     
        return goHome()

def deletebranch(request, Pageid):
    if request.user.is_staff:
        Page = findPage(Pageid)
        if Page.parent:
            parentPage = Page.parent
            Page.kill_branch()
            return HttpResponseRedirect("/Page:"+str(parentPage.id)+"/")
        else:
            Page.kill_branch()
            return HttpResponseRedirect("/")
    return goHome()

def Page404(request):
    return render_to_response("404Page.html", context_instance=RequestContext(request))
