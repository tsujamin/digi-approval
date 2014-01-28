from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'digiapproval_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^digiapproval/', include('digiapproval_project.apps.digiapproval.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pages/', include('django.contrib.flatpages.urls'))
)
