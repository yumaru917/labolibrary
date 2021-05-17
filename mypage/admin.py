from django.contrib import admin

from mypage.models import *

# Register your models here.

admin.site.register(Laboratory)
admin.site.register(UniversityArea)
admin.site.register(University)
admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(ExaminationInfo)
admin.site.register(NotificationsForLaboratory)
admin.site.register(NotificationsForUser)
