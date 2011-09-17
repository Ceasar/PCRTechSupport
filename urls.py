from django.conf.urls.defaults import patterns, include, url
from app.views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^cart', cart),
    (r'^course/(\d+)/$', course),
    (r'', index),
)

