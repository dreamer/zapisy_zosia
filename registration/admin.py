from django.contrib import admin
from models import *

class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'day_1', 'day_2', 'day_3',
    'breakfast_2',
    'breakfast_3',
    'breakfast_4',    
    'dinner_1',
    'dinner_2',
    'dinner_3',
    'bus',
    'vegetarian',
    'paid',
    'shirt_size',
    'shirt_type',
    )
admin.site.register(UserPreferences, UserPreferencesAdmin)
admin.site.register(Organization)
