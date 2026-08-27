from django.contrib import admin
from .models import students
from .models import teachers,studentdocument
# Register your models here.
admin.site.register(students)
admin.site.register(teachers)
admin.site.register(studentdocument)