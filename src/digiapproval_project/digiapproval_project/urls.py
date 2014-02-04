from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^digiapproval/',
        include('digiapproval_project.apps.digiapproval.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^builder/', include('digiapproval_project.apps.spec_builder.urls')),
)
