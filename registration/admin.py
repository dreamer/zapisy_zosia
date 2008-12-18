from django.contrib import admin
from models import *

class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'day_1', 'day_2', 'day_3')

admin.site.register(UserPreferences, UserPreferencesAdmin)
admin.site.register(Organization)
