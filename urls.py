from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from app.views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
print admin.autodiscover()
print "autodiscovered.."

urlpatterns = patterns('',
    (r'^recommended/', recommended),
    (r'^options', options),
    (r'^course/(\w+)/(\w+)/?$', course),
    (r'^course/(\w+)/?$', course),
    (r'^add/(\w+)/(\w+)/?', add),
    (r'^semester/(\d{4})/(\w+)/?$', semester),
    (r'^admin/?', include(admin.site.urls)),
    (r'^transcript-import/?$', transcript_import),
    (r'^transcript-import/submit$', transcript_import_submit),
    (r'^recommendations-admin/clear$', recommendations_admin_clear),
    (r'^recommendations-admin/generate$', recommendations_admin_generate),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'), 
    (r'^login/', user_login),
    (r'', index),
)

