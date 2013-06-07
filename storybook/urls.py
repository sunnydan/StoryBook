from django.conf.urls.defaults import *
from views import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home),
    url(r'^login/$', login),
    url(r'^logout/$', logout, {'next_page': '/'}),
    url(r'^register/$', register),
    url(r'^accounts/profile/$', profile),
    url(r'^Page:(\d+)/$', Page),
    url(r'^writenextPage:(\d+)/$', writenextPage),
    url(r'^submitnewPage:(\d+)/$', submitnewPage),
    url(r'^editPage:(\d+)/$', editPage),
    url(r'^submiteditedPage:(\d+)/$', submiteditedPage),
    url(r'^approve:(\d+)/$', approvePage),
    url(r'^deletebranch:(\d+)/$', deletebranch),

    url(r'^Page;404/$', Page404),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^tinymce/', include('tinymce.urls')),
)
