from django.conf.urls import patterns, include, url
from digiapproval_project.apps.digiapproval import forms, views
from registration.backends.default.views import RegistrationView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # hook in our profile and registration override
    url(r'^accounts/profile/$', views.profile, name='profile'),
    url(r'^accounts/register/$',
        RegistrationView.as_view(form_class=forms.CustomerRegistrationForm),
        name='registration_register'),

    # make / work
    url(r'^$', views.index),

    # apps
    url(r'^digiapproval/',
        include('digiapproval_project.apps.digiapproval.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
)
