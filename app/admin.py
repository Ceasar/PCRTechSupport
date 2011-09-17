from django.contrib import admin

from models import UserProfile, Course, Semester

print "discovered"

admin.site.register(UserProfile)
admin.site.register(Course)
admin.site.register(Semester)
