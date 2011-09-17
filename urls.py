from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from app.views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
print admin.autodiscover()
print "autodiscovered.."

urlpatterns = patterns('',
    (r'^cart', cart),
    (r'^course/(\d+)/$', course),
    (r'^semester/(\d{4})/(\w+)/$', semester),
    (r'^admin/', include(admin.site.urls)),
    (r'^transcript-import/?$', transcript_import),
    (r'^transcript-import/submit$', transcript_import_submit),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'), 
    (r'^login/', user_login),
    (r'', index),
)

