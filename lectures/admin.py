from django.contrib import admin
from models import *

class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_time')

admin.site.register(Lecture, LectureAdmin)
