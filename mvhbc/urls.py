from django.conf.urls import patterns, include, url
from mvhbc import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'clubmanager.views.home', name='home'),
    # url(r'^clubmanager/', include('clubmanager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', views.home, name="home"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/', views.about, name="about"),
    url(r'^membership/', views.membership, name="membership"),
    url(r'^officers/', views.officers, name="officers"),
    url(r'^accounts/login/', 'django.contrib.auth.views.login', {'template_name': 'competition_login.html'}, name="accounts_login"),
    url(r'^competition/', include('competition.urls')),
    url(r'^resources/', views.resources, name="resources"),
)
