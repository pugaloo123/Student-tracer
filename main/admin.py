from django.contrib import admin
from .models import Student, Subject, Grade, Group


admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(Group)
