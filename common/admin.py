from django.contrib import admin
from models import *

class ZosiaDefinitionsAdmin(admin.ModelAdmin):
    list_display = [ 'active_definition', 'registration_start', 'registration_final',
			'lectures_suggesting_start', 'lectures_suggesting_final', 
			'rooming_start', 'rooming_final' ]


admin.site.register(ZosiaDefinition, ZosiaDefinitionsAdmin)


