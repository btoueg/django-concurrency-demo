from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from myapp.views import *

urlpatterns = patterns('',
    url(r'^order/$', OrderList.as_view(), name='order-list'),
    url(r'^order/(?P<pk>[0-9]+)/$', OrderDetail.as_view(), name='order-detail'),
    url(r'^order/(?P<pk>[0-9]+)/abort/$', OrderAbort.as_view(), name='order-abort'),

    url(r'^admin/', include(admin.site.urls)),
)
