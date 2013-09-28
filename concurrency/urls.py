from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from .views import OrderCreate, OrderCancel

urlpatterns = patterns('',
    url(r'^create_order/$', OrderCreate.as_view(), name='order-create'),
    url(r'^cancel_order/(?P<pk>[0-9]+)/$', OrderCancel.as_view(), name='order-cancel'),

    url(r'^admin/', include(admin.site.urls)),
)
