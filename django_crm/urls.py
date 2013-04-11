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
#    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^login/$', loginPage),
    (r'^siteMedia/(?P<path>.*)$', 'django.views.static.serve',
     { 'document_root': siteMedia }),
    (r'^userRegistration/$', userRegistration),
    (r'^logout/$', logoutPage),
    url(r'^workDailyRecord/(?P<mode_name>\w+/)?$', workDailyRecord, name="todayWork"),
    (r'^user/search/$', searchUser),
    # url(r'^workDailyRecord/$', TodayLogView.as_view(), name="todayWork"), #https://docs.djangoproject.com/en/dev/topics/http/urls/?from=olddocs#naming-url-patterns
    url(r'^workDailyRecord/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$', DailyLogView.as_view(), name='dayWork'),
    url(r'^workDailyRecord/(?P<year>\d{4})-(?P<month>\d{2})/$', MonthlyLogView.as_view(), name='monthWork'),
    url(r'^workDailyRecord/(?P<year>\d{4})/$', YearlyLogView.as_view(), name='yearWork'),
    url(r'^customer/$', customerList.as_view(), name="customer"),
    (r'^customer/new/$', customerRegistration),
    url(r'^customer/(?P<slug>[^/]+)/$', customerDetail, name="customerDetailView"),
    url(r'^customer/(?P<slug>[^/]+)/notes/$', addCustomerNotes, name="addCustomerNotes"),
    url(r'^customer/(?P<slug>[^/]+)/notes/(?P<pk>[\d]+)/$', actionCustomerNote, name="actionCustomerNote"),
    url(r'^customer/(?P<slug>[^/]+)/IPaddrs/((?P<pk>[\d]+)?/)?$', actionCustomerIPaddrs, name="addCustomerIPaddrs"),
    url(r'^list/(?P<slug>[^/]+)/((?P<kind>[^/]+)?/)?(?P<page>[^/]+)?$', listing, name="listing"),
    url(r'^customer/(?P<slug>[^/]+)/Domains/(?P<pk>[\d]+)?$', actionCustomerDomains, name="actionCustomerDomains"),
    url(r'^customer/(?P<slug>[^/]+)/Equipments/(?P<pk>[\d]+)?$', actionCustomerEquipments, name="actionCustomerEquipments"),
    url(r'^customer/(?P<slug>[^/]+)/PersonInCharges/(?P<pk>[\d]+)?$', actionCustomerPersonInCharges, name="actionCustomerPersonInCharges"),
)