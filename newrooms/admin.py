from django.contrib import admin
from models import *

class NewroomsAdmin(admin.ModelAdmin):
    list_display = ['number','capacity','locators']
    
    def locators(self,obj):
        return ",".join([])

admin.site.register(NRoom, NewroomsAdmin)

class UserInRoomAdmin(admin.ModelAdmin):
    list_display = ['locator','room']

admin.site.register(UserInRoom, UserInRoomAdmin)
