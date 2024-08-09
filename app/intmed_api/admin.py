from django.contrib import admin

from .models import Consult, Doctor, Schedule, Speciality

admin.site.register(Doctor)
admin.site.register(Consult)
admin.site.register(Schedule)
admin.site.register(Speciality)
