from django.conf.urls import patterns, include, url
import os.path
from crm.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

siteMedia = os.path.join(
		os.path.dirname(__file__), 'siteMedia'
		)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_crm.views.home', name='home'),
    # url(r'^django_crm/', include('django_crm.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	(r'^$', mainPage),
	(r'^login/$', 'django.contrib.auth.views.login'),
	(r'^siteMedia/(?P<path>.*)$', 'django.views.static.serve',
	 { 'document_root': siteMedia }),
	(r'^userRegister/$', userRegister),
)
