from django.conf.urls import patterns, include, url
import os.path
from crm.views import *
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

print settings.MEDIA_ROOT

siteMedia = os.path.join(
    os.path.dirname(__file__), 'siteMedia'
)

# import ipdb;ipdb.set_trace()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_crm.views.home', name='home'),
    # url(r'^django_crm/', include('django_crm.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^djemals/', include(admin.site.urls)),
    (r'^$', mainPage),
#    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^login/$', loginPage),
    (r'^siteMedia/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': siteMedia}),
    (r'^userRegistration/$', userRegistration),
    (r'^logout/$', logoutPage),
    url(r'^workDailyRecord/(?P<mode_name>[^/\d]+/)?$', workDailyRecord, name="todayWork"),
    url(r'^user/search/$', searchUser, name="searchUser"),
    # url(r'^workDailyRecord/$', TodayLogView.as_view(), name="todayWork")
    # https://docs.djangoproject.com/en/dev/topics/http/urls/?from=olddocs#naming-url-patterns
    url(r'^workDailyRecord/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/$',
        login_required(DailyLogView.as_view()), name='dayWork'),
    url(r'^workDailyRecord/(?P<year>\d{4})-(?P<month>0?\d{1})/$',
        login_required(MonthlyLogView.as_view()), name='monthWork'),
    url(r'^workDailyRecord/(?P<year>\d{4})/$', YearlyLogView.as_view(),
        name='yearWork'),
    # https://docs.djangoproject.com/en/1.4/topics/class-based-views/#decorating-class-based-views
    url(r'^customer/$', login_required(customerList.as_view()), name="customer"),
    (r'^customer/new/$', customerRegistration),
    url(r'^customer/(?P<slug>[^/]+)/$', customerDetail,
        name="customerDetailView"),
    url(r'^customer/(?P<slug>[^/]+)/notes/$', addCustomerNotes, name="addCustomerNotes"),
    url(r'^customer/(?P<slug>[^/]+)/notes/(?P<pk>[\d]+)/$',
        actionCustomerNote, name="actionCustomerNote"),
    url(r'^customer/(?P<slug>[^/]+)/IPaddrs/((?P<pk>[\d]+)?/)?$', actionCustomerIPaddrs, name="addCustomerIPaddrs"),
    url(r'^list/(?P<slug>[^/]+)/((?P<kind>[^/]+)?/)?(?P<page>[^/]+)?$',
        listing, name="listing"),
    url(r'^customer/(?P<slug>[^/]+)/Domains/(?P<pk>[\d]+)?$', actionCustomerDomains, name="actionCustomerDomains"),
    url(r'^customer/(?P<slug>[^/]+)/Equipments/(?P<pk>[\d]+)?$', actionCustomerEquipments, name="actionCustomerEquipments"),
    url(r'^customer/(?P<slug>[^/]+)/PersonInCharges/(?P<pk>[\d]+)?$', actionCustomerPersonInCharges, name="actionCustomerPersonInCharges"),
    url(r'^responsingAttackDetection/$', responsingAttackDetection, name="responsingAttackDetection"),
    url(r'^responsingAttackDetection/new/$', responsingAttackDetectionNew,
        name="responsingAttackDetectionNew"),
    url(r'^responsingAttackDetection/(?P<slug>[^/]+)/$',
        responsingAttackDetectionDetail,
        name="responsingAttackDetectionDetail"),
    url(r'^user/(?P<slug>[\w]+)/$',
        userDetail,
        name="userDetail"),
    url(
        r'^ip/(?P<slug>[^/]+)?/?$',
        ipDetail,
        name="ipDetail"),
    url(r'^getIpAddressCountry/(?P<ip>[^/]+)/$',
        getIpAddressCountry,
        name="getIpAddressCountry"),
    url(r'^board/$',
        board,
        name="board"),
    url(r'^board/new/$',
        boardNew,
        name="boardNew"),
    url(r'^board/(?P<pk>[^/]+)/$',
        boardDetail,
        name="boardDetail"),
    url(r'^equipment/(?P<slug>[^/]+)?/?$',
        equipmentDetail,
        name="equipmentDetail"),
    url(r'^customer/(?P<slug>[^/]+)/tong/(?P<year>[^/]+)/?$',
        yearTong,
        name="yearTong"),
    url(r'^message/$',
        messageList,
        name="messageList"),
    url(r'^message/(?P<pk>[^/]+)/?$',
        messageDetail,
        name="messageDetail"),
    url(r'^attachment/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT},
        name="attachment"),
)
